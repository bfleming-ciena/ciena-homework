"""test."""
import pygame
from math import sin, cos, pi, radians, sqrt
from weapons import BareHands
from g_environment import GameConfig
import random


class Character:
    """General base class for objects in the world."""

    def __init__(self, gamedisplay, init_x=0, init_y=0):
        """Initialize defaults."""
        self.img = pygame.image.load('images/hand.png')
        self.gamedisplay = gamedisplay
        self.x = init_x
        self.y = init_y
        self.health = 50
        self.alive = True
        self.weapon = BareHands()
        self.weapon_active = False
        self.hide = False

    def equip(self, weapon):
        """Take a weapon object and assigns it to this character."""
        self.weapon = weapon

    def wield_weapon(self, wield_weapon):
        """Set state of character using their weapon."""
        self.weapon_active = wield_weapon

    def take_damage(self, damage):
        """Simple register damage and check if dead."""
        self.health = self.health - damage
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.img = pygame.image.load('images/tomestone.png')

    def move(self, x, y):
        """Increment movement, called during the game loop to animate the characters."""
        self.x = self.x + x
        self.y = self.y + y

    def attack(self, opponent):
        """Initialize defaults."""
        opponent.take_damage(self.weapon.use())

        # Not used, but maybe we want to see the damage.
        return self.weapon.use()

    def render(self):
        """Initialize defaults."""
        self.gamedisplay.blit(self.img, (self.x_c, self.y_c))


class Frostgiant(Character):
    """Frosty."""

    def __init__(self, gamedisplay, init_x=0, init_y=0):
        """Init defaults."""
        super().__init__(gamedisplay, init_x, init_y)
        self.angle = radians(45)  # for animation
        self.img = pygame.image.load('images/frostgiant.png')
        self.health = 75
        self.hunt_speed = 1

    def render(self):
        """Display the object on the game board."""
        if self.hide is True:
            return

        if self.alive is False:
            self.gamedisplay.blit(self.img, (self.x, self.y))
            return

        # Little animation moving them in a small circle.
        self.angle = self.angle + random.randint(1, 5)
        self.x_c = self.x + 2 * cos(radians(self.angle))
        self.y_c = self.y - 2 * sin(radians(self.angle))

        self.gamedisplay.blit(self.img, (self.x_c, self.y_c))

        # Show the weapon icon and the health bar during combat
        if self.weapon_active:
            self.gamedisplay.blit(self.weapon.img, (self.x_c - 10, self.y_c - 10))
            pygame.draw.rect(self.gamedisplay, (255, 0, 0), (self.x_c, self.y_c, int(self.health), 1))

    def hunt(self, player):
        """Move toward the player."""
        x2 = (self.x - player.x) ** 2
        y2 = (self.y - player.y) ** 2
        dist = sqrt(x2 + y2)

        if (player.moving is True) and (dist < 75 and dist > 10):
            if player.x > self.x:
                self.x = self.x + self.hunt_speed

            if player.x < self.x:
                self.x = self.x - self.hunt_speed

            if player.y > self.y:
                self.y = self.y + self.hunt_speed

            if player.y < self.y:
                self.y = self.y - self.hunt_speed


class Toadman(Character):
    """Toady."""

    def __init__(self, gamedisplay, init_x=0, init_y=0):
        """Initi defaults."""
        super().__init__(gamedisplay, init_x, init_y)
        self.angle = radians(45)
        self.img = pygame.image.load('images/toadman.png')
        self.hunt_speed = 2

    def render(self):
        """Display object on the game board."""
        if self.hide is True:
            return

        if self.alive is False:
            self.gamedisplay.blit(self.img, (self.x, self.y))
            return

        self.angle = self.angle + random.randint(1, 5)

        self.x_c = self.x + 2 * cos(radians(self.angle))
        self.y_c = self.y - 2 * sin(radians(self.angle))

        self.gamedisplay.blit(self.img, (self.x_c, self.y_c))

        if self.weapon_active:
            self.gamedisplay.blit(self.weapon.img, (self.x_c - 10, self.y_c - 10))
            pygame.draw.rect(self.gamedisplay, (255, 0, 0), (self.x_c, self.y_c, int(self.health), 1))

    def hunt(self, player):
        """Iincremnetally move toward the player."""
        x2 = (self.x - player.x) ** 2
        y2 = (self.y - player.y) ** 2
        dist = sqrt(x2 + y2)

        if (player.moving is True) and (dist < 75 and dist > 10):
            if player.x > self.x:
                self.x = self.x + self.hunt_speed

            if player.x < self.x:
                self.x = self.x - self.hunt_speed

            if player.y > self.y:
                self.y = self.y + self.hunt_speed

            if player.y < self.y:
                self.y = self.y - self.hunt_speed


class Hero(Character):
    """Hero, ninja."""

    def __init__(self, gamedisplay, init_x=0, init_y=0):
        """Init defaults."""
        super().__init__(gamedisplay, init_x, init_y)
        self.alive = True
        self.health = 2000
        self.max_health = 2000
        self.kills = 0
        self.moving = False

    def move(self, x, y):
        """Increment of movement, called from the game loop to animate the character."""
        # Don't let him go off the screen left or right
        if self.x + x <= 1:
            x = 0
        if self.x + x >= GameConfig.DISPLAY_WIDTH - 32:
            x = 0

        super().move(x, y)

    def rack_kill(self):
        """Hero will track his kills."""
        self.kills = self.kills + 1

    def render(self):
        """Draw him and his state."""
        self.x_c = self.x
        self.y_c = self.y

        if self.weapon_active:
            self.img = pygame.image.load('images/ninja.png')
        elif self.moving:
            self.img = pygame.image.load('images/ninja.png')
        else:
            self.img = pygame.image.load('images/stealth.png')

        self.gamedisplay.blit(self.img, (self.x_c, self.y_c))

        # Put the weapon a bit offset so it's visible.
        if self.weapon_active:
            self.gamedisplay.blit(self.weapon.img, (self.x_c + 20, self.y_c - 10))
