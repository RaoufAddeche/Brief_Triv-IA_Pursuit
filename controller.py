import random
from themes import theme_choice
from enums import Themes
from database_utils import DatabaseUtils

user = DatabaseUtils()

id_question= user.create_question(Themes.LANGAGES_DE_PROGRAMMATION.value, "testL")
user.create_answer(id_question, "1", False)
user.create_answer(id_question, "O2e", False)
user.create_answer(id_question, "Mon3B", False)
user.create_answer(id_question, "Tre", True)




list_players = user.get_players()
liste_theme = ["Bases de données", "Langages de programmation", "Ligne de commandes", "Actualités IA", "DevOps", "promo tech IA !"]
liste_joueur = list_players

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



# Fonction principale du jeu
def ask_Questions(joueur, iscamembert, id_theme):

    print(f"C'est au tour de {joueur.name}")
    question_choisie = random.choice(user.get_question_list(id_theme))
    print(question_choisie.text)


    reponse = input("votre réponse :")

    #si reponse correcte le joueur continue, sinon joueur suivant
    reponse_correcte = "reponse"
    if reponse == reponse_correcte:
        return good_answer(joueur, iscamembert, id_theme)

    else:
        return wrong_answer(joueur)

new_turn()