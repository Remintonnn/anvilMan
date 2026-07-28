from enum import Enum, StrEnum
import json

"""
This thing Generates the json file of Enchantment infos
comp is for storing compatible items
ench is for storing enchantment names

In case you're wondering, No, I didn't type these by hand,
most of these entry are generated via google sheet,
except for the mutexEnch part, which uhhh is doable but why
"""

TheBigDict = {}
class comp(Enum):
    """Compatible items"""
    hat = "Helmet"
    cloth = "Chestplate"
    pants = "Leggings"
    shoes = "Boots"
    wing = "Elytra"
    armors = [hat,cloth,pants,shoes]
    # [*comp.armors.value,comp.wing.value] works too
    armorsAndWing = [hat,cloth,pants,shoes,wing]
    sword = "Sword"
    axe = "Axe"
    mase = "Mase"
    spear = "Spear"
    meleeSAMS = [sword,axe,mase,spear]
    meleeSAS = [sword,axe,spear]
    meleeSMS = [sword,mase,spear]
    meleeSS = [sword,spear]
    pickaxe = "Pickaxe"
    shovel = "Shovel"
    hoe = "Hoe"
    shears = "Shears"
    miningToolPASSH = [pickaxe,axe,shovel,shears,hoe]
    miningToolPASH = [pickaxe,axe,shovel,hoe]
    bow = "Bow"
    crossbow = "Crossbow"
    trident = "Trident"
    fishingRod = "FishingRod"
    shield = "Shield"
    all = "All"
class ench(StrEnum):
    """Enchantment names"""
    # Vanilla
    protection="protection"
    fireProtection="fireProtection"
    featherFalling="featherFalling"
    blastProtection="blastProtection"
    projectileProtection="projectileProtection"
    thorns="thorns"
    respiration="respiration"
    depthStrider="depthStrider"
    aquaAffinity="aquaAffinity"
    sharpness="sharpness"
    smite="smite"
    baneOfArthropods="baneOfArthropods"
    knockback="knockback"
    fireAspect="fireAspect"
    looting="looting"
    efficiency="efficiency"
    silkTouch="silkTouch"
    unbreaking="unbreaking"
    fortune="fortune"
    power="power"
    punch="punch"
    flame="flame"
    infinity="infinity"
    luckOfTheSea="luckOfTheSea"
    lure="lure"
    frostWalker="frostWalker"
    mending="mending"
    curseOfBinding="curseOfBinding"
    curseOfVanishing="curseOfVanishing"
    impaling="impaling"
    riptide="riptide"
    loyalty="loyalty"
    channeling="channeling"
    multishot="multishot"
    piercing="piercing"
    quickCharge="quickCharge"
    soulSpeed="soulSpeed"
    swiftSneak="swiftSneak"
    windBurst="windBurst"
    density="density"
    breach="breach"
    lunge="lunge"
    sweepingEdge="sweepingEdge"
    # bud
    voiceKizunaAkari="voiceKizunaAkari"
    voiceYuzukiYukari="voiceYuzukiYukari"
    voiceKotonohaAkane="voiceKotonohaAkane"
    voiceKotonohaAoi="voiceKotonohaAoi"
    autoRepair="autoRepair"
    criticalChance="criticalChance"
    oreSmelting="oreSmelting"
    vampiric="vampiric"
    healthy="healthy"
    gale="gale"
    breakRecovery="breakRecovery"
    extension="extension"
    spear="spear"
    miniaturize="miniaturize"
    giantify="giantify"
    nimble="nimble"
    frozen="frozen"
    delicacy="delicacy"
    steadySneak="steadySneak"
    wisdom="wisdom"
    sacrificeExperience="sacrificeExperience"
    knockbackResistance="knockbackResistance"
    buoyancy="buoyancy"
    gravity="gravity"
    stubborn="stubborn"
    fragile="fragile"
    windBlast="windBlast"
    eternal="eternal"
    overclocking="overclocking"
    lightSpeed="lightSpeed"
    infiniteDurability="infiniteDurability"
