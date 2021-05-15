from enum import Enum


class Direction(Enum):
    # [0] - y
    # [1] - x
    up = [-1, 0]
    right = [0, 1]
    down = [1, 0]
    left = [0, -1]

    @classmethod
    def get_direction(cls, number):
        return {
            0: Direction.up,
            1: Direction.right,
            2: Direction.down,
            3: Direction.right
        }.get(number, 0)
