from typing import Tuple

import sys

import pygame as pg

from const import *
from saving import save_scores


class CurrentScene(object):
    _current_scene: int = SCENE_MAIN_MENU

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CurrentScene, cls).__new__(cls)
        return cls.instance

    def __call__(self, scene: int = None) -> None | int:
        if scene:
            self._current_scene = scene
            return
        return self._current_scene


current_scene = CurrentScene()


class MainMenu:
    _is_run: bool = False

    def __init__(self, screen: pg.Surface,
                 center_screen: Tuple[int, int],
                 clock: pg.time.Clock,
                 fps: int = 60):
        self.screen = screen
        self.center_screen = self.x_screen, self.y_screen = center_screen
        self.clock = clock
        self.FPS = fps

    def run(self):
        from menu.button import MainMenuButton, button_gr

        self._is_run = True

        MainMenuButton(text='start', action=lambda: self.change_scene(SCENE_GAME), pos=(10, 50 * 0 + 10))
        MainMenuButton(text='settings', pos=(10, 60 * 1 + 10))

        while self._is_run:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    sys.exit(0)

            # Update
            mouse_pos = pg.mouse.get_pos()
            mouse_left_click = pg.mouse.get_pressed()[0]
            button_gr.update(mouse_pos, mouse_left_click)

            # Render
            self.screen.fill(pg.Color('black'))
            button_gr.draw(self.screen)

            pg.display.flip()
            self.clock.tick(self.FPS)

    def change_scene(self, scene: int):
        self._is_run = False
        current_scene(scene)


class Game:
    _is_run: bool = False

    def __init__(self, screen: pg.Surface,
                 center_screen: Tuple[int, int],
                 clock: pg.time.Clock,
                 fps: int = 60):
        self.screen = screen
        self.center_screen = self.x_screen, self.y_screen = center_screen
        self.clock = clock
        self.FPS = fps

    def run(self):
        self._is_run = True

        from entitys import Player, Enemy, enemy_gr, bullet_gr, player_gr, get_player, scores

        Player()
        Enemy((self.x_screen - 25, self.y_screen - 50))

        while self._is_run:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    sys.exit(0)

                elif e.type == pg.USEREVENT:
                    # Костыль которым я горжусь
                    get_player().isTime = True
                    # player.isTime = True

                elif e.type == pg.KEYDOWN and e.key == pg.K_f:
                    print('saving')
                    save_scores(scores())

            # Update
            player_gr.update()
            enemy_gr.update()
            bullet_gr.update()

            # Render
            self.screen.fill(pg.Color('black'))
            enemy_gr.draw(self.screen)
            bullet_gr.draw(self.screen)
            player_gr.draw(self.screen)

            pg.display.flip()
            self.clock.tick(self.FPS)
