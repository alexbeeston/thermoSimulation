# def getEnergy(m, cp, t1, t2):
#     return m*cp*(t2-t1)
#
# def gett2(dH, m, cp, t1):
#     return (dH / (m * cp)) + t1
#
#
# m = 15  # kg
# cp = 4.184  # kJ/ (kg * c)
# t1 = 20 # C
# t2 = 30 # C
# dH = 627.6 # kJ
#
# print("--Config--")
# print("  m = " + str(m))
# print("  t1 = " + str(t1))
# print("  t2 =  " + str(t2))
# print("  dH =  " + str(dH))
# print("dH(m, cP, dT) = " + str(getEnergy(m, cp, t1, t2)))
# print("t2(dH, m, cP, t1) = " + str(gett2(dH, m, cp, t1)))

###
#PIP INSTALL MATPLOT
###

# libraries
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
#
# # Data
# df = pd.DataFrame({'x': range(1, 11), 'y1': np.random.randn(10), 'y2': np.random.randn(10) + range(1, 11),
#                    'y3': np.random.randn(10) + range(11, 21)})
#
# # multiple line plot
# plt.plot('x', 'y1', data=df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
# plt.plot('x', 'y2', data=df, marker='', color='olive', linewidth=2)
# plt.plot('x', 'y3', data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
# plt.legend()

import matplotlib.pyplot as plt

x = [0, 1, 2, 3, 4, 5]
y1 = [1, 3, 5, 7, 8, 9]
y2 = [2, 2, 2, 7, 7, 7]

plt.plot(x, y1, color="green")
plt.plot(x, y2, color="orange")
plt.xlabel("Time")
plt.ylabel("stuff")
plt.title("my chart!")
plt.show()
