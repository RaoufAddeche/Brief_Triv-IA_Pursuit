from enum import Enum, StrEnum

class Filenames(StrEnum):
    SQLITE_DB = "triv-IA_Pursuit.db"

class Themes(Enum):
    BASES_DE_DONNEES : 0
    LANGAGES_DE_PROGRAMMATION : 1
    LIGNE_DE_COMMANDES : 2
    ACTUALITES_IA : 3
    DEVOPS : 4
    TECH_IA : 5
    