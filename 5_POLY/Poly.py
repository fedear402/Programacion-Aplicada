import matplotlib.pyplot as plt
import numpy as np


class Poly:
    def __init__(self, n=0, coefs=None):
        if coefs is None:
            coefs = [0]
        self.n = n
        self.coefs = coefs

    def __call__(self, x):
        if isinstance(x, (int, float)):
            evaluacion = 0
            for (potencia, coeficiente) in zip(list(range(0, self.n + 1)), self.coefs):
                evaluacion += coeficiente * (x ** potencia)
            return evaluacion

    def __str__(self):
        expresion = "p(x)="
        for (potencia, coeficiente) in zip(list(range(0, self.n + 1)), self.coefs):
            if potencia == 0 or coeficiente < 0:
                expresion += f" {round(coeficiente, 4)}x^{potencia}"
            elif coeficiente > 0:
                expresion += f" +{round(coeficiente, 4)}x^{potencia}"
        return expresion

    def copy(self):
        return Poly(self.n, self.coefs.copy())

    def poly_plt(self, a, b, **kwargs):
        x = np.linspace(a, b, 300)
        y = list(map(self, x))

        # % Parametros esteticos de graficacion hechos por chatGPT
        fig, ax = plt.subplots()
        # Set plot limits
        ax.set_xlim(a, b)
        # Find the range of y values and center the plot around the x-axis
        y_range = max(y) - min(y)
        y_center = (max(y) + min(y)) / 2
        ax.set_ylim(y_center - y_range / 2, y_center + y_range / 2)
        # Plot the polynomial
        ax.plot(x, y, **kwargs)
        # Plot the x-axis
        ax.axhline(y=0, color='k', linewidth=0.5)
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.6)
        # %
        plt.title(self)
        plt.show()

    def __add__(self, other):
        sumante = Poly(self.n, self.coefs.copy())
        sumado = other
        if isinstance(other, (int, float)):
            sumado = Poly(0, [other])
        if sumado.n < sumante.n:
            sumado = Poly(sumante.n, [i for i in sumado.coefs] + [0] * (sumante.n - sumado.n))
        elif sumado.n > sumante.n:
            sumante = Poly(sumado.n, [i for i in sumante.coefs] + [0] * (sumado.n - sumante.n))
        suma_coeficientes = [a + b for a, b in zip(sumante.coefs, sumado.coefs)]
        return Poly(len(suma_coeficientes) - 1, suma_coeficientes)

    def __radd__(self, other):
        sumado = Poly(self.n, self.coefs.copy())
        sumante = other
        if isinstance(other, (int, float)):
            sumante = Poly(0, [other])
        if sumado.n < sumante.n:
            sumado = Poly(sumante.n, [i for i in sumado.coefs] + [0] * (sumante.n - sumado.n))
        elif sumado.n > sumante.n:
            sumante = Poly(sumado.n, [i for i in sumante.coefs] + [0] * (sumado.n - sumante.n))
        suma_coeficientes = [a + b for a, b in zip(sumante.coefs, sumado.coefs)]
        return Poly(len(suma_coeficientes) - 1, suma_coeficientes)

    def __sub__(self, other):
        restante = Poly(self.n, self.coefs.copy())
        restado = other
        if isinstance(other, (int, float)):
            restado = Poly(0, [other])
        if restado.n < restante.n:
            restado = Poly(restante.n, [i for i in restado.coefs] + [0] * (restante.n - restado.n))
        elif restado.n > restante.n:
            restante = Poly(restado.n, [i for i in restante.coefs] + [0] * (restado.n - restante.n))
        resta_coeficientes = [a - b for a, b in zip(restante.coefs, restado.coefs)]
        return Poly(len(resta_coeficientes) - 1, resta_coeficientes)

    def __rsub__(self, other):
        restado = Poly(self.n, self.coefs.copy())
        restante = other
        if isinstance(other, (int, float)):
            restante = Poly(0, [other])
        if restado.n < restante.n:
            restado = Poly(restante.n, [i for i in restado.coefs] + [0] * (restante.n - restado.n))
        elif restado.n > restante.n:
            restante = Poly(restado.n, [i for i in restante.coefs] + [0] * (restado.n - restante.n))
        suma_coeficientes = [a - b for a, b in zip(restante.coefs, restado.coefs)]
        return Poly(len(suma_coeficientes) - 1, suma_coeficientes)

    def __mul__(self, other):
        multiplicante = Poly(self.n, self.coefs.copy())
        multiplicado = other if isinstance(other, self.__class__) else Poly(0, [other])
        relacion_suma = {i: [] for i in range(multiplicado.n + multiplicante.n + 1)}
        for potencia_self, coeficiente_self in zip(range(multiplicante.n + 1), multiplicante.coefs):
            for potencia_other, coeficiente_other in zip(range(multiplicado.n + 1), multiplicado.coefs):
                relacion_suma[potencia_self + potencia_other].append(coeficiente_self * coeficiente_other)
        return Poly(multiplicado.n + multiplicante.n, [sum(i) for i in list(relacion_suma.values())])

    def __rmul__(self, other):
        multiplicado = Poly(self.n, self.coefs.copy())
        multiplicante = other if isinstance(other, self.__class__) else Poly(0, [other])
        relacion_suma = {i: [] for i in range(multiplicado.n + multiplicante.n + 1)}
        for potencia_self, coeficiente_self in zip(range(multiplicante.n + 1), multiplicante.coefs):
            for potencia_other, coeficiente_other in zip(range(multiplicado.n + 1), multiplicado.coefs):
                relacion_suma[potencia_self + potencia_other].append(coeficiente_self * coeficiente_other)
        return Poly(multiplicado.n + multiplicante.n, [sum(i) for i in list(relacion_suma.values())])

    def __divmod__(self, other, dividendo, divisor):
        resto = dividendo.copy()
        cociente = Poly(dividendo.n - divisor.n, [0] * (dividendo.n - divisor.n + 1))
        if dividendo.n < divisor.n:
            cociente = Poly()
        elif divisor.n == 0:
            resto = dividendo
        else:
            while resto.n >= divisor.n:
                cociente.coefs[resto.n - divisor.n] = resto.coefs[-1] / divisor.coefs[-1]
                last = Poly(resto.n - divisor.n, [0] * (resto.n - divisor.n + 1))
                last.coefs[-1] = resto.coefs[-1] / divisor.coefs[-1]
                resto = Poly(resto.n - 1, (resto - (last * divisor)).coefs[:-1])
        return cociente, resto

    def __floordiv__(self, other):
        dividendo = Poly(self.n, self.coefs.copy())
        divisor = other if isinstance(other, self.__class__) else Poly(0, [other])
        return self.__divmod__(other, dividendo, divisor)[0]

    def __rfloordiv__(self, other):
        divisor = Poly(self.n, self.coefs.copy())
        dividendo = other if isinstance(other, self.__class__) else Poly(0, [other])
        return self.__divmod__(other, dividendo, divisor)[0]

    def __mod__(self, other):
        dividendo = Poly(self.n, self.coefs.copy())
        divisor = other if isinstance(other, self.__class__) else Poly(0, [other])
        return self.__divmod__(other, dividendo, divisor)[1]

    def __rmod__(self, other):
        divisor = Poly(self.n, self.coefs.copy())
        dividendo = other if isinstance(other, self.__class__) else Poly(0, [other])
        return self.__divmod__(other, dividendo, divisor)[1]

    def derivada(self):
        return Poly(self.n - 1, [pot * coef for pot, coef in zip(range(1, self.n + 1), self.coefs[1:])])

    def tangente(self, punto):
        df = self.derivada()
        df_x0 = Poly(0, [df(punto)])
        f_x0 = Poly(0, [self(punto)])
        x_a = Poly(1, [-punto, 1])
        return df_x0 * x_a + f_x0

    def linear_root(self):
        if self.n == 1:
            return (- self.coefs[0]) / (- self.coefs[1])
        else:
            return None

    def rootfind(self, a=-50, b=50, tolerancia=1e-7, max_iter=9999, aprox=5, tol_isclose=1e-14):
        """ a, b: son los limites para la biseccion y para Newton Raphson
            tolerancia: el minimo intervalo entre a y b para dar resultado en el proceso de biseccion
            max_iter: le maximo de iteraciones de Newton Raphson y de Bisección tambén
            aprox: el numero de digitos de redondeo del resultado. Si es -1 no aproxima
            tol_isclose: a veces python hace la imagen de una raiz y no da 0, da algo muy chico cerca de 0 aunque
                deberia ser 0 asi que este parametro especifica que tanto alrededor de 0 se va a tolerar el resultado.
            """
        orig_a = a
        orig_b = b
        counter = 0
        salida = None
        # Newton-Raphson por si los dos puntos del intervalo tienen mismo signo en su imagen
        # Trata de encontrar dos puntos a, b donde NO tengan el mismo signo (o bien una raiz)
        # while: 1) que sean del mismo signo 2) no pasarse de iteraciones 3) que no se haya quedado trabado
        while self(a) * self(b) > 0 and counter < max_iter and abs(a - b) > tolerancia:

            # Achica los intervalos con el cero de la tangente en cada punto
            a = self.tangente(a).linear_root()
            b = self.tangente(b).linear_root()

            # Se fija si hay raiz
            if abs(self(a) - tol_isclose) < tol_isclose:
                salida = a if aprox == -1 else round(a, aprox)
                break
            if abs(self(b) - tol_isclose) < tol_isclose:
                salida = b if aprox == -1 else round(b, aprox)
                break

            counter += 1

        # Si despues de la max_iter de Newton Raphson no llego a un intervalo con signos distintos
        if self(a) * self(b) > 0:
            a = orig_a
            b = orig_b

            # Aca se fijaría si hubiese una raiz doble con una especie de biseccion
            for _ in range(max_iter):
                c = (a + b) / 2

                # Si la raíz quedó justo en a o en b
                if abs(self(a) - tol_isclose) < tol_isclose:
                    salida = a if aprox == -1 else round(a, aprox)
                    break
                if abs(self(b) - tol_isclose) < tol_isclose:
                    salida = b if aprox == -1 else round(b, aprox)
                    break
                # Chequea si el intervalo ya es muy chico o ya es una raiz
                if abs(b - a) < tolerancia and self(c) == 0:
                    salida = c if aprox == -1 else round(c, aprox)
                    break

                # Agarra el intervalo desde la mitad al punto donde la tangente tenga signo opuesta
                if self.tangente(a).coefs[1] * self.tangente(c).coefs[1] < 0:
                    b = c
                else:
                    a = c

        # Entra aca cuando Newton Raphson haya encontrado un intervalo con cambio de signo pero no una raiz
        else:
            for _ in range(max_iter):
                c = (a + b) / 2

                # Si la raíz quedó justo en a o en b
                if abs(self(a) - tol_isclose) < tol_isclose:
                    salida = a if aprox == -1 else round(a, aprox)
                    break
                if abs(self(b) - tol_isclose) < tol_isclose:
                    salida = b if aprox == -1 else round(b, aprox)
                    break

                # Chequea si el intervalo ya es muy chico o ya es una raiz
                if abs(b - a) < tolerancia or abs(self(c) - tol_isclose) < tol_isclose:
                    salida = c if aprox == -1 else round(c, aprox)
                    break

                # Agarra el intervalo desde la mitad al punto que haga que haya un cambio de signo
                if self(a) * self(c) < 0:
                    b = c
                else:
                    a = c

        return salida

    def findroots(self, a=-50, b=50):
        actual = self.copy()
        monomios_divisbles = []
        if all(j == 0 for j in self.coefs[2:]):
            return self.linear_root()
        while actual.n > 0:
            raiz = actual.rootfind()
            if raiz is None:
                monomios_divisbles.append(actual)
                break
            else:
                monomio = Poly(1, [-raiz, 1])
                monomios_divisbles.append(monomio)
                actual = actual // monomio
        return [-(i.coefs[0]) for i in monomios_divisbles if i.n == 1]


