from typing import Any

import pygame

from settings import *
from abc import ABC, abstractmethod


class Bullet(pygame.sprite.Sprite):
    _image = pygame.image.load(r'res/fire_bullet_no_bound.png')
    _image = pygame.transform.rotozoom(_image, 0, 1)

    def __init__(self, position: Vector2 = None, direction: Vector2 = None, damage=0, speed=0) -> None:
        super().__init__()
        if position:
            self.center_pos = position.copy()
        if direction:
            self.direction = direction.copy().normalize()
            self.angle = self.direction.angle_to(Vector2(0, -1))
        self.damage = damage
        self.speed = speed

    @property
    def image(self):
        return pygame.transform.rotate(self._image, self.angle)

    @property
    def rect(self):
        return self.image.get_rect(center=self.center_pos)

    def update(self, *args: Any, **kwargs: Any) -> None:
        dx = self.speed * self.direction.x
        dy = self.speed * self.direction.y
        self.center_pos += (dx, dy)


class NormalBullet(Bullet):
    pass


class BlueNormalBullet(Bullet):
    _image = pygame.image.load(r'res/blue-bullet.png')
    _image = pygame.transform.rotozoom(_image, 0, 1)
    pass


class TrackingBullet(Bullet):
    _image = pygame.image.load(r'res/missile.png')
    _image = pygame.transform.rotozoom(_image, 0, 1)

    def __init__(self, position: Vector2 = None, direction: Vector2 = None, damage=0, speed=0, alive_time=1000000) -> None:
        super().__init__()
        if position:
            self.center_pos = position.copy()
        if direction:
            self.direction = direction.copy().normalize()
        self.damage = damage
        self.speed = speed
        from ship import Ship
        self.target: Ship = None
        self.angle = 0
        self.generate_time = pygame.time.get_ticks()
        self.alive_time = alive_time

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.target is not None and self.target.health.alive():
            self.direction = (self.target.center_pos - self.center_pos).normalize()
            self.angle = self.direction.angle_to(Vector2(0, -1))
        dx = self.speed * self.direction.x
        dy = self.speed * self.direction.y
        self.center_pos += (dx, dy)

        # remove bullet if it survival time exceeded
        if pygame.time.get_ticks() - self.generate_time > self.alive_time:
            self.center_pos = (-999, -999)


class Weapon(ABC):
    def __init__(self):
        self.is_upgradable_skills_added = False
        self._upgradable_skills = {}

    @abstractmethod
    def attack(self, start_pos: Vector2, direction: Vector2) -> list[Bullet]:
        pass
    
    @property
    def upgradable_skills(self):
        if not self.is_upgradable_skills_added:
            self.is_upgradable_skills_added = True
            return self._upgradable_skills
        return {}


class NormalGun(Weapon):
    sound = pygame.mixer.Sound(r'res/normal_gun.wav')

    def __init__(self):
        super().__init__()
        self.shoot_rate = 5
        self.scatter_count = 1
        self.scatter_angle = 3
        self.last_shoot_time = 0
        self.bullet = Bullet(damage=2, speed=7)
        self._upgradable_skills = {
            f"{self.__class__.__name__}: Increase bullet damage": self.bullet_damage_up,
            f"{self.__class__.__name__}: Increase bullet speed": self.bullet_speed_up,
            f"{self.__class__.__name__}: Increase shoot rate": self.shoot_rate_up,
            f"{self.__class__.__name__}: Increase scatter count": self.scatter_count_up,
        }

    def attack(self, start_pos: Vector2, direction: Vector2) -> list[Bullet]:
        if pygame.time.get_ticks() - self.last_shoot_time < 1000 / self.shoot_rate:
            return []

        self.sound.play()
        bullets = []
        angle = -(self.scatter_count // 2) * self.scatter_angle
        for i in range(self.scatter_count):
            new_bullet = NormalBullet(start_pos, direction.rotate(angle), self.bullet.damage, self.bullet.speed)
            bullets.append(new_bullet)
            angle += self.scatter_angle

        self.last_shoot_time = pygame.time.get_ticks()

        return bullets

    def bullet_damage_up(self):
        self.bullet.damage += 1

    def bullet_speed_up(self):
        self.bullet.speed += 1

    def shoot_rate_up(self):
        self.shoot_rate += 1

    def scatter_count_up(self):
        self.scatter_count += 1


class Missile(Weapon):
    sound = pygame.mixer.Sound(r'res/missile.mp3')

    def __init__(self):
        super().__init__()
        self.shoot_rate = 0.75
        self.scatter_count = 1
        self.scatter_angle = 4
        self.last_shoot_time = 0
        self.bullet = TrackingBullet(damage=5, speed=4)
        self.bullet.alive_time = 1000000
        self._upgradable_skills = {
            f"{self.__class__.__name__}: Increase missile damage": self.bullet_damage_up,
            f"{self.__class__.__name__}: Increase missile speed": self.bullet_speed_up,
            f"{self.__class__.__name__}: Increase launch rate": self.shoot_rate_up,
            f"{self.__class__.__name__}: Increase missile count": self.scatter_count_up,
        }

    def attack(self, start_pos: Vector2, direction: Vector2) -> list[Bullet]:
        if pygame.time.get_ticks() - self.last_shoot_time < 1000 / self.shoot_rate:
            return []

        self.sound.play()
        bullets = []
        angle = -(self.scatter_count // 2) * self.scatter_angle
        for i in range(self.scatter_count):
            new_bullet = TrackingBullet(start_pos, direction.rotate(angle), self.bullet.damage,
                                        self.bullet.speed, self.bullet.alive_time)
            bullets.append(new_bullet)
            angle += self.scatter_angle

        self.last_shoot_time = pygame.time.get_ticks()

        return bullets

    def bullet_damage_up(self):
        self.bullet.damage += 2

    def bullet_speed_up(self):
        self.bullet.speed += 1

    def shoot_rate_up(self):
        self.shoot_rate += 0.05

    def scatter_count_up(self):
        self.scatter_count += 1


class AutoAimingGun(Weapon):
    sound = pygame.mixer.Sound(r'res/normal_gun.wav')
    
    def __init__(self):
        super().__init__()
        self.shoot_rate = 1
        self.last_shoot_time = 0
        self.bullet = Bullet(damage=1, speed=5)
        self.bullet_num = 3
        self._upgradable_skills = {
            f"{self.__class__.__name__}: Increase bullet damage": self.bullet_damage_up,
            f"{self.__class__.__name__}: Increase bullet speed": self.bullet_speed_up,
            f"{self.__class__.__name__}: Increase bullet num": self.bullet_num_up,
            f"{self.__class__.__name__}: Increase shoot rate": self.shoot_rate_up,
        }

    def attack(self, start_pos: Vector2, direction: Vector2) -> list[Bullet]:
        if pygame.time.get_ticks() - self.last_shoot_time < 1000 / self.shoot_rate:
            return []

        self.sound.play()
        bullets = []
        for i in range(self.bullet_num):
            new_bullet = BlueNormalBullet(start_pos, direction, self.bullet.damage, self.bullet.speed + i)
            bullets.append(new_bullet)

        self.last_shoot_time = pygame.time.get_ticks()

        return bullets

    def bullet_damage_up(self):
        self.bullet.damage += 1

    def bullet_speed_up(self):
        self.bullet.speed += 1

    def bullet_num_up(self):
        self.bullet_num += 1

    def shoot_rate_up(self):
        self.shoot_rate += 1
