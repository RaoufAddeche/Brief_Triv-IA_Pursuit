from enums import Filenames
import sqlmodel as sm
from sqlalchemy import Engine
import os

import init_db as idb

from playermodels import Player
from questionmodels import Question, Answer

class DatabaseUser() :

    def __init__(self) :
        self.engine = idb.get_engine()

        # Vérification de l'existence de la base de données pour décider si elle doit être créée
        need_creation = True
        for filename in os.listdir(os.getcwd()):
            if filename == Filenames.SQLITE_DB:
                need_creation = False
                break

        # Si la base de données n'existe pas, on la crée
        if need_creation:
            echo_object = sm.SQLModel.metadata.create_all(self.engine)

    def create_question(self, id_theme : int, text :str) -> int :
        id_question = 0
        with sm.Session(self.engine) as session:
            new_question = Question(id_theme=id_theme, text = text)
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

        return return_question

    def get_question_list(self, id_theme : int) -> list[Question] :
        question_list = []
        with sm.Session(self.engine) as session:
            statement = sm.select(Question) 
            results = session.exec(statement)
            question_list = list(results)

        return question_list

    def create_answer(self, id_question : int, text :str, is_correct : bool) :
        with sm.Session(self.engine) as session:
            new_answer = Answer(id_question=id_question, text = text, is_correct = is_correct)
            session.add(new_answer)
            session.commit()

    def create_player(self, name :str) :
        with sm.Session(self.engine) as session:
            new_player = Player(
                name=name,
                num_of_questions_with_bad_answer=0,
                num_of_questions_with_correct_answer=0,
                camenbert_BASES_DE_DONNEES=False,
                camenbert_LANGAGES_DE_PROGRAMMATION=False,
                camenbert_LIGNE_DE_COMMANDES=False,
                camenbert_ACTUALITES_IA=False,
                camenbert_DEVOPS=False,
                camenbert_TECH_IA=False)
            session.add(new_player)
            session.commit()

if __name__ == "__main__" :
    user = DatabaseUser()
    user.create_player("Nicolas")
    user.create_player("Victor")
    user.create_player("Raouff")
    user.create_player("Samuel")

    id_question= user.create_question(0, "Trouvez l'intrus")
    user.create_answer(id_question, "SQL Server", False)
    user.create_answer(id_question, "Oracle", False)
    user.create_answer(id_question, "Mongo DB", False)
    user.create_answer(id_question, "Turtle DB", True)

    



