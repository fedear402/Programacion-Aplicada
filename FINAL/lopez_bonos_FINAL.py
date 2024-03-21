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
        ''' basis:
        0 : 30/360
        1 : Actual/Actual
        2 : Actual/360
        3 : Actual/365
        '''

        days_between = self.days_between(self.fecha, other.fecha)

        if basis == 0:  # 30/360
            factor = ((other.fecha[2]-self.fecha[2]) * 360 + (other.fecha[1] - self.fecha[1]) * 30 + (other.fecha[0] - self.fecha[0]))
            return factor / 360
        
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
        start_day, start_month, start_year = start[0], start[1], start[2]
        end_day, end_month, end_year = end[0], end[1], end[2]

        if start_year > end_year:
            return True
        elif start_year == end_year:
            if start_month > end_month:
                return True
            elif start_month == end_month:
                return start_day > end_day
        return False

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

class FixedIncome():
    def __init__(self, cashflow:dict):
        '''
        cashflow: diccionario con fechas como keys y flujos como values
        '''
        self.cashflow = cashflow
        self.fechas = list(self.cashflow.keys())
        self.basis = {
            '30/360':0,
            'actual/actual':1,
            'actual/360':2,
            'actual/365':3
        }
    
    def discounted_cashflows(self, at, tir, freq=1, basis="30/360"):
        '''
        Devuelve to dos los flujos descontados a una tir a partir de una fecha at
        '''
        salida = {}
        for fecha in self.fechas:
            if at <= fecha:
                
                descuento = ((1+tir/freq)**( at.yearfrac(fecha, self.basis[self.day_count]) * freq ))
                salida[fecha] = self.cashflow[fecha]/descuento
        return salida

    def valores_futuros(self, since, val_to, tir, freq=1, basis="30/360"):
        '''
        Devuelve to dos los flujos capitalizados a una tir desde since hasta val_to
        el valor existe en t=val_to
        '''
        salida = {}
        for fecha in self.fechas:
            if since <= fecha and val_to >= fecha:
                capitalizo = ((1+tir/freq)**(fecha.yearfrac(val_to, self.basis[self.day_count])*freq))
                salida[fecha] = self.cashflow[fecha]*capitalizo
        return salida

    def precio(self, at, tir, freq=1, basis="30/360"):
        '''
        Devuelve el precio de un bono a una tir a partir de una fecha at'''
        return sum(self.discounted_cashflows(at, tir, freq, basis).values())

    def tir(self, at, price, freq=1, basis="30/360", primer=0.14, tol=0.0001, max_iterations=1000):
        """
        Calcula la TIR con Newton-Raphson, dado un precio
        """
        est = primer

        for _ in range(max_iterations):

            #  Saca el dirty con el estimado
            dirty_price = self.precio(at, est, freq, basis)

            #  Si es suficientente chico devuelve esa tir
            if abs(price - dirty_price) <= tol:
                return est

            #  Calcula el dirty a un diferencial
            dirty_price_higher = self.precio(at, est + tol, freq, basis)

            #  Con el diferencial saca la derivada
            derivative = (dirty_price_higher - dirty_price) / tol
            est = est - (dirty_price - price) / derivative

        raise ValueError("TIR no converge")

    def reinvertidos_descontados(self, since, at, tir, freq=1, basis="30/360"):
        '''
        reinvierte el cupon corrido y capitaliza el principal
        '''
        capitalizados = self.valores_futuros(since, at, tir, freq, basis)
        descontados = self.discounted_cashflows(at, tir, freq, basis)
        union = {**capitalizados, **descontados}
        return  sum(union.values())

    def dur(self, at, price, freq=1, basis="30/360"):
        tir = self.tir(at, price, freq, basis)
        salida = []
        for fecha in self.fechas:
            if at <= fecha:
                discounted = self.discounted_cashflows(at, tir, freq, basis)
                salida.append(discounted[fecha] * at.yearfrac(fecha, self.basis[self.day_count])/ price)
        return sum(salida)

    def mod_duration(self, at, price, freq=1, basis="30/360"):
        tir = self.tir(at, price, freq, basis)
        salida = []
        for fecha in self.fechas:
            if at <= fecha:
                discounted = self.discounted_cashflows(at, tir, freq, basis)
                salida.append((discounted[fecha] * at.yearfrac(fecha, self.basis[self.day_count])/ price)/(1+tir))
        return sum(salida)

    def Duration2(self, at, tir = 0.0, disc = None, cap = None, dtasa = 0.001):
        '''
        at  es la fecha en la que esta valuando el bono. 
        Lo que hago es chequear para varias fechas 
        '''
        fechas = [fecha for fecha in self.cashflow.keys() if fecha > at]
        desc = tir if disc is None else disc
        capi = tir if cap is None else cap

        # fech = []
        # freq = 2
        # for fecha in Fecha.schedule(at, list(self.cashflow.keys())[-1], 12):
        #     for i in range(20):
        #         fech.append(fecha.add2date(i, 0, 0))
        
        
        for fecha in [fecha for fecha in  Fecha.schedule(at, list(self.cashflow.keys())[-1], 12)]:
            capitalizados = self.valores_futuros(at, fecha, capi , freq, self.basis[self.day_count])
            descontados = self.discounted_cashflows(fecha, desc, freq, self.basis[self.day_count])
            valact = sum({**capitalizados, **descontados}.values())

            capitalizados_sube = self.valores_futuros(at, fecha, capi + dtasa, freq, self.basis[self.day_count])
            descontados_sube = self.discounted_cashflows(fecha, desc + dtasa, freq, self.basis[self.day_count])
            valact_sube = sum({**capitalizados_sube, **descontados_sube}.values())

            capitalizados_baja = self.valores_futuros(at, fecha, capi - dtasa, freq, self.basis[self.day_count])
            descontados_baja = self.discounted_cashflows(fecha, desc - dtasa, freq, self.basis[self.day_count])
            valact_baja = sum({**capitalizados_baja, **descontados_baja}.values())
            if abs(valact_sube - valact_baja) < 0.001:
                return at.yearfrac(fecha, self.basis[self.day_count])

