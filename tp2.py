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

import sys
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

# on vérifie si le syndrome est non nul dabord si c'est le cas, on vérifie la parité globale pour savoir si il y a une ou deux erreurs.
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


number_of_messages = 1000
messages = list(gen_rand_msg(4) for _ in range(number_of_messages)) # gen 1000 messages to ensure robustness lol

# generate codes
codes = []
for message in messages:
    codes.append(build_modified_hamming_code(message))

codes_not_extended = []
for message in messages:
    codes_not_extended.append(build_code(message))


# introduire erreure(s)
def introduce_error_into_codes_array(codes:list, number_of_errors:int)->list:
    codes_with_errors = []
    for code in codes:
        err_pos = random.randint(1,len(code))
#        print(err_pos)
        if number_of_errors == 2:
            err_pos2 = random.randint(1,len(code))
            while err_pos2 == err_pos: # make sure the numbers are different to ensure exactly 2 errors introduced
                err_pos2 = random.randint(1,len(code))
#            print(err_pos2)
            code = introduce_error(code, err_pos2) # apply first error
        codes_with_errors.append(introduce_error(code, err_pos)) # apply either first or second
    return codes_with_errors

#codes_with_errors_not_exteded = []
#for code in codes_not_extended:
#    err_pos = random.randint(1,len(code))
#    err_pos2 = random.randint(1,len(code))
#    while err_pos2 == err_pos: # make sure the numbers are different to ensure exactly 2 errors introduced
#        err_pos2 = random.randint(1,len(code))
#    first_error = introduce_error(code, err_pos)
#    codes_with_errors_not_exteded.append(introduce_error(first_error, err_pos2))

# errors should be different from call to call despite hardcoded seed
# seed provides reproducable results though
codes_with_errors = introduce_error_into_codes_array(codes, 1)
codes_with_errors_not_extended = introduce_error_into_codes_array(codes_not_extended, 1)
codes_with_errors2 = introduce_error_into_codes_array(codes, 2)
codes_with_errors_not_extended2 = introduce_error_into_codes_array(codes_not_extended, 2)

# calcul_syndromes
def syndrome_fill(codes_with_errors:list):
    syndromes = []
    for code in codes_with_errors:
        rx_m = np.asarray(code)
        #print(rx_m[:7])
        syndromes.append(calc_syndrome(H_LUT, rx_m[:7]))
    return syndromes

syndromes = syndrome_fill(codes_with_errors)
syndromes2 = syndrome_fill(codes_with_errors2)
syndromes_not_extended = syndrome_fill(codes_with_errors_not_extended)
syndromes_not_extended2 = syndrome_fill(codes_with_errors_not_extended2)

def correct_codes_list(codes_with_errors, original_codes, syndromes):
    num_err_detected_and_fixed = 0
    num_err_detected_but_unfixable = 0
    num_err_falsely_fixed = 0 # detected with non extended and fixed but different to initial code
    # corriger l'erreur
    # WARNING: assume max of two errors
    corrected_codes = []
    for i in range(len(codes_with_errors)):
        extended = False
        if len(codes_with_errors[0]) == 8:
            extended = True
        error_position = get_error_position(syndromes[i])
        if(error_position == 0): # syndrome is 0
            if extended:
                if is_global_parity_valid(codes_with_errors[i]) == False:
                    corrected_codes.append(introduce_error(codes_with_errors[i], 8)) # correct parity bit
                    num_err_detected_and_fixed += 1
        else: # syndrome indicates error
            if extended:
                if is_global_parity_valid(codes_with_errors[i]) == False: # only one error found
                    corrected_codes.append(introduce_error(codes_with_errors[i], error_position))
                    num_err_detected_and_fixed += 1
                else:
                    num_err_detected_but_unfixable += 2
            else:
                corrected_codes.append(introduce_error(codes_with_errors[i], error_position))
                if corrected_codes[-1] != original_codes[i]:
                    num_err_falsely_fixed += 1
                else:
                    num_err_detected_and_fixed += 1

    return {'corrected codes': corrected_codes, 'num_err_detected_and_fixed': num_err_detected_and_fixed, 'num_err_detected_but_unfixable': num_err_detected_but_unfixable, 'num_err_falsely_fixed': num_err_falsely_fixed}

