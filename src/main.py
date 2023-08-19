from typing import Tuple

import os.path
import csv

import pygame as pg


def save_scores(_scores: int,
                _dir: str = '../data/safes/',
                title: str = 'dev_safe1',
                mode: str = 'w'):  # В будущем исправить на более универсальную функцию
    _dir = os.path.abspath(_dir)

    if not os.path.exists(_dir):
        raise ValueError(f"Путь сохранения не корректен: {_dir}")

    file_name = title + '.csv'
    full_path = _dir + '/' + file_name

    if not os.path.isfile(full_path) and mode == 'a':
        raise ValueError(f"Режим записи не корректен: {mode=}")

    data = [['scores'],
            [f'{_scores}']]  # Со временем дополнять

    with open(file=full_path, mode=mode, encoding='utf-8') as f:
        writer = csv.writer(f)

        for row in data:
            writer.writerow(row)


class App:
    """Добавить сохранение прогресса"""

    _is_run: bool = False
    FPS: int = 60

    def __init__(self, screen: Tuple[int, int] = (900, 650)):
        pg.init()
        self.screen = pg.display.set_mode(screen)
        self.x_screen, self.y_screen = self.screen.get_rect().center
        self.clock = pg.time.Clock()

        self.main_menu_result: bool = False

    def run(self):
        self._is_run = True

        flag = self.main_scene()

        if flag:
            self._is_run = True
            self.game_scene()

    def main_scene(self) -> bool:
        from menu.button import MainMenuButton, button_gr

        MainMenuButton(text='start', action=self.change_to_game_scene)

        while self._is_run:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self._is_run = False

            # Update
            mouse = pg.mouse.get_pos()
            is_clicked = pg.mouse.get_pressed()[0]

            button_gr.update(mouse, is_clicked)

            # Render
            self.screen.fill(pg.Color('black'))
            button_gr.draw(self.screen)

            pg.display.flip()
            self.clock.tick(self.FPS)

        return self.main_menu_result

    def game_scene(self):
        from entitys import Player, Enemy, enemy_gr, bullet_gr, player_gr, get_player, scores

        Player()
        Enemy((self.x_screen - 25, self.y_screen - 50))

        while self._is_run:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self._is_run = False  # Выход из игры

                elif e.type == pg.USEREVENT:
                    # Костыль которым я горжусь
                    get_player().isTime = True
                    # player.isTime = True

                elif e.type == pg.KEYDOWN and e.key == pg.K_f:
                    print('saving')
                    save_scores(scores.get())

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

        pg.quit()

    def change_to_game_scene(self):
        self._is_run = False
        self.main_menu_result = True


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