################################################################################################
class Bonos(FixedIncome):
    def __init__(self, **kwargs):
        '''
        los rates y dates de amortizacion capitalizacion cupones se pueden ingresar
        de las dos maneras pero al final todo el codigo los interpreta a
        los dates como una lista y los rates como un diccionario de forma {date:rate}.
        para eso estan las funciones que formatean, abajo.
        '''
        self.ticker = kwargs['ticker']
        self.issue_date = kwargs['issue_date']
        self.maturity = kwargs['maturity']
        self.face_value = kwargs['face_value']
        self.day_count = kwargs['day_count']
        
        self.coupon_freq = kwargs['coupon_freq']  # frequencia de pago de cupones
        self.coupon_dates = kwargs['coupon_dates']  # fechas de pago de cupon
        self.coupon_rates = kwargs['coupon_rates']  # tasas de cupon
        
        self.amort_dates = kwargs['amort_dates']  # fechas de amortizacion
        self.amort_rates = kwargs['amort_rates']  # tasas de amortizacion

        self.currency = kwargs['currency']
        self.basis = {
            '30/360':0,
            'actual/actual':1,
            'actual/360':2,
            'actual/365':3
        }

        self.fechas = self.fechar()

        self.capitaliza = kwargs['capitaliza']  # Bool
        # fechas de capitalizacion
        self.cap_dates = kwargs['cap_dates'] if self.capitaliza else self.fechas
        # tasas de capitalizacion
        self.cap_rates = kwargs['cap_rates'] if self.capitaliza else {self.fechas[i]:0 for i in range(len(self.fechas))}
        self.cap_rates = self._capit_rates()

        self.all = self.main()

        self.devengados = {self.fechas[i]:self.all[0][i] for i in range(len(self.fechas))}
        self.percibidos = {self.fechas[i]:self.all[1][i] for i in range(len(self.fechas))}
        self.capitalizado = {self.fechas[i]:self.all[2][i] for i in range(len(self.fechas))}
        self.amortizado = {self.fechas[i]:self.all[3][i] for i in range(len(self.fechas))}
        self.residual = {self.fechas[i]:self.all[4][i] for i in range(len(self.fechas))}
        self.flujo = {self.fechas[i]:[i+j for i, j in zip(self.all[1], self.all[3])][i] for i in range(len(self.fechas))}

        super().__init__(self.flujo)

    #### FORMATO #################
    def _amort_rates(self):
        """ Le podes dar en el kwargs una lista o un diccionario
        con fechas de key y el porcentaje como value.

         - Si le das un diccionario simplemente cambia los fines de semana
         el dates puede ser None

         - Si le das un string "lineal", le tenes que dar una lista de fechas.
         Interpreta que cada una de las fechas amortiza un mismo porcentaje
         (1 / la cantidad de fechas)
        """
        salida = None
        #  Aca ya le das un diccionario con fechas y cuanto amortiza cada fecha
        if isinstance(self.amort_rates, dict):
            salida = {i if not i.isweekend() else i.nextweekday():j
                    for i, j in self.amort_rates.items()}
            self.amort_rates = salida
            self.amort_dates = list(salida.keys())

        #  Esto para que puedas darle un solo valor y lo divide entre todas las fechas
        elif self.amort_rates == "lineal":
            salida = {i if not i.isweekend() else i.nextweekday():1/len(self.amort_dates)
                    for i in self.amort_dates}
            self.amort_rates = salida
            self.amort_dates = list(salida.keys())

        return salida

    def _coup_rates(self):
        """ Le podes dar en el kwargs una lista o un diccionario
        con fechas de key y el porcentaje como value.

         - Si le das un diccionario simplemente cambia los fines de semana
         el dates puede ser None

         - Si le das un int interpreta que cada una de las fechas dadas en
         coupon_dates paga ese porcentaje
        """

        salida = None

        if isinstance(self.coupon_rates, dict):
            salida = {i if not i.isweekend() else i.nextweekday():j
                    for i, j in self.coupon_rates.items()}
            self.coupon_rates = salida
            self.coupon_dates = list(salida.keys())

        #  Esto para que puedas darle un solo valor y lo divide entre todas las fechas
        elif isinstance(self.coupon_rates, float):
            salida = {i if not i.isweekend() else i.nextweekday():(self.coupon_rates/self.coupon_freq)
                    for i in self.coupon_dates}
            self.coupon_rates = salida
            self.coupon_dates = list(salida.keys())

        return salida

    def _capit_rates(self):
        """ Le podes dar en el kwargs una lista o un diccionario
        con fechas de key y el porcentaje como value.

         - Si le das un diccionario simplemente cambia los fines de semana
         el dates puede ser None

         - Si le das un int interpreta que cada una de las fechas dadas en
         cap_dates capitaliza ese porcentaje
        """

        salida = None


        if isinstance(self.cap_rates, dict):
            salida = {i if not i.isweekend() else i.nextweekday():j
                    for i, j in self.cap_rates.items()}
            self.cap_rates = salida
            self.cap_dates = list(salida.keys())

        #  Esto para que puedas darle un solo valor y lo divide entre todas las fechas
        elif isinstance(self.cap_rates, float):
            salida = {i if not i.isweekend() else i.nextweekday():self.cap_rates
                    for i in self.cap_dates}
            self.cap_rates = salida
            self.cap_dates = list(salida.keys())

        return salida

    def fechar(self):
        '''
        lista con todas las fechas en las que pasa algo.
        esto activa el reformato cuando inicializa
        '''
        coupons = self._coup_rates()
        amorts =  self._amort_rates()
        combinado = Fecha.combinar(coupons.keys(), amorts.keys())
        return [i if not i.isweekend() else i.nextweekday() for i in combinado]

    #### MAIN #####################
    def main(self):
        '''
        aca se arma el calendario total del bono que queda como atributo despues
        '''
        amortizado = [0]*len(self.fechas)
        residual = [self.face_value for _ in range(len(self.fechas))]
        cap = [0]*len(self.fechas)
        iper = [0]*len(self.fechas)
        idev = [0]*len(self.fechas)

        amort_start = self.fechas.index(list(self.amort_rates.keys())[0])
        coupons =  self.coupon_rates


        for i, fecha in enumerate(self.fechas):

            if fecha in self.amort_dates:
                if isinstance(residual[amort_start-1], float):
                    amortizado[i] = residual[amort_start-1] * self.amort_rates[fecha]
                elif isinstance(residual[amort_start-1], list):
                    amortizado[i] = 0
                    total = sum([i for i in residual[amort_start-1]])
                    for val in residual[amort_start-1]:
                        amortizado[i] += residual[amort_start-1] * self.amort_rates[fecha]

            if fecha in self.coupon_dates:
                capital = self.cap_rates[fecha] if fecha in self.cap_dates else 0
                iper[i] = residual[i-1] * self.coupon_rates[fecha] * (1 - capital)
                idev[i] = residual[i-1] * self.coupon_rates[fecha]


            if fecha in self.cap_dates:
                cap[i] = idev[i] * self.cap_rates[fecha]

            residual[i] = residual[i-1] - amortizado[i] + cap[i]

        return idev, iper, cap, amortizado, residual

    #### CALENDARIO ##############
    def calendario(self):
        '''
        para hacer el print
        '''
        data = {
            'fechas': (self.fechas),
            'i-dev' : list(self.devengados.values()),
            'i-per' : list(self.percibidos.values()),
            'cap' : list(self.capitalizado.values()),
            'amort': list(self.amortizado.values()),
            'residual': list(self.residual.values()),
            'flujo' : list(self.flujo.values())
        }
        return data

    def calendario_print(self, just=10):
        cal = self.calendario()
        keys = []
        for i in cal.keys():
            keys.append(f"{i}")
        keys = [key.ljust(just) for key in keys]
        print(" | ".join(keys))

        complet = []
        for value in cal.values():
            complet.append(value)
        for i in range(len(complet[0])):
            values = []
            for j in range(len(complet)):
                if isinstance(complet[j][i], float):
                    values.append(f"{complet[j][i]:.4f}".ljust(just))
                else:
                    values.append(f"{complet[j][i]}".ljust(just))
            print(" | ".join(values))

    #### ANALISIS ################
    def cupon_corrido(self, at):
        i = Fecha.combinar(self.fechas, [at]).index(at)
        last_pmt_date = self.fechas[i-1] if i-1 > 0 else at
        next_pmt_date = self.fechas[i]
        next_pmt = self.devengados[next_pmt_date]
        return next_pmt * last_pmt_date.yearfrac(at, self.basis[self.day_count]) * self.coupon_freq

    def clean(self, at:Fecha, tir):
        return super().precio(at, tir, self.coupon_freq, self.day_count)

    def dirty(self, at:Fecha, tir):
        return self.clean(at, tir) + self.cupon_corrido(at)

    def duration(self, at, price, clean=False):
        # if clean:
        #     price = price + self.cupon_corrido(at)
        # tir = super().tir(at, price, self.coupon_freq, self.day_count)
        # salida = []
        # for fecha in self.fechas:
        #     if at <= fecha:
        #         discounted = super().discounted_cashflows(at, tir, self.coupon_freq, self.day_count)
        #         salida.append(discounted[fecha] * at.yearfrac(fecha, self.basis[self.day_count])/ price)
        # return sum(salida)
        return super().dur(at, price, self.coupon_freq, self.day_count)

    def duration_mod(self, at, price, clean=False):
        # if clean:
        #     price = price + self.cupon_corrido(at)
        # tir = super().tir(at, price, self.coupon_freq, self.day_count)
        # salida = []
        # for fecha in self.fechas:
        #     if at <= fecha:
        #         discounted = super().discounted_cashflows(at, tir, self.coupon_freq, self.day_count)
        #         salida.append((discounted[fecha] * at.yearfrac(fecha, self.basis[self.day_count])/ price)/(1+tir))
        return super().mod_duration(at, price, self.coupon_freq, self.day_count)

    def current_yield(self, at, price, clean=False, until=(0,0,1)):
        '''
        Devuelve el current yield hasta la fecha until, por default un año'''
        if clean:
            price = price + self.cupon_corrido(at)
        until = at.add2date(until[0], until[1], until[2])
        next_index = Fecha.combinar(self.fechas, [at]).index(at)
        last_index = Fecha.combinar(self.fechas, [until]).index(until)

        next_coupon_payments = self.main()[0][next_index:last_index]
        current_yield = sum(next_coupon_payments) / price

        return current_yield

    def capital_gains(self, at, price, clean=False, until=(0,0,1)):
        '''
        Devuelve el capital gains hasta la fecha until, por default un año'''
        if clean:
            price = price + self.cupon_corrido(at)

        tir = super().tir(at, price, self.coupon_freq, self.day_count)

        new_at = at.add2date(until[0], until[1], until[2])

        f = self.dirty(new_at, tir)
        capital_gains = (f - price) / price
        return capital_gains

    def info(self, at, **informacion):
        '''
        Devuelve un diccionario con tir, precios, duration, current yield y capital gains
        Se le puede dar informacion de clean, dirty o tir, cualquiera de las tres
        informacion = 
            {
            'clean': precio limpio
            'dirty': precio sucio
            'tir': tasa interna de retorno
            'until': fecha hasta la que se calcula el current yield o capital gains
            }
        
        '''
        accrued = self.cupon_corrido(at)

        if informacion.get('clean') is not None:
            dirty = informacion['clean'] + accrued
            clean = informacion['clean']
            tir = super().tir(at, dirty, self.coupon_freq, self.day_count)

        if informacion.get('dirty') is not None:
            dirty = informacion['dirty']
            clean = informacion['dirty'] - accrued
            tir = super().tir(at, dirty, self.coupon_freq, self.day_count)

        if informacion.get('tir') is not None:
            dirty = self.dirty(at, informacion['tir'])
            clean = dirty - accrued
            tir = informacion['tir']

        duration = self.duration(at, dirty)
        current_yield = self.current_yield(at, dirty, informacion['until']
                                           if informacion.get('until') is not None else (0,0,1) )
        capital_gains = self.capital_gains(at, dirty, informacion['until']
                                           if informacion.get('until') is not None else (0,0,1) )
        duration_mod = self.duration_mod(at, dirty)

        return {
            'ticker' : self.ticker,
            'maturity' : self.maturity,
            'precio dirty' : dirty,
            'precio clean' : clean,
            'accrued' : accrued,
            'tir' : tir,
            'current_yield': current_yield,
            'capital_gains' : capital_gains,
            'duration' : duration,
            'duration_modificada' : duration_mod
            
        }

