def getEnergy(m, cp, t1, t2):
    return m*cp*(t2-t1)

def gett2(dH, m, cp, t1):
    return (dH / (m * cp)) + t1


m = 15  # kg
cp = 4.184  # kJ/ (kg * c)
t1 = 20 # C
t2 = 30 # C
dH = 627.6 # kJ

print("--Config--")
print("  m = " + str(m))
print("  t1 = " + str(t1))
print("  t2 =  " + str(t2))
print("  dH =  " + str(dH))
print("dH(m, cP, dT) = " + str(getEnergy(m, cp, t1, t2)))
print("t2(dH, m, cP, t1) = " + str(gett2(dH, m, cp, t1)))
