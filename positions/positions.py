class Position:
    def __init__(self, id, theme_id):
        self.id = id
        self.theme = theme_id
        self.replay = True if (id+1)%7 == 0 else False
        self.iscamembert = True if id%7 == 0 else False
        self.img = str(id) + ".png"

    def move(self, dice, direction):
        """
        return id of the next position
        """
        if direction:
            return (self.id + dice)%42
        else:
            return (self.id - dice)%42


def create_all_position():
    """
    0 : "Bases de données"
    1 : "Langages de programmation"
    2 : "Ligne de commandes"
    3 : "Actualités IA"
    4 : "DevOps"
    5 : "promo tech IA !"
    6 : case de relance
    """
    list_positions = []
    board = [0,1,2,3,4,5,6,2,0,1,3,4,2,6,5,3,2,0,5,4,6,1,3,0,4,5,1,6,3,4,2,5,0,1,6,4,3,1,5,0,2,6]
    for i, b in enumerate(board):
        list_positions.append(Position(i,b))
    return list_positions

