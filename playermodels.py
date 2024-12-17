from sqlmodel import Field, SQLModel
from typing import Optional

class Player(SQLModel, table=True):
    id_player: Optional[int] = Field(default=None, primary_key=True)

    name : str
    num_of_questions_with_correct_answer : int 
    num_of_questions_with_bad_answer : int 
    camembert_BASES_DE_DONNEES : bool
    camembert_LANGAGES_DE_PROGRAMMATION : bool
    camembert_LIGNE_DE_COMMANDES : bool
    camembert_ACTUALITES_IA : bool
    camembert_DEVOPS : bool
    camembert_TECH_IA : bool
    
    __table_args__ = {'extend_existing': True} 
