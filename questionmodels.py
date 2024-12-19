from sqlmodel import Field, Relationship, SQLModel
from typing import Optional

class Question(SQLModel, table=True):
    id_question: Optional[int] = Field(default=None, primary_key=True)
    theme_id : int = Field()
    text : str = Field()

    answers : list["Answer"]= Relationship(back_populates="question") 

    __table_args__ = {'extend_existing': True} 

class Answer(SQLModel, table=True):
    id_answer : Optional[int] = Field(default=None, primary_key=True)
    text : str = Field()
    is_correct : bool = Field()

    question_id : Optional[int] = Field(default=None, foreign_key="question.id_question")
    question : Optional[Question] = Relationship(back_populates="answers")
    
    __table_args__ = {'extend_existing': True} 
    