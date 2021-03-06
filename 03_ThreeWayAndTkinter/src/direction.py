# -*- coding: utf-8 -*-

from __future__ import annotations
import enum
from typing import Set


class Direction(enum.IntEnum):
    LEFT, RIGHT, UP, DOWN = range(4)

    @classmethod
    def all_directions(cls) -> Set[Direction]:
        return {cls.LEFT, cls.RIGHT, cls.UP, cls.DOWN}
