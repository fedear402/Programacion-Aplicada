#result = ""
#q = int(input("Convert to binary: "))
#while q >= 0:
#    r = q % 2
#    result += str(r)
#    q = q // 2

#print(q)
def binary(a):
    result = ""
    while a > 0:
        r = a % 2
        result += str(r)
        a = a // 2
    return result

print(binary(5))