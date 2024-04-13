
import cell
import edge
import point
import copy

class State:

    player1_score = 0
    player2_score = 0
    cells = []
    edges = []
    
    def __init__(self, game):
        self.player1_score = copy.deepcopy(game.player1_score)
        self.ai_cells = copy.deepcopy(game.player2_score)

        self.cells = copy.deepcopy(game.cells)
        self.edges = copy.deepcopy(game.edges)


    def add_edge(self, i):
        self.edges[i].used = True
    
        possible_cells = []
        for cell in self.cells:
            if cell.contains(self.edges[i]):
                possible_cells.append(cell)
        
        for cell in possible_cells:
            if cell.check_full():
               self.player2_score += 1