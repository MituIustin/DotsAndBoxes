import pygame

class Cell:

    point1 = None
    point2 = None
    point3 = None
    point4 = None
    edge1 = None
    edge2 = None
    edge3 = None
    edge4 = None
    points = []
    edges = []

    def __init__(self, point1, point2, point3, point4, edge1, edge2, edge3, edge4):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.point4 = point4
        self.edge1 = edge1
        self.edge2 = edge2
        self.edge3 = edge3
        self.edge4 = edge4
    
    def __str__(self):
        return str(self.point1) + "\n" + str(self.point2) + "\n" + str(self.point3) + "\n" + str(self.point4) 
    
    def contains(self, edge):
        if self.edge1 == edge:
            return True
        if self.edge2 == edge:
            return True
        if self.edge3 == edge:
            return True
        if self.edge4 == edge:
            return True
        return False
    
    def check_full(self):
        if not self.edge1.used:
            return False
        if not self.edge2.used:
            return False
        if not self.edge3.used:
            return False
        if not self.edge4.used:
            return False
        return True
    
    def draw(self, surface, color, size):
        pygame.draw.rect(surface, color, pygame.Rect(self.point1.x, self.point1.y, size, size))