########################################################################################################################################################
class BonoDatabase(Bonos):
  def __init__(self, **db):
    '''
    db: diccionario con la informacion de los bonos a agregar a la base de datos'''
    self.database = {ticker:data for ticker, data in db.items()}

  def add(self, *nuevos):
    '''
    nuevos: lista con la informacion de los bonos a agregar a la base de datos'''
    for bono in nuevos:
      self.database[bono['ticker']] = bono

########################################################################################################################################################
class Portfolio(FixedIncome):
    def __init__(self, database, **portbonos):
        '''
        database: base de datos de bonos
        portbonos: diccionario con las cantidades de valores nominales de cada bono'''

        #  guarda la base de datos con bonos
        self.database = database

        #  guarda los nominales de cada bono
        self.laminas = {ticker:n for ticker, n in portbonos.items()}

        #  guarda cada bono como objeto de clase Bonos
        self.objetos_simple = {ticker:Bonos(**d) for ticker, d in self.database.database.items()}
       
        #  crea otra base de datos con las cantidades verdaderas
        self.db_nominales = {ticker:d['face_value']*self.laminas[ticker] for ticker, d in self.database.database.items()}
        for ticker, d in self.database.database.items():
            d['face_value'] = self.db_nominales[ticker]
        self.objetos = {ticker:Bonos(**d) for ticker, d in self.database.database.items()}
       
        #  guarda los pesos de cada bono en la cartera 
        self.weights = {ticker:(n/sum(portbonos.values())) for ticker, n in portbonos.items()}
        super().__init__(self.cf())

    def dates(self):
        '''
        Calcula las fechas de pago del portafolio como la union de las fechas de pago de cada bono'''
        fech = []
        for bono in self.objetos.values():
            fech.append(bono.fechas)
        return Fecha.combinar(*fech)

    def cf(self):
        '''
        Calcula el flujo de caja del portafolio como la suma de los flujos de cada bono'''
        cashflows = {}
        for fecha in self.dates():
            cashflows[fecha] = 0
        for bono in self.objetos.values():
            bond_cashflows = bono.flujo
            for date, cashflow in bond_cashflows.items():
                cashflows[date] += cashflow
        return cashflows

    def portfolio_duration(self, at, **prices):
        '''
        Calcula la duration del portafolio como un weighted average the cada duration'''
        return sum([self.weights[ticker]*bono.duration(at, prices[ticker]) for ticker, bono in self.objetos_simple.items()])
    
    def portfolio_duration_mod(self, at, **prices):
        '''
        Calcula la duration modificada del portafolio como un weighted average the cada duration'''
        return sum([self.weights[ticker]*bono.duration_mod(at, prices[ticker]) for ticker, bono in self.objetos_simple.items()])
    
    def portfolio_price(self, at, **prices):
        '''
        Calcula el precio del portafolio como un weighted average the cada precio'''
        return sum([n*prices[ticker] for ticker, n in self.laminas.items()])

    def portfolio_tir(self, at, **prices):
        '''
        Calcula la tir del portafolio a partir del cashflow generado en cf()'''
        return super().tir(at, self.portfolio_price(at, **prices))

    def imunizar_dos(self, at, objetivo, tol=0.01, **prices):
        assert len(self.objetos) == 2
        '''
        Busca los weights entre los dos portfolios dados que logra una duration objetivo
        '''

        initial_weights = [i for i in self.weights.values()]
        main_weight = new_weight = initial_weights[0]
        initial_duration = duration = self.portfolio_duration(at, **prices)
        bonoA = list(self.objetos_simple.values())[0]
        bonoB = list(self.objetos_simple.values())[1]
        priceA = prices[list(self.objetos_simple.keys())[0]]
        priceB = prices[list(self.objetos_simple.keys())[1]]
        dif_entre = abs(bonoA.duration(at, priceA) - bonoB.duration(at, priceB))
        for _ in range(1000):
            if abs(duration - objetivo) < tol:
                return f"deberia distribuir en {list(self.laminas.keys())[0]}, la cantidad: {new_weight * sum(self.laminas.values())} y en {list(self.laminas.keys())[1]}, la cantidad: {(1-new_weight) * sum(self.laminas.values())}"
            else:
                if objetivo > duration:
                    new_weight -= dif_entre/1000
                else:
                    new_weight += dif_entre/1000
                new_weight = max(0, min(new_weight, 1))
                # print("TEST new weight", new_weight)
                duration = new_weight * bonoA.duration(at, priceA) + (1 - new_weight) * bonoB.duration(at, priceB)

                # print("TEST duration", duration, objetivo)
 
