from enum import Enum

from calc.enchantments import Enchantment as Ench
from calc.enchantments import enchantments as enchs # not cap cuz it's an instance
from calc.enchantments import EnchantmentId as EnchId
from calc.enchantments import EnchantmentTags as EnchTag
from calc.enchantments import EnchantableItems as EnchItems# Constants

MAX_LEVEL = 39
def PUNISHEMNT(n):return (2**n)-1

class Book:
    def __init__(self,enchs:list[tuple[Ench,int]]=None,punishment:int=0,amount:int=0,custom:bool=False):
        self.enchess = [] if enchs is None else enchs
        self.punishent = punishment
        self.amount = amount
        self.isCustom = custom
    def addEnch(self,ench:Ench,lvl:int):
        self.enchess.append((ench,lvl))
    def asList(self) -> tuple[list[tuple[Ench,int]],int,int,bool]:
        return [self.enchess,self.punishent,self.amount,self.isCustom]

def generateBooks(targetEnchs:list[tuple[bool,Ench,int]]):
    bookBag:list[Book] = []
    for data in targetEnchs:
        book = Book()
        fromOneUp,ench,lvl = data
        if not fromOneUp: book.addEnch(ench,lvl); book.amount=1
        else: book.addEnch(ench,1); book.amount=2**(lvl-1)
        bookBag.append(book)
    return bookBag