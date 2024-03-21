import numpy as np
import matplotlib.pyplot as plt


class Poly:
    def __init__(self, n=0, coefs=None):
        if coefs is None:
            coefs = [0]

        # Crea una instancia solo si tiene sentido el grado y la cantidad de coeficientes
        # Ej. no puede ser Poly(4, [1, 2]) o Poly(2, [8, 9, 1, 2])
        if n == (len(coefs) - 1) or n == 0:
            self.n = n
            self.coefs = coefs
        else:
            if n > (len(coefs) - 1):
                raise ValueError("Faltan coeficientes")
            else:
                raise ValueError("Demasiados coeficientes")

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

    def __repr__(self):
        return self.__str__()

    def copy(self):
        return Poly(self.n, self.coefs.copy())

    def obj(self):
        return f"Poly({self.n}, {self.coefs})"

    @staticmethod
    def str(s):
        if s.startswith("p(x)="):
            terms = s.split(" ")[1:]
        elif s.startswith(" p(x)="):
            terms = s.split(" ")[2:]
        else:
            terms = s.split(" ")

        coefs = []

        for term in terms:
            coef, exp = term.split("x^")
            coef = coef.strip()

            if coef == "":
                coef = "1"
            elif coef == "-":
                coef = "-1"

            coefs.append(float(coef))

        grado = len(coefs) - 1

        return Poly(grado, coefs)

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

    def __eq__(self, other):
        return self.n == other.n and self.coefs == other.coefs

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

    def __pow__(self, power):
        if power == 0:
            salida = Poly()
        elif power == 1:
            salida = self
        else:
            final = self
            for i in range(power + 1):
                final *= self
            salida = final

    def derivada(self):
        return Poly(self.n - 1, [pot * coef for pot, coef in zip(range(1, self.n + 1), self.coefs[1:])])

    def tangente(self, punto):
        df = self.derivada()
        df_x0 = Poly(0, [df(punto)])
        f_x0 = Poly(0, [self(punto)])
        x_a = Poly(1, [-punto, 1])
        return df_x0 * x_a + f_x0

    def linear_root(self, aprox=6):
        if all(j == 0 for j in self.coefs[2:]) or self.n == 1:
            return (- self.coefs[0]) / (self.coefs[1])
        else:
            return None

    def isfactor(self, maybe):
        return self % maybe == Poly()

    def islinear(self):
        return self.n == 1 and self.coefs[1] == 1

    def rootfind(self, a=-50, b=50, tolerancia=1e-7, max_iter=7500, aprox=6, tol_isclose=1e-14):
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

            # Se fija si hay raiz
            if abs(self(a)) < tol_isclose:
                salida = a if aprox == -1 else round(a, aprox)
                break
            if abs(self(b)) < tol_isclose:
                salida = b if aprox == -1 else round(b, aprox)
                break
            counter += 1

        # Si despues de la max_iter de Newton Raphson no llego a un intervalo con signos distintos
        if self(a) * self(b) > 0 and salida is None:
            a = orig_a
            b = orig_b
            # Aca se fijaría si hubiese una raiz doble con una especie de biseccion
            for _ in range(max_iter):
                c = (a + b) / 2 if self.derivada()(a) != 0 else orig_a
                # Si la raíz quedó justo en a o en b
                if abs(self(a)) < tol_isclose:
                    salida = a if aprox == -1 else round(a, aprox)
                    break
                if abs(self(b)) < tol_isclose:
                    salida = b if aprox == -1 else round(b, aprox)
                    break
                # Chequea si el intervalo ya es muy chico o ya es una raiz
                if abs(b - a) < tolerancia or abs(self(c)) < tol_isclose:
                    salida = c if aprox == -1 else round(c, aprox)
                    break

                # Agarra el intervalo desde la mitad al punto donde la tangente tenga signo opuesta
                if self.tangente(a).coefs[1] * self.tangente(c).coefs[1] < 0:
                    b = c
                else:
                    a = c

        # Entra aca cuando Newton Raphson haya encontrado un intervalo con cambio de signo pero no una raiz
        elif salida is None:
            # print("bsc")
            for _ in range(max_iter):
                c = (a + b) / 2

                # Si la raíz quedó justo en a o en b
                if abs(self(a)) < tol_isclose:
                    salida = a if aprox == -1 else round(a, aprox)
                    break
                if abs(self(b)) < tol_isclose:
                    salida = b if aprox == -1 else round(b, aprox)
                    break
                # Chequea si el intervalo ya es muy chico o ya es una raiz
                if abs(b - a) < tolerancia or abs(self(c)) < tol_isclose:
                    salida = c if aprox == -1 else round(c, aprox)
                    break

                # Agarra el intervalo desde la mitad al punto que haga que haya un cambio de signo
                if self(a) * self(c) < 0:
                    b = c
                else:
                    a = c

        return salida

    @staticmethod
    def comun_coefs(*coefs):
        def mcd(a, b):
            while b:
                a, b = b, a % b
            return a

        mcd_result = mcd(coefs[0], coefs[1])
        for number in coefs[2:]:
            mcd_result = mcd(mcd_result, number)
        return mcd_result

    def poly_factored(self, tol=0.000001, aprox=5):
        comun = Poly.comun_coefs(*self.coefs)
        if abs(comun) < tol or abs(comun - 1) < tol:
            return self
        else:
            return Poly(0, [-round(comun, aprox)]), Poly(self.n, [round(i // -comun, aprox) for i in self.coefs])

    def factores(self, a=-50, b=50, aprox=5, factores=None, tol=0.009):
        actual = Poly(self.n, self.coefs.copy())
        if factores is None:
            factores = []
        raiz = self.rootfind()
        if raiz is None:
            factores.append(self)
        else:
            factor = Poly(1, [-raiz, 1])

        # Aca chequea que el input no sea una funcion lineal en secreto
            if all(j == 0 for j in self.coefs[2:]) or self.n == 1:
                factores.append(Poly(1, [-self.linear_root(), 1]))

            # Aca si no tiene raices, devuelve el mismo
            elif abs((self % factor).coefs[0]) > tol:
                factores.append(self)

            else:
                factores.append(factor)
                actual = actual // factor
                actual = Poly(actual.n, [round(c, aprox) for c in actual.coefs])
                actual.factores(a, b, aprox, factores, tol)
            return factores

    def raices(self, aprox=5):
        raices = []
        factores = []
        factors = self.factores()
        if factors is not None:
            for item in factors:
                if isinstance(item, (tuple, list)):
                    r = 1
                    for t in item:
                        r *= t
                    factores.append(r)
                else:
                    factores.append(item)

            for factr in factores:
                if factr.n == 1:
                    raices.append(factr.linear_root())
        else:
            raices = None
            return raices
        return raices if aprox == -1 and raices is not None else [round(root, aprox) for root in raices]


# def MCD_poly(lista=None):
#     if lista is None:
#         lista = list()
#     factores_totales = [i for k in [k.factores() for k in lista] for i in k]
#     comunes = {i for i in factores_totales if factores_totales.count(i) == len(lista)}
#     return list(comunes)[0] if bool(comunes) else Poly()


# def MCM_main(a, b):
#     mcd = MCD_poly([a, b])
#     comun = (a * b) // mcd
#     return comun
#
#
# def MCM_poly(lista=None):
#     if lista is None:
#         lista = list()
#     elif len(lista) == 1:
#         return lista[0]
#     else:
#         comunes = MCM_main(lista[0], lista[1])
#         for poly in lista[2:]:
#             comunes = MCM_main(comunes, poly)
#         return comunes


if __name__ == "__main__":
    p = Poly(6, [-36, 0, 49, 0, -14, 0, 1])
    p1 = Poly(2, [1, -3, 2])  # (x - 1)(x - 2)
    p2 = Poly(3, [1, -5, 8, -4])  # (x - 1)(x - 2)^2
    p3 = Poly(2, [1, -4, 4])  # (x - 2)^2
    p4 = Poly(3, [1, -6, 11, -6])  # (x - 1)(x - 2)(x - 3)
    p5 = Poly(2, [1, -5, 6])  # (x - 2)(x - 3)
    p6 = Poly(2, [2, 4, -8])
    # print("SALIDA", p.raices(), p)
    poly1 = Poly(2, [1, -3, 2])  # OK
    poly2 = Poly(3, [-6, 11, -6, 1])  # OK
    poly3 = Poly(4, [4, -20, 28, -20, 4])  # OK
    poly4 = Poly(5, [-1, 5, -10, 10, -5, 1])  # OK?
    poly5 = Poly(6, [1, -6, 15, -20, 15, -6, 1])  # OK
    poly6 = Poly(2, [1, -2, 1])  # OK
    poly7 = Poly(2, [1, 0, -1])  # OK
    poly8 = Poly(2, [1, -1, 0])  # OK
    poly9 = Poly(2, [1, 0, 1])  # OK
    poly10 = Poly(3, [1, -3, 3, -1])  # OK : multiplicidad 3
    poly11 = Poly(3, [2, -7, 6, -1])  # OK
    poly12 = Poly(4, [1, -4, 6, -4, 1])  # OK?
    poly13 = Poly(4, [1, 2, 1, -6, -12])  # OK
    poly14 = Poly(3, [1, -1, -1, 1])  # OK
    poly15 = Poly(3, [1, -1, 1, 1])  # OK
    poly16 = Poly(2, [4, -4, 1])  # OK
    poly17 = Poly(2, [1, 2, 1])  # OK
    poly18 = Poly(3, [-18, 11, 2, 1])  # OK
    poly19 = Poly(5, [-2, 11, -12, 7, -1, 9])  # OK
    poly20 = Poly(5, [81, -108, 54, -12, 1, 9])  # OK
    poly21 = Poly(4, [1, 0, 1, 1, 1])  # OK
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
        poly15,
        poly16,
        poly17,
        poly18,
        poly19,
        poly20,
        poly21
    ]
    #
    for i in polys:
        print(
            f"NUEVA {i} MIA: raices {i.raices()} Deberia ser = {list(filter(np.isreal, np.polynomial.polynomial.polyroots(i.coefs)))}" + "\n")  # OK
    # f"NUEVA  Poly({i.n}, {i.coefs}):  {i} MIA: raices {i.raices()} factores {i.factores()} Deberia ser = {list(filter(np.isreal, np.polynomial.polynomial.polyroots(i.coefs)))}" + "\n")  # OK
    # print(f"NUEVA  Poly( {poly9.n}, {poly9.coefs}):  {poly9} MIA: raices {poly9.raices()} factores {poly9.factores()} Deberia ser = {list(filter(np.isreal, np.polynomial.polynomial.polyroots(poly9.coefs)))}" + "\n")
