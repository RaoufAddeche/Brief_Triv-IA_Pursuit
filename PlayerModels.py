from sqlmodel import Field, SQLModel
from typing import Optional

class Player(SQLModel, table=True):
    id_player: Optional[int] = Field(default=None, primary_key=True)
    num_of_questions_with_correct_answer : int 
    num_of_questions_with_bad_answer : int 
    camenberts : list[int]
