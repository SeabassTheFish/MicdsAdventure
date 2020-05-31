#!/usr/local/bin/python3

# The Command abstract class
from .gameDirector import GameDirector
from . import player as plr
from . import item as i
from . import npc
from . import enums
from .eventHandler import *
from .utils import *
import sys
from datetime import datetime


# All commands must return some string in their execute, even if it's empty.

class Command:
    def __init__(self):
        pass

    def execute(self, player, director):
        if isinstance(director, GameDirector) and isinstance(player, plr.Player):
            director.storeLast(self, player)
        else:
            raise Exception("Bad player or director for execute command")

# General Commands
class Nonsense(Command):
    def __init__(self):
        super().__init__()

    def execute(self, player, director):
        return "Nonsense!"

class Quit(Command):
    def __init__(self):
        super().__init__()

    def execute(self, player=None, director=None):
        sys.exit()

# Interaction Commands
class Interact(Command):
    def __init__(self, target):
        super().__init__()
        self.target = target

    def execute(self, player, director):
        super().execute(player, director)

class ItemInteract(Interact):
    def __init__(self, type, target):
        super().__init__(target)
        self.type = type
        self.target = target

    def execute(self, player, director):
        super().execute(player, director)
        if self.type == "use":
            return useItem(player, director, self.target)
        elif self.type == "don":
            item = player.getItemByName(" ".join(self.target))
            if item is not None:
                if isinstance(item, i.Wearable):
                    player.donItem(item)
                    return "Donned " + "\"" + item.getName() + "\""
                else:
                    return "You can't wear that."
            else:
                return "Don what?"
        elif self.type == "doff":
            item = player.getItemByName(" ".join(self.target))
            if item is not None:
                if isinstance(item, i.Wearable):
                    player.doffItem(item)
                    return "Doffed " + "\"" + item.getName() + "\""
                else:
                    return "You can't take that off."
            else:
                return "Doff what?"
        elif self.type == "take":
            item = director.getItemByName(player, " ".join(self.target))
            if item is not None:
                player.getCurrentRoom().removeItem(item)
                player.addItem(item)
                return "\"" + item.getName() + "\" added to inventory."
            return "Take what?"
        elif self.type == "drop":
            item = player.getItemByName(" ".join(self.target))
            if item is not None:
                player.removeItem(item)
                player.getCurrentRoom().addItem(item)
                return "\"" + item.getName() + "\" dropped."
            return "Drop what?"
        elif self.type == "inspect":
            item = director.getItemByName(player, " ".join(self.target))
            if item is None:
                item = player.getItemByName(" ".join(self.target))

            if item is not None:
                return item.getInspect()
        return ""


class CharacterInteract(Interact):
    def __init__(self, target):
        super().__init__(target)

    def execute(self, player, director):
        super().execute(player, director)
        return ""

class PlayerInteract(CharacterInteract):
    def __init__(self, target):
        super().__init__(target)

    def execute(self, player, director):
        super().execute(player, director)
        return ""

class NPCInteract(CharacterInteract):
    def __init__(self, target):
        super().__init__(target)

    def execute(self, player, director):
        super().execute(player, director)
        return ""

# All the sense commands
class Sense(Command):
    def __init__(self):
        super().__init__()

    def execute(self, player, director):
        super().execute(player, director)

class Compass(Sense):
    def __init__(self):
        super().__init__()

    def execute(self, player, director):
        super().execute(player, director)
        outstrings = {
            "north": "|",
            "south": "|",
            "east": "-",
            "west": "-",
            "northeast": "@@",
            "northwest": "@@",
            "southeast": "@@",
            "southwest": "@@",
            "up": "|",
            "down": "|",
            "in": "@",
            "out": "@"
        }
        for exit in player.getCurrentRoom().getExits():
            if str(exit.getDirection().name).lower() in outstrings:
                outstrings[exit.getDirection().name.lower()] = enums.ShortDirection(exit.getDirection().value).name
# The above line finds the corresponding short direction and puts it on the compass

        return ("@@@@@^@@@@@#@{}@@{}@@{}@#@@\@@{}@@/@@#&lt;{}---*---{}&gt;#@@/@@{}@@\@#@{}@@{}@@{}@#@@@@@V#@@{}@@@{}".format(\
        outstrings["northwest"],
        outstrings["north"],
        outstrings["northeast"],
        outstrings["up"],
        outstrings["west"],
        outstrings["east"],
        outstrings["down"],
        outstrings["southwest"],
        outstrings["south"],
        outstrings["southeast"],
        outstrings["in"],
        outstrings["out"]
        ))

class Inventory(Sense):
    def __init__(self):
        super().__init__()

    def execute(self, player, director):
        super().execute(player, director)
        inventory = player.getInventory()
        if len(inventory) == 0:
            return "Your hands are empty"
        else:
            outstring = player.getName() + " is holding: \n"
        for item in inventory:
            outstring = outstring + "    " + item.getName() + ": " + item.getLore() + "\n"
        return outstring

class Look(Sense):
    def __init__(self):
        super().__init__()

    def execute(self, player, director):
        super().execute(player, director)
        return str(player.getCurrentRoom())

class Wearing(Sense):
    def __init__(self):
        super().__init__()

    def execute(self, player, director):
        super().execute(player, director)
        outArray = []
        for item in player.getWearing():
            if item != 0:
                outArray.append(item)

        outstring = ""
        if len(outArray) != 0:
            outstring = player.getName() + " is wearing:"
            for item in outArray:
                outstring = outstring + "\n\t\"" + item.getName() + "\" on their " + enums.WearableLoc(item.getLocation()).name.lower()
        return outstring

# The movement command
class Movement(Command):
    def __init__(self, direction):
        super().__init__()
        self.direction = direction
        if not isinstance(direction, enums.Direction):
            raise Exception("No direction on movement")

    def execute(self, player, director):
        super().execute(player, director)
        if player.getCurrentRoom().canMove(self.direction):
            director.movePlayer(player, player.getCurrentRoom().getLeadsToByDirection(self.direction))
            roomEntry = onRoomEntry(player, director)
            return roomEntry
        else:
            return "You can't go that way"

class Shout(Command):
    def __init__(self, words):
        super().__init__()
        self.words = words

    def execute(self, player, director):
        super().execute(player, director)
        eventHandle = onShout(player, director, self.words)
        if eventHandle is not "":
            return eventHandle
        return words.upper()

class Help(Command):
    def __init__(self):
        super().__init__()

    def execute(self, player, director):
        super().execute(player, director)
        file = open("./textAdventure/help.txt", "r")
        return " " 

class G(Command):
    def __init__(self):
        super().__init__()

    def execute(self, player, director):
        super().execute(player, director)
        director.returnLast(player).execute()
        return " "

class Save(Command):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def execute(self, player, director):
        super().execute(player, director)
        writeFile = open("./{}.json".format(datetime.now().strftime("%H_%M_%S")), "w+")
        writeFile.write(generateSaveFile(player, director))
        writeFile.close()
        return "Saved!"

class Restore(Command):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def execute(self, player, director):
        super().execute(player, director)

