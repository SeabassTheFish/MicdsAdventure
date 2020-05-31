#!/usr/local/bin/python3

#The parser file
from . import commands as com
from .enums import Direction

class P:
    def __init__(self):
        pass

    def parse(self, inputString, player, director):
        splitString = inputString.lower().replace("\"", "").split(" ")
        verb = splitString[0];
        if len(splitString[1:]) == 0 and verb == "save":
            splitString.append("")
        commandConverter = {
            "drop": com.ItemInteract("drop", splitString[1:]),
            "take": com.ItemInteract("take", splitString[1:]),
            "grab": com.ItemInteract("take", splitString[1:]),
            "use": com.ItemInteract("use", splitString[1:]),
            "don": com.ItemInteract("don", splitString[1:]),
            "doff": com.ItemInteract("doff", splitString[1:]),
            "inspect": com.ItemInteract("inspect", splitString[1:]),
            "examine": com.ItemInteract("inspect", splitString[1:]),
            "look": com.Look(),
            "compass": com.Compass(),
            "inventory": com.Inventory(),
            "i": com.Inventory(),
            "quit": com.Quit(),
            "q": com.Quit(),
            "north": com.Movement(Direction.NORTH),
            "n": com.Movement(Direction.NORTH),
            "south": com.Movement(Direction.SOUTH),
            "s": com.Movement(Direction.SOUTH),
            "east": com.Movement(Direction.EAST),
            "e": com.Movement(Direction.EAST),
            "west": com.Movement(Direction.WEST),
            "w": com.Movement(Direction.WEST),
            "southeast": com.Movement(Direction.SOUTHEAST),
            "se": com.Movement(Direction.SOUTHEAST),
            "southwest": com.Movement(Direction.SOUTHWEST),
            "sw": com.Movement(Direction.SOUTHWEST),
            "northeast": com.Movement(Direction.NORTHEAST),
            "ne": com.Movement(Direction.NORTHEAST),
            "northwest": com.Movement(Direction.NORTHWEST),
            "nw": com.Movement(Direction.NORTHWEST),
            "up": com.Movement(Direction.UP),
            "u": com.Movement(Direction.UP),
            "down": com.Movement(Direction.DOWN),
            "d": com.Movement(Direction.DOWN),
            "in": com.Movement(Direction.IN),
            "out": com.Movement(Direction.OUT),
            "help": com.Help(),
            "?": com.Help(),
            "g": com.G(),
            "wearing": com.Wearing(),
            "talk": com.CharacterInteract(splitString[1:]),
            "t": com.CharacterInteract(splitString[1:]),
            "quit": com.Quit(),
            "q": com.Quit(),
            "save": com.Save(splitString[1:]),
            "shout": com.Shout(splitString[1:]),
            "say": com.Shout(splitString[1:]),

        }

        if verb in commandConverter:
            outstring = commandConverter[verb].execute(player, director)
            if outstring is not "":
                return outstring
        return com.Nonsense().execute(player, director)

