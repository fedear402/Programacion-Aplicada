import sys
import numpy as np
import matplotlib.pyplot as plt
import importlib

path = "/Users/fedelopez/Library/CloudStorage/OneDrive-Personal/Documents/UDESA/05_Cuatrimestre/Prog_Aplicada/CODIGO/3_MYARRAY"
if not(path in sys.path):
    sys.path.append(path)

path2 = "/Users/fedelopez/Library/CloudStorage/OneDrive-Personal/Documents/UDESA/05_Cuatrimestre/Prog_Aplicada/CODIGO/5_POLY"
if not(path2 in sys.path):
    sys.path.append(path2)

ma = importlib.import_module(name="MyArray")
ply = importlib.import_module(name="Poly")

print(ply.Poly(1, [2, 2]))
print(ma.MyArray([1, 2, 2, 2], 2, 2, True).set_col(1, [2, 3]))

