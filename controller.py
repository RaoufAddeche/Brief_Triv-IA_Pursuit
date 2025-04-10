import random
from enums import Themes
from database_utils import DatabaseUtils
from positions import create_all_position, Position, create_center_position
from playermodels import Player
from enums import Themes


def new_turn(index_player=0):
    player = list_players[index_player]
    return ask_questions(player)


def good_answer(player: Player, iscamembert: bool, id_theme: int) :
    """
    If the player answer correctly, he can play again
    """
    print("bonne réponse !")
    player.num_of_questions_with_correct_answer += 1 # update stats
    if iscamembert:
        update_camembert(player, id_theme) # add coresponding camembert
        
    if player.is_final_step(): # If the player have all camemberts
        if player.position_id == 99: # si le joueur est au centre
            print(f"{player.name} a tous les camemberts ! Il est maintenant dans la dernière ligne droite.")
            return last_step(player) # Envoie le player à la dernière ligne droite du jeu
        elif player.position_id < 42: # si le joueur est sur le cercle
            position = list_diag_positions[int(player.position_id/7)][0] # recupère la première position dans la diagonale correspondante
            player.position_id = position.id
        else: # si le joueur est sur la diagonale
            position = found_diag_position(player) # recupère l'objet Position correspondant à la position
            new_position = position.move_to_win()
            player.position_id = new_position

    user.update_player(player) # sauvegarde dans la db, vraiment necessaire ?
    return new_turn(list_players.index(player))

def found_diag_position(player : Player) -> Position:
    """
    return Position object from the id_position of the player
    """
    if player.position_id < 42: # Si le joueur est sur l'exterieur
        return list_positions[player.position_id]
    elif player.position_id == 99: # Si le joueur est sur la case centrale
        return list_diag_positions[-1]
    for item in list_diag_positions[:-1]: # si le joueur est sur une diagonale
        for position in item:
            if player.position_id == position:
                return position

def streamlit_found_diag_position(player : Player, outter_positions: list[Position], center_positions: list[list]):
    """
    return Position object
    """
    if player.position_id < 42:
        return outter_positions[player.position_id]
    print("ligne 50 : ", player.position_id)
    for item in center_positions[:-1]:
        for position in item:
            if player.position_id == position:
                return position


def update_camembert(player : Player, id_theme : int):
    """
    Met à jour les camemberts du joueur s'il répond correctement à une question.
    """
    camembert_names = list(map( lambda t : str(t).removeprefix('Themes.'), Themes))
    camembert_name = camembert_names[id_theme]
    setattr(player, f"camembert_{camembert_name}", True)

def cheat_get_all_camemberts(player):
    for x in range (0, 6):
        update_camembert(player, x)

def wrong_answer(player):
    """
    If he's wrong, next player
    """
    print("mauvaise réponse !")
    player.num_of_questions_with_bad_answer += 1
    user.update_player(player)
    n = (list_players.index(player)+1)%len(list_players)
    return new_turn(n)



# Fonction principale du jeu
def ask_questions(player):

    print(f"C'est au tour de {player.name}")
    print(player.position_id)
    print(player.is_final_step())
    if player.is_final_step():
        if player.position_id == 99:
            return last_step(player)
        position = found_diag_position(player)
        id_theme = position.theme
        is_camembert = False
    else :
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
    print(question.text)
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
    print(player.position_id, "hop2")
    user.update_player(player)
    id_theme = list_positions[player.position_id].theme
    iscamembert = list_positions[player.position_id].iscamembert
    return((id_theme,iscamembert))

def get_possible_move(current_pos, dice_roll):
    return (current_pos.move(dice_roll, True), current_pos.move(dice_roll, False))    


def last_step(player):
    """
    Fonction pour gérer la dernière ligne droite du jeu.
    """
    print(f"C'est la dernière ligne droite pour {player.name}!")
    print(player.position_id)
    remaining_question = 6
    themes = ["BASES_DE_DONNEES", "LANGAGES_DE_PROGRAMMATION", "LIGNE_DE_COMMANDES", "ACTUALITES_IA", "DEVOPS", "TECH_IA"]

    for item in themes:
        theme_name = item
        print(f"Il reste {remaining_question} questions.")
        remaining_question = remaining_question -1
        theme_id = Themes[theme_name].value # obtenir l'id depuis l'enum
        question_choisie = random.choice(user.get_question_list(theme_id))

        print(f"question du theme {theme_name}:")


        reponse = question_resolution(question_choisie)
        if reponse.is_correct:
            print("Réponse correcte!")
        else:
            print("Mauvaise réponse! Le player passe au tour suivant.")
            return wrong_answer(player)
    else:
        print("Le joueur a reussi a répondre aux 6 questions, il remporte la partie")
        return True

# from typing import cast

if __name__ == "__main__":
    list_positions = create_all_position()
    list_diag_positions = create_center_position()
    user = DatabaseUtils()
    camembert_names = list(map( lambda t : str(t).removeprefix('Themes.'), Themes))
    id_game = user.create_game()
    user.create_player(id_game, "winner")
    user.create_player(id_game, "Raouf")
    list_players = user.get_players(id_game)
    # for player in list_players :
    #     if player.name == "Winner" :
    #         player = cast(Player, player).
    for item in camembert_names:
        setattr(list_players[0], f"camembert_{item}", True)
    user.update_player(list_players[0])
    list_players = user.get_players(id_game)
    list_player = list_players
    print(list(map( lambda t : str(t).removeprefix('Themes.'), Themes)))
    new_turn()





