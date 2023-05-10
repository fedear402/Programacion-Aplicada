class MyArray:
    def __init__(self, lista, r, c, by_row):
        self.lista = lista
        self.r = r
        self.c = c
        self.by_row = by_row

    # % GETS
    def get_pos(self, j, k):
        """ toma las coordenadas j,k en la matriz y devuelve la posicion
            m asociada en la lista"""
        return self.c * (j - 1) + k - 1 if self.by_row else self.r * (k - 1) + j - 1

    def get_coords(self, m):
        """ toma una posición m en la lista y devuelve en forma de tupla las
            coordenadas j,k correspondientes en la matriz.
            """
        if self.by_row:
            for k in range(1, self.c + 1):
                for j in range(1, self.r + 1):
                    if self.get_pos(j, k) == m:
                        return j, k
        else:
            for _ in range(self.r + 1):
                a = 1
                b = 0
                for _ in range(self.c + 1):
                    b += 1
                    if self.get_pos(a, b) == m:
                        return a, b

    def get_elem(self, j, k):
        """ devuelve el elemento en (j, k)"""
        return self.lista[self.get_pos(j, k)]

    def get_row(self, j):
        """ devuelve el contenido de la fila j"""
        return [self.get_elem(j, k) for k in range(1, self.c + 1)]

    def get_col(self, k):
        """ devuelve el contenido de la columna j"""
        return [self.get_elem(j, k) for j in range(1, self.r + 1)]

    # % SWITCH
    def switch(self):
        """ devuelve un objeto con la misma matriz,
            pero alterando la lista elems y cambiando el valor de verdad de by_row.
            """
        nueva = []
        if self.by_row:
            for i in range(self.r):
                for j in range(i, self.c * self.r, self.r):
                    nueva.append(self.lista[j])
        else:
            for i in range(self.c):
                for j in range(i, self.c * self.r, self.c):
                    nueva.append(self.lista[j])
        return MyArray(nueva, self.r, self.c, not self.by_row)

    # % DELETES
    def del_row(self, j):
        if self.by_row:
            return MyArray(self.lista[0:self.get_pos(j, 1)] + self.lista[
                                                              self.get_pos(j, self.c + 1):self.get_pos(self.r,
                                                                                                       self.c + 1)],
                           self.r - 1, self.c, self.by_row)
        else:
            nueva = self.lista.copy()
            borrar = self.get_pos(j, 1)
            for i in range(self.c):
                nueva.pop(borrar)
                borrar += self.c - 2
            return MyArray(nueva, self.r, self.c, self.by_row)

    def del_col(self, k):
        if self.by_row:
            nueva = []
            for i in range(len(self.lista)):
                if self.get_coords(i)[1] != k:
                    nueva.append(self.lista[i])
                else:
                    continue
            return MyArray(nueva, self.r, self.c - 1, self.by_row)
        else:
            parte1 = self.lista[0:self.get_pos(1, k)]
            parte2 = self.lista[self.get_pos(self.r, k) + 1:self.c * self.r]
            return MyArray(parte1 + parte2, self.r, self.c - 1, self.by_row)

    # % SWAPS
    def swap_rows(self, j_1, j_2):
        '''devuelve un objeto de la clase con las filas (j,k) intercambiadas. 
        '''
        if self.by_row:
            listt = self.lista.copy()
            l1 = listt[self.get_pos(j_1, 1):self.get_pos(j_1, self.c + 1)]
            l2 = listt[self.get_pos(j_2, 1):self.get_pos(j_2, self.c + 1)]
            listt[self.get_pos(j_1, 1):self.get_pos(j_1, self.c + 1)] = l2
            listt[self.get_pos(j_2, 1):self.get_pos(j_2, self.c + 1)] = l1
            return MyArray(listt, self.r, self.c, self.by_row)
        else:
            listt = self.lista.copy()
            for c in range(1, self.c + 1):
                for l in range(1, self.r + 1):
                    if l == j_1:
                        v1 = listt[self.get_pos(l, c)]
                    if l == j_2:
                        listt[self.get_pos(j_1, c)] = listt[self.get_pos(l, c)]
                        listt[self.get_pos(j_2, c)] = v1
            return MyArray(listt, self.r, self.c, self.by_row)

    def swap_cols(self, c_1, c_2):
        """ devuelve un objeto de la clase con las
            columnas (l,m) intercambiadas. """
        if self.by_row:
            listt = self.lista.copy()
            for l in range(1, self.r + 1):
                for c in range(1, self.c + 1):
                    if c == c_1:
                        v1 = listt[self.get_pos(l, c)]
                    if c == c_2:
                        listt[self.get_pos(l, c_1)] = listt[self.get_pos(l, c)]
                        listt[self.get_pos(l, c_2)] = v1
            return MyArray(listt, self.r, self.c, self.by_row)
        else:
            listt = self.lista.copy()
            l1 = listt[self.get_pos(1, c_1):self.get_pos(self.r, c_1) + 1]
            l2 = listt[self.get_pos(1, c_2):self.get_pos(self.r, c_2) + 1]
            listt[self.get_pos(1, c_1):self.get_pos(self.r, c_1) + 1] = l2
            listt[self.get_pos(1, c_2):self.get_pos(self.r, c_2) + 1] = l1
            return MyArray(listt, self.r, self.c, self.by_row)

    # % ESCALARES
    def scale_row(self, j, x):
        """ toma el objeto y devuelvan otro del mismo tipo, pero con la fila
            j multiplicada por el factor x"""
        listt = self.lista.copy()
        for c in range(1, self.c + 1):
            listt[self.get_pos(j, c)] = listt[self.get_pos(j, c)] * x
        return MyArray(listt, self.r, self.c, self.by_row)

    def scale_col(self, k, y):
        """toma el objeto y deuelve otro del mismo tipo, pero
            con la columna k multiplicada por y"""
        listt = self.lista.copy()
        for l in range(1, self.r + 1):
            listt[self.get_pos(l, k)] = listt[self.get_pos(l, k)] * y
        return MyArray(listt, self.r, self.c, self.by_row)

    # % TRANSPONER
    def transpose(self):
        """ devuelve un elemento de la clase, pero con la matriz transpuesta.
            (A.transpose()).transpose() = A."""
        return MyArray(self.lista, self.c, self.r, not self.by_row)

    def flip_cols(self):
        """ que devuelven una copia del elemento de la clase,
            pero reflejado especularmente en sus filas."""
        if self.by_row:
            listt = self.lista.copy()
            for l in range(1, self.r + 1):
                mp = self.get_row(l)[::-1]
                listt[self.get_pos(l, 1):self.get_pos(l, self.c + 1)] = mp
            return MyArray(listt, self.r, self.c, self.by_row)
        else:
            listt = self.lista.copy()
            for l in range(1, self.r + 1):
                mp = self.get_row(l)[::-1]
                for c in range(1, self.c + 1):
                    listt[self.get_pos(l, c)] = mp[c - 1]
            return MyArray(listt, self.r, self.c, self.by_row)

    # % FLIPS
    def flip_rows(self):
        """ que devuelven una copia del elemento de la clase,
            pero reflejado especularmente en sus columnas"""
        if self.by_row:
            listt = self.lista.copy()
            for c in range(1, self.c + 1):
                mp = self.get_col(c)[::-1]
                for l in range(1, self.r + 1):
                    listt[self.get_pos(l, c)] = mp[l - 1]
            return MyArray(listt, self.r, self.c, self.by_row)
        else:
            listt = self.lista.copy()
            for c in range(1, self.c + 1):
                mp = self.get_col(c)[::-1]
                listt[self.get_pos(1, c):self.get_pos(self.r, c) + 1] = mp
            return MyArray(listt, self.r, self.c, self.by_row)

    # % DETERMINANTE
    def det(self):
        """ Devuelve el determinante de una matriz cuadrada"""
        if self.r == self.c:
            n = self.r
            if n == 2:
                return self.get_elem(1, 1) * self.get_elem(2, 2) - self.get_elem(1, 2) * self.get_elem(2, 1)
            else:
                deet = 0
                for i in range(1, n + 1):
                    deet += ((-1) ** (i + 1)) * self.get_elem(i, 1) * self.del_col(1).del_row(i).det()
                return deet
        else:
            return "None"

    def cero(self):
        """ Devuelve una matriz del tamaño de la propia con ceros"""
        if self.c == self.r:
            return MyArray([j for j in [i for i in [0] * self.r] * self.c], self.r, self.c, self.by_row)
        else:
            return "No es cuadrada"

    def identidad(self):
        """ Devuelve la matriz identidad del tamaño de la propia si es cuadrada"""
        if self.c == self.r:
            identidad = [0 if self.get_coords(i)[0] != self.get_coords(i)[1] else 1 for i in range(len(self.lista))]
            return MyArray(identidad, self.r, self.c, self.by_row)
        else:
            return "No es cuadrada"

    def myprint(self):
        """ imprime la matriz en un formato mas legible"""
        print('\n')
        for k in range(1, self.r + 1):
            print(self.get_row(k))
        print('\n')
        return None

    # % DUNDERS
    def __add__(self, a):
        if type(a) == int:
            return MyArray([a + i for i in self.lista], self.r, self.c, self.by_row)
        elif type(a) == self.__class__ and self.r == a.r and self.c == a.c:
            return MyArray([(a.lista[i] + self.lista[i]) for i in range(len(self.lista))], self.r, self.c, self.by_row)

    def __radd__(self, a):
        if type(a) == int:
            return MyArray([a + i for i in self.lista], self.r, self.c, self.by_row)
        elif type(a) == self.__class__ and self.r == a.r and self.c == a.c:
            return MyArray([(a.lista[i] + self.lista[i]) for i in range(len(self.lista))], self.r, self.c, self.by_row)

    def __sub__(self, a):
        if type(a) == int:
            return MyArray([i - a for i in self.lista], self.r, self.c, self.by_row)
        elif type(a) == self.__class__ and self.r == a.r and self.c == a.c:
            return MyArray([(self.lista[i] - a.lista[i]) for i in range(len(self.lista))], self.r, self.c, self.by_row)

    def __rsub__(self, a):
        if type(a) == int:
            return MyArray([a - i for i in self.lista], self.r, self.c, self.by_row)
        elif type(a) == self.__class__ and self.r == a.r and self.c == a.c:
            return MyArray([(self.lista[i] - a.lista[i]) for i in range(len(self.lista))], self.r, self.c, self.by_row)

    def __mul__(self, a):
        if type(a) == int:
            return MyArray([i * a for i in self.lista], self.r, self.c, self.by_row)
        elif type(a) == self.__class__ and self.r == a.r and self.c == a.c:
            return MyArray([(self.lista[i] * a.lista[i]) for i in range(len(self.lista))], self.r, self.c, self.by_row)

    def __rmul__(self, a):
        if type(a) == int:
            return MyArray([i * a for i in self.lista], self.r, self.c, self.by_row)
        elif type(a) == self.__class__ and self.r == a.r and self.c == a.c:
            return MyArray([(self.lista[i] * a.lista[i]) for i in range(len(self.lista))], self.r, self.c, self.by_row)

    def __matmul__(self, a):
        if type(a) == self.__class__ and self.c == a.r:
            aux = [0] * self.r * a.c
            salida = MyArray(aux, self.r, a.c, self.by_row)
            counter = 0
            for i in range(1, self.r + 1):
                for h in range(1, a.c + 1):
                    aux[counter] = sum([(self.get_row(i)[k] * a.get_col(h)[k]) for k in range(len(a.get_col(i)))])
                    counter += 1
        else:
            salida = "tipo incorrecto o no es cuadrada"
        return salida

    def __pow__(self, power):
        if self.r == self.c:
            if power == 0:
                salida = MyArray(self.identidad(), self.r, self.c, self.by_row)
            elif power == 1:
                salida = self
            else:
                final = self
                for i in range(power + 1):
                    final @= self
                salida = final
        else:
            salida = "No es cuadrada"
        return salida

    # % INVERSA
    def cofactores(self):
        aux = [0] * self.r * self.c
        salida = MyArray(aux, self.r, self.c, self.by_row)
        counter = 0
        for i in range(1, self.r + 1):
            for h in range(1, self.c + 1):
                aux[counter] = round(((-1) ** (i + h) * self.del_col(i).del_row(h).det()), 7)
                counter += 1
        return salida

    def inversa(self, metodo=0, aprox=5):
        if metodo == 0:
            deet = self.det()
        else:
            deet = self.det2()
        if deet == 0:
            return "no es inversible"
        else:
            return MyArray([round(1 / deet * i, aprox) for i in self.cofactores().lista], self.r, self.c, self.by_row)

    # ELIMINIACION GAUSSIANA
    def u(self):
        if self.lista[0] == 0:
            pass
        else:
            aux = MyArray(self.lista.copy(), self.r, self.c, self.by_row)
            # k_factores = []
            n_swaps = 0
            for i in range(1, self.c):
                eliminar = aux.get_col(i)[i:]
                pivot = aux.get_elem(i, i)
                counter = 0
                while pivot == 0:
                    aux = aux.swap_rows(i, i + counter)
                    counter += 1
                    n_swaps += 1
                    if n_swaps == self.r:
                        counter = 0
                        continue
                counter = i
                for k in eliminar:
                    k_factor = k / pivot
                    # k_factores.append(k_factor)
                    reemplazar = []
                    count2 = 0
                    for g in aux.get_row(i):
                        count2 += 1
                        res = aux.get_elem(counter + 1, count2) - (k_factor * g)
                        reemplazar.append(res)
                    aux.lista[(self.c * counter):(self.c * counter) + self.c] = reemplazar
                    counter += 1
            return aux, n_swaps

    def diag_prod(self):
        prod = []
        for i in range(1, self.c + 1):
            prod.append(self.get_elem(i, i))
        res = 1
        for i in prod:
            res *= i
        return res

    def det2(self):
        return ((-1) ** self.u()[1]) * self.u()[0].diag_prod()


