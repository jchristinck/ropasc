def write_text(pygame, screen, font, location, text, color):
    font.render_to(screen, location, text, color)
    pygame.display.flip()
