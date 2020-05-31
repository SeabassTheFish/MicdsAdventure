#!/usr/local/bin/python3

# This is the item class

from datetime import datetime

class Item:
    def __init__(self, id, name, lore, created, inspect='', value=0):
        self.id = id
        self.name = name
        self.lore = lore
        self.inspect = inspect
        self.value = value
        self.dateCreated = datetime.strptime(created, "%Y-%m-%d %H:%M:%S.%f")

    def __str__(self):
        return self.name + ": " + self.lore

    def getName(self):
        return self.name
    def getLore(self):
        return self.lore
    def getId(self):
        return self.id
    def getValue(self):
        return self.value
    def strId(self):
        return self.id + ": " + self.__str__()
    def getDate(self):
        return self.dateCreated
    def getInspect(self):
        return self.inspect
    def toJson(self, room):
        return {\
            "id": self.id,
            "Name": self.name,
            "Lore": self.lore,
            "Start": room.getId(),
            "Value": self.value,
            "Location": 0,
            "Created": datetime.strftime(self.dateCreated, "%Y-%m-%d %H:%M:%S.%f")
        }

    def addValue(self, newValue):
        self.value = newValue

class Wearable(Item):
    def __init__(self, id, name, lore, location, created, inspect='', value=0):
        super().__init__(id, name, lore, created, inspect, value)
        self.location = location

    def getLocation(self):
        return self.location
    def toJson(self, room):
        return {\
            "id": self.id,
            "Name": self.name,
            "Lore": self.lore,
            "Start": room.getId(),
            "Value": self.value,
            "Location": self.location,
            "Created": datetime.strftime(self.dateCreated, "%Y-%m-%d %H:%M:%S.%f")
        }


