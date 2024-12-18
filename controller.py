import random
from themes import theme_choice
from enums import Themes
from database_utils import DatabaseUtils
from playermodels import Player

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

def update_camembert(joueur, id_theme):
    """
    Met à jour les camemberts du joueur s'il répond correctement à une question.
    """
    camembert_names = ["BASES_DE_DONNEES", "LANGAGES_DE_PROGRAMMATION", "LIGNE_DE_COMMANDES", "ACTUALITES_IA", "DEVOPS", "TECH_IA"]
    camembert_name = camembert_names[id_theme]
    setattr(joueur, f"camembert_{camembert_name}", True)

def good_answer(joueur, iscamembert, id_theme):
    """
    If the player answer correctly, he can play again
    """
    # if is camembert , +1 en fonction de l'id du theme et du joueur
    print("bonne réponse !")
    joueur.num_of_questions_with_correct_answer += 1

    if iscamembert:
        update_camembert(joueur, id_theme)
        
    # Check si le joueur a tout les camemberts
    if joueur.is_final_step():
        print(f"{joueur.name} a tous les camemberts ! Il est maintenant dans la dernière ligne droite.")
        # Envoie le joueur à la dernière ligne droite du jeu
        return last_step(joueur)

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

# Logique pour finir le jeu
def last_step(joueur):
    """
    Fonction pour gérer la dernière ligne droite du jeu.
    """
    print(f"C'est la dernière ligne droite pour {joueur.name}!")
    # Le joueur doit répondre à 6 questions correctes pour gagner le jeu
    questions_needed = 6
    correct_answers = 0

    while correct_answers < questions_needed:
        question_choisie = random.choice(user.get_question_list(Themes.BASES_DE_DONNEES.value))  # ou autre thème 
        print(question_choisie.text)

        reponse = question_resolution(question_choisie)
        if reponse.is_correct:
            correct_answers += 1
            print(f"Réponse correcte! Il reste {questions_needed - correct_answers} questions.")
        else:
            print("Mauvaise réponse! Le joueur passe au tour suivant.")

    print(f"{joueur.name} a réussi à répondre correctement aux 6 questions! Il a gagné")

new_turn()


#




