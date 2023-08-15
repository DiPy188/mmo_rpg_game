from typing import Dict

import threading as thread
import time


class Timer:
    _stack: Dict[str, int | float] = dict()

    def start(self, title: str, seconds: int | float):
        pass  # Продолжить
