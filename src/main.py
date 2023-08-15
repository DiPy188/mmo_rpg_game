from typing import Tuple

import pygame as pg

from entitys import Player, Enemy, enemy_gr, bullet_gr, player_gr, get_player


class App:
    """Добавить сохранение прогресса"""

    _is_run: bool = False
    FPS: int = 60

    def __init__(self, screen: Tuple[int, int] = (900, 650)):
        pg.init()
        self.screen = pg.display.set_mode(screen)
        x, y = self.screen.get_rect().center
        self.clock = pg.time.Clock()

        Player()
        Enemy((x - 25, y - 50))

    def run(self):
        self._is_run = True

        while self._is_run:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self._is_run = False  # Выход из игры

                elif e.type == pg.USEREVENT:
                    # Костыль которым я горжусь
                    get_player().isTime = True
                    # player.isTime = True

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


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
