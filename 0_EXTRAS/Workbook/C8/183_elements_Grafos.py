elements = [ "hydrogen",
        "helium",
        "lithium",
        "beryllium",
        "boron",
        "carbon",
        "nitrogen",
        "oxygen",
        "fluorine",
        "neon",
        "sodium",
        "magnesium",
        "aluminium",
        "silicon",
        "phosphorus",
        "sulfur",
        "chlorine",
        "argon",
        "potassium",
        "calcium",
        "scandium",
        "titanium",
        "vanadium",
        "chromium",
        "manganese",
        "iron",
        "cobalt",
        "nickel",
        "copper",
        "zinc",
        "gallium",
        "germanium",
        "arsenic",
        "selenium",
        "bromine",
        "krypton",
        "rubidium",
        "strontium",
        "yttrium",
        "zirconium",
        "niobium",
        "molybdenum",
        "technetium",
        "ruthenium",
        "rhodium",
        "palladium",
        "silver",
        "cadmium",
        "indium",
        "tin",
        "antimony",
        "tellurium",
        "iodine",
        "xenon",
        "cesium",
        "barium",
        "lanthanum",
        "cerium",
        "praseodymium",
        "neodymium",
        "promethium",
        "samarium",
        "europium",
        "gadolinium",
        "terbium",
        "dysprosium",
        "holmium",
        "erbium",
        "thulium",
        "ytterbium",
        "lutetium",
        "hafnium",
        "tantalum",
        "tungsten",
        "rhenium",
        "osmium",
        "iridium",
        "platinum",
        "gold",
        "mercury",
        "thallium",
        "lead",
        "bismuth",
        "polonium",
        "astatine",
        "radon",
        "francium",
        "radium",
        "actinium",
        "thorium",
        "protactinium",
        "uranium",
        "neptunium",
        "plutonium",
        "americium",
        "curium",
        "berkelium",
        "californium",
        "einsteinium",
        "fermium",
        "mendelevium",
        "nobelium",
        "lawrencium",
        "rutherfordium",
        "dubnium",
        "seaborgium",
        "bohrium",
        "hassium",
        "meitnerium",
        "darmstadtium",
        "roentgenium",
        "copernicium",
        "nihonium",
        "flerovium",
        "moscovium",
        "livermorium",
        "tennessine",
        "oganesson",
        "ununennium"
    ]

def predecesores(a):
    predecesores = []
    for element in elements:
        if a[0] == element[-1]:
            predecesores.append(element)
    return predecesores

def sucesores(a):
    sucesores = []
    for element in elements:
        if a[-1] == element[0]:
            sucesores.append(element)
    return sucesores

####lista de diccionarios de adyacentes
la_matrix = []
for i in elements:
    la_matrix.append({})
    la_matrix[-1][i] = sucesores(i)
print(la_matrix)

####dado un nodo, genera una lista de adyacencia como 0, 1
def rower(a: dict):
    matrix_row = []
    for j in elements:
        if j in a[list(a.keys())[0]]:
            matrix_row.append(1)
        else:
           matrix_row.append(0)
    return matrix_row

####Agrega las filas a una matriz
matrix_adyacentes = []
for i in la_matrix:
    matrix_adyacentes.append(rower(i))

print(matrix_adyacentes)

#################################
    