if __name__ == "__main__":
    mypoly = Poly(4, [2, -3, 0, 4, -6])  # GRADO 4
    mypoly1 = Poly(2, [2, 0, -1])
    mypoly2 = Poly(6, [3, 4, -5, -9, 0, 1, 2])
    mypoly3 = Poly(1, [2, 3])  # LINEAL
    mypoly4 = Poly(2, [3, 2, 1])  # SIN RAICES
    mypoly5 = Poly(3, [-9, 15, -7, 1])

    # mypoly1.poly_plt(-2, 1)
    # mypoly5.poly_plt(0.5, 3.5)
    # mypoly4.poly_plt(-2, 1)

    # %%% ADD SUB MULT DIV
    # print(f"CALL {mypoly}; Evaluada en 3 =====> {mypoly(3)}" + "\n")
    # print(f"ADD {mypoly}    +    3 =====> {(mypoly + 3)}" + "\n")
    # print(f"ADD {mypoly}    +    {mypoly2} =====> {(mypoly + mypoly2)}" + "\n")
    # print(f"RADD 3    +    {mypoly} =====>  {(3 + mypoly)}" + "\n")
    # print(f"SUB {mypoly}    -    3 =====> {(mypoly - 3)}" + "\n")
    # print(f"SUB {mypoly}    -    {mypoly2} =====> {(mypoly - mypoly2)}" + "\n")
    # print(f"RSUB 3    -    {mypoly} =====>  {(3 - mypoly)}" + "\n")
    # print(f"MUL {mypoly}    *    3 =====>  {(mypoly * 3)}" + "\n")
    # print(f"MUL {mypoly}    *    {mypoly2} =====> {(mypoly * mypoly2)}" + "\n")
    # print(f"RMUL 3    *    {mypoly} =====>  {(3 * mypoly)}" + "\n")
    # print(f"DIV {mypoly2}    //    {mypoly} =====> {(mypoly2 // mypoly)}" + "\n")
    # print(f"DIV {mypoly2}    //    {3} =====> {(mypoly2 // 3)}" + "\n")
    # print(f"DIV {3}    //    {mypoly2} =====> {(3 // mypoly2)}" + "\n")
    # print(f"DIV {mypoly}    //    {mypoly2} =====> {(mypoly // mypoly2)}" + "\n")
    # print(f"MOD {mypoly2}    %     {mypoly} =====> {(mypoly2 % mypoly)}" + "\n")
    # print(f"MOD 3    %     {mypoly2} =====> {(3  %  mypoly)}" + "\n")
    # print(f"MOD {mypoly2}    %     {3} =====> {(mypoly2 % 3)}" + "\n")
    # print(f"MOD {mypoly}    %     {mypoly2} =====> {(mypoly  %  mypoly2)}" + "\n")
    # print(f"DIV {mypoly2}    //    {mypoly3} =====> {(mypoly2 // mypoly3)}" + "\n")
    # print(f"MOD {mypoly2}    %     {mypoly3} =====> {(mypoly2  %  mypoly3)}" + "\n")

    # %%% RAICES
    # print(f"DERIVADA {mypoly} =====> {mypoly.derivada()}")
    # print(f"TANGENTE {mypoly} en 3 =====> {mypoly.tangente(3)}")
    # print(f"LINEAR ROOT {mypoly} : {mypoly.tangente(3).linear_root()}")
    # print(f"ROOTFIND NEWTON RAPHSON {mypoly1} : {mypoly1.rootfind_nr(-1.5)}")
    # print(f"ROOTFIND BISECCION {mypoly5} : {mypoly5.rootfind(0, 2)}")
    # # print(f"ROOTFIND BISECCION {mypoly4} : {mypoly4.rootfind(-2.5, 0)}")
    # print(f"res div con monomio : {mypoly5 // Poly(1, [-mypoly5.rootfind(0, 2), 1])}")
    # res1 = mypoly5 // Poly(1, [-mypoly5.rootfind(0, 2), 1])
    # print(f"monomio con raiz : {Poly(1, [-mypoly5.rootfind(0, 2), 1])}")
    # print(f" resto : {mypoly5 % Poly(1, [-mypoly5.rootfind(0, 2), 1])}")
    # print(f"res root {res1.rootfind(2, 4)}")
    # print(f"FINDROOTS : {mypoly5.findroots()}")
    # a1 = mypoly1.rootfind()
    # print(f"1{mypoly1} : {a1} : {Poly(1, [-a1, 1])} : {mypoly1//Poly(1, [-a1, 1])}")
    #
    # print(f"2{mypoly2} : {mypoly2.rootfind()}")
    #
    # print(f"{mypoly3} : {mypoly3.rootfind()}")
    #
    # print(f"4{mypoly4} : {mypoly4.rootfind()}")
    #
    # print(f"5{mypoly5} : {mypoly5.rootfind()}")

    # %% STRESS TEST GPT
    poly1 = Poly(2, [1, -3, 2])
    poly2 = Poly(3, [-6, 11, -6, 1])
    poly3 = Poly(4, [4, -20, 28, -20, 4])
    poly4 = Poly(5, [-1, 5, -10, 10, -5, 1])
    poly5 = Poly(6, [1, -6, 15, -20, 15, -6, 1])
    poly6 = Poly(2, [1, -2, 1])
    poly7 = Poly(2, [1, 0, -1])
    poly8 = Poly(2, [1, -1, 0])
    poly9 = Poly(2, [1, 0, 1])
    poly10 = Poly(3, [1, -3, 3, -1])
    poly11 = Poly(3, [2, -7, 6, -1])
    poly12 = Poly(4, [1, -4, 6, -4, 1])
    poly13 = Poly(4, [1, 2, 1, -6, -12])
    poly14 = Poly(3, [1, -1, -1, 1])
    poly15 = Poly(3, [1, -1, 1, 1])
    polys = [
        poly1,
        poly2,
        poly3,
        poly4,
        poly5,
        poly6,
        poly7,
        poly8,
        poly9,
        poly10,
        poly11,
        poly12,
        poly13,
        poly14,
        poly15
    ]
    for i in polys:
        print(f"n1  {i.coefs}:  {i} MIA: {i.findroots()}  Deberia ser = {list(filter(np.isreal, np.polynomial.polynomial.polyroots(i.coefs)))}" + "\n")  # OK

    p1 = Poly(2, [4, -4, 1])  # doble
    p2 = Poly(2, [1, 2, 1])  # doble
    p3 = Poly(3, [-18, 11, 2, 1])  # doble
    # print(f"p1 {p1.coefs}: {p1} MIA: {p1.rootfind()} Deberia ser = {list(filter(np.isreal, np.polynomial.polynomial.polyroots(p1.coefs)))}" + "\n")
    # print(f"p2 {p2.coefs}: {p2} MIA: {p2.rootfind()} Deberia ser = {list(filter(np.isreal, np.polynomial.polynomial.polyroots(p2.coefs)))}" + "\n")
    # print(f"p3 {p3.coefs}: {p3} MIA: {p3.rootfind()} Deberia ser = {list(filter(np.isreal, np.polynomial.polynomial.polyroots(p3.coefs)))}" + "\n")

    p4 = Poly(5, [-2, 11, -12, 7, -1])  # multiplicidad 3
    # print(f"p4 {p4.coefs}: {p4} MIA: {p4.rootfind()} Deberia ser = {list(filter(np.isreal, np.polynomial.polynomial.polyroots(p4.coefs)))}" + "\n")

    p5 = Poly(5, [81, -108, 54, -12, 1])  # multiplicdad 4
    # print(f"p5 {p5.coefs}: {p5} MIA: {p5.rootfind()} Deberia ser = {list(filter(np.isreal, np.polynomial.polynomial.polyroots(p5.coefs)))}" + "\n")

    p6 = Poly(4, [1, 0, 1])  # sin raices reales
    # print(f"p6 {p6.coefs}: {p6} MIA: {p6.rootfind()} Deberia ser = {list(filter(np.isreal, np.polynomial.polynomial.polyroots(p6.coefs)))}" + "\n")
