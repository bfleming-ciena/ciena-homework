"""General routines to the game universe."""
from math import sqrt


class Colors:
    """pregen colors."""

    BLACK = (0, 0, 0)
    GRAY = (150, 150, 150)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    ORANGE = (255, 100, 0)


class GameConfig:
    """Configurable options. Globals, basically."""

    NUM_ENEMIES = 50
    ROOM = 0
    NUM_ROOMS = 5
    DISPLAY_WIDTH = 400
    DISPLAY_HEIGHT = 600


class Observer:
    """Routes to watch over what's happening in the world."""

    def __init__(self):
        """Initialize defaults."""

    def distance(self, hero, enemy):
        """Distance between two objects."""
        x2 = (enemy.x - hero.x) ** 2
        y2 = (enemy.y - hero.y) ** 2
        dist = sqrt(x2 + y2)
        return dist

    def check_battle(self, hero, enemy):
        """Determine if an enemy is in fighting distance and enages their weapon."""
        dist = self.distance(hero, enemy)

        if dist <= 40:
            enemy.wield_weapon(True)
            return True
        else:
            enemy.wield_weapon(False)
            return False


class Arena:
    """Battle ground. Does the battle computations."""

    def __init__(self):
        """initalizer."""
        self.observer = Observer()

    def battle(self, hero, enemy):
        """Queue star trek fighting music."""
        if hero.weapon_active:
            # Hero wepon is active, so the hero will be doing damage too.
            hero.attack(enemy)
            if enemy.alive is False:
                hero.rack_kill()
            enemy.attack(hero)
        elif hero.moving:
            enemy.attack(hero)
