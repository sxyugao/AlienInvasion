from pygame import Vector2, Rect
import key_mode
import pygame as pg


pg.init()
CAPTION = 'Alien Invasion'
SCREEN_SIZE = Vector2(700, 900)
SCREEN_RECT = Rect((0, 0), SCREEN_SIZE)
BOUNDING_BOX_WIDTH = 30
BATTLEFIELD_RECT = Rect(-BOUNDING_BOX_WIDTH,
                        -BOUNDING_BOX_WIDTH * 10,
                        SCREEN_SIZE.x + 2 * BOUNDING_BOX_WIDTH,
                        SCREEN_SIZE.y + 11 * BOUNDING_BOX_WIDTH)
KEY_MODE = key_mode.KEY_MODE_1
REFRESH_RATE = 60
GLOBAL_FONT_NAME = "Consolas"
GLOBAL_BACKGROUND_COLOR_NAME = "antiquewhite1"
EMOJI_FONT_NAME = "Segoe UI Emoji"
GLOBAL_FONT_24 = pg.font.SysFont(GLOBAL_FONT_NAME, 24)
GLOBAL_FONT_30 = pg.font.SysFont(GLOBAL_FONT_NAME, 30)
GLOBAL_FONT_36 = pg.font.SysFont(GLOBAL_FONT_NAME, 36)
GLOBAL_FONT_48 = pg.font.SysFont(GLOBAL_FONT_NAME, 48)
