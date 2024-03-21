# definimos la funcion

def mcd(a, b):
    # cociente entero entre a // b
    q = a // b 
    # remanente 
    r = a - (b * q) 
    print(f"\nVariables de esta ronda son:\n\n\
          a y b:\t ({a}, {b})\n\
          q: {q},\t\t {a} // {b}\n\
          r: {r},\t {b}*{q}")
    # Condicional caso que b = 0 terminamos
    if r == 0:
        print("\n\nMCD es:\t({},{})\n\n".format(b,r))
    # caso contrario repetimos o hacemos recursividad
    else:
        mcd(b,r)

mcd(234,24)