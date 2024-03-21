

import matplotlib.pyplot as plt
import math
import numpy as np

class RootFinder:
    def __init__(self, f):
        self.f = f
    
    def plot(self, start=1, end=100):
        x = np.linspace(start, end, 300)
        plt.plot(x, list(map(f, x)))
        plt.plot(x, [0 for _ in x])
    
    def biseccion(self, a, b):
        if np.sign(self(a)) != np.sign(self.f(b)):
            if np.sign(b / 2) == np.sign(f(a)):
                
                biseccion(a, b, c)
        else:
            
            pass
    
def f(x):
    return math.sin(x) * math.log(x) - x + 37

if __name__ == "__main__":
    root_finder = RootFinder(f)
    root_finder.plot(20, 50)
    plt.show()
    
    # -------- MAP
    # def suma(a):
    #     return sum(a)
    # matrix = [[1, 2, 3], [1, 2, 3]]
    # a = list(zip(*matrix))
    # print(a)
    # b = list(map(list, a))
    # print(b)
    # c = list(map(lambda a: sum(a), a))
    # print(c)