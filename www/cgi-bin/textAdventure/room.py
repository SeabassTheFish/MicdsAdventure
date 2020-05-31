#!/usr/local/bin/python3

# This is the room class
from . import exit
from . import item
from . import container
from . import enums

class Room:
    def __init__(self, id, name="Empty Room", lore="empty room"):
        self.name = name
        self.id = id
        self.lore = lore
        self.items = []
        self.exits = []
        self.containers = []
        self.npcs = []
        self.visited = False

    def __str__(self):
        outstring = self.name + ": " + self.lore
        if len(self.items) is not 0:
            outstring = outstring + "#This room contains:"
            for item in self.items:
                outstring = outstring + "#@@" + str(item)
        if len(self.npcs) is not 0:
            outstring = outstring + "#Occupying this room is:"
            for npc in self.npcs:
                outstring = outstring + "#@@" + str(npc)
        return outstring

    # Allowing other methods to access member variables
    def getName(self):
        return self.name
    def getExits(self):
        return self.exits
    def getStringExits(self):
        return [str(x) for x in self.exits]
    def getExit(self, index):
        return self.exits[index]
    def getLore(self):
        return self.lore
    def getId(self):
        return self.id
    def getItems(self):
        return self.items
    def getContainers(self):
        return self.containers
    def getNPCs(self):
        return self.npcs
    def getLeadsToByDirection(self, direction):
        for exit in self.exits:
            if exit.getDirection() == direction:
                return exit.getLeadsTo()
        return None

    # Little function to help the GameDirector
    def canMove(self, direction):
        for ex in self.exits:
            if ex.getDirection().value == direction.value:
                return True
        return False


    # Allowing other methods to change member variables
    def setName(self, newName):
        self.name = newName
    def setExits(self, newExits):
        self.exits = newExits
    def setExit(self, newExit, index):
        self.exits[index] = newExit
    def setLore(self, newLore):
        self.lore = newLore
    def setVisited(self, vis=True):
        self.visited = vis

    # Add functions
    def addExit(self, newExit):
        self.exits.append(newExit)
    def addItem(self, newItem):
        self.items.append(newItem)
    def addNPC(self, newNPC):
        self.npcs.append(newNPC)
    def removeItem(self, oldItem):
        self.items.remove(oldItem)
    def addContainer(self, newContainer):
        self.containers.append(newContainer)

