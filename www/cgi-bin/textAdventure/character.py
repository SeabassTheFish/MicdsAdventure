#!/usr/local/bin/python3

#This is the character abstract
from . import room

class Character:
    def __init__(self, name):
        self.name = name
        self.currentRoom = room.Room("MTR")

    # All the get functions
    def getName(self):
        return self.name
    def getCurrentRoom(self):
        return self.currentRoom

    # All the set functions
    def setName(self, name):
        self.name = name
    def setRoom(self, room):
        self.currentRoom = room

