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
                font.render_to(screen, (930, 400), str(p.speed), (255, 255, 255))
                font.render_to(screen, (930, 440), str(p.hunt_range), (255, 255, 255))
                font.render_to(screen, (930, 480), str(p.avoid_range), (255, 255, 255))
                font.render_to(screen, (930, 520), str(p.escape_range), (255, 255, 255))
                font.render_to(screen, (930, 560), str(p.conquer_range), (255, 255, 255))
                x = p.pos[0] + 5
                y = p.pos[1] + 5
                pygame.draw.circle(screen, (0, 0, 0), (x, y), 10, 5)
                pygame.draw.line(screen, (150, 0, 0), (x, y), (x + p.dirs[0][0], y + p.dirs[0][1]))
                pygame.draw.line(screen, (0, 150, 0), (x, y), (x + p.dirs[1][0], y + p.dirs[1][1]))
                pygame.draw.line(screen, (0, 0, 150), (x, y), (x + p.dirs[2][0], y + p.dirs[2][1]))
    font.render_to(screen, (930, 150), "p      s      hr     av    er    cr", (255, 255, 255))
    for i in range(game.num_factions):
        font.render_to(screen, (930, 200 + 50 * i), str(game.num_players_faction[i]), (255, 255, 255))
        font.render_to(screen, (1010, 200 + 50 * i), str(int(game.faction_stats[i][0])), (255, 255, 255))
        font.render_to(screen, (1090, 200 + 50 * i), str(int(game.faction_stats[i][1])), (255, 255, 255))
        font.render_to(screen, (1170, 200 + 50 * i), str(int(game.faction_stats[i][2])), (255, 255, 255))
        font.render_to(screen, (1250, 200 + 50 * i), str(int(game.faction_stats[i][3])), (255, 255, 255))
        font.render_to(screen, (1330, 200 + 50 * i), str(int(game.faction_stats[i][4])), (255, 255, 255))
    if game.winner:
        font.render_to(screen, (930, 100), "winner is: " + str(game.winner.index(1) + 1), (255, 255, 255))
    frame_rate = round(len(times) / sum(times) if sum(times) > 0 else 0, 1)
    font.render_to(screen, (1315, 5), str(frame_rate), (255, 255, 255))
    font.render_to(screen, (930, 685), "pause: space", (255, 255, 255))
    font.render_to(screen, (930, 715), "new start: r", (255, 255, 255))
    font.render_to(screen, (930, 750), "reload config: F5", (255, 255, 255))
    font.render_to(screen, (930, 785), "one step: n", (255, 255, 255))
    font.render_to(screen, (930, 820), "toggle highlight player: h", (255, 255, 255))
    font.render_to(screen, (930, 855), "switch player: left & right", (255, 255, 255))
    pygame.display.flip()
