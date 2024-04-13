
import pygame
import time
import math

from cell import Cell
from edge import Edge
from point import Point
from state import State

class Game:

    def a_star(self):
        return
    
    def min_max(self, state, depth, alpha, beta, maximize):
        if depth == 0:
            return [-1, state.player2_score - state.player1_score]
        
        states = []
        for (i, edge) in enumerate(state.edges):
            if edge.used == False:  
                temp_state = State(state)   
                temp_state.add_edge(i)     
                states.append([i,temp_state])
                

        if maximize:
            max_val = -999
            
            for state in states:
                index, eval = self.min_max(state[1], depth - 1, alpha, beta, False)
                if eval >= max_val:
                    max_val = eval
                    index = state[0]
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return index, max_val
        else:
            min_val = 999
            for state in states:
                index, eval = self.min_max(state[1], depth - 1, alpha, beta, True)
                if eval <= min_val:
                    min_val = eval
                    index = state[0]
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return index, min_val

    def bayes(Self):
        return 

    # algorithm handler

    def next_state(self, current_state):
        if self.algorithm == 0:
            self.current_state = self.a_star(current_state)
        if self.algorithm == 1:
            self.current_state = State(self)
            l = self.min_max(current_state, self.depth + 1, -9999, 9999, True)
            print(l)
            return l[0]
        if self.algorithm == 2:
            self.current_state = self.bayes(current_state)

    # draws the white points
            
    def draw_points(self):
        for point in self.points:
            pygame.draw.circle(self.window, 
                                self.colors["white"], 
                                (point.x, point.y),
                                5)

    # draws the edges between points
            
    def draw_edges(self):
        for i, edge in enumerate(self.edges):
            if edge.used == True:
                if edge.orizontal == True:
                    x = edge.point1.x - 2
                    y = edge.point1.y + 3
                    rect_width = 5
                    rect_height = self.padding - 5
                    pygame.draw.rect(self.window,
                                    self.colors["green"],
                                    (x,
                                    y,
                                    rect_width,
                                    rect_height))
                else:
                    x = edge.point2.x - self.padding + 3
                    y = edge.point2.y - 2
                    rect_width = self.padding - 5
                    rect_height = 5
                    pygame.draw.rect(self.window,
                                    self.colors["green"],
                                    (x,
                                    y,
                                    rect_width,
                                    rect_height))
     

    # draw the players scores

    def draw_text(self):
        font = pygame.font.Font('freesansbold.ttf', 32)

        text = font.render("P1 Score = " + str(self.player1_score) , True, self.colors["blue"], self.colors["black"])
        textRect = text.get_rect()
        textRect.center = (150, 50)

        text2 = font.render("P2 Score = " + str(self.player2_score) , True, self.colors["red"], self.colors["black"])
        textRect2 = text2.get_rect()
        textRect2.center = (450, 50)

        self.window.blit(text, textRect)
        self.window.blit(text2, textRect2)

    def user_move(self, event):
        
        (index_point1, index_point2) = self.determine_points_user(event.pos[0], event.pos[1])
        index_edge_user = self.determine_edge_user(index_point1, index_point2)
        
        if self.edges[index_edge_user].used:
            print("Allready used!")
            self.user_turn = True
            return
    
        self.edges[index_edge_user].used = True

        possible_cells = []
        for cell in self.cells:
            if cell.contains(self.edges[index_edge_user]):
                possible_cells.append(cell)
        
        again = False
        
        for cell in possible_cells:
            if cell.check_full():
                again = True
                if self.user_blue:
                    self.player1_score += 1
                    cell.draw(self.window, self.colors["blue"], self.cell_size)
                else:
                    self.player2_score += 1
                    cell.draw(self.window, self.colors["red"], self.cell_size)
        
        #time.sleep(1)
        self.end = self.game_over()
        if self.end:
            return
        
        self.user_turn = again
        
        self.ai_move()

    def ai_move(self):
        
        index_edge_ai = self.next_state(self)
        self.edges[index_edge_ai].used = True

        possible_cells = []
        for cell in self.cells:
            if cell.contains(self.edges[index_edge_ai]):
                possible_cells.append(cell)
        
        again = False
        
        for cell in possible_cells:
            if cell.check_full():
                again = True
                if not self.user_blue:
                    self.player1_score += 1
                    cell.draw(self.window, self.colors["blue"], self.cell_size)
                else:
                    self.player2_score += 1
                    cell.draw(self.window, self.colors["red"], self.cell_size)
        
        self.end = self.game_over()
        if self.end:
            return
        
        if again:
            self.ai_move()

        self.user_turn = True

    def make_move(self, event):

        if self.user_turn:
            self.user_move(event)
        else:
            self.ai_move()
        

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end = True
            if self.user_turn and event.type == pygame.MOUSEBUTTONDOWN:
                self.make_move(event)
                    
    # checks if game is over
                
    def game_over(self):
        return False

    # creates simply dictionary of colors

    def create_colors(self):
        colors = {}
        colors["white"] = (255, 255, 255)
        colors["red"] = (252, 91, 122)
        colors["blue"] = (78, 193, 255)
        colors["green"] = (0, 255, 0)
        colors["black"] = (12, 12, 12)
        return colors

    # creates the white points

    def create_points(self):
        points = []
        for row in range(self.rows + 1):
            for col in range(self.cols + 1):
                x = row * self.cell_size + 2 * self.padding
                y = col * self.cell_size + 3 * self.padding
                point = Point(x, y)
                points.append(point)
        return points

    # creates the edges between points

    def create_edges(self):
        edges = []
        for j in range(self.rows + 1):
            for i in range(self.cols):
                new_edge = Edge(self.points[i + (self.cols + 1) * j], self.points[i + 1 + (self.cols + 1) * j])
                new_edge.used = False
                new_edge.orizontal = True
                edges.append(new_edge)

        for j in range(self.cols):
            for i in range(self.rows + 1):
                new_edge = Edge(self.points[i + (self.cols + 1) * j], self.points[i + (self.cols + 1) * (j + 1)])
                new_edge.used = False
                new_edge.orizontal = False
                edges.append(new_edge)
        return edges

    # creates the cells

    def create_cells(self):
        cells = []
        for j in range(self.rows):
            for i in range(self.cols):
                point1 = self.points[i + (self.cols + 1) * j]
                point2 = self.points[i + 1 + (self.cols + 1) * j]
                point3 = self.points[i + (self.cols + 1) * (j + 1) + 1]
                point4 = self.points[i + (self.cols + 1) * (j + 1)]
                edge1 = self.edges[self.determine_edge_user(i + (self.cols + 1) * j, i + 1 + (self.cols + 1) * j)]
                edge2 = self.edges[self.determine_edge_user(i + 1 + (self.cols + 1) * j, i + (self.cols + 1) * (j + 1) + 1)]
                edge3 = self.edges[self.determine_edge_user(i + (self.cols + 1) * (j + 1) + 1, i + (self.cols + 1) * (j + 1))]
                edge4 = self.edges[self.determine_edge_user(i + (self.cols + 1) * j, i + (self.cols + 1) * (j + 1))]
                new_cell = Cell(point1, point2, point3, point4, edge1, edge2, edge3, edge4)
                cells.append(new_cell)
        return cells
    
    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) )

    # returns the points based on the location of the mouse

    def determine_points_user(self, x, y):
        index0 = -1
        index1 = -1
        min_distance = 99999999
        

        for i, point in enumerate(self.points):
            dist = self.distance(x, y, point.x, point.y) 
            if dist < min_distance:
                min_distance = dist
                index0 = i
        min_distance = 99999999

        for i, point in enumerate(self.points):
            dist = self.distance(x, y, point.x, point.y) 
            if dist < min_distance and i != index0:
                min_distance = dist
                index1 = i
        return (index0, index1)

    # returns the index of the edge based on the points

    def determine_edge_user(self, index1, index2):
        for i, edge in enumerate(self.edges):
            if edge.point1 == self.points[index1] and edge.point2 == self.points[index2]:
                return i
            if edge.point2 == self.points[index1] and edge.point1 == self.points[index2]:
                return i
        return None
    
    # game constructor

    def __init__(self):

        self.width = 600                    # width of the window
        self.height = 600                   # height of the window
        self.cell_size = 40                 # the size of a cell
        self.padding = 40                   # padding for margins of the windows
        self.rows = self.cols = 11          # number of rows and columns


        self.user_blue = True
        self.user_turn = True  

        self.pos = None                     

        self.colors = self.create_colors()
        self.points = self.create_points()
        self.edges = self.create_edges()
        self.cells = self.create_cells()
        self.player1_score = 0
        self.player2_score = 0
        self.current_state = State(self)    # current_state, updated every move
        self.states = []
        self.difficulty = 0                 # 0 -> easy, 1 -> medium, 2 -> hard
        self.end = False                    # is game finished
        self.algorithm = 1                  # 0 -> A*, 1 -> MinMax, 2 -> Bayes Networks

        self.depth = 1
    

        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height))        # creates the main window
        
        self.draw_points()
        # while game is running
        
        while not self.end:
            
            self.event_handler()
            self.draw_edges()
            self.draw_text()

            pygame.display.update()
        pygame.quit()

game = Game()


"""
p1 e1 p2

e4    e2

p4 e3 p3

"""