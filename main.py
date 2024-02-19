import pygame
import screen_updates
from configparser import ConfigParser
from game import Game
import time
import timeit
import collections


if __name__ == "__main__":
    WINDOW = (1400, 900)
    FIELD = (WINDOW[0] - 500, WINDOW[1])

    # initialization
    pygame.init()
    config = ConfigParser()
    config.read('config.ini')
    min_frame_time = float(config.get('rules', 'min_frame_time'))
    screen = pygame.display.set_mode(WINDOW)
    pygame.display.set_caption("Rock Paper Scissors Simulator")
    font = pygame.freetype.Font("fonts/Arial.ttf", 36)
    game = Game(config, FIELD)
    times = collections.deque(maxlen=10)

    state = 2  # 0 stop, 1 pausing, 2 running, 3 one step
    while state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    state = 2 if state == 1 else 1
                elif keys[pygame.K_ESCAPE]:
                    state = 0
                elif keys[pygame.K_h]:
                    game.highlight_player = not game.highlight_player
                elif keys[pygame.K_n]:
                    state = 3
                elif keys[pygame.K_F5]:
                    game.reload_config = True
                elif keys[pygame.K_r]:
                    game.players = game.new_players()
                elif keys[pygame.K_LEFT]:
                    game.highlight_id = game.highlight_id - 1 if game.highlight_id > 0 else len(game.players) - 1
                elif keys[pygame.K_RIGHT]:
                    game.highlight_id = game.highlight_id + 1 if game.highlight_id < len(game.players) else 0
        if state == 1:
            screen_updates.game_screen(game, screen, font, times)
        if state >= 2:
            start_time = timeit.default_timer()
            game.step(screen, font, times)
            screen_updates.game_screen(game, screen, font, times)
            simulation_time = timeit.default_timer() - start_time
            if simulation_time < min_frame_time:
                time.sleep(min_frame_time - simulation_time)
            times.append(timeit.default_timer() - start_time)
            if state == 3:
                state = 1
        if game.reload_config:
            config.read('config.ini')
            del game
            game = Game(config, FIELD)
    pygame.quit()
