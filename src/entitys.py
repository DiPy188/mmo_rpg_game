from typing import Tuple, Any, Dict

import pygame as pg

from const import *

enemy_gr = pg.sprite.Group()
bullet_gr = pg.sprite.Group()
player_gr = pg.sprite.Group()
chest_gr = pg.sprite.Group()


class Chest(pg.sprite.Sprite):
    _items: Dict[str, int]

    def __init__(self, pos: Tuple[int, int]):
        super(Chest, self).__init__(chest_gr)

        self.image = pg.Surface(pos)
        self.image.fill(pg.Color('blue'))  # Заменить на текстуру
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self._items = None  # Рандом айтемов

    def get(self) -> Dict[str, int]:
        self.kill()
        return self._items


class Bullet(pg.sprite.Sprite):
    _distance: int = 0
    _direction: int = None
    _speed: int = 0

    def __init__(self, direction: int, pos: Tuple[int, int] = (500, 500), speed: int = 6,
                 size: Tuple[int, int] = None):
        super(Bullet, self).__init__(bullet_gr)

        size = (10, 20) if direction in [LOOK_UP, LOOK_DOWN] else \
            (20, 10) if direction in [LOOK_RIGHT, LOOK_LEFT] else None

        self.image = pg.Surface(size)  # Заменить на картинку
        self.image.fill(pg.Color('yellow'))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self._direction = direction
        self._speed = speed

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.movement()
        self.check_collide()

    def movement(self, *args: Any, **kwargs: Any) -> None:
        if self._direction == LOOK_RIGHT:
            self.rect.x += self._speed
        elif self._direction == LOOK_LEFT:
            self.rect.x -= self._speed
        elif self._direction == LOOK_UP:
            self.rect.y -= self._speed
        elif self._direction == LOOK_DOWN:
            self.rect.y += self._speed

        self._distance += self._speed

        if self._distance >= 800:
            self.kill()

    def check_collide(self, *args: Any, **kwargs: Any) -> None:
        for en in enemy_gr:
            if self.rect.colliderect(en.rect):
                en.kill()
                self.kill()


class Enemy(pg.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int] = (200, 0)):
        super(Enemy, self).__init__(enemy_gr)

        self.image = pg.Surface(ENTITY_SIZE)  # Заменить на картинку
        self.image.fill(pg.Color('darkred'))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class Player(pg.sprite.Sprite):  # Добавить систему очков
    PLAYER_SPEED: int = 3

    _isUp: bool = False
    _isDown: bool = False
    _isLeft: bool = False
    _isRight: bool = False
    _isInteraction: bool = False  # Не забыть про взаимодействия
    isTime: bool = True
    _look: int = LOOK_RIGHT
    timeDelay: int = 500

    hp: int = 100

    def __init__(self, pos: Tuple[int, int] = (0, 0)):
        super(Player, self).__init__(player_gr)

        self.image = pg.Surface(size=ENTITY_SIZE)  # Заменить на картинку
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.image.fill(pg.Color('green'))

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.check_keyboard()
        self.movement()
        self.check_collide()

    def check_keyboard(self, *args: Any, **kwargs: Any) -> None:
        keyboard = pg.key.get_pressed()

        # Управление персонажем
        if keyboard[pg.K_d]:
            self._isRight = True
        else:
            self._isRight = False

        if keyboard[pg.K_a]:
            self._isLeft = True
        else:
            self._isLeft = False

        if keyboard[pg.K_w]:
            self._isUp = True
        else:
            self._isUp = False

        if keyboard[pg.K_s]:
            self._isDown = True
        else:
            self._isDown = False

        # Стрельба
        # Заменить set_timer на таймер в отдельном потоке
        if self.isTime:
            if keyboard[pg.K_RIGHT]:
                self.isTime = False
                self._look = LOOK_RIGHT
                Bullet(self._look, pos=(self.rect.right, self.rect.y + 20))

                pg.time.set_timer(pg.USEREVENT, self.timeDelay, 1)
            elif keyboard[pg.K_LEFT]:
                self.isTime = False
                self._look = LOOK_LEFT
                Bullet(self._look, pos=(self.rect.left, self.rect.y + 20))

                pg.time.set_timer(pg.USEREVENT, self.timeDelay, 1)
            elif keyboard[pg.K_UP]:
                self.isTime = False
                self._look = LOOK_UP
                Bullet(self._look, pos=(self.rect.centerx - 5, self.rect.top))

                pg.time.set_timer(pg.USEREVENT, self.timeDelay, 1)
            elif keyboard[pg.K_DOWN]:
                self.isTime = False
                self._look = LOOK_DOWN
                Bullet(self._look, pos=(self.rect.centerx - 5, self.rect.bottom))
                pg.time.set_timer(pg.USEREVENT, self.timeDelay, 1)

    def movement(self, *args: Any, **kwargs: Any) -> None:
        if self._isRight:
            self._look = LOOK_RIGHT
            self.rect.x += self.PLAYER_SPEED
        if self._isLeft:
            self._look = LOOK_LEFT
            self.rect.x -= self.PLAYER_SPEED
        if self._isUp:
            self._look = LOOK_UP
            self.rect.y -= self.PLAYER_SPEED
        if self._isDown:
            self._look = LOOK_DOWN
            self.rect.y += self.PLAYER_SPEED

    def check_collide(self, *args: Any, **kwargs: Any) -> None:
        for en in enemy_gr:
            if self.rect.colliderect(en.rect):
                self.kill()


def get_player() -> Player:
    return player_gr.__iter__().__next__()
