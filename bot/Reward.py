from enum import Enum


class Reward(Enum):
    VERY_HIGH = 1000
    HIGH = 500
    LITTLE_HIGH = 200
    LITTLE_LOW = -200
    LOW = -500
    VERY_LOW = -1000
