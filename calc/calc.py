from enum import Enum
from itertools import product
from time import time
import cProfile
from dataclasses import dataclass
from dataclasses import field

from calc.enchantments import Enchantment as Ench
from calc.enchantments import enchantments as enchs # not cap cuz it's an instance
from calc.enchantments import EnchantmentId as EnchId
from calc.enchantments import EnchantmentTags as EnchTag
from calc.enchantments import EnchantableItems as EnchItems# Constants

MAX_LEVEL = 39
MAX_TREE_SIZE = 32 # punishent=5

@dataclass(frozen=True)
class Book:
    """I just realized that having a Book class who says Book.isBook = False is kinda funny,
    but I don't really wanna name it 'Item' or something else generic""" # plus me lazy
    enchess:dict[Ench,int] = field(default_factory=dict)
    punishent:int=0
    amount:int=1 # only used for table display and init countDict, will be ignored durning calculation
    isBook:bool=True
    equ:Enum=None
    isCustom:bool=False
    _key=None

    def __post_init__(self):
        if isinstance(self.enchess,list):
            object.__setattr__(self,"enchess",dict(self.enchess))
        object.__setattr__(self, "isBook", self.equ is None)
        object.__setattr__(self, "_key", (tuple(sorted((ench.Id, lvl)for ench, lvl in self.enchess.items())),self.punishent,self.isBook))
    def asList(self) -> tuple[dict[Ench,int],int,int,bool,bool]:
        return [self.enchess,self.punishent,self.amount,self.isBook,self.isCustom]
    def copy(self,enchs:dict[Ench,int]|list[tuple[Ench,int]]=None,punishment:int=None,amount:int=None,equ:Enum|None=None,custom:bool=None):
        if isinstance(enchs,list):enchs=dict(enchs)
        if enchs is None: enchs = self.enchess
        if punishment is None: punishment = self.punishent
        if amount is None: amount = self.amount
        if equ is None: equ = self.equ
        if custom is None: custom = self.isCustom
        return Book(enchess=enchs,punishent=punishment,amount=amount,equ=equ,isCustom=custom)
    def getPenaltylvl(self):
        return (1<<self.punishent)-1
    def combineWith(self,b2:"Book") -> tuple["Book",int,dict[Ench,int]]:
        """Returns a new book, return (newBook,cost,wastedEnch)
           newBook may be None if the combine failed,
           success or not has nothing to do with MAX_LEVEL, only basic anvil rules"""
        if self.isBook and not b2.isBook: return (None,0,{}) # can't do that
        cost = self.getPenaltylvl()+b2.getPenaltylvl()
        wasted:dict[Ench,int]={}
        nbChess = self.enchess.copy()
        valid = False # if any enchantment sticks, accroding to vanilla
        for ench,lvl in b2.enchess.items():
            if not self.isBook and not ench.isCompatibleWith(self.equ):
                wasted[ench] = wasted.get(ench,0) + (1<<(lvl-1))
                continue
            # TODO: conflict detection, performance tho
            # cost += 1 if conflict
            if nbChess.get(ench) is None: nbChess[ench]=lvl
            elif nbChess[ench]==lvl: nbChess[ench]+=1
            else:
                old = nbChess[ench]
                if lvl>old: wasted[ench] = wasted.get(ench,0)+(1<<(old-1)); nbChess[ench]=lvl
                else: wasted[ench]=wasted.get(ench,0)+(1<<(lvl-1))
            valid = True
            cost += nbChess[ench]*(ench.multiplierBook if b2.isBook else ench.multiplierItem)
        nPunishent = max(self.punishent,b2.punishent)+1
        return (Book(enchess=nbChess,punishent=nPunishent,equ=self.equ,isCustom=self.isCustom) if valid else None),cost,wasted
    def key(self):
        """No longer includes amount"""
        return self._key

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
        # return self.__str__()
        return f"Book({self.enchess},{self.punishent},{self.amount},{self.equ},{self.isCustom})"
    def __eq__(self, otherBook):
        # isCustom is ignored cuz not relevent to calculation
        # amount is ignored in favor of external countDict
        if not isinstance(otherBook, Book): return NotImplemented
        if self.isBook != otherBook.isBook: return False
        if self.punishent != otherBook.punishent: return False
        if self.enchess != otherBook.enchess: return False
        return True
    def __hash__(self):
        return hash(self._key)