########################################################################################################################################################
# EJERCICO 1

def ejercicio1(x, m, freq=2, precio_objetivo=100, vn=100, n_amorts=3, 
                tir_objetivo=0.075, duration_objetivo=6, bono_start=Fecha("9/8/2023"), tol=0.01, max_iter=100):
    '''
    
    '''
    cupones = Fecha.schedule(bono_start, m, freq)
    rates = {}
    rates[cupones[0]] = x/freq
    rates[cupones[1]] = x/freq
    rates[cupones[2]] = (x + 0.01)/freq
    rates[cupones[3]] = (x + 0.01)/freq
    rates[cupones[4]] = (x + 0.02)/freq
    rates[cupones[5]] = (x + 0.02)/freq
    for fecha in cupones[5:]:
        rates[fecha] = (x + 0.03)/freq

    bono_inicial = Bonos(**{
        'ticker' : "UDESA_1",
        'issue_date' : bono_start,
        'maturity' : m,
        
        'coupon_rates' : rates,
        'coupon_dates' : cupones,
        'coupon_freq' : freq,

        'irregular_first_coupon' : False,

        'amort_dates' : Fecha.schedule(m.add2date(0, 0, -1), m, freq),
        'amort_rates' : "lineal",

        'face_value' : vn,
        'day_count' : "30/360",  # asumo
        'settlement_plus' : 0,
        'currency' : "USD",

        'capitaliza' : False,

    }
    )

    precio = bono_inicial.clean(bono_start, tir_objetivo)
    duration = bono_inicial.duration(bono_start, precio)


    if abs(duration - duration_objetivo) > 0.01:
        if duration < duration_objetivo:
            return ejercicio1(x,  m.add2date(0,6,0))
        
    dif = abs(precio - precio_objetivo)
    if abs(precio - precio_objetivo) > 0.01:
        if precio < precio_objetivo:
            return ejercicio1(x + dif/1000, m)
        if precio > precio_objetivo:
            return ejercicio1(x - dif/1000, m)
    else:
        print(bono_inicial.calendario_print())
        return bono_inicial.info(bono_start, tir=tir_objetivo)
    

