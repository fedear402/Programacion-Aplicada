import sys
import importlib
path = "/Users/fedelopez/Library/CloudStorage/OneDrive-Personal/Documents/UDESA/05_Cuatrimestre/Prog_Aplicada/CODIGO/7_BONOS"
if not(path in sys.path):
    sys.path.append(path)

pathpol = "/Users/fedelopez/Library/CloudStorage/OneDrive-Personal/Documents/UDESA/05_Cuatrimestre/Prog_Aplicada/CODIGO/5_POLY"
if not(pathpol in sys.path):
    sys.path.append(pathpol)

from fechasoop import Fecha
ply = importlib.import_module(name="PolynomialC")


class Bonos():
    def __init__(self, **kwargs):
        """
        ticker (str): 
            el nombre del bono
        issue_date (str o datetime): 
            fecha de emisión del bono
        maturity (str o datetime): 
            fecha de vencimiento del bono
        coupon_rates (list of float): 
            las tasas de cupón del bono
        coupon_dates (list of str o datetime): 
            las fechas de pago del cupón
        coupon_freq (int): 
            la frecuencia de los pagos de cupón (anual, semestral, etc.)
        irregular_first_coupon (bool): 
            si el primer cupón tiene un pago inusual
        irregular_first_coupon_type (str): <- LFC, LFCRV, SFC, SFCRV
            si es cierto lo anterior, este define de qué manera es inusual
        amort_perc (list of float): 
            los porcentajes de amortización del bono
        amort_dates (list of str o datetime): 
            las fechas de amortización del bono
        face_value (float): 
            el valor nominal o valor a la par del bono
        day_count (str): 
            el sistema de conteo de días utilizado para calcular el interés
        settlement_plus (int): 
            el número de días después de la fecha de emisión en que el bono se liquida
        currency (str): 
            la moneda en la que se emite el bono
        """

        self.ticker = kwargs['ticker']
        self.issue_date = kwargs['issue_date']
        self.maturity = kwargs['maturity']
        self.coupon_rates = kwargs['coupon_rates']
        self.coupon_dates = kwargs['coupon_dates']
        self.coupon_freq = kwargs['coupon_freq']
        self.irregular_first_coupon = kwargs['irregular_first_coupon']
        self.irregular_first_coupon_type = kwargs['irregular_first_coupon_type'] if self.irregular_first_coupon else None
        self.amort_perc = kwargs['amort_perc']
        self.amort_dates = kwargs['amort_dates']
        self.face_value = kwargs['face_value']
        self.day_count = kwargs['day_count']
        self.settlement_plus = kwargs['settlement_plus']
        self.currency = kwargs['currency']

    def amort(self):
        amort = {}
        for i in range(len(self.coupon_dates)):
            if self.coupon_dates[i] == self.amort_dates[0]:
                for j in range(len(self.amort_dates)):
                    amort[self.amort_dates[j]] = self.face_value * self.amort_perc[j]
                break
            else:
                amort[self.coupon_dates[i]] = 0
        return amort

    def residual(self):
        residual = {}
        queda = self.face_value
        for i in range(len(self.coupon_dates)):
            if self.coupon_dates[i] == self.amort_dates[0]:
                for j in range(len(self.amort_dates)):
                    residual[self.amort_dates[j]] = queda - (self.face_value * self.amort_perc[j])
                    queda -= (self.face_value * self.amort_perc[j])
                break
            else:
                residual[self.coupon_dates[i]] = queda
        return residual
    
    def calendario(self):
        calendario = {}
        for i in range(len(self.coupon_dates)):
            calendario[self.coupon_dates[i]] = self.coupon_rates[i] * list(self.residual().values())[i] + list(self.amort().values())[i]
        return calendario




if __name__ == "__main__":
    start = Fecha("06/09/2001")
    first = Fecha("22 - enero - 2022")
    end = Fecha("22/07/2032")
    amort_start = Fecha("22  . enero . 2026")
    bonodata = {
        'ticker' : "YPF",
        'issue_date' : start,
        'maturity' : end,
        'coupon_rates' : [5.75]*len(Fecha.schedule(first, end, 2)),
        'coupon_dates' : Fecha.schedule(first, end, 2),
        'coupon_freq' : 2,
        'irregular_first_coupon' : False,
        'amort_dates' : Fecha.schedule(amort_start, end, 2),
        'amort_perc' : [1/14] * len(Fecha.schedule(amort_start, end, 2)),
        'face_value' : 100,
        'day_count' : "actual/360",
        'settlement_plus' : 2,
        'currency' : "USD"

        }
    ypf = Bonos(**bonodata)
    print(ypf.calendario())
