from typing import Tuple

import os.path
import csv

import pygame as pg


def save_scores(_scores: int,
                _dir: str = '../data/saves/',
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
