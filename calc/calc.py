from enum import Enum
from time import time
import cProfile
import pstats
from dataclasses import dataclass
from dataclasses import field
from rich.tree import Tree
from rich import print as rprint


from calc.enchantments import Enchantment as Ench
from calc.enchantments import enchantments as enchs # not cap cuz it's an instance
from calc.enchantments import EnchantmentId as EnchId
from calc.enchantments import EnchantmentTags as EnchTag
from calc.enchantments import EnchantableItems as EnchItems# Constants

MAX_LEVEL = 39
MAX_TREE_SIZE = 32 # punishent=5
MAX_TREE_HEIGHT = 5

@dataclass(frozen=True,slots=True)
class Book:
    """I just realized that having a Book class who says Book.isBook = False is kinda funny,
    but I don't really wanna name it 'Item' or something else generic""" # plus me lazy
    enchess:dict[Ench,int] = field(default_factory=dict)
    punishent:int=0
    amount:int=1 # only used for table display and init countDict, will be ignored durning calculation
    isBook:bool=True
    equ:Enum=None
    isCustom:bool=False
    _key:tuple=field(init=False,repr=False)

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
        # result += f"]*{self.amount}"
        result += "]"
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
    # funcs = (genStepDFS,genStepBinTree,genStepTheOneTheOri)
    # todayImFeeling = funcs[1]
    todayImFeeling = genStepTheOneTheOri # feeling the one the ori!
    with cProfile.Profile() as pr:
        todayImFeeling(targetEnchs,bookBag)
        print("===========================")
        stats = pstats.Stats(pr)
        stats.sort_stats("cumtime").print_stats(25)