corrected = correct_codes_list(codes_with_errors, codes, syndromes)
corrected2 = correct_codes_list(codes_with_errors2, codes, syndromes2)
corrected_not_extended = correct_codes_list(codes_with_errors_not_extended, codes_not_extended, syndromes_not_extended)
corrected_not_extended2 = correct_codes_list(codes_with_errors_not_extended2, codes_not_extended, syndromes_not_extended2)

def print_stats(corrected:dict):
    from itertools import islice
    for key, value in islice(corrected.items(), 1, None):
        sys.stdout.write('\t')
        print(f"{key}: {value}")

print('single err:')
print_stats(corrected)
print('double err:')
print_stats(corrected2)
print('single err not extended:')
print_stats(corrected_not_extended)
print('double err not extended:')
print_stats(corrected_not_extended2)

# Dans le cas d'une erreur simple je constate qu'elles sont toutes corrigés pour le hamming non étendu (7,4)
# Pour deux erreures elles sont faussement corrigées
# L'ajout du bit global permet de détecter la présence d'une deuxième erreur et donc de ne pas corriger un bit à tort
# Le code (8, 4), c-a-d hamming étendu

#################################################
# Partie 8 - Comparaison avec d'autres solutions
#################################################

print(
        '''
#################################################
# Partie 8 - Comparaison avec d'autres solutions
#################################################
        '''
        )
#########################################
# Comparaison qualitative des solutions
#########################################
# Sans protection n'apporte rien du tout, est sensible à toutes les erreurs.
# Devrait être utilisé uniquement si les erreurs sont acceptables (ex sortie UART pour débogger)

# Avec bit de parité
# Protection minimale pour détecter la présence d'une et une seule erreur. On peut pas faire mieux avec un seul bit.
# Est utilisé dans l'UART aussi
# Dans le cas d'une détection d'erreur, le récepteur peut demander à retransmettre

# Le CRC est beacoup plus fort comme solution pour détecter les erreurs. Elle marche aussi pour les multiples erreurs
# Le CRC peut aussi être calculé pour un dividende de taille infinie en théorie (même si la probabilité
# de collision augmente avec la taille de ce dividende)
# Les polynomes peuvent être choisis suivant l'application donée
# Le CRC néanmoins ne permet pas de corriger

# Hamming contrairement au CRC permet non seulement de detecter une erreur mais de la corriger
# par contre il peut uniquement détecter et corriger une erreur simple

# Hamming étendu peut détecter et corriger une erreur d'un bit mais il peut aussi détecter 2 erreures



# Le CRC, le bit de parité peuvent que détecter
# Hamming étendu peut uniquement corriger une erreur simple
# Hamming étendu permet de discriminer le cas de deux erreures
# Le CRC reste utile puisqu'il est facile à implémenter en hardware et très flexible en terme de polynome
# et aussi en terme de données d'entrée.
# On préférerait un code plus puissant dans le cas où l'on trouve souvent 2+ erreurs ou que la perte de données est innacceptable.




#################################################
# Partie 9 - Choix ingénieur
#################################################

# La liaison satélitaire peut être sensible à énormément de bruit, le signal de celui-ci sera aussi bien faible
# en puissance une fois arrivé au récepteur
# Un choix de FEC semble intéressant ici pour économiser de la puissance et limiter des 
# retransmissions à longue distance inutiles
# Le choix de schéma FEC dépend du type d'application et de la redondance nécessaire
# Si la modulation est adapée hamming pourrait peut-être sufire? Sinon on choisira un autre code plus puissant

# La liaison CAN utilise un CRC en pratique.
# Ce polynome est concû pour être robuste contre le bruit typique présent dans les voitures.
# Le raisonement derrière semble être une priorisation de sécurité avant la vitesse.
# On préfère alouer tous les bits vers une détection plûtot qu'une correction
# On pourrait pas du tout imaginer hamming par exemple dans utiliser un code hamming.
# Celui-ci n'est pas du tout suffissament robuste

# Pour le stockage SSD, BCH semble être souvent utilisé. C'est une forme de FEC.
# FEC devrait être priorisé puisque l'on peut pas du tout ce permettre de perdre des données dans ce cas.
# Rien ne sert de savoir qu'une erreur est produite si on ne peut pas la corriger

# Hamming pourrait peut-être suffire en satélitaire (à voire).

# Le problème est que Hamming ne prend pas en compte le fait que l'on pourrait avoir plusieurs erreurs dans une même transmission. On trouve beacoup celà dans les SSD, où dans le bus CAN

# Hamming semble être le standard pour de la ram ECC. Celle-ci est souvent affectée par des rayons cosmiques (donc erreure isolée)
