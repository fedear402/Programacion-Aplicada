import numpy as np

def convolucion(a, b):
    out_len = len(a)+len(b)-1
    out = [0] * out_len
    for n in range(out_len):
        aux = []
        for i in range(min(n + 1, len(a))):
            aux.append(a[i] * (0 if n-i >= len(b) else b[n-i]) )
        out[n] = sum(aux)
    
    return out

a = [3, 4, 5, 6]
b = [1, 2, 3, 4, 5, 5]

print(np.convolve(a, b))
print(np.convolve(b, a))
print(convolucion(b, a))

# [ 3 10 22 40 58 73 69 55 30]