# %%
if __name__ == "__main__":
    matriz3x4 = MyArray([1, 2, 5, 6, 7, 3, 8, 9, 10, 5, 33, 3], 3, 4, True)
    matriz3x4_false = MyArray([1, 2, 5, 6, 7, 3, 8, 9, 10, 5, 33, 3], 3, 4, False)
    matriz_ = MyArray([1, 6, 8, 5, 2, 7, 9, 33, 5, 3, 10, 3], 3, 4, False)
    matriz4x4 = MyArray([1, 2, 5, 6, 7, 3, 8, 9, 10, 5, 33, 3, 14, 16, 19, 3], 4, 4, True)
    matriz3x5 = MyArray([1, 2, 5, 6, 14, 7, 3, 8, 9, 15, 10, 5, 33, 3, 16], 3, 5, True)
    matriz2x2 = MyArray([2, 3, 4, 5], 2, 2, True)
    matriz2x3 = MyArray([2, 3, 1, 4, 5, 9], 2, 3, True)
    matriz2x2_1 = MyArray([1, 2, 3, 1], 2, 2, True)
    matriz3x3 = MyArray([1, 2, 3, 4, 5, 6, 9, 2, 5], 3, 3, True)
    matriz3x3_false = MyArray([1, 2, 3, 4, 5, 6, 9, 2, 5], 3, 3, False)
    matriz20x20 = MyArray(
        [14, 91, 52, 74, 30, 26, 57, 34, 84, 90, 17, 25, 13, 22, 58, 4, 49, 97, 32, 31, 90, 67, 40, 83, 23, 94, 12, 61,
         5, 86, 0, 44, 48, 17, 93, 33, 59, 11, 92, 31, 20, 24, 40, 39, 14, 40, 14, 58, 18, 82, 5, 81, 65, 86, 14, 89,
         92, 29, 66, 98, 59, 9, 28, 52, 70, 28, 75, 80, 37, 49, 17, 72, 3, 8, 44, 91, 88, 17, 53, 11, 15, 3, 71, 68, 87,
         44, 72, 25, 28, 90, 45, 2, 74, 4, 88, 22, 48, 17, 53, 1, 14, 33, 86, 22, 30, 83, 1, 33, 72, 49, 65, 65, 20, 38,
         29, 27, 98, 32, 92, 42, 5, 42, 73, 10, 87, 7, 23, 8, 91, 86, 49, 61, 94, 62, 6, 18, 49, 38, 24, 44, 82, 5, 8,
         24, 86, 80, 11, 42, 80, 18, 54, 0, 43, 2, 87, 23, 18, 77, 18, 53, 92, 87, 98, 1, 35, 4, 15, 93, 13, 68, 50, 93,
         25, 3, 39, 77, 47, 18, 23, 94, 96, 15, 41, 99, 60, 67, 60, 99, 31, 93, 26, 40, 94, 2, 98, 63, 13, 8, 84, 45,
         68, 63, 11, 31, 24, 81, 39, 40, 21, 24, 24, 95, 4, 45, 58, 8, 24, 56, 34, 33, 46, 7, 53, 47, 20, 63, 38, 37,
         45, 96, 87, 86, 51, 14, 69, 67, 28, 3, 5, 3, 49, 28, 12, 10, 78, 42, 2, 36, 45, 2, 35, 57, 80, 78, 72, 70, 17,
         35, 35, 18, 49, 70, 57, 71, 13, 19, 45, 76, 51, 85, 19, 42, 96, 99, 67, 69, 28, 48, 93, 60, 40, 54, 16, 83, 74,
         18, 11, 76, 15, 32, 50, 28, 0, 86, 25, 50, 27, 93, 81, 74, 71, 4, 51, 71, 39, 65, 48, 13, 6, 56, 93, 81, 26,
         11, 94, 94, 89, 46, 56, 70, 71, 36, 82, 75, 24, 80, 84, 60, 42, 8, 78, 30, 83, 95, 48, 75, 73, 28, 6, 51, 90,
         75, 70, 63, 25, 60, 78, 25, 44, 90, 76, 81, 20, 53, 27, 16, 45, 95, 17, 25, 48, 96, 38, 15, 4, 53, 83, 89, 74,
         58, 44, 13, 27, 23, 70, 10, 55, 53, 20, 34, 10, 26, 31, 59, 77, 32, 16, 14, 43, 100, 16, 85, 96, 35, 41, 27,
         33, 50, 75, 90], 20, 20, True)
    matriz5x5 = MyArray([2, 2, 3, 4, 5, 6, 2, 9, 8, 7, 8, 9, 2, 2, 1, 4, 2, 0, 5, 3, 3, 5, 2, 8, 3], 5, 5, True)
