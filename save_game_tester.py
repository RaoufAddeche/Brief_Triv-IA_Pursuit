from database_utils import DatabaseUtils
from enums import Themes
from question_data import QuestionData

from typing import cast
import datetime as dt

from playermodels import Game, Player

if __name__ == "__main__" :

    user = DatabaseUtils()

    id_game1 = user.create_game()
    user.create_player(id_game1, "Nicolas")
    user.create_player(id_game1, "Victor")
    user.create_player(id_game1, "Raouf")
    user.create_player(id_game1, "Samuel")

    game1 = user.get_game(id_game1)
    game1 = cast(Game, game1)
    game1.date = dt.date(1777, 11, 22)
    game1.current_round = 66

    for player in game1.players :
        match player.name :
            case "Nicolas" :
                player.camembert_BASES_DE_DONNEES = True
                player.num_of_questions_with_bad_answer = 1
                player.num_of_questions_with_correct_answer = 1
            case "Victor":
                player.camembert_LANGAGES_DE_PROGRAMMATION = True
                player.num_of_questions_with_bad_answer = 2
                player.num_of_questions_with_correct_answer = 2
            case "Raouf":
                player.camembert_ACTUALITES_IA = True
                player.num_of_questions_with_bad_answer = 3
                player.num_of_questions_with_correct_answer = 3
            case "Samuel":
                player.camembert_DEVOPS = True
                player.num_of_questions_with_bad_answer = 4
                player.num_of_questions_with_correct_answer = 4

    user.update_game(game1)

    game2 = user.get_game(game1.id_game) 
    print(game2)

   
                                                     
