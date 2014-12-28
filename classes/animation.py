
class Animation():
    def __init__(self, sprites, rate=1):
        self.sprites = sprites  # A list of sprites
        self.rate = rate  # How many ticks per frame

        self.frame = 0  # Animation frame counter
        self.counter = 0  # Game tick counter

    def update(self):
        """ Update our tick and frame counter. """
        # Increment counter up to a max of self.rate
        self.counter = (self.counter + 1) % self.rate
        # Once counter reaches our rate, we increment frame
        if self.counter == self.rate - 1:
            # Increment frame up to a maximum of num of sprites
            self.frame = (self.frame + 1) % len(self.sprites)

    def get_sprite(self):
        """ Return the current sprite from the sheet. """
        return self.sprites[self.frame]


