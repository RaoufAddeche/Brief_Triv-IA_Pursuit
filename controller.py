import random
from themes import theme_choice

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
J2 = Player("Soraya", 0, 0)


# Données des questions
questions_data = [
    ("Histoire", "Quel est le nom du roi qui a construit Versailles ?"),
    ("Histoire", "Quelle année a marqué la Révolution française ?"),
    ("Science", "Quel est l'élément chimique symbolisé par 'O' ?"),
    ("Science", "Quelle est la planète la plus proche du Soleil ?"),
    ("Géographie", "Quel est le plus grand désert du monde ?"),
    ("Géographie", "Quelle est la capitale du Canada ?")
]


liste_theme = ["Bases de données", "Langages de programmation", "Ligne de commandes", "Actualités IA", "DevOps", "promo tech IA !"]
liste_joueur = [J1, J2]

def new_turn(index_joueur=0):
    joueur = liste_joueur[index_joueur]
    iscamembert = is_camembert(joueur)
    themechoice = theme_choice()
    print("Choisissez votre theme :")
    print("1 pour {}".format(liste_theme[themechoice[0]]))
    print("2 pour {}".format(liste_theme[themechoice[1]]))
    n = choice_input()-1
    id_theme = liste_theme.index(liste_theme[themechoice[n]])
    return ask_Questions(joueur, iscamembert, id_theme)

def ask_Questions(joueur, *args):
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

def good_answer(joueur):
    """
    If the player answer correctly, he can play again
    """
    print("bonne réponse !")
    joueur.num_of_questions_with_correct_answer += 1
    return new_turn(liste_joueur.index(joueur))

def wrong_answer(joueur):
    """
    If he's wrong, next player
    """
    print("mauvaise réponse !")
    joueur.num_of_questions_with_bad_answer += 1
    n = (liste_joueur.index(joueur)+1)%len(liste_joueur)
    return new_turn(n)


# Fonction pour organiser les questions par thème
def questions_by_theme():
    themes = []
    for theme, question in questions_data:
        for t in themes:
            if t['theme'] == theme:
                t['questions'].append(question)
                break
        else:
            themes.append({'theme' : theme, 'questions' : [question]})
    return themes


# Fonction principale du jeu
def ask_Questions(joueur, iscamembert, id_theme):
    themes = questions_by_theme()
    joueurs = ["Joueur 1", "Joueur 2"]
    current_joueur = 0


    while True:

        print(f"C'est au tour de {joueur.name}")

        #Choix aléatoire de 2 themes
        themes_random = random.sample(themes,2)
        print("choissisez un theme :")
        for i, theme in enumerate(themes_random, 1):
            print(f"{i}, {theme}")

        #demander de choisir un theme
        choix= int(input("Entrez le numéro du thème"))
        while choix not in [1,2]:
            choix = int(input("choix invalide"))
        
        theme_choisi = themes_random[choix - 1]
        question_choisie = random.choice(theme_choisi["questions"])
        print(question_choisie)


        reponse = input("votre réponse :")

        #si reponse correcte le joueur continue, sinon joueur suivant
        reponse_correcte = "reponse"
        if reponse == reponse_correcte:
            return good_answer(joueur, is_camembert)

        else:
            return wrong_answer(joueur)

new_turn()