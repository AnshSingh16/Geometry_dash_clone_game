# ui.py
import pygame


def draw_text(surface, text, x, y, size=20, color=(230,230,230), center=False):
    font = pygame.font.SysFont('Arial', size)
    r = font.render(text, True, color)
    if center:
        rect = r.get_rect(center=(x, y))
        surface.blit(r, rect)
    else:
        surface.blit(r, (x, y))