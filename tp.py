# Partie 1 - Génération de données

import random

random.seed(1)

seq_bits = tuple(random.randint(0,1) for _ in range(1000))

# cette séquence représente notre source de données

# on travaille avec des bits puisque c'est l'unité atomique d'information dans le numérique

# cette séquence représente un modèle simplifié, on part du principe que les données génère une séquence 'aléatoire'. En pratique il faudrait étudier la nature de notre source.

# Partie 2 - Simulation d'un canal bruité

# Canal binaire symétrique (BSC), chaque bit est inversé indépendamment avec proba p

proba_bit_flip = 0.1


def canal(data:tuple, bit_flip_probability:float)->tuple:
    if not (0.0 <= bit_flip_probability <= 1.0):
            raise ValueError("Probability must be between 0.0 and 1.0 bounds")

    out = list(data)

    for i, bit in enumerate(out):
            if random.random() < bit_flip_probability:
                out[i] ^= 1  # Clean bit flip!

    return tuple(out)

out = canal(seq_bits, proba_bit_flip)

# le vecteur de bruit représente le canal

# lorsque le bit est affecté par le bruit on obtient une erreur sur celui-ci

# Partie 3 - Analyse des erreurs

def count_diff(in1:tuple, in2:tuple)->int:
    count = 0
    for i in range(len(in1)):
        if in1[i] != in2[i]:
            count += 1
    return count

def bit_error_rate(in1:tuple, in2:tuple)->float:
    return count_diff(in1, in2) / len(in1)

print(f"ber: {bit_error_rate(seq_bits, out)}")

