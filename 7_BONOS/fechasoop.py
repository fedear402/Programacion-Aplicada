class Fecha():
    daynames = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    monthnames = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
                  "noviembre", "diciembre"]
    
    def __init__(self, fecha, orig=(1, 1, 1)):
        """ fecha : puede ser str, tuple o int
        """
        if isinstance(fecha, tuple):
            self.fecha = fecha
            self.fecha_num = __class__.days_between(orig, self.fecha)
            self.dow = self.dayname(self.fecha)[:3]

        elif isinstance(fecha, str):
            separadores = [".", ",", "/", "-", "_", ";", " "]
            fecha_ = list(filter(lambda x: len(x) > 1, [fecha.split(separador) for separador in separadores]))[0]
            fecha_ = [i.replace(" ", "") for i in fecha_]
            dia = int(fecha_[0])
            mes = fecha_[1]
            if not mes.isdigit():
                for i, month in enumerate(__class__.monthnames):
                    if month.startswith(str(mes).lower()):
                        mes = i + 1
            else:
                mes = int(fecha_[1])
            year = int(fecha_[2])
            self.fecha = (dia, mes, year)
            self.fecha_num = __class__.days_between(orig, self.fecha)
            self.dow = __class__.dayname(self.fecha)[:3]

        elif isinstance(fecha, int):
            year = orig[2]
            aux = fecha
            while aux > sum(__class__.monthlengths(year)):
                aux -= sum(__class__.monthlengths(year))
                year += 1
            dedoy = __class__.dedoy(aux, year)
            self.fecha = (dedoy[0], dedoy[1], year)
            self.fecha_num = __class__.days_between(orig, self.fecha)
            self.dow = __class__.dayname(self.fecha)[:3]
        
        day = self.fecha[0]
        month = self.fecha[1]
        year = self.fecha[2]
        assert 1 <= day <= __class__.monthlengths(year)[month]
        assert 1 <= month <= 12

    def __eq__(self, __value: object) -> bool:
        return self.fecha == __value.fecha
    
    def __str__(self):
        return self.num2str()
    
    def __repr__(self):
        return self.num2str()
    
    def __gt__(self, other):
        return Fecha.later_earlier(self.fecha, other.fecha)
    
    def __lt__(self, other):
        return not Fecha.later_earlier(self.fecha, other.fecha)

    def date2num(self, orig=(1,1,1)):
        return __class__.days_between(orig, self.fecha)
    
    def num2date(self):
        return self.fecha

    def date2str(self, format=0, sep="-"):
        """ formatos
        0 : "dd-mm-yyyy"
        1 : "dd-mmm-yyyy"
        2 : "dd-mm-yy"
        3 : "dd-mmm-yy"
        """
        day = self.fecha[0]
        month = self.fecha[1]
        year = self.fecha[2]
        if format == 0:
            return f"{day}{sep}{month}{sep}{year}"
        elif format == 1:
            return f"{day}{sep}{__class__.monthnames[month][:3]}{sep}{year}"
        elif format == 2:
            return f"{day}{sep}{month}{sep}{int(str(year)[:2])}"
        elif format == 3:
            return f"{day}{sep}{__class__.monthnames[month][:3]}{sep}{int(str(year)[:2])}"
        
    def num2str(self, format=0, sep="-"):
        return self.date2str(format, sep)
    
    def add2date(self, dias=0, meses=0, years=0):
        start_day, start_month, start_year = self.fecha[0], self.fecha[1], self.fecha[2]

        # MESES
        end_month = (start_month+meses)%12 if (start_month+meses) != 12 else 1

        # AÑOS
        if start_month > 0:
            end_year = start_year + years + (start_month+meses)//12
        else:
            end_year = start_year + years - (start_month+meses)//12

        # DIAS
        end_day = start_day + dias
        while end_day > __class__.monthlengths(end_year)[end_month]:
            end_day -= __class__.monthlengths(end_year)[end_month]
            end_month += 1
            if end_month == 13:
                end_month = 1
                end_year += 1
                
        while end_day < 1:
            end_day += __class__.monthlengths(end_year)[end_month]
            end_month -= 1
            if end_month == 0:
                end_month = 12
                end_year -= 1
        return __class__((end_day, end_month, end_year))
        
    def timetodate(self, dateB, units="d"):
        end_day, end_month, end_year = dateB.fecha[0], dateB.fecha[1], dateB.fecha[2]
        start_day, start_month, start_year = self.fecha[0], self.fecha[1], self.fecha[2]
        changed = False
        if __class__.later_earlier(self.fecha, dateB.fecha):
            start_day, end_day, = end_day, start_day
            start_month, end_month = end_month, start_month
            start_year, end_year = end_year, start_year
            changed = True
        """ devuelva el tiempo entre la fecha self y la fecha dateB 
        entendiendo que si dateB es posterior a dateA debe devolverse un tiempo positivo 
        y si es anterior un tiempo negativo. En units puede especificarse la forma en que se devolverá el tiempo. 
        Puede devoverse en "d" (días) "dm" (días y meses) o "dmy" (días,meses y años) . Por default será endías.
        """
        days = __class__.days_between(self.fecha, dateB.fecha)
        months = 0
        years = 0
        if units == "d":
            salida = days if not changed else (-days)

        elif units == "dm":
            while days > __class__.monthlengths(start_year)[start_month]:
                days -= __class__.monthlengths(start_year)[start_month]
                if start_month != 12:
                    start_month += 1
                else:
                    start_month = 1
                months += 1
            salida =(days, months) if not changed else (-days, -months)

        elif units == "dmy":
            entireyears = 0
            while days > __class__.monthlengths(start_year)[end_month]:
                days -= __class__.monthlengths(start_year)[end_month]
                if months != 12:
                    months += 1
                else:
                    entireyears += 1
                    months = 1
                    if entireyears > 1:
                        years += 1

            salida = (days, months, years) if not changed else (-end_day, -months, -years)
        
        return salida

    @staticmethod
    def schedule(start_date, end_date, frequency:int):
        """ devuelva un calendario de pagos desde la fecha de inicio a la fecha final. 
        La salida debe ser una lista de objetos de tipo fecha.
        """
        leg = []
        while end_date > start_date:
            leg.append(start_date)
            start_date = start_date.add2date(0, int(12/frequency))
        return leg

    @staticmethod
    def leap(year:int):
        """ Devuelve True si el año es biciesto.
        """
        return year % 4 == 0 if year % 100 != 0 else year % 400 == 0

    @staticmethod
    def monthlengths(year:int):
        """ Devuelve una lista con la cantidad de dias en cada mes de el año dado.
            pst: el 0 al principio es para que sea mas cómoda la indexación cuando se usa el metodo
        """
        return [0, 31, 29 if __class__.leap(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    @staticmethod
    def doy(day:int, month:int, year:int):
        """ Day of Year: devuelve el numero de dia en el año.
            Ejemplo: 3/2/2023 es el 34to dia del año (31 + 3)
        """
        return sum(__class__.monthlengths(year)[:month]) + day
    
    @staticmethod
    def dedoy(daynum:int, year:int):
        """ Inverso de doy
            toma una el ordinal del año de una fecha y devuelve a que fecha de ese año corresponde
        """
        assert 1 <= daynum <= sum(__class__.monthlengths(year))
        aux = daynum
        month = 1
        for length in __class__.monthlengths(year):
            if aux > length:
                aux -= length
                month += 1
                continue
            break
        return aux, month - 1
    
    @staticmethod
    def later_earlier(start:tuple, end:tuple):
        end_day, end_month, end_year = end[0], end[1], end[2]
        start_day, start_month, start_year = start[0], start[1], start[2]
        """ helper para days_between
            determina si la fecha primera en el argumento es mas tarde que el segundo argumento
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
    def days_between(start:tuple, end:tuple):
        end_day, end_month, end_year = end[0], end[1], end[2]
        start_day, start_month, start_year = start[0], start[1], start[2]
        """ devuelve la distancia en dias entre dos fechas, sin incluir la fecha final
            si la fecha end es mas temprana a la start, las da vuelta
            """
        if __class__.later_earlier(start, end):
            start_day, end_day, = end_day, start_day
            start_month, end_month = end_month, start_month
            start_year, end_year = end_year, start_year

        gesamt = sum([sum(__class__.monthlengths(year)) for year in range(start_year, end_year + 1)])
        start_tail = __class__.doy(start_day, start_month, start_year)
        end_tail = sum(__class__.monthlengths(end_year)) - __class__.doy(end_day, end_month, end_year) - 1
        return gesamt - start_tail - end_tail

    @staticmethod
    def dayname(fecha:tuple):
        """ para conocer que dia fue cierta fecha:
            - toma los dias que hay desde el sabado 16/10/1582 (primer con el Calendario Georgiano) 
            y la fecha cuyo nombre queres saber.
            - le resta 3 (mod 7) para tener el indice del dia en Fecha.daynames 
                (EJ: el indice del 16/10/1582, deberia ser [5], sabado; 
                primero, tomo los dias entre 16/10/1582 y la fecha objetivo --tmb. 16/10/1582--, que es 1;
                al restarle 3, queda -2, lo que mod7 es 5)
            """
        start = (16, 10, 1582)
        return __class__.daynames[(__class__.days_between(start, fecha) - 3) % 7]
    
if __name__ == "__main__":
    start = Fecha("3/7/2010")
    print(start.fecha, start.add2date(-300, -35, -4))
    print(start.fecha, start.add2date(300, 35, 4))
    start = Fecha("2/5/2013")
    end = Fecha("2/12/2030")
    print(start.timetodate(end, units="dmy"))