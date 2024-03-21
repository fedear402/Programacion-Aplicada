numerals = {1000: "M" , 500 : "D" , 100 : "C" , 50 : "L", 10 : "X" , 9 : "IX" , 
                8 : "VIII" , 7 : "VII" , 6 : "VI" , 5 : "V" , 4 : "IV" , 3 : "III" , 2 : "II", 1 : "I"}
def roman_numerals(a):
    if a in numerals:
        return numerals[a]
    else:
        numeral = ""
        for i in numerals:
            if a // i < 1:
                numeral += i
        return numeral

print(roman_numerals(51))