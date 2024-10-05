# utilities.py
import pygame

def init_pygame():
    pygame.init()
    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    return screen, screen_size  # screenとscreen_sizeを返す


def quit_pygame():
    pygame.quit()
