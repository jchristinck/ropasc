import pygame
from configparser import ConfigParser
import screen_updates
import game
import player

if __name__ == "__main__":
    ORANGE = (255, 140, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # initialization
    pygame.init()
    config = ConfigParser()
    config.read('config.ini')
    # print(config.get('rules', 'teams_equal'))

    screen = pygame.display.set_mode((1600, 900))
    pygame.display.set_caption("Rock Paper Scissors Simulator")

    font = pygame.freetype.Font("fonts/Arial.ttf", 36)
    screen_updates.write_text(pygame, screen, font, (635, 350), "initializing game", (255, 255, 255))

    game.initialize()

    state = 1  #
    while state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False

        # logic

    pygame.quit()
