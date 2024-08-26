from abc import ABC, abstractmethod

import numpy as np
import pygame
from pygame import Vector2
from pygame.locals import Color
import pygame.freetype


class Interface(ABC):
    def __init__(self):
        self.alive = True

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def handle_input(self):
        pass

    def call_sub_interface(self, sub_interface: "Interface"):
        while sub_interface.alive:
            sub_interface.display()
            pygame.display.update()
            sub_interface = sub_interface.handle_input()


def render_multiline_text(surface: pygame.Surface, font: pygame.font.Font,
                          text: str, topleft: Vector2, color: Color=Color('black')) -> Vector2:
    """

    :return: Vector2 where next line of text start.
    """
    text_list = text.split('\n')
    topleft = topleft.copy()
    for line in text_list:
        text = font.render(line, True, color)
        rect = text.get_rect(topleft=topleft)
        surface.blit(text, topleft)
        topleft.y = topleft.y + rect.height

    return topleft


def add_check_mark(s: str):
    return '-> ' + s + ' <-'


def darken(surface: pygame.Surface, brightness_factor: float):
    pixels = pygame.surfarray.array3d(surface).astype(np.float64)

    # Perform the multiplication and clip values to stay within the valid range (0 to 255)
    pixels *= brightness_factor
    pixels = np.clip(pixels, 0, 255)

    # Convert the result back to uint8 before blitting it back to the surface
    pixels = pixels.astype(np.uint8)
    pygame.surfarray.blit_array(surface, pixels)
