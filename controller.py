import random

""" test avec une fausse classe en attendant le reste : """

class Player():
    def __init__(self, name, num_of_questions_with_correct_answer=0, 
                num_of_questions_with_bad_answer=0, camembert_BASES_DE_DONNEES=False, camembert_LANGAGES_DE_PROGRAMMATION=False, camembert_LIGNE_DE_COMMANDES=False,
                camembert_ACTUALITES_IA=False, camembert_DEVOPS=False, camembert_TECH_IA=False
                ):
            self.name = name
            self.num_of_questions_with_correct_answer = num_of_questions_with_correct_answer
            self.num_of_questions_with_bad_answer = num_of_questions_with_bad_answer
            self.camembert_BASES_DE_DONNEES = camembert_BASES_DE_DONNEES
            self.camembert_LANGAGES_DE_PROGRAMMATION = camembert_LANGAGES_DE_PROGRAMMATION
            self.camembert_LIGNE_DE_COMMANDES = camembert_LIGNE_DE_COMMANDES
            self.camembert_ACTUALITES_IA = camembert_ACTUALITES_IA
            self.camembert_DEVOPS = camembert_DEVOPS
            self.camembert_TECH_IA = camembert_TECH_IA

J1 = Player("nico",3,5)


liste_theme = ["Bases de données", "Langages de programmation", "Ligne de commandes", "Actualités IA", "DevOps", "promo tech IA !"]

def new_turn(joueur):
    iscamembert = is_camembert(joueur)
    themechoice = theme_choice()
    print("Choisissez votre theme :")
    print("1 pour {}".format(liste_theme[themechoice[0]]))
    print("2 pour {}".format(liste_theme[themechoice[1]]))
    n = choice_input()-1
    id_theme = liste_theme.index(liste_theme[themechoice[n]])
    return ask_Questions(iscamembert, joueur, id_theme)

def ask_Questions(*args):
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

def theme_choice():
    """
    return : tuple with two different int in [0,5]
    """
    n = random.randint(0,5)
    m = random.randint(0,5)
    while n == m:
        m = random.randint(0,5)
    return n,m

def is_camembert(joueur):
    """
    True if number of answers is a mutliple of 3
    return : bool
    """
    nb_question = int(joueur.num_of_questions_with_correct_answer+joueur.num_of_questions_with_bad_answer+1)
    if nb_question%3 == 0:
        return True
    else :
        return False

print(new_turn(J1))