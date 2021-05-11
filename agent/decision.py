
class Decision(object):

    def __init__(self, environment, direction):
        self.environment = environment
        self.direction = direction
        self.rating = 0

    def set_rating(self, rating: float):
        self.rating = rating
