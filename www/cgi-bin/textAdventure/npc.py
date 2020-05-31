#!/usr/local/bin/python3

# This is the NPC Class
from .character import Character

class NPC(Character):
    def __init__(self, id, name, dialogue, ai, health):
        super().__init__(name) # Gives the NPC a name and null current room
        self.id = id
        self.name = name
        self.dialogue = dialogue
        self.ai = ai
        self.health = health

    def __str__(self):
        return self.name

    def getId(self):
        return self.id
    def getName(self):
        return self.name
    def getDialogue(self):
        return self.dialogue
    def getAI(self):
        return self.ai
    def getHealth(self):
        return self.health

    def setHealth(self, newHealth):
        self.health = newHealth
    def setAI(self, newAI):
        self.ai = newAI

