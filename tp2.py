# TP2 Correction d'erreurs avec le code de Hamming (7,4) et (8,4)

#################################################
# Partie 1 - Codage de Hamming (7,4)
#################################################
print(
        '''
#################################################
# Partie 1 - Codage de Hamming (7,4)
#################################################
'''
)
# 4 bits info, auquels sont ajoutés 3 bits de parité pour former un mot codé de 7 bits.

data = "1011" # d3,d2,d1,d0

def build_code(msg:str)->tuple:
    if len(msg) != 4:
        raise ValueError("Le message doit être de 4 bits")

    d1 = int(msg[0])
    d2 = int(msg[1])
    d3 = int(msg[2])
    d4 = int(msg[3])

    p1 = d1^d2^d4
    p2 = d1^d3^d4
    p3 = d2^d3^d4

    return (p1, p2, d1, p3, d2, d3, d4)

code = build_code(data)
print(f"original code:\n{code}")

# le mot clé optenu est 1010101
# Le rôle des bits de parité est de détecter la présence d'erreur et de la localiser à l'aide de 'coordonnées'.
# Ces bits jouent le rôle de SEC (Single Error Correction), DED (Double Error Detection)
# On ajoute de la redondance pour protéger contre les erreurs de transmission

#################################################
# Partie 2 - Correction d'une erreur simple
#################################################
print(
        '''
#################################################
# Partie 2 - Correction d'une erreur simple
#################################################
'''
)

import numpy as np

# 1 indexed
def introduce_error(code:tuple, bit_position:int)->tuple:
    if bit_position < 1:
        raise ValueError("Invalid bit position")
    temp_code = list(code)
    temp_code[bit_position-1] = temp_code[bit_position-1] ^ 1
    return tuple(temp_code)

code_with_error = introduce_error(code, 6)
print(f"code with error:\n{code_with_error}")

H = np.array([
            [1,1,0,1,   1,0,0], # Q combined with I3
            [1,0,1,1,   0,1,0],
            [0,1,1,1,   0,0,1],
            ])

# version of H with ordered colums to give a LUT and directly provide the answer
H_LUT = np.array([
            [0,0,0,1,1,1,1], # Q combined with I3
            [0,1,1,0,0,1,1],
            [1,0,1,0,1,0,1],
            ])

def calc_syndrome(H:np.ndarray, rx_msg:np.ndarray)->np.ndarray:
    return np.dot(H,rx_msg)%2

syndrome = calc_syndrome(H_LUT, np.asarray(code_with_error))

print(f"syndrome: {syndrome}")


# Le mot reçu après l'erreur est 0110001
# Le syndrome optenu est 110 donc bit position 6

# Pour déduire la position de l'erreur on utilise un tableau LUT (Look-up table)
# Puisque H est ordonée on obtient directement la position de l'erreur en binaire
# sur le vecteur colone correspondant en binaire

def get_error_position(synd:np.ndarray)->int:
    error_position = 0
    for i in range(len(synd)):
        error_position += 2**i*synd[len(synd)-1-i]
    return error_position

err_pos = get_error_position(syndrome)
print(f"Error found at position {err_pos}")

fixed_code_1_err = introduce_error(code_with_error, err_pos)
if(fixed_code_1_err == code):
    print('Code corrected successfully!')
else:
    print('Code could not be corrected')

# Le mot corrigé est forcément iddentique au mot codé initial si uniquement une erreur
# a été injectée.

#################################################
# Partie 3 - Les Limites du code de Hamming (7,4)
#################################################

print(
        '''
#################################################
# Partie 3 - Les Limites du code de Hamming (7,4)
#################################################
'''
)

code_with_error = introduce_error(code_with_error, 3)
print("Code avec erreures sur bits 3 et 6:")
print(code_with_error)

syndrome_2_errors = calc_syndrome(H_LUT, np.asarray(code_with_error))
print(f'syndrome avec erreurs injectées sur bits 3 et 6: {syndrome_2_errors}')
err_pos2 = get_error_position(syndrome_2_errors)
print(f"Error found at position {err_pos2}")
fixed_code_2_err = introduce_error(code_with_error, err_pos2)
print(calc_syndrome(H_LUT, np.asarray(fixed_code_2_err))) # syndrome indique que le code parait maintenant corrigé
if(fixed_code_2_err == code):
    print('Code corrected successfully!')
else:
    print('Code could not be corrected')
# Non le résultat n'est pas correct
# La correction n'est pas appliquée correctement, et la détection du bit erroné sera mauvaise
# Le code Hamming simple est basé sur la notion de parité.
# Une correction basée sur la simple détection va permettre de satisfaire le calcule du syndrome
# Du point de vue du récepteur le code est maintenant corrigé sauf que ce n'est pas le cas
# Hamming simple (sans 8ème bit) est incapable de corriger ou détecter 2 erreures.
# Pour détecter une deuxième erreur on doit ajouter un bit de parité global

#################################################
# Partie 4 - Passage au code de Hamming étendu
#################################################

print(
        '''
#################################################
# Partie 4 - Passage au code de Hamming étendu
#################################################
'''
)

def build_modified_hamming_code(msg:str)->tuple:
    if len(msg) != 4:
        raise ValueError("Le message doit être de 4 bits")

    d1 = int(msg[0])
    d2 = int(msg[1])
    d3 = int(msg[2])
    d4 = int(msg[3])

    p1 = d1^d2^d4
    p2 = d1^d3^d4
    p3 = d2^d3^d4

    g = p1^ p2^ d1^ p3^ d2^ d3^ d4

    return (p1, p2, d1, p3, d2, d3, d4, g)

