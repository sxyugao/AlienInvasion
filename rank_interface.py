import sys

import pygame

from interface import Interface, render_multiline_text
from rank import Rank
from pygame import Rect, Color
from settings import *


class RankInterface(Interface):
    def __init__(self, surface: pygame.Surface):
        # Display the game over interface
        super().__init__()
        parent_screen_rect = surface.get_rect()
        sub_rect = Rect(
            parent_screen_rect.w / 4, parent_screen_rect.h / 4,
            parent_screen_rect.w / 2, parent_screen_rect.h / 2 + 50,
        )
        sub_surface = surface.subsurface(sub_rect)
        self.surface = sub_surface
        self.rank = Rank()

    def display(self):
        self.surface.fill(Color(GLOBAL_BACKGROUND_COLOR_NAME))
        pygame.draw.rect(self.surface, Color("black"), self.surface.get_rect(), 3)
        RankInterface.render_rank_info(self.surface, pygame.Vector2(10, 10), self.rank.get_list()[:10])

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                self.alive = False
        return self

    @staticmethod
    def render_rank_info(surface: pygame.Surface, top_left: pygame.Vector2, rank_list: list) -> pygame.Vector2:
        font = pygame.font.SysFont(GLOBAL_FONT_NAME, 36)
        text = f'''Ranking:'''
        top_left = render_multiline_text(surface, font, text, top_left)

        for i, score in enumerate(rank_list):
            text = f'''#{i + 1} '''.ljust(4) + str(score).rjust(10, " ")
            top_left = render_multiline_text(surface, font, text, top_left)

        return top_left
