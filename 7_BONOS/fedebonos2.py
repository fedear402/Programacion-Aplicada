from fedebonos_copy import Fecha
from fedebonos_copy import Bonos


##################################################################################################
# issue = Fecha("22/01/2021")
# mat = Fecha("22/07/2032")
# freq = 1
# calendar = Fecha.schedule(issue, mat, freq)

# first = Fecha("22/01/2023")
# amort_start = Fecha("22/enero/2026")
# cupdates=Fecha.schedule(first, mat, freq)
# caps = Fecha.schedule(issue, amort_start.add2date(0,0,-1), freq)
# amorts = Fecha.schedule(amort_start, mat, freq)

# bonodataYPF1 = {
#     'ticker' : "YPF",
#     'issue_date' : issue,
#     'maturity' : mat,

#     'coupon_rates' : [0.0575]*len(cupdates),
#     'coupon_dates' : cupdates,
#     'coupon_freq' : freq,
#     'irregular_first_coupon' : False,

#     'amort_dates' : amorts,
#     'amort_perc' : [1/len(amorts)] * len(amorts),

#     'face_value' : 100,
#     'day_count' : "actual/365",
#     'settlement_plus' : 2,
#     'currency' : "USD",

#     'capitaliza' : False,
#     'cap_dates' : caps,
#     'cap_rates' : [0.0]*len(caps)

#     }
# today = Fecha("30/5/2023")
# # ypf = Bonos(**bonodataYPF1)
# # print(ypf.calendario_full_print())
# # print(ypf.info(today, dirty=106))


# # #############################################################################    
# issue = Fecha("23/01/2021")

# first = Fecha("23/01/2022")

# amort_start = Fecha("23/01/2029")

# mat = Fecha("23/07/2032")

# freq = 2
# calendar = Fecha.schedule(issue, mat, freq)

# cupdates=Fecha.schedule(first, mat, freq)
# caps = Fecha.schedule(issue, amort_start.add2date(0,0,-1), freq)
# amorts = Fecha.schedule(amort_start, mat, freq)

# bonodataYPF2 = {
#     'ticker' : "YPF2",
#     'issue_date' : issue,
#     'maturity' : mat,
#     'coupon_rates' : [0.0575]*len(cupdates),
#     'coupon_dates' : cupdates,
#     'coupon_freq' : freq,
#     'irregular_first_coupon' : False,
#     'amort_dates' : amorts,
#     'amort_perc' : [1/len(amorts)] * len(amorts),
#     'face_value' : 100,
#     'day_count' : "actual/365",
#     'settlement_plus' : 2,
#     'currency' : "USD",
#     'capitaliza' : False,
#     'cap_dates' : caps,
#     'cap_rates' : [0.0]*len(caps)

#     }
# ypf2 = Bonos(**bonodataYPF2)
# # print(ypf2.calendario_full_print())
# # print(ypf2.info(today, dirty=104))


# #############################################################################
# issueb1 = Fecha("1/1/2020")
# maturityb1 = Fecha("1/1/2030")
# freqb1 = 1
# cupondatesb1 = Fecha.schedule(Fecha("1/1/2021"), maturityb1, freqb1)

# bono1 = Bonos(**{
#     'ticker' : "BONO1",
#     'issue_date' : issueb1,
#     'maturity' : issueb1,
#     'coupon_rates' : [0.067]*len(cupondatesb1),
#     'coupon_dates' : cupondatesb1,
#     'coupon_freq' : freqb1,
#     'irregular_first_coupon' : False,
#     'amort_dates' : [maturityb1],
#     'amort_perc' : [1],
#     'face_value' : 1000,
#     'day_count' : "30/360",
#     'settlement_plus' : 2,
#     'currency' : "USD",
#     'capitaliza' : False,
#     'cap_dates' : caps,
#     'cap_rates' : [0.0]*len(caps)        
# })
# print(bono1.calendario_full_print())
# print("TIR", bono1.tir(issueb1,  881.7349781, estimado_inicial=0.1))
# print("VAN", bono1.van(issueb1, 881.734978112087, 0.1))
# print(bono1.info(issueb1, tir= 0.08495082 ))


# issueb2 = Fecha("1/1/2020")
# maturityb2 = Fecha("1/1/2030")
# freqb2 = 2
# cupondatesb2 = Fecha.schedule(issueb2, maturityb2, freqb2)