for key, val in ejercicio1(0.0, Fecha("9/8/2026")).items():
    print("ej1: ", key, val)

## LA DURATION DA BASTANTE LEJOS, PORQUE PRIMERO ENCUENTRO UNA MATURITY QUE CON X = 0% ME DE MAS O MENOS
## ESA DURATION Y RECIEN DESPUES LO PONGO A EDITAR LOS CUPONES CON X. NO ES IDEAL

##################################################################################################################
# # EJERCICO 2

# '''
# (1) Del 31-dic-03 (inclusive) al 31-dic-08 (exclusive): 3,97% pago en efvo., 4,31% capitaliza
# (2) Del 31-dic-08 (inclusive) al 31-dic-13 (exclusive): 5,77% pago en efvo., 2,51% capitaliza
# (3) Del 31-dic-13 (inclusive) al 31-dic-33 (exclusive): 8,28% pago en efvo.
# '''
# freq = 2
# issue = Fecha("31/12/2003")
# mat = Fecha("31/12/2033")
# amort_start = Fecha("30-jun-2024")
# tir = 0.3
# cupones = {}
# for fecha in Fecha.schedule(Fecha("31-dic-2003"),Fecha("30-jun-2008"),2 ):
#     cupones[fecha] = 0.0397/2

# for fecha in Fecha.schedule(Fecha("31-dic-2008"),Fecha("30-jun-2013"),2 ):
#     cupones[fecha] = 0.0577/2

