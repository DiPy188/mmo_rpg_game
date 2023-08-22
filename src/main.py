from typing import Tuple

import pygame as pg

from const import *
from scenes import *


class App:
    """Добавить сохранение прогресса"""

    _is_run: bool = False
    FPS: int = 60

    def __init__(self, screen: Tuple[int, int] = (900, 650)):
        pg.init()
        self.screen = pg.display.set_mode(screen)
        self.center_screen = self.x_screen, self.y_screen = self.screen.get_rect().center
        self.clock = pg.time.Clock()

        self.main_menu_result: bool = False

    def run(self):
        self._is_run = True

        while self._is_run:
            if current_scene() == SCENE_MAIN_MENU:
                self._is_run = True
                menu = MainMenu(self.screen, self.center_screen, self.clock, self.FPS)
                menu.run()
            elif current_scene() == SCENE_GAME:
                self._is_run = True
                game = Game(self.screen, self.center_screen, self.clock, self.FPS)
                game.run()
            else:
                self._is_run = True
                self.gag_scene()

    def gag_scene(self):
        self._is_run = True

        font = pg.font.SysFont(name='arial', size=48, bold=True)

        text = font.render('This is empty scene', True, pg.Color('red'))
        text_rect = text.get_rect()
        text_rect.center = self.center_screen

        while self._is_run:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self._is_run = False

            # Update

            # Render
            self.screen.fill(pg.Color('black'))
            self.screen.blit(text, text_rect)

            pg.display.flip()
            self.clock.tick(self.FPS)


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