class enchTags(StrEnum):
    vanilla="vanilla"
    catBud="catBud"

def EnchantmentObjectMaker(ID:Enum,CompatibleItems:list|Enum,Muitiplier:int,MaxLevel:int,Names:list[str],Tags:None):
    global TheBigDict
    if Tags is None: Tags = []
    if isinstance(CompatibleItems,Enum): CompatibleItems = CompatibleItems.value
    if not isinstance(CompatibleItems,list): CompatibleItems = [CompatibleItems]
    if not isinstance(Names,list): Names = [Names]
    dictThing = {
        "CompatibleItems":CompatibleItems,
        "Muitiplier":Muitiplier,
        "MaxLevel":MaxLevel,
        "MutexEnch":[],
        "Tags":Tags,
        "Names":Names
    }
    TheBigDict[ID]=dictThing

def VanillaEnch():
    def EOM(Name, CompatibleItems, Multiplier, MaxLevel, Names):
        return EnchantmentObjectMaker(Name, CompatibleItems, Multiplier, MaxLevel, Names, [enchTags.vanilla])
    # Ordered via ID, see https://minecraft.wiki/w/Anvil_mechanics#Costs_for_combining_enchantments
    EOM(ench.protection,comp.armors,1,4,["保護","Protection"])
    EOM(ench.fireProtection,comp.armors,1,4,["火焰保護","Fire Protection"])
    EOM(ench.featherFalling,comp.shoes,1,4,["輕盈","Feather Falling"])
    EOM(ench.blastProtection,comp.armors,2,4,["爆炸保護","Blast Protection"])
    EOM(ench.projectileProtection,comp.armors,1,4,["投射物保護","Projectile Protection"])
    EOM(ench.thorns,comp.armors,4,3,["尖刺","Thorns"])
    EOM(ench.respiration,comp.hat,2,3,["水中呼吸","Respiration"])
    EOM(ench.depthStrider,comp.shoes,2,3,["深海漫遊","Depth Strider"])
    EOM(ench.aquaAffinity,comp.hat,2,1,["親水性","Aqua Affinity"])
    EOM(ench.sharpness,comp.meleeSAS,1,5,["鋒利","Sharpness"])
    EOM(ench.smite,comp.meleeSAMS,1,5,["不死剋星","Smite"])
    EOM(ench.baneOfArthropods,comp.meleeSAMS,1,5,["節肢剋星","Bane of Arthropods"])
    EOM(ench.knockback,comp.meleeSS,1,2,["擊退","Knockback"])
    EOM(ench.fireAspect,comp.meleeSMS,2,2,["燃燒","Fire Aspect"])
    EOM(ench.looting,comp.meleeSS,2,3,["掠奪","Looting"])
    EOM(ench.efficiency,comp.miningToolPASSH,1,5,["效率","Efficiency"])
    EOM(ench.silkTouch,comp.miningToolPASH,4,1,["絲綢之觸","Silk Touch"])
    EOM(ench.unbreaking,comp.all,1,3,["耐久","Unbreaking"])
    EOM(ench.fortune,comp.miningToolPASH,2,3,["幸運","Fortune"])
    EOM(ench.power,comp.bow,1,5,["強力","Power"])
    EOM(ench.punch,comp.bow,2,2,["衝擊","Punch"])
    EOM(ench.flame,comp.bow,2,1,["火焰","Flame"])
    EOM(ench.infinity,comp.bow,4,1,["無限","Infinity"])
    EOM(ench.luckOfTheSea,comp.fishingRod,2,3,["海洋的祝福","Luck of the Sea"])
    EOM(ench.lure,comp.fishingRod,2,3,["魚餌","Lure"])
    EOM(ench.frostWalker,comp.shoes,2,2,["冰霜行者","Frost Walker"])
    EOM(ench.mending,comp.all,2,1,["修補","Mending"])
    EOM(ench.curseOfBinding,comp.armorsAndWing,4,1,["綁定詛咒","Curse of Binding"])
    EOM(ench.curseOfVanishing,comp.all,4,1,["消失詛咒","Curse of Vanishing"])
    EOM(ench.impaling,comp.trident,2,5,["魚叉","Impaling"])
    EOM(ench.riptide,comp.trident,2,3,["波濤","Riptide"])
    EOM(ench.loyalty,comp.trident,1,3,["忠誠","Loyalty"])
    EOM(ench.channeling,comp.trident,4,1,["喚雷","Channeling"])
    EOM(ench.multishot,comp.crossbow,2,1,["分裂箭矢","Multishot"])
    EOM(ench.piercing,comp.crossbow,1,4,["貫穿","Piercing"])
    EOM(ench.quickCharge,comp.crossbow,1,3,["快速上弦","Quick Charge"])
    EOM(ench.soulSpeed,comp.shoes,4,3,["靈魂疾走","Soul Speed"])
    EOM(ench.swiftSneak,comp.pants,4,3,["迅捷潛行","Swift Sneak"])
    EOM(ench.windBurst,comp.mase,2,3,["風爆","Wind Burst"])
    EOM(ench.density,comp.mase,1,5,["緻密","Density"])
    EOM(ench.breach,comp.mase,2,4,["破甲","Breach"])
    EOM(ench.lunge,comp.spear,1,3,["突刺","Lunge"])
    EOM(ench.sweepingEdge,comp.sword,2,3,["橫掃之刃","Sweeping Edge"])
