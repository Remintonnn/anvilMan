import json
from dataclasses import dataclass
from enum import Enum
from calc.enchJsonGen.enchJsonGen import ench as EnchantmentId
from calc.enchJsonGen.enchJsonGen import enchTags as EnchantmentTags
from calc.enchJsonGen.enchJsonGen import comp as EnchantableItems

THE_ENCH_CONFLICT_MAP = []

class EnchantmentsClass:
    def __getitem__(self, key:str):
        return self.dict[key]
    def __init__(self):
        ENCH_JSON = r"calc/enchJsonGen/Ench.json"
        self.dict:dict[str,Enchantment] = {}
        self.totalEnchantments = 0
        with open(ENCH_JSON,"r",encoding="UTF-8") as jsonFile:
            totalEnch = json.load(jsonFile)
            for id, content in totalEnch.items():
                ench = Enchantment(
                    self.totalEnchantments,
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
                self.totalEnchantments += 1

@dataclass(frozen=True,slots=True)
class Enchantment:
    Id:int # only used for computing
    IdStr:str
    compatibleItems:list[str]
    maxlvl:int
    multiplierBook:int
    multiplierItem:int
    mutexEnch:list[str]
    tags:list[str]
    names:list[str]
    def isCompatibleWith(self,item:str|Enum):
        """Not optimized, please cache the result"""
        if isinstance(item,Enum): item = item.value
        if EnchantableItems.all.value in self.compatibleItems: return True
        return item in self.compatibleItems
    def conflictsWith(self,ench:"Enchantment"):
        return THE_ENCH_CONFLICT_MAP[self.Id] & (1<<ench.Id)
    def __str__(self):
        return self.names[0]
    def __repr__(self):
        return f"Enchantment({self.Id},{self.compatibleItems},{self.maxlvl},{self.multiplierBook},{self.multiplierItem},{self.mutexEnch},{self.tags},{self.names})"
    def __eq__(self, otherEnch):
        if not isinstance(otherEnch,Enchantment): return NotImplemented
        return self.Id==otherEnch.Id
    def __lt__(self, otherEnch):
        if not isinstance(otherEnch,Enchantment): return NotImplemented
        return self.Id<otherEnch.Id
    def __ge__(self, otherEnch):
        if not isinstance(otherEnch,Enchantment): return NotImplemented
        return self.Id>otherEnch.Id
    def __hash__(self):
        return self.Id

enchantments = EnchantmentsClass()
THE_ENCH_CONFLICT_MAP = [0]*enchantments.totalEnchantments
IdStr2Id={ench.IdStr:ench.Id for ench in enchantments.dict.values()}
for enchA in enchantments.dict.values():
    THE_ENCH_CONFLICT_MAP.append(0)
    for enchB in enchA.mutexEnch:
        THE_ENCH_CONFLICT_MAP[enchA.Id] |= 1 << IdStr2Id[enchB]