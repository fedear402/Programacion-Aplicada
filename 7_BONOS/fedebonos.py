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
        self.ticker = kwargs['ticker']
        self.issue_date = kwargs['issue_date']
        self.maturity = kwargs['maturity']
        self.coupon_rates = kwargs['coupon_rates']
        self.coupon_dates = kwargs['coupon_dates']
        self.coupon_freq = kwargs['coupon_freq']
        self.irregular_first_coupon = kwargs['irregular_first_coupon']
        self.irregular_first_coupon_type = kwargs['irregular_first_coupon_type']
        self.amort_perc = kwargs['amort_perc']
        self.amort_dates = kwargs['amort_dates']
        self.face_value = kwargs['face_value']
        self.day_count = kwargs['day_count']
        self.settlement_plus = kwargs['settlement_plus']
        self.currency = kwargs['currency']

    def CF(self):
        

if __name__ == "__main__":
    print(Fecha("2/2/2023").fecha)
    print(Fecha("2/2/2023").fecha)

