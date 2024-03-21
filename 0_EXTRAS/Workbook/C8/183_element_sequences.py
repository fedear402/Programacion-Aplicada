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
###Diccionario de primera letra con lista de elementos que empiezan con esa letra
# first_letters_index = {}
# for i in elements:
#     if i[0] not in first_letters_index:
#         first_letters_index[i[0]] = []
#     first_letters_index[i[0]].append(i)

# length_of_letters_index = {}
# for j in first_letters_index:
#     if j not in length_of_letters_index:
#         length_of_letters_index[j] = len(first_letters_index[j])
# ###
# # possible_paths = []
# # def paths(b):
# #     for m[-1] in first_letters_index[b]:
        

# ###funcion que busca por la ultima letra del input entre el dicc de primeras letras
# sequence = []
# def element_sequence(a):
#     while True:
#         sequence.append(a)
#         first_letters_index[a[0]].remove(a)
#         if a in elements:
#             if a[-1] in first_letters_index and first_letters_index[a[-1]] != []:
#                 a = first_letters_index[a[-1]][-1]
#             else:
#                 break
# element_sequence("magnesium")
# print(sequence)


# def predecesores(a):
#     predecesores = []
#     for element in elements:
#         if a[0] == element[-1]:
#             predecesores.append(element)
#     return predecesores

def sucesores(a, b):
    sucesores = []
    for element in b:
        if a[-1] == element[0]:
            sucesores.append(element)
    return sucesores
paths = [[]]
def pather(a):
    for i in sucesores(a, elements):
        new_elements = elements[:]
        if sucesores(i, new_elements) != []:
            paths[-1].append(i)
            new_elements.remove(a)
            pather(i)
        else:
            paths[-1].append(i)
            paths.append([])
            continue
    return paths
            
print(pather("magnesium"))