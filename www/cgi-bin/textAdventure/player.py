#!/usr/local/bin/python3

# This is the player class
from . import enums
from .character import Character
from . import commands as com

class Player(Character):
    def __init__(self, name="Sbeve"):
        super().__init__(name) # Gives the player a name and a null current room
        self.wearing = [0,0,0,0,0,0,0,0,0]
        self.inventory = []
        self.points = 0
        self.moves = 0
        self.lastMove = com.Nonsense()
        self.currentRoom = None

    # All the get functions. Some are inherited from Character
    def getInventory(self):
        return self.inventory
    def getItemByName(self, name):
        for item in self.inventory:
            if item.getName().lower() == name:
                return item
        for item in self.wearing:
            if item != 0:
                if item.getName().lower() == name:
                    return item
    def getWearing(self):
        return self.wearing
    def getLastMove(self):
        return self.lastMove
    def calcPoints(self):
        return str(self.points) + "/" + str(self.moves)

    # All the set functions are defined in the superclass Character

    # All the add and remove functions
    def addItem(self, item):
        self.inventory.append(item)
    def removeItem(self, item):
        self.inventory.remove(item)
    def storeLast(self, command):
        if isinstance(command, com.Command):
            self.lastMove = command
    def setInventory(self, inventory):
        self.inventory = inventory

    def donItem(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
        self.wearing[item.getLocation()] = item
    def doffItem(self, item):
        if item in self.wearing:
            self.wearing.remove(item)
            self.inventory.append(item)

    def addMove(self):
        self.moves += 1
    def addPoints(self, points):
                self.points += points

