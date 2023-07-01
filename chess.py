def tablero(n, result=[1, 0]):
    if n == 0:
        return None
    if n == 1:
        return tuple(result)
    else:
        a = result[0]+2 if n%2 != 0 else result[0]
        b = result[1]+2 if n%2 == 0 else result[1]
        return tablero(n-1, result=[result[0] + a, result[1] + b])
        

"""
1: 1, 0
2: 1, 2
3: 3, 2
4: 3, 4
5: 5, 4
6: 5, 6
7: 7, 6
8: 7, 8
9: 9, 8
10: 9, 10
"""

if __name__ == "__main__":
    for i in range(11):
        print(f"tablero de n = {i}, (negras, blancas) {tablero(i)} ")