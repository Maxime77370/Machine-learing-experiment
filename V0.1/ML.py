import matplotlib.pyplot as plt
import numpy as np
import random as rd

def f(n, x):
    S = np.sin(X)
    coef = []
    return S, coef

def ML(generation ,enfant, pas, n, x):
    coef_global = [0]*n
    delta_min = None
    for k_1 in range(generation):
        for k_2 in range(enfant):
            coef = coef_global[:]
            S = 0
            for i in range(n):
                coef[i] = coef[i] + pas*(rd.random()*2-1)
                S += x**i*coef[i]
            delta = np.sum((np.abs(S-Y1)))
            if delta_min == None or delta < delta_min :
                delta_min = delta
                coef_local = coef[:]
                S_best = S
                plt.plot(x, S_best,'g', linewidth=0.2)
                plt.pause(0.00001)
                print(delta_min)
        coef_global = coef_local[:]
    return S, coef_global

X = np.linspace(0,5,100)
Y1, coef_1 = f(10,X)
plt.plot(X,Y1,'b')
Y2, coef_2 = ML(500,100,0.01,10,X)
plt.plot(X,Y1,'b')
plt.plot(X,Y2,'r')
print(coef_1)
print(coef_2)
plt.show()