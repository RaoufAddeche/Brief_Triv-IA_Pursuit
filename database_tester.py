
from database_utils import DatabaseUtils
from enums import Themes
from question_data import QuestionData

if __name__ == "__main__" :

    question_data = QuestionData()
    #question_data.question_export("all_data.json")

    user = DatabaseUtils()
    user.create_database(True)

    question_data.question_import("all_data.json")

    # id_question= user.create_question(Themes.BASES_DE_DONNEES.value, "Trouvez l'intrus")
    # user.create_answer(id_question, "SQL Server", False)
    # user.create_answer(id_question, "Oracle", False)
    # user.create_answer(id_question, "MongoDB", False)
    # user.create_answer(id_question, "Turtle DB", True)

    # id_question= user.create_question(Themes.BASES_DE_DONNEES.value, "Quelle est la base de données de Google Maps ?")
    # user.create_answer(id_question, "Elasticsearch", False)
    # user.create_answer(id_question, "Bigtable", True)
    # user.create_answer(id_question, "PostgreSQL", False)
    # user.create_answer(id_question, "Cassandra", False)

    # questions = user.get_question_list(Themes.BASES_DE_DONNEES.value)
    # for question in questions :
    #     print("______________________________________________")
    #     print(question.text)
    #     for answer in question.answers :
    #         print(f"  {answer.text}, is_correct={answer.is_correct}")

    
    







    # list_players = user.get_players()


