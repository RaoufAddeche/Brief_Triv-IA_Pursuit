from sqlmodel import Field, Relationship, SQLModel
from typing import Optional

class Question(SQLModel, table=True):
    id_question: Optional[int] = Field(default=None, primary_key=True)
    id_theme : int 
    text : str
    answers : list["Answer"]= Relationship(back_populates="question") 

class Answer(SQLModel, table=True):
    id_anwser : Optional[int] = Field(default=None, primary_key=True)
    text : str
    is_correct : bool

    question_id: Optional[int] = Field(default=None, foreign_key="question.id_question")
    question :Optional[Question] = Relationship(back_populates="answers")
    