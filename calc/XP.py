THE_BIG_LIST=[0]
def _lvl2xp(n:int):
    if n<=16: # 0~16
        return n**2 + 6*n
    if n<32: # 17~31
        return 2.5*n*n - 40.5*n + 360
    else: # 32+
        return 4.5*n*n - 162.5*n + 2220

for i in range(1,127):
    THE_BIG_LIST.append(_lvl2xp(i))

def getXP(lvl:int):
    if lvl<128: return THE_BIG_LIST[lvl]
    return _lvl2xp(lvl)