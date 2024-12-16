from sqlmodel import Field, SQLModel
from typing import Optional

class Question(SQLModel, table=True):
    id_question: Optional[int] = Field(default=None, primary_key=True)
    id_theme : int 
    text : str
    answers : list["Answer"]  

class Answer(SQLModel, table=True):
    id_anwser : Optional[int] = Field(default=None, primary_key=True)
    id_question: int
    id_theme : int 
    text : str
    