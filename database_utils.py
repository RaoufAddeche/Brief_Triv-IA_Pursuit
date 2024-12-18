
import sqlmodel as sm
from sqlalchemy import Engine
import os
import datetime as dt

import init_db as idb
from enums import Filenames, Themes
from typing import Optional

from playermodels import Game, Player
from questionmodels import Question, Answer

class DatabaseUtils() :
    
    def __init__(self, need_creation = False) :
        self.engine = idb.get_engine()

        need_creation = True
        for filename in os.listdir(os.getcwd()):
            if filename == Filenames.SQLITE_DB:
                need_creation = False
                break

        if need_creation:
            self.create_database()
            
    def create_database(self, delete_old_one = False):
        if delete_old_one :
            os.remove(Filenames.SQLITE_DB)

        echo_object = sm.SQLModel.metadata.create_all(self.engine)

    #__________________________________________________________________________
    #
    # region game
    #__________________________________________________________________________
    def create_game(self) -> int :
        id_game = -1
        with sm.Session(self.engine) as session:
            new_game = Game(current_round=0, date = dt.date.today())
            new_game.players = []
            session.add(new_game)
            session.commit()
            id_game = new_game.id_game

        return id_game
    
    def get_game(self, id_game) -> Game :
        return_game = None
        with sm.Session(self.engine) as session:
            statement = sm.select(Game).where(Game.id_game==id_game)
            results = session.exec(statement)
            return_game = results.one()
            return_game.players = list(return_game.players)
            
        return return_game

    #__________________________________________________________________________
    #
    # region player
    #__________________________________________________________________________

    def get_player_by_id(self, id) -> Optional[Player]:
        with sm.Session(self.engine) as session:
            return session.exec(sm.select(Player).where(Player.id_player == id)).one_or_none()
    
    def create_player(self, id_game: int, player_name :str) -> Optional[Player]:
        with sm.Session(self.engine) as session:
            new_player = Player(
                name=player_name,
                num_of_questions_with_bad_answer=0,
                num_of_questions_with_correct_answer=0,
                camembert_BASES_DE_DONNEES=False,
                camembert_LANGAGES_DE_PROGRAMMATION=False,
                camembert_LIGNE_DE_COMMANDES=False,
                camembert_ACTUALITES_IA=False,
                camembert_DEVOPS=False,
                camembert_TECH_IA=False,
                game_id = id_game)
        
            session.add(new_player)
            session.commit() 
            player_id = new_player.id_player
            
        return self.get_player_by_id(player_id)


    def get_players(self, id_game : int) -> list[Player]:
        list_players = []
        with sm.Session(self.engine) as session:
            statement = sm.select(Player).where(Player.game_id==id_game)
            results = session.exec(statement)
            list_players = list(results)
        return list_players

    def update_player(self, player :Player) :
        with sm.Session(self.engine) as session:
            statement = sm.select(Player).where(Player.id_player == player.id_player)
            results = session.exec(statement)
            session_player = results.one()
            session_player.name = player.name
            session_player.num_of_questions_with_bad_answer = player.num_of_questions_with_bad_answer
            session_player.num_of_questions_with_correct_answer = player.num_of_questions_with_correct_answer
            session_player.camembert_BASES_DE_DONNEES = player.camembert_BASES_DE_DONNEES
            session_player.camembert_LANGAGES_DE_PROGRAMMATION = player.camembert_LANGAGES_DE_PROGRAMMATION
            session_player.camembert_LIGNE_DE_COMMANDES = player.camembert_LIGNE_DE_COMMANDES
            session_player.camembert_ACTUALITES_IA = player.camembert_ACTUALITES_IA
            session_player.camembert_DEVOPS = player.camembert_DEVOPS
            session_player.camembert_TECH_IA = player.camembert_TECH_IA
            session_player.game_id = player.game_id 
        
            session.add(session_player)
            session.commit()

    #__________________________________________________________________________
    #
    # region question
    #__________________________________________________________________________
    def create_question(self, id_theme : int, text :str) -> int : 
        id_question = 0
        with sm.Session(self.engine) as session:
            new_question = Question(theme_id=id_theme, text = text)
            session.add(new_question)
            session.commit()
            id_question = new_question.id_question

        return id_question
    
    def get_question(self, id_question : int) -> Question :
        return_question = None
        with sm.Session(self.engine) as session:
            statement = sm.select(Question).where(Question.id_question==id_question)
            results = session.exec(statement)
            return_question = results.one()
            return_question.answers = list(return_question.answers)
            
        return return_question

    def get_question_list(self, id_theme : int) -> list[Question] :
        question_list = []
        with sm.Session(self.engine) as session:
            statement = sm.select(Question).where(Question.theme_id==id_theme) 
            results = session.exec(statement)
            question_list = list(results)
            for question in question_list :
                question.answers = list(question.answers)

        return question_list
    
    #__________________________________________________________________________
    #
    # region answer
    #__________________________________________________________________________
    def create_answer(self, id_question : int, text :str, is_correct : bool) :
        with sm.Session(self.engine) as session:
            new_answer = Answer(question_id=id_question, text = text, is_correct = is_correct)
            session.add(new_answer)
            session.commit()

    