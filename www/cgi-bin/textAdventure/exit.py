#!/usr/local/bin/python3

# This is the exit class. It's made to link two rooms to each other to allow movement.

from . import enums
from . import room

class Exit:
    def __init__(self, leadsTo, direction):
        self.direction = direction
        self.shortDirection = enums.ShortDirection(self.direction.value)
        self.leadsTo = leadsTo

    # All the get functions
    def getDirection(self):
        return self.direction
    def getShortDirection(self):
        return self.shortDirection
    def getLeadsTo(self):
        return self.leadsTo
    def __str__(self):
        return self.leadsTo.getId() + " to the " + self.direction.name

