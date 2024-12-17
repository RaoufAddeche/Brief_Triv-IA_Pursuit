from sqlmodel import Field, SQLModel
from typing import Optional

class Question(SQLModel, table=True):
    id_question: Optional[int] = Field(default=None, primary_key=True)
    id_theme : int 
    text : str
    #answers : list["Answer"]  
    __table_args__ = {'extend_existing': True} 

class Answer(SQLModel, table=True):
    id_anwser : Optional[int] = Field(default=None, primary_key=True)
    id_question: int
    text : str
    is_correct : bool
    
    __table_args__ = {'extend_existing': True} 
    