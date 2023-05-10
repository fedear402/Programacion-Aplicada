#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 18:04:59 2023

@author: fedelopez
"""

import random


def quedarse():
    victorias_quedarse = [0] * 1000
    for i in range(len(victorias_quedarse)):
        out = random.randint(1, 3)
        if out == 1:
            victorias_quedarse[i] = 1
        elif out == 2 or out == 3:
            continue
    return sum(victorias_quedarse)


def cambiar():
    victorias_cambiar = [0] * 1000
    for i in range(len(victorias_cambiar)):
        out = random.randint(1, 2)
        if out == 1:
            victorias_cambiar[i] = 1
        elif out == 2:
            continue
    return sum(victorias_cambiar)


print(quedarse())
print(cambiar())