# TODO: isCustom propagation(Only them has weird edge case)
def generateSteps(targetEnchs:list[tuple[bool,Ench,int]],bookBag:list[Book]):
    with cProfile.Profile() as pr:
        genStepBinTree(targetEnchs,bookBag)
        # genStepDFS(targetEnchs,bookBag)
        print("===========================")
        pr.print_stats("cumtime")
def genStepBinTree(targetEnchs:list[tuple[bool,Ench,int]],bookBag:list[Book]):
    def ncw():return (None,393,None) # Default value for newBook,Cost,Waste
    # The amount in Book will be ignored, use countDict[Book] instead
    # There is no need to dynamic assign new Id for the books prduced durning combining
    # because those books are stored in the DPMAN, and won't appear in generateSplits
    book2IdDict:dict[Book,int]=dict((bookBag[i],i) for i in range(len(bookBag)))
    id2BookDict:dict[int,Book]=dict((i,bookBag[i]) for i in range(len(bookBag)))
    # The bb has been replaced :sob:
    countDict:dict[int,int]=dict((book2IdDict[b],b.amount) for b in bookBag)

    wasteAllowed = calWasteAllowed(targetEnchs,bookBag)
    # value None means bookBag cannot be combined
    DPMAN:dict[any,tuple[Book,int,dict[Ench,int]]] = {} # Dynamic Programming Module And Notes

    interation = 0; recu = 0
    cacHit,cacMis=0,0
    def loopBoi(cd:dict[int,int]):
        nonlocal cacHit,cacMis
        key = bagKey(cd)
        DPMAN[key] = ncw(); cacMis+=1 # we checked cache hit outside before calling self
        
        # nonlocal interation,recu
        # interation+=1
        for bl,amountL,br,amountR in generateSplits(cd): # we assume bl+br=br+bl for now
            # recu+=1; print(f"{interation}:{recu}")
            nbL,ccL,wwL = ncw()
            nbR,ccR,wwR = ncw()
            keyL,keyR = bagKey(bl),bagKey(br)
            leftReady = amountL==1 or keyL in DPMAN # use in because None values
            rightReady = amountR==1 or keyR in DPMAN
            if not leftReady: cacMis+=1; nbL,ccL,wwL = loopBoi(bl)
            else:
                if amountL!=1: cacHit += 1
                nbL,ccL,wwL = (id2BookDict[next(iter(bl))],0,{}) if amountL==1 else DPMAN[keyL]
            if not rightReady: cacMis+=1; nbR,ccR,wwR = loopBoi(br)
            else:
                if amountR!=1: cacHit += 1
                nbR,ccR,wwR = (id2BookDict[next(iter(br))],0,{}) if amountR==1 else DPMAN[keyR]
            nb,cc,ww = combine(nbL,nbR)
            if nb is None: continue
            cc = cc+ccL+ccR; ww = wasteCombine(ww,wwL,wwR)
            DPnb,DPcc,DPww = DPMAN[key]
            if DPnb is None: DPMAN[key] = (nb,cc,ww)
            elif nb.punishent<DPnb.punishent or (nb.punishent<=DPnb.punishent and cc<DPcc):
                DPMAN[key]=(nb,cc,ww)
        return DPMAN[key]

    def combine(bl:Book,br:Book) -> tuple[Book,int,dict[Ench,int]]:
        nb,cc,ww = ncw()
        if bl is None or br is None: return nb,cc,ww
        nb1,c1,w1 = bl.combineWith(br)
        nb2,c2,w2 = br.combineWith(bl)
        if isCombValid(nb1,c1,w1): nb=nb1;cc=c1;ww=w1
        if isCombValid(nb2,c2,w2) and c2<cc: nb=nb2;cc=c2;ww=w2 # we only compare cost for now
        return nb,cc,ww
    def generateSplits(countDict: dict[int,int]):
        bookCount = sum(countDict.values())
        vectors = (range(num + 1) for num in countDict.values())
        seen = set()
        left:dict[int,int]={}; right:dict[int,int]={} # more CD!
        for leftSet in product(*vectors): # leftSet = (0,4,4,2) for example, if 4 items in bookBag
            left.clear();right.clear()
            leftCount = sum(leftSet); rightCount = bookCount-leftCount
            if leftCount==0 or rightCount==0: continue
            if leftCount>MAX_TREE_SIZE or rightCount>MAX_TREE_SIZE: continue
            rightSet = tuple(num-leftBook for num,leftBook in zip(countDict.values(),leftSet))
            canon = min(leftSet, rightSet)
            if canon in seen: continue
            seen.add(canon)

            for (bookId, bookAmount), leftAmount in zip(countDict.items(), leftSet):
                rightAmount = bookAmount - leftAmount
                if leftAmount: left[bookId] = leftAmount
                if rightAmount: right[bookId] = rightAmount
            yield left, leftCount, right, rightCount
    def isCombValid(success:bool,cost:int,waste:dict[Ench,int]):
        if success is None: return False
        if cost>MAX_LEVEL: return False
        for ench,amount in wasteAllowed.items():
            if waste.get(ench,0)>amount: return False
        return True
    def wasteCombine(w1,w2,w3):
        result = {}
        for waste in (w1,w2,w3):
            for ench,amount in waste.items():
                result[ench] = result.get(ench,0)+amount
        return result
    def bagKey(cd:dict[int,int]):
        return tuple(cd.items())

    start = time()
    print("start loop")
    print(f"Total books: {sum(b.amount for b in bookBag)}, totalTypes: {len(bookBag)}")
    loopBoi(countDict)
    resultBook,totalXPCost,wastedEnch = DPMAN[bagKey(countDict)]
    if not resultBook is None:
        print(f"{resultBook}, PENALTY = {resultBook.getPenaltylvl()}")
        if len(wastedEnch):
            print("WASTED:")
            for ench,amount in wastedEnch.items():
                print(f"{ench.names[0]}*{amount}")
        print("FOUND COMBINATION")
    else:print("DIDN'T FOUND COMBINATION BRUH")
    print(f"done loop in {time()-start}")
    print(f"cacH:M = {cacHit}:{cacMis}")
    print(f"cacheLen = {len(DPMAN)}")
def genStepDFS(targetEnchs:list[tuple[bool,Ench,int]],bookBag:list[Book]):
    bb = [book.copy() for book in bookBag] # bb stands for bookBag
    wasteAllowed = calWasteAllowed(targetEnchs,bookBag)
    DPMAN = {} # Dynamic Programming Module And Notes

    # interation = 0; recu = 0
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
        

        # nonlocal interation, recu
        # interation += 1
        for punDif,punMax,i,it in pairs:
            # recu += 1; print(f"{interation}:{recu}")
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

def generateBooks(targetEnchs:list[tuple[bool,Ench,int]],targetEqu:Enum):
    bookBag:list[Book] = [Book(equ=targetEqu)]
    for data in targetEnchs:
        enchs,amount = [],0
        fromOneUp,ench,lvl = data
        if not fromOneUp: enchs.append((ench,lvl)); amount+=1
        else: enchs.append((ench,1)); amount=2**(lvl-1)
        book = Book(enchess=dict(enchs),amount=amount)
        bookBag.append(book)
    return bookBag