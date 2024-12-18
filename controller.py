import random
from themes import theme_choice
from enums import Themes
from database_utils import DatabaseUtils
from positions.positions import create_all_position, Position


list_positions = create_all_position()

user = DatabaseUtils()

id_question= user.create_question(Themes.LANGAGES_DE_PROGRAMMATION.value, "testL")
user.create_answer(id_question, "1", False)
user.create_answer(id_question, "O2e", False)
user.create_answer(id_question, "Mon3B", False)
user.create_answer(id_question, "Tre", True)

id_question= user.create_question(Themes.LIGNE_DE_COMMANDES.value, "testqsdaL")
user.create_answer(id_question, "1", False)
user.create_answer(id_question, "O2e", False)
user.create_answer(id_question, "Mon3B", False)
user.create_answer(id_question, "Tre", True)

id_question= user.create_question(Themes.ACTUALITES_IA.value, "tesqjsdtL")
user.create_answer(id_question, "1", False)
user.create_answer(id_question, "O2e", False)
user.create_answer(id_question, "Mon3B", False)
user.create_answer(id_question, "Tre", True)

id_question= user.create_question(Themes.DEVOPS.value, "tesqstL")
user.create_answer(id_question, "1", False)
user.create_answer(id_question, "O2e", False)
user.create_answer(id_question, "Mon3B", False)
user.create_answer(id_question, "Tre", True)




list_players = user.get_players()
liste_theme = ["Bases de données", "Langages de programmation", "Ligne de commandes", "Actualités IA", "DevOps", "promo tech IA !"]
liste_joueur = list_players

def new_turn(index_joueur=0):
    joueur = liste_joueur[index_joueur]
    return ask_Questions(joueur)


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



def good_answer(player, iscamembert, id_theme):
    """
    If the player answer correctly, he can play again
    """
    # if is camembert , +1 en fonction de l'id du theme et du joueur
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
def ask_Questions(player):

    print(f"C'est au tour de {player.name}")
    input("un input pour lancer le dés")
    dice = random.randint(1,6)
    r =input("voulez vous avancer dans le sens horaire (h) ou anti-horraire (a) ?" )
    if r == "h":
        new_position = list_positions[player.position_id].move(dice,True)
    else:
        new_position = list_positions[player.position_id].move(dice,False)
    player.position_id = new_position
    user.update_player(player)
    id_theme = list_positions[player.position_id].theme
    iscamembert = list_positions[player.position_id].iscamembert

    question = (random.choice(user.get_question_list(id_theme)))
    reponse = question_resolution(question)

    #si reponse correcte le joueur continue, sinon joueur suivant
    if reponse.is_correct:
        return good_answer(player, iscamembert, id_theme)

    else:
        return wrong_answer(player)

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
            print("Mauvaise réponse!")

    print(f"{joueur.name} a réussi à répondre correctement aux 6 questions! Il a gagné")

new_turn()


#