# for fecha in Fecha.schedule(Fecha("31-dic-2013"),Fecha("30-jun-2033"),2 ):
#     cupones[fecha] = 0.0828/2


# capitalizaciones = {}
# for fecha in Fecha.schedule(Fecha("31-dic-2003"),Fecha("30-jun-2008"),2 ):
#     capitalizaciones[fecha] = 0.0431/2

# for fecha in Fecha.schedule(Fecha("31-dic-2008"),Fecha("30-jun-2013"),2 ):
#     capitalizaciones[fecha] = 0.0251/2


# today = Fecha("22/6/2023")


# DICA = Bonos(**{
#     'ticker' : "DICA",
#     'issue_date' : Fecha("31/12/2003"),
#     'maturity' : mat,
    
#     'coupon_rates' : cupones,
#     'coupon_dates' : None,
#     'coupon_freq' : freq,

#     'irregular_first_coupon' : False,

#     'amort_dates' : Fecha.schedule(amort_start, Fecha("30/12/2033"), freq),
#     'amort_rates' : "lineal",

#     'face_value' : 100,
#     'day_count' : "30/360",  # asumo
#     'settlement_plus' : 0,
#     'currency' : "USD",

#     'capitaliza' : True,
#     'cap_rates' : capitalizaciones,
#     'cap_dates' : capitalizaciones.keys()

