from typing import Tuple

import sys

import pygame as pg

from const import *
from saving import save_scores


class CurrentScene(object):
    _current_scene: int = SCENE_MAIN_MENU

    def __new__(cls):  # Singleton
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
        from menu.button import Button, button_gr

        self._is_run = True

        Button(text='start', action=lambda: self.change_scene(SCENE_GAME, button_gr), pos=(10, 50 * 0 + 10))
        Button(text='settings', pos=(10, 60 * 1 + 10))

        while self._is_run:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    sys.exit(0)

            # Update
            mouse_pos = pg.mouse.get_pos()
            is_mouse = pg.mouse.get_pressed()[0]
            button_gr.update(mouse_pos, is_mouse)

            # Render
            self.screen.fill(pg.Color('black'))
            button_gr.draw(self.screen)

            pg.display.flip()
            self.clock.tick(self.FPS)

    def change_scene(self, scene: int, buttons: pg.sprite.Group):
        for butt in buttons:
            butt.kill()
        self._is_run = False
        current_scene(scene)


class Game:
    _is_run: bool = False
    _is_pause: bool = False

    def __init__(self, screen: pg.Surface,
                 center_screen: Tuple[int, int],
                 clock: pg.time.Clock,
                 fps: int = 60):
        self.screen = screen
        self.center_screen = self.x_screen, self.y_screen = center_screen
        self.clock = clock
        self.FPS = fps

    def run(self):
        from entitys import Player, Enemy, enemy_gr, bullet_gr, player_gr, get_player, scores

        self._is_run = True

        Player()
        Enemy((self.x_screen - 25, self.y_screen - 50))

        scores_font = pg.font.SysFont(name='arial', size=30, bold=True)

        while self._is_run:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    sys.exit(0)

                elif e.type == pg.USEREVENT:
                    # Костыль которым я горжусь
                    get_player().isTime = True
                    # player.isTime = True

                elif e.type == pg.KEYDOWN:
                    match e.key:
                        case pg.K_ESCAPE:
                            self.pause_menu(scores())

            # Update
            player_gr.update()
            enemy_gr.update()
            bullet_gr.update()
            scores_txt = scores_font.render(f'scores: {scores()}', True, pg.Color('white'))
            scores_txt_rect = scores_txt.get_rect()
            scores_txt_rect.topright = (900, 0)

            # Render
            self.screen.fill(pg.Color('black'))

            # Render objects
            enemy_gr.draw(self.screen)
            bullet_gr.draw(self.screen)
            player_gr.draw(self.screen)

            # Render UI
            self.screen.blit(scores_txt, scores_txt_rect)

            pg.display.flip()
            self.clock.tick(self.FPS)

    def pause_menu(self, scores: int):
        from menu.button import Button, button_gr

        self._is_pause = True

        text_writer = pg.font.SysFont(name='arial', size=46, bold=True)
        text = text_writer.render('Pause Menu', True, pg.Color('white'))
        text_rect = text.get_rect()
        text_rect.center = (self.x_screen, 150)

        Button(text='Continue', pos=(self.x_screen - 75, self.y_screen - 25), action=self.exit_pause_menu)
        Button(text='Save', pos=(self.x_screen - 75, (self.y_screen - 25) + 100), action=lambda: save_scores(scores))
        Button(text='Exit', pos=(self.x_screen - 75, (self.y_screen - 25) + 200), action=lambda: sys.exit(0))

        while self._is_pause:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    sys.exit(0)

                elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    self.exit_pause_menu()

            # Update
            mouse_pos = pg.mouse.get_pos()
            is_mouse = pg.mouse.get_pressed()[0]
            button_gr.update(mouse_pos, is_mouse)

            # Render
            self.screen.fill(pg.Color('black'))
            button_gr.draw(self.screen)
            self.screen.blit(text, text_rect)

            pg.display.flip()
            self.clock.tick(self.FPS)

    def exit_pause_menu(self):
        self._is_pause = False
