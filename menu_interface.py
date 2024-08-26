import sys
from enum import Enum, auto

import pygame
from pygame.locals import *

from interface import Interface, darken, add_check_mark
from main_game_interface import MainGameInterface
from rank_interface import RankInterface
from settings import *


class MenuItem(Enum):
    START_GAME = 0
    RANKING = auto()
    QUIT = auto()

    @property
    def name_to_render(self):
        return ' '.join(self.name.split('_'))


class MenuInterface(Interface):

    def __init__(self):
        super().__init__()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(CAPTION)
        self.font = pygame.font.SysFont(GLOBAL_FONT_NAME, 36)
        self.title_font = pygame.font.SysFont(GLOBAL_FONT_NAME, 48)
        self.color = pygame.Color(0, 0, 0)
        self.selected_item = 0

    def render_menu_item(self):
        for menu_item in MenuItem:
            index = menu_item.value
            text = menu_item.name_to_render

            # if selected, render like -> xxx <-
            if index == self.selected_item:
                text = add_check_mark(text)

            text_surface = self.font.render(text, True, self.color)
            text_rect = text_surface.get_rect(center=(SCREEN_SIZE.x // 2, SCREEN_SIZE.y // 2 + index * 40))

            self.screen.blit(text_surface, text_rect)

    def render_title(self):
        tile_text = "Alien Invasion"
        text_surface = self.title_font.render(tile_text, True, Color('black'))
        text_rect = text_surface.get_rect(center=(SCREEN_SIZE.x // 2, SCREEN_SIZE.y // 3))
        self.screen.blit(text_surface, text_rect)

    def render_logo(self):
        logo_text = "👽"
        font = pygame.font.SysFont(EMOJI_FONT_NAME, 36)
        text_surface = font.render(logo_text, True, Color('black'))
        text_rect = text_surface.get_rect(center=(SCREEN_SIZE.x // 2, SCREEN_SIZE.y // 4))
        self.screen.blit(text_surface, text_rect)

    def display(self):
        self.clock.tick(REFRESH_RATE)
        self.screen.fill(pygame.Color(GLOBAL_BACKGROUND_COLOR_NAME))
        self.render_logo()
        self.render_title()
        self.render_menu_item()

    def handle_input(self) -> Interface:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == pygame.K_UP or event.key == KEY_MODE.UP:
                    select_sound = pygame.mixer.Sound(r'res/button.wav')
                    select_sound.play()
                    self.selected_item = (self.selected_item - 1) % len(MenuItem)
                if event.key == pygame.K_DOWN or event.key == KEY_MODE.DOWN:
                    select_sound = pygame.mixer.Sound(r'res/button.wav')
                    select_sound.play()
                    self.selected_item = (self.selected_item + 1) % len(MenuItem)
                if event.key == pygame.K_RETURN or event.key == KEY_MODE.SHOOT:
                    select_sound = pygame.mixer.Sound(r'res/button.wav')
                    select_sound.play()
                    if self.selected_item == MenuItem.START_GAME.value:  # Start Game
                        return MainGameInterface(self.screen)
                    elif self.selected_item == MenuItem.RANKING.value:
                        darken(self.screen, 0.5)
                        rank_interface = RankInterface(self.screen)
                        self.call_sub_interface(rank_interface)
                    elif self.selected_item == MenuItem.QUIT.value:  # Quit
                        pygame.quit()
                        sys.exit()

        return self
