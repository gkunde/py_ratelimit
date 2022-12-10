"""
MIT License

Copyright (c) 2022 Garrett Kunde

This source code is licensed under the MIT License found in the
LICENSE file in the root directory of this source tree.

If LICENSE file is not included, please visit :
    https://github.com/gkunde/py_ratelimit
"""
import time
from typing import Any


class RateLimit:
    """
    A process rate limiter.

    :param max_count: The maximum number of triggers allowed per period.

    :param period: The maximum number of seconds for a period.
    """

    DEFAULT_KEY = "__ALL__"
    SLEEP_PERIOD = 1

    def __init__(self, max_count: int, period: int):

        self.max_count = int(max_count)
        self.period = int(period)

        self.__checkpoints: dict[str, list[float]] = {}
    
    def check(self, key: Any = None) -> None:
        """
        Check if program execution requires a pause.

        :param key: Any hashable object, to enable multiple rate limiters.
        """

        if key not in self.__checkpoints:
            self.__checkpoints[key] = []

        for _ in range(self.period + 1):

            expiration = time.time() - self.period

            self.__checkpoints[key] = [cp for cp in self.__checkpoints[key] if cp >= expiration]

            if len(self.__checkpoints[key]) < self.max_count:
                break

            time.sleep(self.SLEEP_PERIOD)
        
        self.__checkpoints[key].append(time.time())
