from game_logic import GameLogic
from interface import Interface, render_multiline_text, darken, add_check_mark
from rank_interface import RankInterface

import sys
import pygame

from rank import Rank
from settings import *
from pygame.locals import *
from bar import PlayerHealthBar, ExpBar, EnemyHealthBar
import pygame.freetype


class MainGameInterface(Interface):
    def __init__(self, surface: pygame.Surface):
        super().__init__()
        self.clock = pygame.time.Clock()
        if surface:
            self.surface = surface
        else:
            self.surface = pygame.display.set_mode(SCREEN_SIZE)
        self.game_logic = GameLogic()

        # Health bar position
        self.health_bar = PlayerHealthBar(Rect(30, 20, 300, 20))
        self.exp_bar = ExpBar(Rect(30, 70, 300, 20))

        # Score display settings
        self.score_font = pygame.font.SysFont(GLOBAL_FONT_NAME, 24)
        self.score_top_left = (20, 120)
        pygame.mixer.music.load(r'res/bgm.mp3')
        pygame.mixer.music.play()

    def display(self):
        self.clock.tick(60)

        # Set background color
        self.surface.fill(pygame.Color(GLOBAL_BACKGROUND_COLOR_NAME))

        # Render player
        self.surface.blit(self.game_logic.player.image, self.game_logic.player.rect)

        # Render enemy
        for enemy in self.game_logic.enemies:
            self.surface.blit(enemy.image, enemy.rect)
            enemy_health_bar_rect = enemy.rect.scale_by(1, 0.1)
            enemy_health_bar_rect = enemy_health_bar_rect.move(0, enemy.rect.height // 2 + enemy_health_bar_rect.height)
            EnemyHealthBar.render(self.surface, enemy_health_bar_rect, enemy.health.current_health, enemy.MAX_HEALTH)
        for bullet in self.game_logic.player_bullets:
            self.surface.blit(bullet.image, bullet.rect)
        for bullet in self.game_logic.enemy_bullets:
            self.surface.blit(bullet.image, bullet.rect)

        # Render health bar
        health = self.game_logic.player.health
        self.health_bar.render(self.surface, health.current_health, health.max_health)

        # Render exp bar
        exp = self.game_logic.player.exp
        self.exp_bar.render(self.surface, exp.current_exp, exp.level)

        # Render score
        self.render_score()

    def render_score(self):
        score = self.game_logic.score
        score_text = f'Score: {score}'
        text = self.score_font.render(score_text, True, Color('black'))
        self.surface.blit(text, self.score_top_left)

    def handle_input(self) -> Interface:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP and event.key == KEY_MODE.PAUSE:
                darken(self.surface, 0.5)
                self.call_sub_interface(PauseInterface(self.surface))

        # Check if game is over
        if self.game_logic.game_over:
            # Darken the screen
            darken(self.surface, 0.5)

            # Display the game over interface
            game_over_interface = GameOverInterface(self.surface, self.game_logic.score)
            return game_over_interface

        while self.game_logic.level_up > 0:
            skill_choices = self.game_logic.random_skills()
            cur_level = self.game_logic.player.exp.level - self.game_logic.level_up
            self.call_sub_interface(
                LevelUpInterface(self.surface, cur_level, skill_choices)
            )

            self.game_logic.level_up -= 1

        self.game_logic.update()

        return self


class LevelUpInterface(Interface):
    sound = pygame.mixer.Sound(r'res/level_up.wav')

    def __init__(self, surface: pygame.Surface, cur_level: int, skill_choices: list):
        super().__init__()
        parent_screen_rect = surface.get_rect()
        sub_rect = Rect(
            50, parent_screen_rect.h / 4,
            parent_screen_rect.w - 100, parent_screen_rect.h / 3,
        )
        LevelUpInterface.sound.play()
        self.surface = surface.subsurface(sub_rect)
        self.cur_level = cur_level
        self.skill_choices = skill_choices
        self.selected_item = 0
        self.font = pygame.font.SysFont(GLOBAL_FONT_NAME, 20)
        self.color = pygame.Color(0, 0, 0)

    def display(self):
        self.surface.fill(Color(GLOBAL_BACKGROUND_COLOR_NAME))
        pygame.draw.rect(self.surface, Color("black"), self.surface.get_rect(), 3)

        text_surface = GLOBAL_FONT_36.render(f'''Lv.{self.cur_level - 1} -> Lv.{self.cur_level}''',
                                             True, self.color)
        text_rect = text_surface.get_rect(center=(self.surface.get_rect().w / 2, text_surface.get_rect().h))
        center = Vector2(text_rect.center)
        self.surface.blit(text_surface, text_rect)

        text_surface = GLOBAL_FONT_36.render('Choose your skill', True, self.color)
        center.y += text_rect.height
        text_rect = text_surface.get_rect(center=center)
        self.surface.blit(text_surface, text_rect)

        text_surface = GLOBAL_FONT_36.render('-----------------', True, self.color)
        center.y += text_rect.height
        text_rect = text_surface.get_rect(center=center)
        self.surface.blit(text_surface, text_rect)

        for index, skill_choice in enumerate(self.skill_choices):
            text = skill_choice[0]

            if index == self.selected_item:
                text = add_check_mark(text)

            text_surface = GLOBAL_FONT_24.render(text, True, self.color)
            center.y += text_rect.height
            text_rect = text_surface.get_rect(center=center)

            self.surface.blit(text_surface, text_rect)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == pygame.K_UP:
                    select_sound = pygame.mixer.Sound(r'res/button.wav')
                    select_sound.play()
                    self.selected_item = (self.selected_item - 1) % len(self.skill_choices)
                if event.key == pygame.K_DOWN:
                    select_sound = pygame.mixer.Sound(r'res/button.wav')
                    select_sound.play()
                    self.selected_item = (self.selected_item + 1) % len(self.skill_choices)
                if event.key == pygame.K_RETURN:
                    select_sound = pygame.mixer.Sound(r'res/button.wav')
                    select_sound.play()
                    self.skill_choices[self.selected_item][1]()
                    self.alive = False
        return self


class PauseInterface(Interface):
    def __init__(self, surface: pygame.Surface):
        super().__init__()
        parent_screen_rect = surface.get_rect()
        sub_rect = Rect(
            parent_screen_rect.w / 4 - 10, parent_screen_rect.h / 3,
            parent_screen_rect.w / 2 + 20, parent_screen_rect.h / 5,
        )
        sub_surface = surface.subsurface(sub_rect)
        self.surface = sub_surface
        self.orignial_volume = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(self.orignial_volume * 0.5)

    def display(self):
        self.surface.fill(Color(GLOBAL_BACKGROUND_COLOR_NAME))
        pygame.draw.rect(self.surface, Color("black"), self.surface.get_rect(), 3)
        text = f'''Game paused'''
        topleft = render_multiline_text(self.surface, pygame.font.SysFont(GLOBAL_FONT_NAME, 48),
                                        text, Vector2(10, 10), Color("black"))
        text = f'''-----------'''
        topleft = render_multiline_text(self.surface, pygame.font.SysFont(GLOBAL_FONT_NAME, 48), text, topleft)
        text = f'''Press key to continue...'''
        topleft = render_multiline_text(self.surface, pygame.font.SysFont(GLOBAL_FONT_NAME, 22), text, topleft)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                pygame.mixer.music.set_volume(self.orignial_volume)
                select_sound = pygame.mixer.Sound(r'res/button.wav')
                select_sound.play()
                self.alive = False
        return self


class GameOverInterface(Interface):
    sound = pygame.mixer.Sound(r'res/player_dead.wav')

    def __init__(self, surface: pygame.Surface, score: int):
        super().__init__()
        parent_screen_rect = surface.get_rect()
        game_over_interface_rect = Rect(
            parent_screen_rect.w / 4, parent_screen_rect.h / 4,
            parent_screen_rect.w / 2, parent_screen_rect.h / 2 + 50,
        )
        self.score = score
        self.surface = surface.subsurface(game_over_interface_rect)
        self.font = pygame.font.SysFont(GLOBAL_FONT_NAME, 36)
        self.score_font = pygame.font.SysFont(GLOBAL_FONT_NAME, 24)
        self.score_font.set_bold(True)
        self.score_font.set_underline(True)
        self.rank = Rank()
        self.rank.add(self.score)
        self.over_time = pygame.time.get_ticks()
        pygame.mixer.music.stop()
        GameOverInterface.sound.play()

    def display(self):
        self.surface.fill(Color(GLOBAL_BACKGROUND_COLOR_NAME))
        pygame.draw.rect(self.surface, Color("black"), self.surface.get_rect(), 3)

        text = f'''Game over!'''
        top_left = render_multiline_text(self.surface, pygame.font.SysFont(GLOBAL_FONT_NAME, 48),
                                        text, Vector2(10, 10), Color("black"))

        text = f'''--------------'''
        top_left = render_multiline_text(self.surface, self.font, text, top_left)

        text = f'''Score:''' + str(self.score).rjust(7, " ")
        top_left = render_multiline_text(self.surface, self.font, text, top_left)

        text = f'''--------------'''
        top_left = render_multiline_text(self.surface, self.font, text, top_left)

        top_left = RankInterface.render_rank_info(self.surface, top_left, self.rank.get_list()[:5])

        text = f'''--------------'''
        top_left = render_multiline_text(self.surface, self.font, text, top_left)

        text = f'''Press any key to continue'''
        top_left = render_multiline_text(self.surface, pygame.font.SysFont(GLOBAL_FONT_NAME, 20), text, top_left)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == KEYUP and pygame.time.get_ticks() - self.over_time > 500:
                select_sound = pygame.mixer.Sound(r'res/button.wav')
                select_sound.play()
                from menu_interface import MenuInterface
                return MenuInterface()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        return self


