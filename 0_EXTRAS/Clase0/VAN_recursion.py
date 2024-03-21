# def van(flujos: list, tir: float):
#     flujos_van = flujos[1:]
#     flujos_van[0] 
#     flujos_van.pop(0)

def npv(cashflows, irr, period):
    current_cashflow = cashflows[0]
    discounted_cashflow = current_cashflow / ((1 + irr) ** period)
    return discounted_cashflow + npv(cashflows[1:], irr, period + 1)

print(npv([22, 2312, 123123, 12312, 12312, 123], 0.062, 0))