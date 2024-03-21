class Calendario():
    daynames = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    weekends = ["sabado", "domingo"]
    weekdays = ["lunes", "martes", "miercoles", "jueves", "viernes"]
    monthnames = [0, "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
                  "noviembre", "diciembre"]
    
    def __init__(self, day, month, year, ws="lunes", **kwargs):
        assert 1 <= day <= Calendario.monthlengths(year)[month]
        assert 1 <= month <= 12
        self.day = day
        self.month = month
        self.year = year
        self.dayname = Calendario.dayname(day, month, year)

        # Dia de la semana, depende de ws (week-start)
        self.dow = (Calendario.daynames.index(self.dayname) - Calendario.daynames.index(ws)) % 7 + 1
        self.doy = Calendario.doy(day, month, year)  # Day of Year
        # self.woy =
        # self.wom =
        self.monthname = Calendario.monthnames[month]
        self.str = f"{self.dayname} {self.day} de {self.monthname} de {self.year}"
        self.isweekend = self.dayname in Calendario.weekends
        
    @staticmethod
    def leap(year):
        """ Devuelve True si el año dado es biciesto; sino devuelve False
            """
        return year % 4 == 0 if year % 100 != 0 else year % 400 == 0
    
    @staticmethod
    def monthlengths(year):
        """ Devuelve una lista con la cantidad de dias en cada mes de el año dado
            el 0 al principio es para que sea mas cómoda la indexación cuando se usa el metodo
            """
        return [0, 31, 29 if Calendario.leap(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    @staticmethod
    def doy(day, month, year):
        """ Day of Year: devuelve el numero de dia en el año
            Ejemplo: 3/2/2023 es el 34to dia del año (31 + 3)
            """
        return sum(Calendario.monthlengths(year)[:month]) + day

    @staticmethod
    def later_earlier(start_day, start_month, start_year, end_day, end_month, end_year):
        """ helper para days_between
            determina si la fecha de inicio es en realidad la final
            """
        salida = True
        if start_year <= end_year:
            salida = False
            if start_month <= end_month:
                salida = False
                if start_day <= end_day:
                    salida = False
        return salida

    @staticmethod
    def days_between(start_day, start_month, start_year, end_day, end_month, end_year):
        """ devuelve la distancia en dias entre dos fechas, sin incluir la fecha final
            si la fecha end es mas temprana a la start, las da vuelta
            """
        if Calendario.later_earlier(start_day, start_month, start_year, end_day, end_month, end_year):
            start_day, end_day, = end_day, start_day
            start_month, end_month = end_month, start_month
            start_year, end_year = end_year, start_year

        gesamt = sum([sum(Calendario.monthlengths(year)) for year in range(start_year, end_year + 1)])
        start_tail = Calendario.doy(start_day, start_month, start_year)
        end_tail = sum(Calendario.monthlengths(end_year)) - Calendario.doy(end_day, end_month, end_year) - 1
        print(gesamt, start_tail, end_tail)
        return gesamt - start_tail - end_tail

    @staticmethod
    def dayname(day, month, year):
        """ para conocer que dia fue cierta fecha:
            - toma los dias que hay desde el sabado 16/10/1582 (primer con el calendario Georgiano) 
            y la fecha cuyo nombre queres saber.
            - le resta 3 (mod 7) para tener el indice del dia en Calendario.daynames 
                (EJ: el indice del 16/10/1582, deberia ser [5], sabado; 
                primero, tomo los dias entre 16/10/1582 y la fecha objetivo --tmb. 16/10/1582--, que es 1;
                al restarle 3, queda -2, lo que mod7 es 5)
            """
        return Calendario.daynames[(Calendario.days_between(16, 10, 1582, day, month, year) - 3) % 7]


if __name__ == "__main__":
    print(Calendario.dayname(16, 10, 1582), "\n") # Sabado
    print(Calendario.dayname(6, 5, 2023), "\n")  # Sabado
    print("5,5,2023-5,5,2023", Calendario.days_between(5, 5, 2023, 5, 5, 2023), "\n")
    print("1,1,0-5,5,2023",Calendario.days_between(1, 1, 0, 5, 5, 2023), "\n")  # 739011
    print("1,1,1-5,5,2023",Calendario.days_between(1, 1, 1, 5, 5, 2023), "\n")  # 738645
    print("20,10,2010-5,5,2023",Calendario.days_between(20, 12, 2010, 5, 5, 2023), "\n")  # 4520
