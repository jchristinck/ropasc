import pygame


def write_text(screen, font, location, text, color):
    font.render_to(screen, location, text, color)
    pygame.display.flip()


def game_screen(game, screen, font, times):
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, game.field[0], game.field[1]))
    color = (0, 0, 0)
    for p in game.players:
        if p.faction == 0:
            color = (255, 0, 0)
        elif p.faction == 1:
            color = (0, 255, 0)
        elif p.faction == 2:
            color = (0, 0, 255)
        elif p.faction == 3:
            color = (255, 255, 0)
        elif p.faction == 4:
            color = (0, 255, 255)
        elif p.faction == 5:
            color = (255, 0, 255)
        pygame.draw.rect(screen, color, pygame.Rect(p.pos[0], p.pos[1], 10, 10))
    if game.highlight_player:
        for p in game.players:
            if p.id == game.highlight_id:
                x = p.pos[0] + 5
                y = p.pos[1] + 5
                pygame.draw.circle(screen, (0, 0, 0), (x, y), 10, 5)
                pygame.draw.line(screen, (150, 0, 0), (x, y), (x + p.dirs[0][0], y + p.dirs[0][1]))
                pygame.draw.line(screen, (0, 150, 0), (x, y), (x + p.dirs[1][0], y + p.dirs[1][1]))
                pygame.draw.line(screen, (0, 0, 150), (x, y), (x + p.dirs[2][0], y + p.dirs[2][1]))
    frame_rate = round(len(times) / sum(times) if sum(times) > 0 else 0, 1)
    font.render_to(screen, (1315, 5), str(frame_rate), (255, 255, 255))
    font.render_to(screen, (930, 685), "pause: space", (255, 255, 255))
    font.render_to(screen, (930, 715), "new start: r", (255, 255, 255))
    font.render_to(screen, (930, 750), "reload config: F5", (255, 255, 255))
    font.render_to(screen, (930, 785), "one step: n", (255, 255, 255))
    font.render_to(screen, (930, 820), "toggle highlight player: h", (255, 255, 255))
    font.render_to(screen, (930, 855), "switch player: left & right", (255, 255, 255))
    pygame.display.flip()
