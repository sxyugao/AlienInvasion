from ship import Ship
import pygame
from settings import *
from weapon import *
from exp import Exp


class PlayerShip(Ship):

    def __init__(self, initial_position: Vector2):
        super().__init__(initial_position)
        self._image = pygame.image.load(r'res/spaceship.png')
        self._image = pygame.transform.rotozoom(self._image, 0, 0.3)
        self.shoot_point_offset = self._image.get_size()[0] / 2
        self.speed = 3
        self.exp = Exp()

        self._upgradable_skills = {
            f"{self.__class__.__name__}: Add 20HP": self.add_xp,
            f"{self.__class__.__name__}: Add move speed": self.move_speed_up
        }
        self.pending_weapon = [Missile(), AutoAimingGun()]
        for i in range(len(self.pending_weapon)):
            self._upgradable_skills.update({
                f"New weapon: {self.pending_weapon[i].__class__.__name__}": self.add_weapon(i)
            })

    def move(self, direction: Vector2):
        self.center_pos += direction * self.speed
        if not BATTLEFIELD_RECT.contains(self.rect):
            self.center_pos -= direction * self.speed

    def update(self):
        pass

    def add_xp(self):
        self.health.reduce(-20)

    def move_speed_up(self):
        self.speed += 1
    
    @property
    def shooting_direction(self):
        return Vector2(0, -1)

    @property
    def upgradable_skills(self):
        return self._upgradable_skills
    
    def add_weapon(self, index):
        def func():
            self.weapons.append(self.pending_weapon[index])
        return func
