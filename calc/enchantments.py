import json
from enum import Enum
from calc.enchJsonGen.enchJsonGen import ench as EnchantmentId
from calc.enchJsonGen.enchJsonGen import enchTags as EnchantmentTags
from calc.enchJsonGen.enchJsonGen import comp as EnchantableItems

class EnchantmentsClass:
    def __getitem__(self, key:str):
        return self.dict[key]
    def __init__(self):
        ENCH_JSON = r"calc/enchJsonGen/Ench.json"
        self.dict:dict[str,Enchantment] = {}
        with open(ENCH_JSON,"r",encoding="UTF-8") as jsonFile:
            totalEnch = json.load(jsonFile)
            for id, content in totalEnch.items():
                ench = Enchantment(
                    content["Id"],
                    content["CompatibleItems"],
                    content["MaxLevel"],
                    content["MultiplierBook"],
                    content["MultiplierItem"],
                    content["MutexEnch"],
                    content["Tags"],
                    content["Names"]
                )
                self.dict[id] = ench

class Enchantment:
    def __init__(self,Id,comp,maxlvl,mulBook,mulItem,mutex,tags,names):
        self.Id = Id
        self.compatibleItems:list[str] = comp
        self.maxlvl:int = maxlvl
        self.multiplierBook:int = mulBook
        self.multiplierItem:int = mulItem
        self.mutexEnch:list[str] = mutex
        self.tags:list[str] = tags
        self.names:list[str] = names
    def isCompatibleWith(self,item:str|Enum):
        if isinstance(item,Enum): item = item.value
        if EnchantableItems.all.value in self.compatibleItems: return True
        return item in self.compatibleItems
    def conflictsWith(self,ench:"Enchantment"):
        return ench.Id in self.mutexEnch

enchantments = EnchantmentsClass()
# ==================

# tot = Enchantments()
# for k in tot.dict.keys():
#     e = tot.dict[k]
#     print(tot.dict[k].names)
# print(EnchantmentId.protection)