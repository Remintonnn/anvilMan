import json
from calc.enchJsonGen.enchJsonGen import ench as EnchantmentId
from calc.enchJsonGen.enchJsonGen import enchTags as EnchantmentTags
from calc.enchJsonGen.enchJsonGen import comp as enchItems

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
                    content["CompatibleItems"],
                    content["Muitiplier"],
                    content["MaxLevel"],
                    content["MutexEnch"],
                    content["Tags"],
                    content["Names"]
                )
                self.dict[id] = ench

class Enchantment:
    def __init__(self,comp,multiplier,maxlvl,mutex,tags,names):
        self.compatableItems:list[str] = comp
        self.multiplier:int = multiplier
        self.maxlvl:int = maxlvl
        self.mutexEnch:list[str] = mutex
        self.tags:list[str] = tags
        self.names:list[str] = names

enchantments = EnchantmentsClass()
# ==================

# tot = Enchantments()
# for k in tot.dict.keys():
#     e = tot.dict[k]
#     print(tot.dict[k].names)
# print(EnchantmentId.protection)