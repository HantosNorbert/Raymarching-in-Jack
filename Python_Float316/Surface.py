# A class for surface objects defined at a specific point:
# contains a signed distance from the closest object and its
# color. Technically a Vec2 with a specific purpose.
from Float316 import Float316

class Surface:
    def __init__(self, sd: Float316, col: Float316):
        self.sd = sd
        self.col = col
