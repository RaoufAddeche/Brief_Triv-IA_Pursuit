
from database_utils import DatabaseUtils
from enums import Themes
from question_data import QuestionData

if __name__ == "__main__" :

    question_data = QuestionData()
    #question_data.question_export("all_data.json")

    user = DatabaseUtils()
    user.create_database(True)

    question_data.question_import("all_data.json")



