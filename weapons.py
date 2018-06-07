"""The armory."""
import pygame


class Weapon:
    """Base class."""

    def __init__(self):
        """Initialize defaults."""
        self.name = "Unknown"
        self.damage = 0

    def set_damage(self, damage):
        """Can change the damage value of the weapon. Upgrades, etc..."""
        self.damage = damage

    def use(self):
        """Weapon is used, returns the damage it does."""
        return self.damage


class BareHands(Weapon):
    """You're in trouble."""

    def __init__(self):
        """Initialize defaults."""
        self.name = "Hands"
        self.damage = 0
        self.img = pygame.image.load('images/hand.png')


class Hammer(Weapon):
    """Have a nail."""

    def __init__(self):
        """Initialize defaults."""
        self.name = "Hammer"
        self.damage = 2
        self.img = pygame.image.load('images/hammer.png')


class Scimitar(Weapon):
    """Price of thieves/toads."""

    def __init__(self):
        """Initialize defaults."""
        self.name = "Scimitar"
        self.damage = 1
        self.img = pygame.image.load('images/scimitar.png')

    # def attack(self)
        # return self.damage


class Crossbow(Weapon):
    """Where's chewbacca."""

    def __init__(self):
        """Initialize defaults."""
        self.name = "CrossBow"
        self.damage = 10
        self.img = pygame.image.load('images/crossbow.png')
