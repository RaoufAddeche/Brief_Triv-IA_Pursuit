import random
from themes import theme_choice
from enums import Themes
from database_utils import DatabaseUtils
from positions.positions import create_all_position, Position
from playermodels import Player

def new_turn(index_player=0):
    player = liste_player[index_player]
    return ask_questions(player)


def good_answer(player, iscamembert, id_theme):
    """
    If the player answer correctly, he can play again
    """
    # if is camembert , +1 en fonction de l'id du theme et du player
    print("bonne réponse !")
    player.num_of_questions_with_correct_answer += 1
    if iscamembert:
        update_camembert(player, id_theme)
        
    # Check si le player a tout les camemberts
    if player.is_final_step():
        print(f"{player.name} a tous les camemberts ! Il est maintenant dans la dernière ligne droite.")
        # Envoie le player à la dernière ligne droite du jeu
        return last_step(player)
    user.update_player(player)
    return new_turn(liste_player.index(player))

def update_camembert(player, id_theme):
    """
    Met à jour les camemberts du joueur s'il répond correctement à une question.
    """
    camembert_names = ["BASES_DE_DONNEES", "LANGAGES_DE_PROGRAMMATION", "LIGNE_DE_COMMANDES", "ACTUALITES_IA", "DEVOPS", "TECH_IA"]
    camembert_name = camembert_names[id_theme]
    setattr(player, f"camembert_{camembert_name}", True)


def wrong_answer(player):
    """
    If he's wrong, next player
    """
    print("mauvaise réponse !")
    player.num_of_questions_with_bad_answer += 1
    user.update_player(player)
    n = (liste_player.index(player)+1)%len(liste_player)
    return new_turn(n)



# Fonction principale du jeu
def ask_questions(player):

    print(f"C'est au tour de {player.name}")
    id_theme, is_camembert = roll_dice(player)
    while id_theme == 6:
        print("Vous pouvez relancer le dés !")
        id_theme, is_camembert = roll_dice(player)
    
    if is_camembert:
        print("c'est un camembert")

    question = (random.choice(user.get_question_list(id_theme)))
    reponse = question_resolution(question)

    #si reponse correcte le player continue, sinon player suivant
    if reponse.is_correct:
        return good_answer(player, is_camembert, id_theme)

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


def roll_dice(player):
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
    return((id_theme,iscamembert))


def last_step(player):
    """
    Fonction pour gérer la dernière ligne droite du jeu.
    """
    print(f"C'est la dernière ligne droite pour {player.name}!")
    remaining_question = 6
    themes = ["BASES_DE_DONNEES", "LANGAGES_DE_PROGRAMMATION", "LIGNE_DE_COMMANDES", "ACTUALITES_IA", "DEVOPS", "TECH_IA"]

    for item in themes:
        theme_name = item
        remaining_question = remaining_question -1
        theme_id = Themes[theme_name].value # obtenir l'id depuis l'enum
        question_choisie = random.choice(user.get_question_list(theme_id))

        print(f"question du theme {theme_name}:")
        print(question_choisie.text)




        reponse = question_resolution(question_choisie)
        if reponse.is_correct:
            print(f"Réponse correcte! Il reste {remaining_question -1} questions.")
        else:
            print("Mauvaise réponse! Le player passe au tour suivant.")
            return wrong_answer(player)
    else:
        print("Le joueur a reussi a répondre aux 6 questions, il remporte la partie")
        return True

last_step(liste_player[0])

