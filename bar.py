import pygame
from pygame.sprite import AbstractGroup
from settings import *
from pygame import Color
from exp import Exp


def draw_rect_with_alpha(surface: pygame.Surface, rect: Rect, color: Color):
    s = pygame.Surface(rect.size, pygame.SRCALPHA)
    s.fill(color)
    surface.blit(s, (0, 0))


class Bar(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)

    @staticmethod
    def render(surface: pygame.Surface, rect: Rect,
               front_color: Color, back_color: Color, outer_frame_width: int, progress: float) -> None:
        draw_rect_with_alpha(surface, rect, back_color)
        # render outer bounding
        outer_frame_rect = rect.inflate(outer_frame_width * 2, outer_frame_width * 2)
        pygame.draw.rect(surface, Color('black'), outer_frame_rect, width=outer_frame_width)

        # render inner bar
        inner_rect_width = int(rect.width * progress)  # 根据进度计算内部矩形的宽度
        inner_rect = pygame.Rect(rect.left, rect.top, inner_rect_width, rect.height)
        pygame.draw.rect(surface, front_color, inner_rect)  # 绘制进度条


class PlayerHealthBar:
    heart_image = pygame.image.load(r'res/heart.png')
    heart_image = pygame.transform.rotozoom(heart_image, 0, 0.3)

    def __init__(self, rect: pygame.Rect) -> None:
        self.rect = rect
        self.font = pygame.font.SysFont(GLOBAL_FONT_NAME, 20)
        self.font_color = pygame.Color(0, 0, 0)

    def render(self, surface: pygame.Surface, current_health, max_health) -> None:
        # Render the bar
        Bar.render(surface, self.rect, Color("red"), Color(0, 0, 0, 0),
                   3, current_health / max_health)

        # Render the heart image
        center = (self.rect.topleft[0], self.rect.topleft[1] + self.rect.height / 2)
        surface.blit(PlayerHealthBar.heart_image,
                     PlayerHealthBar.heart_image.get_rect(center=center))

        # Render the text
        text_content = f"{current_health} / {max_health}"
        text = self.font.render(text_content, True, self.font_color)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)


class EnemyHealthBar:
    def __init__(self):
        pass

    @staticmethod
    def render(surface: pygame.Surface, rect: Rect, current_health, max_health) -> None:
        # Render the bar
        Bar.render(surface, rect, Color("red"), Color(0, 0, 0, 0), 1, current_health / max_health)


class ExpBar:
    heart_image = pygame.image.load(r'res/exp.png')

    def __init__(self, rect: pygame.Rect) -> None:
        self.rect = rect
        self.font = pygame.font.SysFont(GLOBAL_FONT_NAME, 20)
        self.color = pygame.Color(0, 0, 0)

    def render(self, surface: pygame.Surface, exp: int, level: int) -> None:
        # Render the bar
        Bar.render(surface, self.rect, Color("green"), Color(0, 0, 0, 0),
                   3, exp / Exp.exp_required_to_upgrade(level))

        # Render the heart image
        center = (self.rect.topleft[0], self.rect.topleft[1] + self.rect.height / 2)
        surface.blit(ExpBar.heart_image,
                     ExpBar.heart_image.get_rect(center=center))

        # Render the text
        text_content = f"Lv.{level} | {exp} / {Exp.exp_required_to_upgrade(level)}"
        text = self.font.render(text_content, True, self.color)
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.centery))
        surface.blit(text, text_rect)