def CatBudEnch():
    def EOM(Name, CompatibleItems, Multiplier, MaxLevel, Names):
        return EnchantmentObjectMaker(Name, CompatibleItems, Multiplier, MaxLevel, Names, [enchTags.catBud])
    EOM(ench.voiceKizunaAkari,comp.hat,1,1,["動作音效 紲星燈","Voice Kizuna Akari"])
    EOM(ench.voiceYuzukiYukari,comp.hat,1,1,["動作音效 結月緣","Voice Yuzuki Yukari"])
    EOM(ench.voiceKotonohaAkane,comp.hat,1,1,["動作音效 琴葉茜","Voice Kotonoha Akane"])
    EOM(ench.voiceKotonohaAoi,comp.hat,1,1,["動作音效 琴葉葵","Voice Kotonoha Aoi"])
    EOM(ench.autoRepair,comp.all,1,3,["自動修補","Auto Repair"])
    EOM(ench.criticalChance,comp.axe,1,4,["爆擊可能","Critical Chance"])
    EOM(ench.oreSmelting,comp.pickaxe,4,1,["自動熔煉","Ore Smelting"])
    EOM(ench.vampiric,comp.meleeSS,1,4,["吸血","Vampiric"])
    EOM(ench.healthy,comp.cloth,1,3,["健康","Healthy"])
    EOM(ench.gale,comp.wing,1,3,["疾風","Gale"])
    EOM(ench.breakRecovery,comp.all,1,1,["毀損救援","Break Recovery"])
    EOM(ench.extension,comp.miningToolPASSH,1,3,["延伸","Extension"])
    EOM(ench.spear,comp.axe,1,3,["長茅","Spear"])
    EOM(ench.miniaturize,comp.armors,1,1,["迷你化","Miniaturize"])
    EOM(ench.giantify,comp.armors,1,2,["巨大化","Giantify"])
    EOM(ench.nimble,comp.wing,1,3,["靈巧","Nimble"])
    EOM(ench.frozen,comp.sword,2,3,["冰凍","Frozen"])
    EOM(ench.delicacy,comp.hat,1,3,["美食","Delicacy"])
    EOM(ench.steadySneak,comp.pants,4,3,["穩重潛行","Steady Sneak"])
    EOM(ench.wisdom,comp.meleeSS,1,5,["智慧","Wisdom"])
    EOM(ench.sacrificeExperience,comp.armors,4,1,["獻祭經驗","Sacrifice Experience"])
    EOM(ench.knockbackResistance,comp.armors,1,2,["擊退保護","Knockback Resistance"])
    EOM(ench.buoyancy,comp.wing,2,3,["浮力","Buoyancy"])
    EOM(ench.gravity,comp.cloth,2,3,["重力","Gravity"])
    EOM(ench.stubborn,comp.cloth,1,4,["掘強","Stubborn"])
    EOM(ench.fragile,comp.cloth,1,3,["脆弱","Fragile"])
    EOM(ench.windBlast,comp.shield,2,5,["風擊","Wind Blast"])
    EOM(ench.eternal,comp.all,1,1,["不滅","Eternal"])
    EOM(ench.overclocking,comp.miningToolPASSH,1,5,["超頻","Overclocking"])
    EOM(ench.lightSpeed,comp.shoes,4,3,["燭光疾走","Light Speed"])
    EOM(ench.infiniteDurability,comp.all,1,1,["無限耐久","Infinite Durability"])

