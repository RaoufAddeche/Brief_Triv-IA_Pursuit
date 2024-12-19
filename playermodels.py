from sqlmodel import Field, Relationship, SQLModel
from typing import Optional
import datetime as dt


class Game(SQLModel, table=True):
    id_game: Optional[int] = Field(default=None, primary_key=True)

    current_round : int = Field(default=1)
    date : dt.datetime

    players : list["Player"]= Relationship(back_populates="game") 
    
    __table_args__ = {'extend_existing': True} 

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

    game_id : Optional[int] = Field(default=None, foreign_key="game.id_game")
    game : Optional[Game] = Relationship(back_populates="players")
    position_id : int = Field(default=0)
    
    __table_args__ = {'extend_existing': True} 

    def is_final_step(self):
        #check si le joueur a tout les camemberts
        return (self.camembert_ACTUALITES_IA and 
                self.camembert_BASES_DE_DONNEES and 
                self.camembert_DEVOPS and 
                self.camembert_LANGAGES_DE_PROGRAMMATION and 
                self.camembert_TECH_IA and 
                self.camembert_LIGNE_DE_COMMANDES)