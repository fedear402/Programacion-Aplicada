#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 15:44:39 2023

@author: fedelopez
"""

def determinante(matriz):
    n = len(matriz)

    if n == 1:
        return matriz[0][0]

    if n == 2:
        #print(matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0])
        return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]

    det = 0
    for i in range(n):
        matriz_cofactor = []
        for j in range(1, n):
            fila_cofactor = []
            for k in range(n):
                if k != i:
                    fila_cofactor.append(matriz[j][k])
            matriz_cofactor.append(fila_cofactor)
        #print(determinante(matriz_cofactor))
        #print(f"{matriz[0][i]} x {matriz_cofactor} ({determinante(matriz_cofactor)}) = {matriz[0][i] * determinante(matriz_cofactor)} ")
        #print(determinante(matriz_cofactor))
        det += ((-1) ** i) * matriz[0][i] * determinante(matriz_cofactor)

    return det


# Ejemplo de uso
matriz_5x5 = [
[ 5,  9,  3,  7,  8],
[ 2,  6,  1,  4,  3],
[10,  3,  6,  2,  1],
[ 7,  8,  9,  5,  4],
[ 4,  1,  3,  6,  7]
    ]

det = determinante(matriz_5x5)
print(det)