from enum import Enum
from collections import Counter
from time import time

from calc.enchantments import Enchantment as Ench
from calc.enchantments import enchantments as enchs # not cap cuz it's an instance
from calc.enchantments import EnchantmentId as EnchId
from calc.enchantments import EnchantmentTags as EnchTag
from calc.enchantments import EnchantableItems as EnchItems# Constants

MAX_LEVEL = 39

class Book:
    """I just realized that having a Book class who says Book.isBook = False is kinda funny,
    but I don't really wanna name it 'Item' or something else generic""" # plus me lazy
    def __init__(self,enchs:dict[Ench,int]|list[tuple[Ench,int]]=None,punishment:int=0,amount:int=0,equ:Enum|None=None,custom:bool=False):
        if isinstance(enchs,list):enchs=dict(enchs)
        self.enchess = {} if enchs is None else enchs
        self.punishent = punishment # amount of anvil use, not raw lvl penalty
        self.amount = amount
        self.isBook = equ is None
        self.equ = equ
        self.isCustom = custom
    def addEnch(self,ench:Ench,lvl:int):
        self.enchess[ench]=lvl
    def asList(self) -> tuple[dict[Ench,int],int,int,bool,bool]:
        return [self.enchess,self.punishent,self.amount,self.isBook,self.isCustom]
    def copy(self,enchs:dict[Ench,int]|list[tuple[Ench,int]]=None,punishment:int=None,amount:int=None,equ:Enum|None=None,custom:bool=None):
        if isinstance(enchs,list):enchs=dict(enchs)
        if enchs is None: enchs = self.enchess.copy()
        if punishment is None: punishment = self.punishent
        if amount is None: amount = self.amount
        if equ is None: equ = self.equ
        if custom is None: custom = self.isCustom
        return Book(enchs,punishment,amount,equ,custom)
    def getPenaltylvl(self):
        return (2**self.punishent)-1
    def combineWith(self,b2:"Book") -> tuple[bool,int,dict[Ench,int]]:
        """Modifys book in place, return (success,cost,wastedEnch)
           the success don't care about MAX_LEVEL, only basic anvil rules"""
        if self.isBook and not b2.isBook: return (False,0,{}) # can't do that
        cost = self.getPenaltylvl()+b2.getPenaltylvl()
        wasted:dict[Ench,int]={}
        valid = False # if any enchantment sticks, accroding to vanilla
        for ench,lvl in b2.enchess.items():
            if not self.isBook and not ench.isCompatibleWith(self.equ):
                wasted[ench] = wasted.get(ench,0) + 2**(lvl-1)
                continue
            # TODO: conflict detection, performance tho
            # cost += 1 if conflict
            nbChess = self.enchess
            if nbChess.get(ench) is None: nbChess[ench]=lvl
            elif nbChess[ench]==lvl: nbChess[ench]+=1
            else:
                lvls = sorted([nbChess[ench],lvl],reverse=True)
                nbChess[ench] = lvls[0] # lvl[1] WASTED
                wasted[ench] = wasted.get(ench,0) + 2**(lvls[1]-1)
            valid = True
            cost += nbChess[ench]*(ench.multiplierBook if b2.isBook else ench.multiplierItem)
        self.punishent = max(self.punishent,b2.punishent)+1
        return valid,cost,wasted

    def key(self):
        return (tuple(sorted((ench.Id, lvl)for ench, lvl in self.enchess.items())),self.punishent,self.amount,self.isBook)
    def __str__(self):
        """debug use only"""
        result = "BOK [" if self.isBook else "EQU ["
        first = True
        for ench,lvl in self.enchess.items():
            if first: first=False
            else: result += ", "
            result += f"{ench.names[0]}{lvl}"
        result += f"]*{self.amount}"
        return result
    def __repr__(self):
        return f"Book({self.enchess},{self.punishent},{self.amount},{self.equ},{self.isCustom})"
    def __eq__(self, otherBook): # isCustom is ignored cuz not relevent to calculation
        if not isinstance(otherBook, Book): return NotImplemented
        if self.amount != otherBook.amount: return False
        if self.isBook != otherBook.isBook: return False
        if self.punishent != otherBook.punishent: return False
        if self.enchess != otherBook.enchess: return False
        return True
    def canStackWith(self,otherBook:"Book"):
        if self.isBook != otherBook.isBook: return False
        if self.punishent != otherBook.punishent: return False
        if self.enchess != otherBook.enchess: return False
        return True

def generateBooks(targetEnchs:list[tuple[bool,Ench,int]],targetEqu:Enum):
    bookBag:list[Book] = [Book(equ=targetEqu,amount=1,)]
    for data in targetEnchs:
        book = Book()
        fromOneUp,ench,lvl = data
        if not fromOneUp: book.addEnch(ench,lvl); book.amount=1
        else: book.addEnch(ench,1); book.amount=2**(lvl-1)
        bookBag.append(book)
    return bookBag