# }
# )

# for key, val in DICA.info(today, tir=tir).items():
#     print("DICA", key, val)
# print("reinvertir y capitalizar a la tir", DICA.Duration2(today, tir=tir))
# print("reinversion a 0.18", DICA.Duration2(today, cap=0.18, tir=tir))

##################################################################################################################
'''
i. Del 15 de Mayo de 2020 (inclusive) al 15 de Noviembre de 2022 (exclusive): CERO POR CIENTO (0%).

ii. Del 15 de Noviembre de 2022 (inclusive) al 15 de Noviembre de 2025 (exclusive):
CERO COMA CINCUENTA POR CIENTO (0,50%).
ii.
Del 15 de Noviembre de 2025 (inclusive) al 15 de Noviembre de 2027 (exclusive):
UNO POR CIENTO (1,00%).
iv.
Del 15 de Noviembre de 2027 (inclusive) al 15 de Noviembre de 2030 (exclusive):
UNO COMA SETENTA Y CINCO POR CIENTO (1,75%).
'''
freq = 2
issue = Fecha("15/05/2020")
mat = Fecha("15/11/2030")

cupones = {}
for fecha in Fecha.schedule(Fecha("15/05/2020"),Fecha("15/05/2022"),2 ):
    cupones[fecha] = 0

