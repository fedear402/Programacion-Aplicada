import cProfile

class Fecha():
    daynames = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    monthnames = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", 
                  "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    weekends = ["sabado", "domingo"]
    weekdays = ["lunes", "martes", "miercoles", "jueves", "viernes"]
    
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

    def __hash__(self):
        return hash(self.fecha)

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
    
    def __ge__(self, other):
        return Fecha.later_earlier(self.fecha, other.fecha) or self == other

    def __le__(self, other):
        return not Fecha.later_earlier(self.fecha, other.fecha) or self == other


    def isweekend(self):
        return self.dow in [i[:3] for i in Fecha.weekends]
    
    def isweekday(self):
        return self.dow in [i[:3] for i in Fecha.weekdays]
    
    def nextweekday(self):
        if self.dow == "sab":
            return self.add2date(2)
        elif self.dow == "dom":
            return self.add2date(1)

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
    
    def yearfrac(self, other, basis=0):

        days_between = self.days_between(self.fecha, other.fecha)

        if basis == 0:  # 30/360
            return days_between / 360
        elif basis == 1:  # Actual/Actual
            return days_between / sum(__class__.monthlengths(self.fecha[2]))
        elif basis == 2:  # Actual/360
            return days_between / 360
        elif basis == 3:  # Actual/365
            return days_between / 365



    def timetodate(self, dateB, units="d"):
        end_day, end_month, end_year = dateB.fecha[0], dateB.fecha[1], dateB.fecha[2]
        start_day, start_month, start_year = self.fecha[0], self.fecha[1], self.fecha[2]

        changed = False
        if __class__.later_earlier(self.fecha, dateB.fecha):
            start_day, end_day, = end_day, start_day
            start_month, end_month = end_month, start_month
            start_year, end_year = end_year, start_year
            changed = True
        
        day_diff = end_day - start_day
        month_diff = end_month - start_month
        year_diff = end_year - start_year

        if day_diff < 0:
            month_diff -= 1
            day_diff += Fecha.monthlengths(start_year)[start_month]
        if month_diff < 0:
            year_diff -= 1
            month_diff += 12

        if units == "d":
            days = Fecha.days_between(self.fecha, dateB.fecha)
            return days if not changed else -days
        elif units == "dm":
            return (day_diff, month_diff) if not changed else (-day_diff, -month_diff)
        elif units == "dmy":
            return (day_diff, month_diff, year_diff) if not changed else (-day_diff, -month_diff, -year_diff) 
        
    @staticmethod
    def schedule(start_date, end_date, frequency:int):
        assert 1 <= frequency <= 12
        """ devuelva un calendario de pagos desde la fecha de inicio a la fecha final. 
        La salida debe ser una lista de objetos de tipo fecha.
        """
        leg = []
        while start_date <= end_date:
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
        """ Inverso de doy():
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
        return gesamt - start_tail - end_tail - 1

    @staticmethod
    def dayname(fecha:tuple):
        """ para conocer que dia fue cierta fecha:
            - toma los dias que hay desde el sabado 16/10/1582 (primer con el Calendario Georgiano) 
            y la fecha cuyo nombre queres saber.
            - le resta 2 (mod 7) para tener el indice del dia en Fecha.daynames 
            (EJ: el indice del 16/10/1582, deberia ser [5], sabado; 
            primero, tomo los dias entre 16/10/1582 y la fecha objetivo --tmb. 16/10/1582--, que es 0;
            al restarle 2, queda -2, lo que mod7 es 5)
            """
        start = (16, 10, 1582)
        return __class__.daynames[(__class__.days_between(start, fecha) - 2) % 7]

    @staticmethod
    def combinar(*args):
        combined = []
        for i in [item for sublist in args for item in sublist]:
            if i not in combined:
                combined.append(i)
        combined.sort(key=lambda date : (date.fecha[2], date.fecha[1], date.fecha[0]))
        return combined

class Bonos():
    def __init__(self, **kwargs):

        self.ticker = kwargs['ticker']
        self.issue_date = kwargs['issue_date']
        self.maturity = kwargs['maturity']
        self.face_value = kwargs['face_value']
        self.day_count = kwargs['day_count']

        self.coupon_freq = kwargs['coupon_freq']  # frequencia de pago de cupones - 1, 2, 3, 4 o 12

        self.coupon_dates = kwargs['coupon_dates']  # fechas de pago de cupon
        self.coupon_rates = kwargs['coupon_rates']  # tasas de cupon 

        self.amort_dates = kwargs['amort_dates']  # fechas de amortizacion
        self.amort_perc = kwargs['amort_perc']  # tasas de amortizacion

        self.cap = kwargs['capitaliza']  # Bool
        self.cap_dates = kwargs['cap_dates'] if self.cap else None  # fechas de capitalizacion
        self.cap_rates  = kwargs['cap_rates'] if self.cap else None  # tasas de capitalizacion 
        
        self.irregular_first_coupon = kwargs['irregular_first_coupon']
        self.irregular_first_coupon_type = kwargs['irregular_first_coupon_type'] if self.irregular_first_coupon else None
        self.settlement_plus = kwargs['settlement_plus']
        self.currency = kwargs['currency']

        self.fechas = self.fechar() # todas las fechas en las que ocurre algo

    #### REFORMATEANDO ###############
    def amort_percs(self):
        """ Le podes dar en el kwargs una lista o un diccionario
        con fechas de key y el porcentaje como value.
         - Si le das un diccionario simplemente cambia los fines de semana
         - Si le das un string "lineal", interpreta que cada una de las fechas
         amortiza un mismo porcentaje la cantidad de fechas en amort_dates
         - si le das 
        """

        if isinstance(self.amort_perc, dict):
            return {i if not i.isweekend() else i.nextweekday():j 
                    for i, j in self.amort_perc.items()}
        
        #  Esto para que puedas darle un solo valor y lo divide entre todas las fechas
        elif self.amort_perc == "lineal":
            return {i if not i.isweekend() else i.nextweekday():1/len(self.amort_perc)
                    for i in self.amort_dates}
        
        #  Esto para darle una lista de valores
        else:
            amortpercss = [0]*len(self.fechas)
            ind = len(self.fechas)-len(self.amort_dates)
            lst = amortpercss[:ind]+self.amort_perc
            return {self.fechas[i] if not self.fechas[i].isweekend() else self.fechas[i].nextweekday():lst[i] for i in range(len(self.fechas))}
  
    def coup_rates(self):
        """ Misma logica que amortizaciones
        si le das una list asume linealidad hasta maturity
        sino sigue de largo con las fechas de un dict
        """
        if isinstance(self.coupon_rates, dict):
            return {i if not i.isweekend() else i.nextweekday():j  for i,j in self.coupon_rates.items()}
        else:
            rates= [0]*len(self.fechas)
            ind = len(self.fechas)-len(self.coupon_dates)
            lst = rates[:ind]+self.coupon_rates
            return {self.fechas[i] if not self.fechas[i].isweekend() else self.fechas[i].nextweekday():lst[i] for i in range(len(self.fechas))}        

    def cap_rates(self):
        if self.cap_rates is not None:
            if isinstance(self.cap_rates, dict):
                return self.cap_rates 
            else:
                capr = [0]*len(self.fechas)
                lst = self.cap_rates + capr[len(self.cap_rates):]
                return {self.fechas[i]:lst[i] for i in range(len(self.fechas))}
        else:
            return {self.fechas[i]:0 for i in range(len(self.fechas))}

    def fechar(self):
        '''
        combina las fechas de pago de cupón y de amortización;
        devuelve todas las fechas en las que pasa algo para el calendario
        y evita los fines de semana.
        '''
        coupons = self.coup_rates()
        amorts =  self.amort_percs()
        combinado = Fecha.combinar(coupons.keys(), amorts.keys())
        return [i if not i.isweekend() else i.nextweekday() for i in combinado]


    #### MAIN #####################################################################
    def main(self):
        amortizado = [0]*len(self.fechas)
        residual = [self.face_value]*len(self.fechas)
        cap = [0]*len(self.fechas)
        iper = [0]*len(self.fechas)
        idev = [0]*len(self.fechas)

        coup_rates = self.coup_rates()
        caprates = self.caprates()
        amortpercs = self.amort_percs()

        for i, fecha in enumerate(self.fechas):

            if fecha in list(amortpercs.keys()):
                #print(self.fechas.index(self.amort_dates[0])-1)
                amortizado[i] = residual[self.fechas.index(self.amort_dates[0] if not self.amort_dates[0].isweekend() else self.amort_dates[0].nextweekday())-1] * amortpercs[fecha]

            if fecha in list(coup_rates.keys()):
                iper[i] =( residual[i-1] * ( coup_rates[fecha] / self.coupon_freq ) ) * (1 - caprates[fecha])
                idev[i] =  residual[i-1] * ( coup_rates[fecha] / self.coupon_freq )
 
            if fecha in list(caprates.keys()):
                cap[i] =( idev[i] ) * caprates[fecha]

            residual[i] = residual[i-1] - amortizado[i] + cap[i]
        return idev, iper, cap, amortizado, residual


        

    #### CALENDARIO ############################################################
    def flujo(self):
        lst = [i+j for i, j in zip(self.main()[1], self.main()[3])]
        return {self.fechas[i]:lst[i] for i in range(len(self.fechas))}

    def flujolst(self):
        return [i+j for i, j in zip(self.main()[1], self.main()[3])]    

    def calendario_full(self):
        data = {
            'fechas': self.fechas,
            'i-dev' : self.main()[0],
            'i-per' : self.main()[1],
            'cap' : self.main()[2],
            'amort': self.main()[3],
            'residual': self.main()[4],
            'flujo' : [i+j for i, j in zip(self.main()[1], self.main()[3])]
        }
        return data

    def calendario_full_print(self, just=10):
        cal = self.calendario_full()
        keys = []
        for i in cal.keys():
            keys.append(f"{i}")  
        keys = [key.ljust(just) for key in keys]
        print(" | ".join(keys))
        all = []
        for value in cal.values():
            all.append(value)
        for i in range(len(all[0])):
            values = []
            for j in range(len(all)):
                if isinstance(all[j][i], float):
                    values.append(f"{all[j][i]:.2f}".ljust(just))
                else:
                    values.append(f"{all[j][i]}".ljust(just))
            print(" | ".join(values))


    #### ANALISIS ############################################################
    def corrido(self, at:Fecha):
        basis = {
            '30/360':0,
            'actual/actual':1,
            'actual/360':2,
            'actual/365':3
        }
        i = Fecha.combinar(self.fechas, [at]).index(at)
        last_pmt_date = self.fechas[i-1] if i-1 > 0 else at
        next_pmt = self.main()[0][i]
        return next_pmt * last_pmt_date.yearfrac(at, basis=basis[self.day_count])*self.coupon_freq

    def clean(self, tir, at:Fecha):
        basis = {
            '30/360':0,
            'actual/actual':1,
            'actual/360':2,
            'actual/365':3
        }
        flujo = self.flujo()
        i = Fecha.combinar(self.fechas, [at]).index(at)
        next_pmt_date = self.fechas[i]
        precio = 0
        for fecha, pago in flujo.items():
            if fecha >= next_pmt_date:
                days = at.yearfrac(fecha, basis=basis[self.day_count])*self.coupon_freq
                disc = pago / ((1+(tir/self.coupon_freq))**days)
                precio += disc
        return precio

    def dirty(self, tir, at:Fecha):
        return self.clean(tir, at) + self.corrido(at) 
    
    def next_cashflows(self, at, price):
        salida = {at:-price}
        for fecha, pago in self.flujo().items():
            if fecha >= at:
                salida[fecha] = pago
        return salida
    
    def next_discounted(self, at, price, r):
        basis = {
            '30/360':0,
            'actual/actual':1,
            'actual/360':2,
            'actual/365':3
        }
        salida = {at:-price}
        for fecha, pago in self.flujo().items():
            if fecha >= at:
                days = at.yearfrac(fecha, basis=basis[self.day_count])*self.coupon_freq
                salida[fecha] = pago/(1+r)**days
            else:
                continue
        return salida
    
    def fraclist(self, at):
        basis = {
            '30/360':0,
            'actual/actual':1,
            'actual/360':2,
            'actual/365':3
        }
        return [at.yearfrac(fecha, basis=basis[self.day_count])*self.coupon_freq for fecha, pago in self.flujo().items() if fecha >= at]
    
    def van(self, at, precio, r):
        return sum(list(self.next_discounted(at, precio, r).values())) + precio

    def tir(self, fecha, precio, estimado_inicial=0.14, tolerancia=0.001, max_iteraciones=1000):
        """
        Saca la tir con el metodo de interpolacion lineal que explica dumrauf
        """
        valor_presente = vpe = self.van(fecha, precio, estimado_inicial)
        estimado = estimado_inicial
        # Si el valor presente es mayor al precio, aumentar la tasa
        if valor_presente > precio:
            iteraciones = 0
            while vpe < precio and iteraciones < max_iteraciones:
                iteraciones += 1
                estimado += tolerancia
                vpe = self.van(fecha, precio, estimado)
            if iteraciones == max_iteraciones:
                return "NO CONVERGE"
            dif_tasas = estimado - estimado_inicial
            dif_a = valor_presente - vpe
            dif_b = valor_presente - precio
            if abs(precio-vpe) < tolerancia:
                return estimado
            return ( estimado_inicial + (dif_b * (dif_tasas) / dif_a) ) * self.coupon_freq

        # Si el valor presente es menor al precio, disminuir la tasa
        elif valor_presente < precio:
            iteraciones = 0
            while vpe < precio and iteraciones < max_iteraciones:
                iteraciones += 1
                estimado -= tolerancia
                vpe = self.van(fecha, precio, estimado)
            if iteraciones == max_iteraciones:
                return "NO CONVERGE"
            dif_tasas = estimado - estimado_inicial
            dif_a = valor_presente - vpe
            dif_b = valor_presente - precio
            if abs(precio-vpe) < tolerancia:
                return estimado
            return ( estimado_inicial + (dif_b * (dif_tasas) / dif_a) ) * self.coupon_freq

    def duration(self, at, precio):
        tir = self.tir(at, precio)
        descontados = list(self.next_discounted(at, precio, tir).values())[1:]
        fraclist = self.fraclist(at)
        salida = [descontados[i]*fraclist[i]/precio for i in range(len(descontados))]
        return sum(salida)

    def duration_mod(self, at, precio):
        tir = self.tir(at, precio)
        descontados = list(self.next_discounted(at, precio, tir).values())[1:]
        fraclist = self.fraclist(at)
        salida = [(descontados[i]*fraclist[i]/precio)/(1+tir) for i in range(len(fraclist))]
        return sum(salida)

    def current_yield(self, at, price, until=(0,0,1)):
        until = at.add2date(until[0], until[1], until[2])
        next_index = Fecha.combinar(self.fechas, [at]).index(at)
        last_index = Fecha.combinar(self.fechas, [until]).index(until)
        next_coupon_payments = self.main()[0][next_index:last_index]
        current_yield = sum(next_coupon_payments) / price
        return current_yield

    def capital_gains(self, at, price, until=(0,0,1)):
        new_at = at.add2date(until[0], until[1], until[2])
        future_price = self.clean(self.tir(at, price), new_at)
        capital_gains = (future_price - price) / price
        return capital_gains

    def info(self, at, dirty=None, tir=None):
        assert tir is not None or dirty is not None
        accrued = self.corrido(at)
        if dirty is None:
            clean = self.clean(tir, at)
            dirty = clean + accrued
        elif tir is None:
            clean = dirty - accrued
            tir = self.tir(at, dirty)
        duration = self.duration(at, dirty)
        current_yield = self.current_yield(at, dirty, (0,0,1) )
        capital_gains = self.capital_gains(at, dirty, (0,0,1) )
        duration_mod = self.duration_mod(at, dirty)
    
        return {
            'precio dirty' : dirty,
            'precio clean' : clean,
            'accrued' : accrued,
            'tir' : tir,
            'duration' : duration,
            'current_yield': current_yield,
            'capital_gains' : capital_gains,
            'duration_modificada' : duration_mod
        }



class Portfolio(Bonos):
    def __init__(self, laminas, datos):
        pass


class Inventory:
    pass

class FixedIncome:
    pass



##################################################################################################
# if __name__ == "__main__":
#     issue = Fecha("22/01/2021")
#     mat = Fecha("22/07/2032")
#     freq = 1
#     calendar = Fecha.schedule(issue, mat, freq)

#     first = Fecha("22/01/2023")
#     amort_start = Fecha("22/enero/2026")
#     cupdates=Fecha.schedule(first, mat, freq)
#     caps = Fecha.schedule(issue, amort_start.add2date(0,0,-1), freq)
#     amorts = Fecha.schedule(amort_start, mat, freq)

#     bonodataYPF1 = {
#         'ticker' : "YPF",
#         'issue_date' : issue,
#         'maturity' : mat,
#         'coupon_rates' : [0.0575]*len(cupdates),
#         'coupon_dates' : cupdates,
#         'coupon_freq' : freq,
#         'irregular_first_coupon' : False,
#         'amort_dates' : amorts,
#         'amort_perc' : [1/len(amorts)] * len(amorts),
#         'face_value' : 100,
#         'day_count' : "actual/365",
#         'settlement_plus' : 2,
#         'currency' : "USD",
#         'capitaliza' : False,
#         'cap_dates' : caps,
#         'cap_rates' : [0.0]*len(caps)

#         }
#     today = Fecha("30/5/2023")
#     # ypf = Bonos(**bonodataYPF1)
#     # print(ypf.calendario_full_print())
#     # print(ypf.info(today, dirty=106))


#     # #############################################################################    
#     issue = Fecha("23/01/2021")

#     first = Fecha("23/01/2022")

#     amort_start = Fecha("23/01/2029")

#     mat = Fecha("23/07/2032")
    
#     freq = 2
#     calendar = Fecha.schedule(issue, mat, freq)

#     cupdates=Fecha.schedule(first, mat, freq)
#     caps = Fecha.schedule(issue, amort_start.add2date(0,0,-1), freq)
#     amorts = Fecha.schedule(amort_start, mat, freq)

#     bonodataYPF2 = {
#         'ticker' : "YPF2",
#         'issue_date' : issue,
#         'maturity' : mat,
#         'coupon_rates' : [0.0575]*len(cupdates),
#         'coupon_dates' : cupdates,
#         'coupon_freq' : freq,
#         'irregular_first_coupon' : False,
#         'amort_dates' : amorts,
#         'amort_perc' : [1/len(amorts)] * len(amorts),
#         'face_value' : 100,
#         'day_count' : "actual/365",
#         'settlement_plus' : 2,
#         'currency' : "USD",
#         'capitaliza' : False,
#         'cap_dates' : caps,
#         'cap_rates' : [0.0]*len(caps)

#         }
#     ypf2 = Bonos(**bonodataYPF2)
#     # print(ypf2.calendario_full_print())
#     # print(ypf2.info(today, dirty=104))


#     #############################################################################
#     issueb1 = Fecha("1/1/2020")
#     maturityb1 = Fecha("1/1/2030")
#     freqb1 = 1
#     cupondatesb1 = Fecha.schedule(Fecha("1/1/2021"), maturityb1, freqb1)

#     bono1 = Bonos(**{
#         'ticker' : "BONO1",
#         'issue_date' : issueb1,
#         'maturity' : issueb1,
#         'coupon_rates' : [0.067]*len(cupondatesb1),
#         'coupon_dates' : cupondatesb1,
#         'coupon_freq' : freqb1,
#         'irregular_first_coupon' : False,
#         'amort_dates' : [maturityb1],
#         'amort_perc' : [1],
#         'face_value' : 1000,
#         'day_count' : "30/360",
#         'settlement_plus' : 2,
#         'currency' : "USD",
#         'capitaliza' : False,
#         'cap_dates' : caps,
#         'cap_rates' : [0.0]*len(caps)        
#     })
#     print(bono1.calendario_full_print())
#     print("TIR", bono1.tir(issueb1,  881.7349781, estimado_inicial=0.1))
#     print("VAN", bono1.van(issueb1, 881.734978112087, 0.1))
#     print(bono1.info(issueb1, tir= 0.08495082 ))


#     issueb2 = Fecha("1/1/2020")
#     maturityb2 = Fecha("1/1/2030")
#     freqb2 = 2
#     cupondatesb2 = Fecha.schedule(issueb2, maturityb2, freqb2)

#     bono2 = Bonos(**{
#         'ticker' : "BONO1",
#         'issue_date' : issueb2,
#         'maturity' : issueb2,
#         'coupon_rates' : [0.15]*len(cupondatesb2),
#         'coupon_dates' : cupondatesb2,
#         'coupon_freq' : freqb2,
#         'irregular_first_coupon' : False,
#         'amort_dates' : [maturityb2],
#         'amort_perc' : [1],
#         'face_value' : 1000,
#         'day_count' : "30/360",
#         'settlement_plus' : 2,
#         'currency' : "USD",
#         'capitaliza' : False,
#         'cap_dates' : caps,
#         'cap_rates' : [0.0]*len(caps)        
#     })

#     BondsDatabase=({
#         'ypf1': bono1,
#         'ypf2': bono2
#     })
#     laminas = {
#         'ypf1': 500,
#         'ypf2': 300
#     }

#     #############################################
#     cupones = {}
#     cupones[Fecha("9 enero 2020")] = 0.00125
#     cupones[Fecha("9 julio 2020")] = 0.00125
#     cupones[Fecha("9 enero 2021")] = 0.00125
#     cupones[Fecha("9 julio 2021")] = 0.02
#     cupones[Fecha("9 enero 2022")] = 0.02
#     cupones[Fecha("9 julio 2022")] = 0.03875
#     cupones[Fecha("9 enero 2023")] = 0.03875
#     cupones[Fecha("9 julio 2023")] = 0.0425
#     cupones[Fecha("9 enero 2024")] = 0.0425
#     tanda_final = Fecha.schedule(Fecha("9 julio 2024"), Fecha("9/1/2038"), 2)
#     for i in range(len(tanda_final)):
#         cupones[tanda_final[i]] = 0.05

#     issue = Fecha("4/9/2020")

#     first = Fecha("9/7/2020")

#     amort_start = Fecha("09/1/2028")

#     mat = Fecha("9/1/2038")

#     freq = 2
#     calendar = Fecha.schedule(first, mat, 2)

#     cupdates = list(cupones.keys())

#     amorts = Fecha.schedule(amort_start, mat, 2)

#     bonodataAE38 = {
#         'ticker' : "YPF2",
#         'issue_date' : issue,
#         'maturity' : mat,
        
#         'coupon_rates' : cupones,
#         'coupon_dates' : list(cupones.keys()),
#         'coupon_freq' : freq,

#         'irregular_first_coupon' : False,

#         'amort_dates' : amorts,
#         'amort_perc' : [1/(len(amorts))] * len(amorts),

#         'face_value' : 100,
#         'day_count' : "30/360",
#         'settlement_plus' : 2,
#         'currency' : "USD",
#         'capitaliza' : False

#         }
#     today=Fecha("14-06-2023")
#     AE38 = Bonos(**bonodataAE38)
#     print(AE38.calendario_full_print())
    
#     for dato, valor in AE38.info(today, dirty=59.9677159).items():
#         print(dato, valor)
#     # cProfile.run('AE38.info(today, dirty=14860/247.8)')
#     # print(AE38.corrido(issue))

    
