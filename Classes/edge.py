
class Edge:

    point1 = None
    point2 = None
    used = False
    orizontal = False
    m = 0

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def __eq__(self, other):
        if self.point1 != other.point1:
            return False
        if self.point2 != other.point2:
            return False
        if self.orizontal != other.orizontal:
            return False
        return True
    
    def __str__(self):
        return str(self.point1) + "\n" + str(self.point2)