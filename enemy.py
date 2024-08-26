import pygame
from pygame import Vector2

from health import Health
from ship import Ship
from settings import *
from weapon import *
import random


class SmallEnemy(Ship):
    MAX_HEALTH = 10

    def __init__(self, initial_position: Vector2):
        super().__init__(initial_position)
        self._image = pygame.image.load(r'res/small-ufo.png')
        self._image = pygame.transform.rotozoom(self._image, 0, 0.1)
        self.speed = 2

        self.exp_reward = 3

        self.score_reward = 6

        self.health = Health(SmallEnemy.MAX_HEALTH)

    def charge(self):
        self.speed += 1

    def update(self) -> None:
        p = random.randint(1, 1000)
        if p >= 995:
            self.charge()
        self.move(self.shooting_direction)


class MediumEnemy(Ship):
    MAX_HEALTH = 20

    def __init__(self, initial_position: Vector2):
        super().__init__(initial_position)
        self._image = pygame.image.load(r'res/medium-ufo.png')
        self._image = pygame.transform.rotozoom(self._image, 0, 1)
        self.speed = 1

        self.exp_reward = 6

        self.score_reward = 12

        self.health = Health(MediumEnemy.MAX_HEALTH)
        self.collision_damage = 20
        self.shoot_point_offset = self._image.get_size()[0] / 2

        gun = NormalGun()
        gun.shoot_rate = 0.5
        gun.speed = 4
        self.weapons.append(gun)

    def update(self) -> None:
        self.move(self.shooting_direction)


class BossEnemy(Ship):
    image = pygame.image.load(r'res/big-ufo.png')
    MAX_HEALTH = 300

    def __init__(self, initial_position: Vector2):
        super().__init__(initial_position)
        self._image = pygame.image.load(r'res/big-ufo.png')
        self.speed = 1
        self.health = Health(BossEnemy.MAX_HEALTH)
        self.target_pos = Vector2(SCREEN_SIZE.x // 2, self.rect.height)
        self.collision_damage = 100
        self.exp_reward = 30
        self.score_reward = 150

        gun = NormalGun()
        gun.scatter_angle = 20
        gun.scatter_count = 3
        gun.shoot_rate = 1
        self.weapons.append(gun)

        missile = Missile()
        missile.shoot_rate = 0.15
        missile.scatter_count = 1
        missile.bullet.speed = 2
        missile.bullet.alive_time = 3500
        self.weapons.append(missile)

        gun = AutoAimingGun()
        gun.shoot_rate = 0.45
        gun.bullet_num = 5
        self.weapons.append(gun)

    @property
    def forward_direction(self) -> Vector2:
        if self.target_pos != self.center_pos:
            return (self.target_pos - self.center_pos).normalize()
        return Vector2(0, 1)

    def update(self) -> None:
        if (self.target_pos - self.center_pos).length() >= 1:
            self.move(self.forward_direction)
        else:
            x = SCREEN_SIZE.x // 4 + random.randint(0, SCREEN_SIZE.x // 2)
            y = random.randint(self.rect.height // 2, self.rect.height)
            self.target_pos = Vector2(x, y)
