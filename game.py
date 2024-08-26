import pygame

from menu_interface import MenuInterface
from settings import *
from interface import Interface
import ctypes


class Game:

    def run(self):
        pygame.init()
        
        app_id = 'AlienInvasion'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        pygame_icon = pygame.image.load(r"res/icon.png")
        pygame.display.set_icon(pygame_icon)
        screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(CAPTION, "👽")

        current_interface: Interface = MenuInterface()

        while True:
            current_interface.display()
            pygame.display.update()
            current_interface = current_interface.handle_input()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
