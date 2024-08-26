import pygame
from dataclasses import dataclass


@dataclass
class KeyMode:
    UP: int
    DOWN: int
    LEFT: int
    RIGHT: int
    SHOOT: int
    PAUSE: int


KEY_MODE_1 = KeyMode(UP=pygame.K_w, DOWN=pygame.K_s,
                     LEFT=pygame.K_a, RIGHT=pygame.K_d, SHOOT=pygame.K_SPACE, PAUSE=pygame.K_RETURN)
KEY_MODE_2 = KeyMode(UP=pygame.K_UP, DOWN=pygame.K_DOWN,
                     LEFT=pygame.K_LEFT, RIGHT=pygame.K_RIGHT, SHOOT=pygame.K_SPACE, PAUSE=pygame.K_RETURN)