for fecha in Fecha.schedule(Fecha("15/11/2022"),Fecha("15-05-2025"),2 ):
    cupones[fecha] = 0.005/2

for fecha in Fecha.schedule(Fecha("15/11/2025"),Fecha("15-05-2027"),2 ):
    cupones[fecha] = 0.01/2

for fecha in Fecha.schedule(Fecha("15-11-2027"),Fecha("15-05-2030"),2 ):
    cupones[fecha] = 0.0175/2




today = Fecha("06/11/2023")


GD30 = Bonos(**{
    'ticker' : "GD30",
    'issue_date' : issue,
    'maturity' : mat,
    
    'coupon_rates' : cupones,
    'coupon_dates' : None,
    'coupon_freq' : freq,

    'irregular_first_coupon' : False,

    'amort_dates' : [Fecha('15-11-2026'), Fecha('15-11-2027'), Fecha('15-11-2028'), Fecha('15-11-2029'), Fecha('15-11-2030')],
    'amort_rates' : "lineal",

    'face_value' : 100000,
    'day_count' : "30/360", 
    'settlement_plus' : 0,
    'currency' : "ARS",

    'capitaliza' : False,
    'cap_rates' : None,
    'cap_dates' : None

}
)

tir = 0.5
precio = 25650
for key, val in GD30.info(today, tir=tir).items():
    print("GD30", key, val)

GD30.calendario_print()