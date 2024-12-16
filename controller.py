import random

J1 = {"name":"nico", "nb_mauvaise_reponse":4, "nb_bonne_reponse":8, "camembert":[]}

liste_theme = ["Bases de données", "Langages de programmation", "Ligne de commandes", "Actualités IA", "DevOps", "promo tech IA !"]

def newTurn(joueur):
    is_camembert = isCamenbert(joueur)
    theme_choice = themeChoice()
    print("Choisissez votre theme :")
    print("1 pour {}".format(liste_theme[theme_choice[0]]))
    print("2 pour {}".format(liste_theme[theme_choice[1]]))
    n = choice_input()-1
    id_theme = liste_theme.index(liste_theme[theme_choice[n]])
    return ask_Questions(is_camenbert, joueur, id_theme)

def ask_Questions():
    pass

def choice_input():
    n=0
    while n not in ["1", "2"]:
        try:
            n = input()
            if n not in ["1", "2"]:
                raise Exception("Vous devez selectionner 1 ou 2") 
        except:
            print("Vous devez selectionner 1 ou 2")
    return int(n)

def themeChoice():
    """
    return : tuple with two different int in [0,5]
    """
    n = random.randint(0,5)
    m = random.randint(0,5)
    while n == m:
        m = random.randint(0,5)
    return n,m

def isCamenbert(joueur):
    """
    True if number of answers is a mutliple of 3
    return : bool
    """
    nb_question = int(joueur["nb_mauvaise_reponse"]+joueur["nb_bonne_reponse"]+1)
    if nb_question%3 == 0:
        return True
    else :
        return False

newTurn(J1)