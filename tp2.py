# TP2 Correction d'erreurs avec le code de Hamming (7,4) et (8,4)

# Partie 1 - Codage de Hamming (7,4)
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

# Partie 2 - Correction d'une erreur simple
from os import error
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

code_with_error = introduce_error(code, 5)
syndrome = calc_syndrome(H_LUT, np.asarray(code_with_error))

print(f"syndrome: {syndrome}")

# Le mot reçu après l'erreur est 0010101
# Le syndrome optenu est 101 donc bit position 5

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

# Le mot corrigé est forcément iddentique au mot codé initial si uniquement une erreur
# a été injectée.

# Partie 3 - Les Limites du code de Hamming (7,4)