# TODO: isCustom propegation(Only them has weird edge case)
def generateSteps(targetEnchs:list[tuple[bool,Ench,int]],bookBag:list[Book]):
    bb = [book.copy() for book in bookBag] # bb stands for bookBag
    wasteAllowed = calWasteAllowed(targetEnchs,bookBag)
    DPMAN = {} # Dynamic Programming Module And Notes

    interation = 0; recu = 0
    def loopBoi(bb:list[Book],wasted:dict[Ench,int]):
        checkerB = [b for b in bb if b.amount>0]
        if len(checkerB)==1: # FOUND
            print(f"{checkerB[0]}, PUNSHENT={checkerB[0].getPenaltylvl()}")
            if len(wasted):
                print("WASTED:")
                for ench,amount in wasted.items():
                    print(f"{ench.names[0]}*{amount}",end=", ")
                    print(f"ALLOWED = {wasteAllowed.get(ench,"INF")}")
            return True

        key=stateKey(bb)
        if key in DPMAN:return DPMAN[key]

        # Generate the combination pair and order them first
        bl = len(bb) # bl stands for bagLength  
        pairs:list[tuple[int,int,int,int]] = []
        for i in range(bl):
            if bb[i].amount<=0:continue
            for it in range(bl):
                if bb[it].amount<=0:continue
                if i==it and bb[i].amount<2: continue
                p1=bb[i].punishent;p2=bb[it].punishent
                # the pairs has (punishent diff, punishent value, i, it) in this order
                # so list.sort() will sort accordingly
                # with pairs with no punishent diff first
                # then the ones with small punishent overall
                pairs.append((abs(p1-p2),max(p1,p2),i,it))
        pairs.sort()
        

        nonlocal interation, recu
        interation += 1
        for punDif,punMax,i,it in pairs:
            recu += 1
            print(f"{interation}:{recu}")
            # bbOld=stateKey(bb)
            success,cost,waste,newBook = tryCombine(bb,i,it)

            if not success or cost > MAX_LEVEL: unCombine(bb,i,it,newBook); continue
            newWaste = {}
            for ench,amount in waste.items():
                newWaste[ench]=newWaste.get(ench,0)+amount
            for ench,amount in wasted.items():
                newWaste[ench]=newWaste.get(ench,0)+amount
            tooMuchWaste = False
            for ench,amount in wasteAllowed.items():
                if newWaste.get(ench,0) > amount: tooMuchWaste = True; break
            if tooMuchWaste: unCombine(bb,i,it,newBook); continue

            found = loopBoi(bb,newWaste)
            DPMAN[stateKey(bb)]=found
            unCombine(bb,i,it,newBook)
            # assert bbOld==stateKey(bb),"STATE RESTORE FAIL"
            if found: print("@",end=""); return True
        return False



    def tryCombine(bb:list[Book],b1Index:int,b2Index:int) -> tuple[bool,int,dict[Ench,int]]:
        """modify bb in place, return False if not valid"""
        # print("COMBINE")
        b1=bb[b1Index];b2=bb[b2Index]
        b1.amount -= 1
        b2.amount -= 1
        nb = b1.copy(amount=1)
        sus,cos,was = nb.combineWith(b2)
        stacked = False
        for b in bb:
            if not b.canStackWith(nb): continue
            b.amount += 1; stacked = True; break
        if not stacked: bb.append(nb)
        return sus,cos,was,nb
    def unCombine(bb:list[Book],b1Index:int,b2Index:int,nb:Book):
        """unmodify the modified bb in place"""
        # print("UNCOMBINE")
        b1=bb[b1Index];b2=bb[b2Index]
        b1.amount += 1
        b2.amount += 1
        found = False
        # print(nb)
        # print("BB:")
        for b in bb:
            # print(b)
            if not b.canStackWith(nb): continue
            b.amount -= 1; found = True
            # if b.amount==0: bb.remove(b)
            break
        if not found: raise RuntimeError("SOMEHOW THE COMBINED NEW BOOK IS GONE")
    def stateKey(bb:list[Book]):
        return tuple(sorted(book.key() for book in bb if book.amount>0))
    start = time()
    print("start loop")
    result = loopBoi(bb,{})
    if result:print("FOUND COMBINATION")
    else:print("DIDN'T FOUND COMBINATION BRUH")
    print(f"done loop in {time()-start}")
    print(stateKey(bookBag))
    # 6407:134780
    # EQU [吸血4, 冰凍3, 智慧5]*1, PUNSHENT=63
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@FOUND COMBINATION
    # done loop in 17.794246196746826

def calWasteAllowed(targetEnchs:list[tuple[bool,Ench,int]],bookBag:list[Book]):
    result:dict[Ench,int] = {}
    for fromOneUp,ench,lvl in targetEnchs:
        result[ench] = -(2**(lvl-1))
    for book in bookBag:
        for ench,lvl in book.enchess.items():
            amount = result.get(ench)
            if amount is None: continue
            result[ench] += (2**(lvl-1))*book.amount
    if any([i<0 for i in result.values()]):raise ValueError("NOT ENOUGHT ENCHBOOK FOR TARGET ENCH IN PENDING TABLE")
    return result