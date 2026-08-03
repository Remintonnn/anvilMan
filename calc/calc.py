from enum import Enum

from calc.enchantments import Enchantment as Ench
from calc.enchantments import enchantments as enchs # not cap cuz it's an instance
from calc.enchantments import EnchantmentId as EnchId
from calc.enchantments import EnchantmentTags as EnchTag
from calc.enchantments import EnchantableItems as EnchItems# Constants

MAX_LEVEL = 39
def PUNISHEMNT(n):return (2**n)-1

def generateBooks(targetEnchs:list[tuple[bool,Ench,int]]):
    bookBag:list[tuple[list[tuple[Ench,int]],int,int,bool]] = []
    for data in targetEnchs:
        # [[(ench,lvl)],punishment,number,custom]
        book:tuple[list[tuple[Ench,int]],int,int,bool] = [[],0,0,False]
        fromOneUp,ench,lvl = data
        if not fromOneUp: book[0].append([ench,lvl]); book[2]=1
        else: book[0].append([ench,1]); book[2]=2**(lvl-1)
        bookBag.append(book)
    return bookBag