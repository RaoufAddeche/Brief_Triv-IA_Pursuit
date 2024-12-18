class Position:
    def __init__(self, id, theme_id):
        self.id = id
        self.theme = theme_id
        self.replay = True if (id+1)%7 == 0 else False
        self.iscamembert = True if id%7 == 0 else False
        self.img = str(id) + ".png"

    def __repr__(self):
        return str(self.id)

    def move(self, dice, direction):
        """
        return id of the next position
        """
        if direction:
            return (self.id + dice)%42
        else:
            return (self.id - dice)%42
        
    def move_to_win(self):
        position = str(self.id)
        return int(position[:-1])


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

def create_center_position():
    """
    create position for diagonales of the circle
    list_center_positions = [[list of first diag], ... , [list of last diag], center_position]
    """
    list_center_positions = []
    diagonale_board = [9914325,9905143,9941032,9943205,9921540,9935201]
    for item in diagonale_board:
        list_positions = []
        position = str(item)
        for i in range(5):
            list_positions.append(Position(int(position),int(position[-1])))
            position = position[:-1]
        list_center_positions.append(list_positions)
    list_center_positions.append(Position(99,7)) # center position
    return list_center_positions


