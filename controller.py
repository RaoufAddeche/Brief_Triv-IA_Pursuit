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

def good_answer(player, iscamembert, id_theme):
    """
    If the player answer correctly, he can play again
    """
    print("bonne réponse !")
    player.num_of_questions_with_correct_answer += 1
    if iscamembert:
        camembert_win(player, id_theme)
    return new_turn(liste_joueur.index(player))

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

    reponse = question_resolution(question_choisie)

    #si reponse correcte le joueur continue, sinon joueur suivant
    if reponse.is_correct:
        return good_answer(joueur, iscamembert, id_theme)

    else:
        return wrong_answer(joueur)

def question_resolution(question):
    list_answers = question.answers
    for i, answer in enumerate(list_answers):
        print(f"choix {i+1} : {answer.text} ")
    
    n=0
    while n not in ["1", "2", "3", "4"]: # trouver mieux
        try:
            n = input("votre réponse :")
            if n not in ["1", "2", "3", "4"]:
                raise Exception("Vous devez selectionner une des réponses") 
        except:
            print("Vous devez selectionner une des réponses")
    return list_answers[int(n)-1]


def camembert_win(player, id_theme):
    pass

new_turn()