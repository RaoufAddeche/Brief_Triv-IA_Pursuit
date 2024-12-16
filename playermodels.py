from sqlmodel import Field, SQLModel
from typing import Optional

class Player(SQLModel, table=True):
    id_player: Optional[int] = Field(default=None, primary_key=True)
    name : str
    num_of_questions_with_correct_answer : int 
    num_of_questions_with_bad_answer : int 
    camenbert_BASES_DE_DONNEES : bool
    camenbert_LANGAGES_DE_PROGRAMMATION : bool
    camenbert_LIGNE_DE_COMMANDES : bool
    camenbert_ACTUALITES_IA : bool
    camenbert_DEVOPS : bool
    camenbert_TECH_IA : bool
