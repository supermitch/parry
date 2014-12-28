import hero

class World(object):
    """ A class to hold all the game elements. """

    def __init__(self, screen_size, assets):
        self.screen_size = screen_size
        self.assets = assets

        self.hero = self.__add_hero()
        self.monster = self.__add_monster()


    def __add_hero(self):
        """ Add our hero to bottom of the screen. """
        sprites = self.assets.images['hero']
        pos = 100, 100
        return hero.Hero(sprites, pos)

    def __add_monster(self):
        sprites = self.assets.images['monster']
        pos = 200, 110
        return hero.Hero(sprites, pos)


    def update(self):
        """ Update all the elements of the world. """

        self.hero.update()
        self.monster.update()

