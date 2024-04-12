

class State:

    user_cells = 0
    ai_cells = 0
    
    def __init__(self, user_score = 0, ai_score = 0):
        self.user_cells = user_score
        self.ai_cells = ai_score