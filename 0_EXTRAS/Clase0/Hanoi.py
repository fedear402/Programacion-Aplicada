# def hanoi(disk, row_start, row_end, row_other):
#     procedure = []
#     if disk == 1:
#         procedure.append([disk, row_start, row_end])
#         return procedure
#     else:
#         hanoi(disk-1, row_start, row_other, row_end)
#         procedure.append([disk, row_start, row_end])
#         return procedure
#         hanoi(disk-1, row_other, row_end, row_start)

# print(hanoi(4, 1, 3, 2))
import time 

def hanoi(n,source,target,helper):
    # con global podemos hacer que una variable interna tenga scope global.
    global count
    if n > 0:
        hanoi(n-1,source,helper,target)
        target.append(source.pop())
        count = count + 1
        hanoi(n-1,helper,target,source)

# Notar que hago multiples llamados y que cambio el orden de los pilares cuando lo hago
        

num_moves = []
for i in range(1,25):
    a = list(range(i,0,-1))
    b = []
    c = []
    count = 0
    hanoi(i,a,c,b)
    num_moves.append(count)
    print(f"\nSo far there had been {count} moves for {i} discs\n")
    print({"a":a,"b":b,"c":c})
    time.sleep(1)