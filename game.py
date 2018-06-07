"""Ciena homework."""
import pygame
import random
from characters import Hero, Toadman, Frostgiant
from weapons import Hammer, Scimitar, Crossbow
from g_environment import Observer, Arena, Colors, GameConfig

pygame.init()
gameDisplay = pygame.display.set_mode((GameConfig.DISPLAY_WIDTH, GameConfig.DISPLAY_HEIGHT))
pygame.display.set_caption('Ciena Gaming - A New Venture')


def text_objects(text, font):
    """Texture surface needed prior to drawing."""
    textsurface = font.render(text, True, Colors.WHITE)
    return textsurface, textsurface.get_rect()


def message_display(text, x, y, size):
    """Use this for game over message etc..."""
    thefont = pygame.font.Font('freesansbold.ttf', size)
    TextSurf, TextRect = text_objects(text, thefont)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)


def init_enemies():
    enemies = []
    for i in range(GameConfig.NUM_ENEMIES):
        toady = Toadman(gameDisplay, random.randint(1,GameConfig.DISPLAY_WIDTH), -random.randint(1, GameConfig.DISPLAY_HEIGHT * GameConfig.NUM_ROOMS))
        toady.equip(Scimitar())
        enemies.append(toady)

    for i in range(int(GameConfig.NUM_ENEMIES * 2)):
        frosty = Frostgiant(gameDisplay, random.randint(1,GameConfig.DISPLAY_WIDTH), -random.randint(1, GameConfig.DISPLAY_HEIGHT * GameConfig.NUM_ROOMS))
        frosty.equip(Crossbow())
        enemies.append(frosty)

    return enemies

def init_hero():
    hero = Hero(gameDisplay, 175, 450)
    # With his mighty hammer
    hero.equip(Hammer())
    return hero

def start_game():

    # Init objects to detect and engage combat events
    arena = Arena()
    observer = Observer()

    # Our mighty ninja

    # Throw down a bunch of enemies

    enemies = init_enemies()
    hero = init_hero()

    # Pygame pacing
    clock = pygame.time.Clock()
    playing = True
    x_change = 0
    y_change = 0
    restart = False
    while playing is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                    hero.moving = True
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                    hero.moving = True
                if event.key == pygame.K_UP:
                    y_change = -5
                    hero.moving = True
                if event.key == pygame.K_DOWN:
                    y_change = 5
                    hero.moving = True
                if event.key == pygame.K_r:
                    restart = True
                if event.key == pygame.K_q:
                    playing = False
                    continue

                # Hero attack event
                if (event.key == pygame.K_SPACE) and (event.type == pygame.KEYDOWN):
                    hero.wield_weapon(True)
            else:
                hero.moving = False

            # Hero has stopped attacking
            if event.type == pygame.KEYUP:
                    x_change = 0
                    y_change = 0
                    if event.key == pygame.K_SPACE:
                        hero.wield_weapon(False)

        # Move hero in response to user input
        hero.move(x_change, y_change)

        # Keeps the hero from going backard in the first ROOM,
        # and the rest of the section allows the hero to move
        # from ROOM to ROOM, giving the illusion of movement.
        if hero.y > GameConfig.DISPLAY_HEIGHT:
            if GameConfig.ROOM == 0:
                hero.y = GameConfig.DISPLAY_HEIGHT - 32
            else:
                hero.y = 0
                for i in enemies:
                    i.move(0, -GameConfig.DISPLAY_HEIGHT)
                GameConfig.ROOM = GameConfig.ROOM - 1

        if hero.y < 0:
            hero.y = GameConfig.DISPLAY_HEIGHT
            GameConfig.ROOM = GameConfig.ROOM + 1
            for i in enemies:
                i.move(0, GameConfig.DISPLAY_HEIGHT)

        # Background screen.
        gameDisplay.fill(Colors.GRAY)

        # All alive enemies will hunt for the hero. If he gets close they will chase him.
        for i in enemies:
            if not i.alive:
                i.render()
            else:
                i.hunt(hero)
                # Check if the hero and an enemy are in fighting range and then let them battle.
                if observer.check_battle(hero, i):
                    arena.battle(hero, i)
                i.render()

        if hero.alive:
            hero.render()

        if GameConfig.ROOM >= GameConfig.NUM_ROOMS:
            message_display("YOU WIN!!   Kills: " + str(hero.kills), 200, 200, 18)
            message_display("Press R to restart", 200, 300, 18)
            for i in enemies:
                i.alive = False
                i.hide = True
            if restart:
                enemies = init_enemies()
                hero = init_hero()
                GameConfig.ROOM = 0
                restart = False

        if not hero.alive:
            message_display("GAME OVER!", 200, 200, 20)
            message_display("Press R to restart", 200, 300, 18)
            for i in enemies:
                i.alive = False

            if restart:
                enemies = init_enemies()
                hero = init_hero()
                GameConfig.ROOM = 0
                restart = False

        if GameConfig.ROOM == 0:
            message_display("Arrow Keys - Go forward.", 200, 200, 20)
            message_display("R - Restart", 200, 250, 20)
            message_display("Q- Quit", 200, 300, 20)
            message_display("Spacebar - Attack", 200, 350, 20)
            message_display("Sneak and kill strategically!", 200, 400, 20)
        # Hero health bar.
        message_display("Health", 20, 20, 12)
        if hero.health < (hero.max_health * .25):
            color = Colors.RED
        elif hero.health < (hero.max_health * .75):
            color = Colors.ORANGE
        else:
            color = Colors.GREEN
        pygame.draw.rect(gameDisplay, color, (10, 30, hero.health / 10, 10))
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()


if __name__ == "__main__":
    start_game()