code_hamming_modified = build_modified_hamming_code(data)
print(f"modified hamming code:\n{code_hamming_modified}")

def is_global_parity_valid(code:tuple)->bool:
    return sum(code) % 2 == 0 # checking parity bit is equivalent to checking if sum is even

if is_global_parity_valid(code_hamming_modified) == True:
    print("Global Parity Valid")
else:
    print("Global Parity Invalid")

# le mot code obtenu sur 8 bits est 01100110
# le bit suplémentaire permet de détecter une deuxième erreur

#################################################
# Partie 5 - Passage au code de Hamming étendu
#################################################

print(
        '''
#################################################
# Partie 5 - Passage au code de Hamming étendu
#################################################
''')

simple_err_modified_harming = introduce_error(code_hamming_modified, 6)
print(f'error modified hamming: {simple_err_modified_harming}')

rx_message = np.asarray(simple_err_modified_harming)
hamming_part = rx_message[:7] # grab only first 7 bits
syndr_mod_haming = calc_syndrome(H_LUT, hamming_part)
print(f'syndrome first 7 bits modified hamming: {syndr_mod_haming}')
if is_global_parity_valid(simple_err_modified_harming) == True:
    print("Global Parity Valid")
else:
    print("Global Parity Invalid")

# on vérifie si le syndrome est non nul dabord
# si c'est le cas, on vérifie la parité globale pour savoir si il y a une ou deux erreurs.
# si la parité n'est pas valide alors le nombre d'erreurs est paire (on suppose une erreur uniquement)
# on corrige comme d'habitude avec le LUT
# sinon il y a un nombre d'erreur paire (on suppose 2) on peut pas la corriger

# Si une erreur seulement elle est localisable.
# oui si il y a uniquement une erreur
# Si l'erreur affecte uniquement le bit de parité global on pourra le déduire du fait que le syndrome sera nul.


#########################################################
# Partie 6 - Étude d'une double erreur avec le code (8,4)
#########################################################
print(
'''
#########################################################
# Partie 6 - Étude d'une double erreur avec le code (8,4)
#########################################################
'''
        )

simple_err_modified_harming = introduce_error(simple_err_modified_harming, 3) # bits 3 and 6 are flipped

rx_message2 = np.asarray(simple_err_modified_harming)
hamming_part2 = rx_message[:7] # grab only first 7 bits
syndr_mod_haming2 = calc_syndrome(H_LUT, hamming_part2)
print(syndr_mod_haming2)
if is_global_parity_valid(simple_err_modified_harming) == True:
    print("Global Parity Valid")
else:
    print("Global Parity Invalid")
# le syndrome indique une erreur alors que la parité globale est correcte
# On en déduit que deux erreurs sont présentes

# On ne peut pas corriger le mot reçu
# Oui le problème est détecté
# On détecte une erreur de plus par rapport à hamming 7,4

#########################################################
# Partie 7 - Étude automatisée sur plusieures messages
#########################################################
print(
'''
#########################################################
# Partie 7 - Étude automatisée sur plusieures messages
#########################################################
'''
        )

import random
random.seed(0) # set for reproducable number gen
def gen_rand_msg(length:int)->str:
    message = random.getrandbits(length)
    message = format(message, '0b').zfill(length) # ensure no trucking if first bit is zero
    return message

messages = list(gen_rand_msg(4) for _ in range(1000)) # gen 1000 messages to ensure robustness lol

# generate codes
codes = []
for message in messages:
    codes.append(build_modified_hamming_code(message))

codes_not_extended = []
for message in messages:
    codes_not_extended.append(build_code(message))

print(codes)

# indroduire 2 erreures par code
codes_with_errors = []
for code in codes:
    err_pos = random.randint(1,len(code))
    err_pos2 = random.randint(1,len(code))
    first_error = introduce_error(code, err_pos)
    codes_with_errors.append(introduce_error(first_error, err_pos2))

codes_with_errors_not_exteded = []
for code in codes_not_extended:
    err_pos = random.randint(1,len(codes_not_extended))
    err_pos2 = random.randint(1,len(codes_not_extended))
    first_error = introduce_error(code, err_pos)
    codes_with_errors_not_exteded.append(introduce_error(first_error, err_pos2))
print(codes_with_errors)

# calcul_syndrome
syndromes = []
for code in codes_with_errors:
    rx_m = np.asarray(code)
    syndromes.append(calc_syndrome(H_LUT, rx_m[:7]))

syndromes_not_extended = []
for code in codes_with_errors:
    rx_m = np.asarray(codes_not_extended)
    syndromes_not_extended.append(calc_syndrome(H_LUT, rx_m))
print(syndromes)

# corriger l'erreur
# WARNING: assume only one error
corrected_codes = []
for i in range(len(codes_with_errors)):
    #print(i)
    error_position = get_error_position(syndromes[i])
    #print(f'error_position : {error_position}')
    if(error_position != 0):
        corrected_codes.append(introduce_error(codes_with_errors[i], error_position))
    else: # global parity must be corrupted
        corrected_codes.append(introduce_error(codes_with_errors[i], 8))
#print(corrected_codes)

if corrected_codes == codes:
    print('all codes corrected successfully')
else:
    print('at least one code failed to correct')

# sans protection on aura forcément toujours une erreur
# pour hamming(7,4) on aurra 1/8 fois une erreur
# pour hamming(8,4) on aurra 


