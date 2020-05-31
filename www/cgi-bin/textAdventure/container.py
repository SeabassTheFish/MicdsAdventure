#!/usr/local/bin/python3

# This is the container class. Literally something that contains items.
from . import item

class Container:
    def __init__(self, id, name="C", lore="C"):
        self.id = id
        self.items = []
        self.name = name
        self.lore = lore

    # All the get functions
    def getId(self):
        return self.id
    def getItems(self):
        return self.items
    def getName(self):
        return self.name
    def getLore(self):
        return self.lore

    # All the set functions
    def setName(self, newName):
        self.name = newName
    def setLore(self, newLore):
        self.lore = newLore

    # All the add and remove functions
    def addItem(self, newItem):
        if isinstance(newItem, item.Item):
            self.items.append(newItem)
        else:
            raise Exception("Container trying to accept non-item")
    def removeItem(self, oldItem):
        if isinstance(oldItem, item.Item):
            if oldItem in self.items:
                self.items.remove(oldItem)
            else:
                raise Exception("Item not in container")
        else:
            raise Exception("Trying to remove non-item from container")
