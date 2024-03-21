import sys
import importlib

path = "/Users/fedelopez/Library/CloudStorage/OneDrive-Personal/Documents/UDESA/05_Cuatrimestre/Prog_Aplicada/CODIGO/5_POLY"
if not (path in sys.path):
    sys.path.append(path)

Poly_mod = importlib.import_module(name="PolynomialC")
Poly = Poly_mod.Poly


class Lagrange(Poly):
    def __init__(self, puntos: list):
        self.puntos = puntos
        ini = __class__.interpol(puntos)
        super().__init__(ini.n, ini.coefs)

    @staticmethod
    def interpol(puntos: list):
        final = []
        for n in range(len(puntos)):
            numerador = Poly(0, [1, 0])
            denominador = 1
            for i in range(len(puntos)):
                if i != n:
                    w = Poly(1, [-puntos[i][0], 1])
                    numerador = numerador * w
                    denominador = denominador * (puntos[n][0] - puntos[i][0])
            final.append(puntos[n][1] * (numerador * (1 / denominador)))
        return sum(final)


if __name__ == "__main__":
    a = Lagrange([(-1, 0), (0, -1), (2, 3)])
    print(a)

    puntosx = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    puntosy = [Poly(2, [-1, 0, 1])(i) for i in puntosx]
    punts = list(zip(puntosx, puntosy))

    b = Lagrange(punts)
    print(b)
