from typing import Tuple, Callable, AnyStr, Any

import pygame as pg

pg.font.init()
button_gr = pg.sprite.Group()
text_writer = pg.font.SysFont(name='arial', size=20)


class MainMenuButton(pg.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int] = (0, 0), action: Callable = None,
                 text: AnyStr = None, size: Tuple[int, int] = (150, 50)):
        super(MainMenuButton, self).__init__(button_gr)
        self.text = text

        self.text_surface = text_writer.render(self.text, True, pg.Color('white'))

        self.image = pg.Surface(size)  # Заменить на текстуру (с изменением состояния)
        self.image.fill(pg.Color('blue'))
        self.image.blit(self.text_surface, self.text_surface.get_rect())
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.action = action

    def update(self, mouse: Tuple[int, int], is_clicked: bool, **kwargs: Any) -> None:
        """ Добавить анимацию (stay, hover, click) """
        if mouse[0] in range(self.rect.left, self.rect.right) and \
                mouse[1] in range(self.rect.top, self.rect.bottom) and is_clicked:
            self.action() if self.action else None
            print('clicked')