# while in theory these are general calculator,
# for optimization the following assumption is made:
# bookBag wont contain any enchantment that conflicts with eachother, so A+B=B+A
# bookBag only contains books with no prior anvil use
# bookBag only contains either lvl 1 book or max lvl book
# With modifications to the algorithm you can get around those limitation
# but the time complexity or 3^n is brutal you know
def genStepTheOneTheOri(targetEnchs:list[tuple[bool,Ench,int]],bookBag:list[Book]):
    """I had the idea about doint the search like this in the very start,
    but as times went by I kinda forgor about that idea,
    but after whatever that's down there, I finally rember this exist now.
    Ancient technology, awake!(the next installment)
    """
    def bagPad(bb:list[Book]): # find the Pad for the Bag
        bookNum = sum(b.amount for b in bb)
        treeDepth = int.bit_length(bookNum-1)
        emptySlots = (1<<treeDepth)-bookNum
        return treeDepth,emptySlots
    wasteAllowed = calWasteAllowed(targetEnchs,bookBag)
    treeDepth,emptySlots = bagPad(bookBag)
    book2IdDict:dict[Book,int]=dict((bookBag[i],i) for i in range(len(bookBag)))
    id2BookDict:dict[int,Book]=dict((i,bookBag[i]) for i in range(len(bookBag)))
    countDict:dict[int,int]=dict((book2IdDict[b],b.amount) for b in bookBag)
    book2IdDict[-1]=-1;id2BookDict[-1]=-1;countDict[-1]=emptySlots
    DPMAN:dict[tuple,DPPOINT] = {} # Dynamic Programming Modules And Notes

    cacHit,cacMis,BAD = 0,0,0
    # Tree? more like ROOT
    # Actually maybe I should call it side, or zoom?
    # this is just deciding order so not like we're going up the tree?
    def loopBoi(cd:dict[int,int],depth:int):
        nonlocal cacHit,cacMis,BAD
        key = bagKey(cd)
        DPMAN[key] = DPPOINT(); cacMis+=1
        for bl,br in generateSplits(cd,depth): # we assume bl+br=br+bl for now
            nbL,ccL,wwL = None,393,None
            nbR,ccR,wwR = None,393,None
            keyL,keyR = bagKey(bl),bagKey(br)
            if keyL in DPMAN: cacHit += 1; nbL,ccL,wwL = DPMAN[keyL].ncw()
            elif depth==1: nbL,ccL,wwL = id2BookDict[next(iter(bl))],0,{}
            else: cacMis+=1; nbL,ccL,wwL = loopBoi(bl,depth-1)
            if keyR in DPMAN: cacHit += 1; nbR,ccR,wwR = DPMAN[keyR].ncw()
            elif depth==1: nbR,ccR,wwR = id2BookDict[next(iter(br))],0,{}
            else: cacMis+=1; nbR,ccR,wwR = loopBoi(br,depth-1)
            nb,cc,ww = combine(nbL,nbR)
            if nb is None: continue
            cc = cc+ccL+ccR; ww = wasteCombine(ww,wwL,wwR)
            DPnb,DPcc,DPww = DPMAN[key].ncw()
            if  DPnb is None or nb.punishent<DPnb.punishent or (nb.punishent<=DPnb.punishent and cc<DPcc):
                DPMAN[key]=DPPOINT(nb,cc,ww,keyL if depth!=1 else None,keyR if depth!=1 else None,bl,br)
        return DPMAN[key].ncw()
    def combine(bl:Book,br:Book) -> tuple[Book,int,dict[Ench,int]]:
        if bl is None or br is None: return None,393,None
        if isinstance(bl,int): return br,0,{}
        if isinstance(br,int): return bl,0,{}
        nb,cc,ww = None,393,None
        nb1,c1,w1 = bl.combineWith(br)
        nb2,c2,w2 = br.combineWith(bl)
        if isCombValid(nb1,c1,w1): nb=nb1;cc=c1;ww=w1
        if isCombValid(nb2,c2,w2) and c2<cc: nb=nb2;cc=c2;ww=w2 # we only compare cost for now
        return nb,cc,ww
    split=0
    def generateSplits(countDict: dict[int,int],depth:int):
        nonlocal split
        cdVal,cdKey = list(countDict.values()),list(countDict.keys())
        left:dict[int,int]; right:dict[int,int] # more CD!
        for leftSet, rightSet in productXL(cdVal,depth,None if -1 not in cdKey else cdKey.index(-1)):
            left={};right={};split+=1
            for bookId, leftAmount, rightAmount in zip(cdKey,leftSet,rightSet):
                if leftAmount: left[bookId] = leftAmount
                if rightAmount: right[bookId] = rightAmount
            yield left, right
    def productXL(bookNums:list[int],treeDepth:int,emptyIndex:int|None):
        totalBook,totalHalf = 1<<treeDepth,1<<(treeDepth-1)
        halfTotalBook = [num//2 for num in bookNums]
        isBookNumEven = [num&1==0 for num in bookNums]
        bookTypes = len(bookNums)
        remaingBooks = []; temp = totalBook
        for num in bookNums: temp-=num; remaingBooks.append(temp)
        # print(f"remainingBooks: {remaingBooks}")
        left = [0]*bookTypes
        def dfs(depth,leftCount,headLess):
            if depth == bookTypes:
                lefties = tuple(left)
                rightiest = tuple(total-lefty for total,lefty in zip(bookNums, lefties))
                yield lefties, rightiest
                return
            maxTake = bookNums[depth]
            for x in range(maxTake + 1):
                bnIsEven,halfPoint = isBookNumEven[depth],halfTotalBook[depth]
                if not headLess and x>halfPoint: break
                if depth!=emptyIndex and bnIsEven:
                    # check if the split is uneven, which leads to ench waste
                    # we only allow [1,1] [0,8] [4,4] here
                    if x!=0 and x!=maxTake and x!=halfPoint: continue
                    # prevent weird splits like ((A,B),(A,C)) for A
                    if totalBook!=2 and x==1: continue
                newCount = leftCount + x # newCount i.e. left only goes up from here
                if newCount+remaingBooks[depth] < totalHalf: continue # took too little
                if newCount > totalHalf: break # took too much
                left[depth] = x
                # the headLess is treated differently, 
                # because for even numbers the half point sits perfectly in the middle
                # so x is not really less when x==halfPoint
                yield from dfs(depth+1, newCount, headLess or (x<halfPoint if bnIsEven else x<=halfPoint))
        yield from dfs(0,0,False)
    def isCombValid(success:bool,cost:int,waste:dict[Ench,int]):
        if success is None: return False
        if cost>MAX_LEVEL: return False
        for ench,amount in waste.items():
            if wasteAllowed.get(ench,393) < amount: return False
        return True
    def wasteCombine(w1,w2,w3):
        result = {}
        for waste in (w1,w2,w3):
            for ench,amount in waste.items():
                result[ench] = result.get(ench,0)+amount
        return result
    def bagKey(cd:dict[int,int]): return tuple(cd.items())
    
    @dataclass(slots=True)
    class DPPOINT:
        book:Book=None
        cost:int=393
        waste:dict[Ench,int]=None
        keyL:tuple=None
        keyR:tuple=None
        bagL:dict[int,int]=None
        bagR:dict[int,int]=None
        def ncw(self): return self.book,self.cost,self.waste
        def __str__(self): return str(self.book)
    def treePrinter(DPMAN:dict[any,DPPOINT],key:tuple,id2BookDict:dict[int,Book]):
        print("TREE WALKING TIME")
        resultBook,totalXPCost,wastedEnch = DPMAN[bagKey(countDict)].ncw()
        root = Tree(f"{resultBook}, PENALTY = {resultBook.getPenaltylvl()}")
        def nodeWalker(key:tuple, parentNode:Tree):
            dp = DPMAN[key]
            kl,kr = dp.keyL,dp.keyR
            bookIdL,bookIdR = next(iter(dp.bagL.keys())),next(iter(dp.bagR.keys()))
            if bookIdL != -1:
                if kl is None: parentNode.add(str(id2BookDict[bookIdL]))
                else: nodeWalker(kl,parentNode.add(""))
            if bookIdR != -1:
                if kr is None: parentNode.add(str(id2BookDict[bookIdR]))
                else: nodeWalker(kr,parentNode.add(""))
        nodeWalker(key, root)
        rprint(root)
        print(f"Total XP lvl cost: {totalXPCost}")
        if len(wastedEnch):
            print("WASTED:")
            for ench,amount in wastedEnch.items():
                print(f"{ench.names[0]}*{amount}")

    start = time()
    print("start loop")
    print(f"Total books: {sum(b.amount for b in bookBag)}, totalTypes: {len(bookBag)}")
    loopBoi(countDict,treeDepth)
    print(f"done loop in {time()-start}")
    print(f"cacH:M = {cacHit}:{cacMis}")
    print(f"cacheLen = {len(DPMAN)}, split = {split}, avg {(split/len(DPMAN)):.2f} split per state")
    print(f"BAD: {BAD}")
    print(f"Vals: {list(countDict.values())}")
    resultBook,totalXPCost,wastedEnch = DPMAN[bagKey(countDict)].ncw()
    if resultBook is not None:
        treePrinter(DPMAN,bagKey(countDict),id2BookDict)
        print("FOUND COMBINATION")
    else:print("DIDN'T FOUND COMBINATION BRUH")
# This only work if bookBag contains no conflicting enchantment, so A+B=B+A
def genStepBinTree(targetEnchs:list[tuple[bool,Ench,int]],bookBag:list[Book]):
    """This will search through all possible Tree and combination,
    garanteeing the optimal solution,
    but with a big O of 4^n or some crazy BS,
    better not use this on more then 20~30 books.
    I just left this here because I have spend too much time on this to remove it,
    Take this as a trophy of past I suppose.
    """ # man the data trees REALLY are a pain in the ass
    def ncw():return None,393,None # Default value for newBook,Cost,Waste
    # The amount in Book will be ignored, use countDict[Book] instead
    # There is no need to dynamic assign new Id for the books prduced durning combining
    # because those books are stored in the DPMAN, and won't appear in generateSplits
    book2IdDict:dict[Book,int]=dict((bookBag[i],i) for i in range(len(bookBag)))
    id2BookDict:dict[int,Book]=dict((i,bookBag[i]) for i in range(len(bookBag)))
    # The bb has been replaced :sob:
    countDict:dict[int,int]=dict((book2IdDict[b],b.amount) for b in bookBag)

    wasteAllowed = calWasteAllowed(targetEnchs,bookBag)
    # value None means bookBag cannot be combined
    DPMAN:dict[any,DPPOINT] = {} # Dynamic Programming Module And Notes

    interation = 0; recu = 0
    cacHit,cacMis=0,0
    # truncate height somehow prunes legit soluion
    heightTruncate = 0
    BAD = 0; heightRecord = 0
    def loopBoi(cd:dict[int,int],height:int=0):
        nonlocal cacHit,cacMis,heightTruncate,BAD,heightRecord
        if height>heightRecord: heightRecord = height
        # if height>MAX_TREE_HEIGHT: BAD+=1
        # we checked cache hit outside before calling self
        key = bagKey(cd)
        DPMAN[key] = DPPOINT(); cacMis+=1
        # nonlocal interation,recu
        # interation+=1
        for bl,amountL,br,amountR in generateSplits(cd): # we assume bl+br=br+bl for now
            # recu+=1; print(f"{interation}:{recu}")
            nbL,ccL,wwL = ncw()
            nbR,ccR,wwR = ncw()
            keyL,keyR = bagKey(bl),bagKey(br)
            leftReady = amountL==1 or keyL in DPMAN # use in because None values
            rightReady = amountR==1 or keyR in DPMAN
            # if height==MAX_TREE_HEIGHT+5 and (not leftReady or not rightReady): heightTruncate += 1; continue
            if not leftReady: cacMis+=1; nbL,ccL,wwL = loopBoi(bl,height+1)
            else:
                if amountL!=1: cacHit += 1
                nbL,ccL,wwL = (id2BookDict[next(iter(bl))],0,{}) if amountL==1 else DPMAN[keyL].ncw()
            if not rightReady: cacMis+=1; nbR,ccR,wwR = loopBoi(br,height+1)
            else:
                if amountR!=1: cacHit += 1
                nbR,ccR,wwR = (id2BookDict[next(iter(br))],0,{}) if amountR==1 else DPMAN[keyR].ncw()
            nb,cc,ww = combine(nbL,nbR)
            if nb is None: continue
            cc = cc+ccL+ccR; ww = wasteCombine(ww,wwL,wwR)
            DPnb,DPcc,DPww = DPMAN[key].ncw()
            if  DPnb is None or nb.punishent<DPnb.punishent or (nb.punishent<=DPnb.punishent and cc<DPcc):
                DPMAN[key]=DPPOINT(nb,cc,ww,keyL if amountL!=1 else None,keyR if amountR!=1 else None,bl,br)
        return DPMAN[key].ncw()
    # cacComb:dict[any,tuple[Book,int,dict[Ench,int]]] = {}
    # cacCombH,cacCombM = 0,0
    def combine(bl:Book,br:Book) -> tuple[Book,int,dict[Ench,int]]:
        # nonlocal cacCombH,cacCombM
        # no need remeber this cuz you see None you know the answer
        nb,cc,ww = ncw()
        if bl is None or br is None: return nb,cc,ww
        # bk = bookKey(bl,br)
        # if bk in cacComb: cacCombH+=1; return cacComb[bk]
        # cacCombM+=1
        nb1,c1,w1 = bl.combineWith(br)
        nb2,c2,w2 = br.combineWith(bl)
        if isCombValid(nb1,c1,w1): nb=nb1;cc=c1;ww=w1
        if isCombValid(nb2,c2,w2) and c2<cc: nb=nb2;cc=c2;ww=w2 # we only compare cost for now
        # cacComb[bk] = (nb,cc,ww)
        return nb,cc,ww
    def generateSplits(countDict: dict[int,int]):
        cdVal,cdKey = list(countDict.values()),list(countDict.keys())
        left:dict[int,int]; right:dict[int,int] # more CD!
        for leftSet, leftCount, rightSet, rightCount in productXL(cdVal):
            left={};right={}
            for bookId, leftAmount, rightAmount in zip(cdKey,leftSet,rightSet):
                if leftAmount: left[bookId] = leftAmount
                if rightAmount: right[bookId] = rightAmount
            yield left, leftCount, right, rightCount
    def productXL(bookNums:list[int]):
        totalBook = sum(bookNums)
        halfTotalBook = [num//2 for num in bookNums]
        isBookNumEven = [num&1==0 for num in bookNums]
        bookTypes = len(bookNums)
        # print(f"halfBooks: {halfTotalBook}, tookTypes: {bookTypes}")
        left = [0]*bookTypes
        def dfs(depth,leftCount,headLess):
            if depth == bookTypes:
                rightCount = totalBook-leftCount
                if leftCount == 0 or rightCount > MAX_TREE_SIZE: return
                lefties = tuple(left)
                rightiest = tuple(total-lefty for total,lefty in zip(bookNums, lefties))
                # if lefties > rightiest: return
                yield lefties, leftCount, rightiest, rightCount
                return
            maxTake = bookNums[depth]
            for x in range(maxTake + 1):
                bnIsEven,halfPoint = isBookNumEven[depth],halfTotalBook[depth]
                if not headLess and x>halfPoint: break
                # print(f"PURGED AT DEPTH {depth} with {x} > {halfTotalBook[depth]}, tup={tuple(left)}")
                # newCount i.e. left only goes up from here
                newCount = leftCount + x
                if newCount == totalBook: break
                if newCount > MAX_TREE_SIZE: break
                left[depth] = x
                # the headLess is treated differently because for even numbers,
                # the half point sits perfectly in the middle
                # so x is not really less when x==halfPoint
                # which is the case for odd numbsrs
                yield from dfs(depth+1, newCount, headLess or (x<halfPoint if bnIsEven else x<=halfPoint))
        yield from dfs(0,0,False)
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
    def bagKey(cd:dict[int,int]): return tuple(cd.items())
    
    @dataclass
    class DPPOINT:
        book:Book=None
        cost:int=393
        waste:dict[Ench,int]=None
        keyL:tuple=None
        keyR:tuple=None
        bagL:dict[int,int]=None
        bagR:dict[int,int]=None
        def ncw(self): return self.book,self.cost,self.waste
        def __str__(self): return str(self.book)
    def treePrinter(DPMAN:dict[any,DPPOINT],key:tuple,id2BookDict:dict[int,Book]):
        print("TREE WALKING TIME")
        root = Tree(str(DPMAN[key]))
        def nodeWalker(key:tuple, parentNode:Tree):
            dp = DPMAN[key]
            kl,kr = dp.keyL,dp.keyR
            if kl is None: parentNode.add(str(id2BookDict[iter(dp.bagL.keys()).__next__()]))
            else: nodeWalker(kl,parentNode.add(""))
            if kr is None: parentNode.add(str(id2BookDict[iter(dp.bagR.keys()).__next__()]))
            else: nodeWalker(kr,parentNode.add(""))
        nodeWalker(key, root)
        rprint(root)

    start = time()
    print("start loop")
    print(f"Total books: {sum(b.amount for b in bookBag)}, totalTypes: {len(bookBag)}")
    loopBoi(countDict)
    print(f"done loop in {time()-start}")
    print(f"cacH:M = {cacHit}:{cacMis}")
    print(f"cacheLen = {len(DPMAN)}")
    print(f"Height truncated: {heightTruncate}")
    print(f"Height record: {heightRecord}")
    print(f"BAD: {BAD}")
    print(f"Vals: {list(countDict.values())}")
    resultBook,totalXPCost,wastedEnch = DPMAN[bagKey(countDict)].ncw()
    if resultBook is not None:
        print(f"PRODUCT PENALTY = {resultBook.getPenaltylvl()}")
        treePrinter(DPMAN,bagKey(countDict),id2BookDict)
        if len(wastedEnch):
            print("WASTED:")
            for ench,amount in wastedEnch.items():
                print(f"{ench.names[0]}*{amount}")
        print("FOUND COMBINATION")
    else:print("DIDN'T FOUND COMBINATION BRUH")
    # start loop
    # Total books: 18, totalTypes: 7
    # EQU [保護4, 獻祭經驗1, 擊退保護2, 耐久3, 健康3, 倔強4], PENALTY = 31
    # FOUND COMBINATION
    # done loop in 3.658159017562866
    # cacH:M = 307339:4303
    # cacheLen = 2152
    # Height truncated: 2873
    # Height record: 10
    # BAD: 0
    # Vals: [1, 1, 1, 4, 8, 1, 2]
def genStepDFS(targetEnchs:list[tuple[bool,Ench,int]],bookBag:list[Book]):
    """Search through all combination of merging steps with DFS!
    This thing is so slow I didn't even get to the find optimal solution part.
    I just left this here because I have spend too much time on this to remove it,
    Take this as a trophy of past I suppose.
    The data classes has changed quite a bit since then, so this function is kinda broken rn.
    """ # I'm surprised how far this thing got, I mean, 20 books before search time exploding
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
    if any(i<0 for i in result.values()):raise ValueError("NOT ENOUGHT ENCHBOOK FOR TARGET ENCH IN PENDING TABLE")
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