def mutexEnchs():
    # See Trident or Dur bar is a lie for more complex mutex relations
    mutexEnchGroups = [
        [
            # DMG
            ench.sharpness,
            ench.smite,
            ench.baneOfArthropods,
            ench.density,
            ench.breach
        ],[
            # Mining Effect
            ench.fortune,
            ench.silkTouch
        ],[
            # Prots
            ench.protection,
            ench.fireProtection,
            ench.projectileProtection,
            ench.blastProtection
        ],[
            # Boots
            ench.depthStrider,
            ench.frostWalker
        ],[
            # Bow
            ench.infinity,
            ench.mending
        ],[
            # Trident 1
            ench.riptide,
            ench.loyalty
        ],[
            # Trident 2
            ench.riptide,
            ench.channeling
        ],[
            # Crossbow
            ench.multishot,
            ench.piercing
        ],[
            # THE VOICE IN MY HEAD
            ench.voiceKizunaAkari,
            ench.voiceYuzukiYukari,
            ench.voiceKotonohaAkane,
            ench.voiceKotonohaAoi
        ],[
            # Dur bar is a lie
            ench.infiniteDurability,
            ench.autoRepair,
            ench.mending
        ],[
            # Dur bar is a lie 2
            ench.infiniteDurability,
            ench.breakRecovery,
        ],[
            # Dur bar is a lie 3
            ench.infiniteDurability,
            ench.unbreaking
        ],[
            # Ore Smelting
            ench.oreSmelting,
            ench.silkTouch
        ],[
            # Vamp
            ench.vampiric,
            ench.sharpness,
            ench.smite,
            ench.baneOfArthropods
        ],[
            # Big or smol
            ench.miniaturize,
            ench.giantify
        ],[
            # Fire of ice
            ench.frozen,
            ench.fireAspect
        ],[
            # Sneaky boi
            ench.steadySneak,
            ench.swiftSneak
        ],[
            # I don't like throns anyway
            ench.sacrificeExperience,
            ench.thorns
        ],[
            # Chat are we cooked 1 (No, I didn't misread overclocking as overcooking)
            ench.overclocking,
            ench.silkTouch,
            ench.fortune
        ],[
            # Chat are we cooked 2 (...OK maybe I did)
            ench.overclocking,
            ench.unbreaking
        ],[
            # Speedy boi
            ench.lightSpeed,
            ench.soulSpeed
        ]
    ]

    # mutexEnch population logics
    for group in mutexEnchGroups:
        for oriEnch in group:
            for mutexEnch in group:
                if oriEnch != mutexEnch and mutexEnch not in TheBigDict[oriEnch]["MutexEnch"]:
                    TheBigDict[oriEnch]["MutexEnch"].append(mutexEnch)

def Dump():
    # need to unEnum before dump
    TBD = {}
    for k,v in TheBigDict.items():
        TBD[k.value] = v
    with open("Ench.json","w",encoding="utf-8") as f:
        json.dump(TBD,f,indent=4,ensure_ascii=False,default=lambda x:x.value if isinstance(x,Enum) else x)


VanillaEnch()
CatBudEnch()
mutexEnchs()
Dump()