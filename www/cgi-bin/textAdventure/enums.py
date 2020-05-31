#!/usr/local/bin/python3

# The valid directions in the game

from enum import Enum

class Direction(Enum):
    NULL = 0
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4
    UP = 5
    DOWN = 6
    IN = 7
    OUT = 8
    NORTHEAST = 13
    NORTHWEST = 14
    SOUTHEAST = 23
    SOUTHWEST = 24


class WearableLoc(Enum):
    NULL = 0
    HEAD = 1
    CHEST = 2
    LEGS = 3
    FEET = 4
    HANDS = 5
    NECK = 6
    WAIST = 7
    FACE = 8

class ShortDirection(Enum):
    NL = 0
    N = 1
    S = 2
    E = 3
    W = 4
    U = 5
    D = 6
    IN = 7
    OUT = 8
    NE = 13
    NW = 14
    SE = 23
    SW = 24

class RunMode(Enum):
    PLAY = 0
    TALK = 1