# bono2 = Bonos(**{
#     'ticker' : "BONO1",
#     'issue_date' : issueb2,
#     'maturity' : issueb2,
#     'coupon_rates' : [0.15]*len(cupondatesb2),
#     'coupon_dates' : cupondatesb2,
#     'coupon_freq' : freqb2,
#     'irregular_first_coupon' : False,
#     'amort_dates' : [maturityb2],
#     'amort_perc' : [1],
#     'face_value' : 1000,
#     'day_count' : "30/360",
#     'settlement_plus' : 2,
#     'currency' : "USD",
#     'capitaliza' : False,
#     'cap_dates' : caps,
#     'cap_rates' : [0.0]*len(caps)        
# })

# BondsDatabase=({
#     'ypf1': bono1,
#     'ypf2': bono2
# })
# laminas = {
#     'ypf1': 500,
#     'ypf2': 300
# }

##########################################################################################
cupones = {}
cupones[Fecha("9 enero 2020")] = 0.0125/2
cupones[Fecha("9 julio 2020")] = 0.0125/2
cupones[Fecha("9 enero 2021")] = 0.0125/2
cupones[Fecha("9 julio 2021")] = 0.02/2
cupones[Fecha("9 enero 2022")] = 0.02/2
cupones[Fecha("9 julio 2022")] = 0.03875/2
cupones[Fecha("9 enero 2023")] = 0.03875/2
cupones[Fecha("9 julio 2023")] = 0.0425/2
cupones[Fecha("9 enero 2024")] = 0.0425/2
tanda_final = Fecha.schedule(Fecha("9 julio 2024"), Fecha("9/1/2038"), 2)
for i in range(len(tanda_final)):
    cupones[tanda_final[i]] = 0.025

issue = Fecha("4/9/2020")
first = Fecha("9/1/2020")
amort_start = Fecha("09/7/2027")
mat = Fecha("9/1/2038")
freq = 2

bonodataAE38 = {
    'ticker' : "AE38",
    'issue_date' : issue,
    'maturity' : mat,
    
    'coupon_rates' : cupones,
    'coupon_dates' : None,
    'coupon_freq' : freq,

    'irregular_first_coupon' : False,

    'amort_dates' : Fecha.schedule(amort_start, mat, 2),
    'amort_rates' : "lineal",

    'face_value' : 100,
    'day_count' : "30/360",
    'settlement_plus' : 2,
    'currency' : "USD",

    'capitaliza' : False,


    }
today = Fecha("14-06-2023")
AE38 = Bonos(**bonodataAE38)
tir = 0.13676166481326904
corr = AE38.cupon_corrido(today)
clean = 59.9677159-corr


print(AE38.calendario_full_print())
print("dirty", AE38.dirty(today, tir))
print("tir", AE38.tir(today, 59.9677159)) 
print("corrido", corr)
print("current yield", AE38.current_yield(today, 59.9677159))
print("capital gains", AE38.capital_gains(today, 59.9677159))
print("duration", AE38.duration(today, 59.9677159))
print("mod duration", AE38.duration_mod(today, 59.9677159))
print()
for key, value in AE38.info(today, dirty=59.9677159).items():
    print(key,value)
##########################################################################################
amorts={}
for fecha in Fecha.schedule(Fecha("8/9/2022"), Fecha("8/9/2024"), 2):
    amorts[fecha] = 0.133
amorts[Fecha("8/3/2025")] = 0.335

first = Fecha("8/3/2022")
mat = Fecha("8/3/2025")

freq = 2

bonodataCP170 = {
    'ticker' : "CP170",
    'issue_date' : None,
    'maturity' : mat,
    
    'coupon_rates' : 0.095,
    'coupon_dates' : Fecha.schedule(first, mat, 2),
    'coupon_freq' : freq,

    'irregular_first_coupon' : False,

    'amort_dates' : None,
    'amort_rates' : amorts,

    'face_value' : 100,
    'day_count' : "30/360",
    'settlement_plus' : 2,
    'currency' : "USD",

    'capitaliza' : False,


    }
today = Fecha("14-06-2023")
CP170 = Bonos(**bonodataCP170)
tir = 0.13676166481326904
corr = CP170.cupon_corrido(today)
dirty = 38000/495.73
clean = dirty-corr

for key, value in CP170.info(today, dirty=dirty).items():
    print(key,value)


main_database = BonoDatabase()
main_database.add(bonodataCP170, bonodataAE38)
main_database.database