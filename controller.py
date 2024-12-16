import random

J1 = {"name":"nico", "nb_mauvaise_reponse":4, "nb_bonne_reponse":7, "camembert":[]}

def themeChoice():
    """
    return : tuple with two different int in [0,5]
    """
    n = random.randint(0,5)
    m = random.randint(0,5)
    while n == m:
        m = random.randint(0,5)
    return n,m

def isCamenbert(Joueur):
    """
    True if number of answers is a mutliple of 3
    return : bool
    """
    nb_reponse = Joueur["nb_mauvaise_reponse"]+Joueur["nb_bonne_reponse"]
    if nb_reponse == 0 :
        return False
    elif nb_reponse%3 == 0:
        return True
    else :
        return False

print(isCamenbert(J1))