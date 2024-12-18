from database_utils import DatabaseUtils
from questionmodels import Question, Answer
from enums import Themes
from typing import cast
import json

class QuestionData() :
    def __init__(self) :
        pass

    def question_import(self, filename : str) :
        pass

    def question_export(self, filename : str) :
        user = DatabaseUtils()

        questions = []
        for theme in Themes :
            questions.extend(user.get_question_list(theme.value))

        question_list = []
        for question in questions :
            question = cast(Question, question)
            current_question = {}
            current_question["text"] = question.text
            current_question["theme_id"] = question.theme_id
            answers = []
            for answer in question.answers :
                current_answer = {}
                current_answer["text"] = answer.text
                current_answer["is_correct"] = answer.is_correct
                answers.append(current_answer)
                
            current_question["answers"] = answers

            question_list.append(current_question)


        with open(filename, "w") as writing_file :
            text = json.dump( question_list, writing_file)

        
