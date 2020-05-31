#!/usr/local/bin/python3

#This is the main class file

# TODO:
# Add new features: NPC, multiplayer, HTTP

from . import character as ch
from . import commands as com
from . import container as con
from . import enums as e
from . import exit as ex
from . import gameDirector as g
from . import item as i
from . import npc as n
from . import player as p
from . import room as r
import json
from . import proparse as pr
from . import eventHandler as eh
from .utils import getRoomById, getEnumByName, generateSaveFile, generateEnvironmentFile

def runAdventure(gamestate, environment, inputText):
    # Init
    player = p.Player()
    director = g.GameDirector()
    director.addPlayer(player)

    parsed = pr.P()

    for element in environment["Rooms"]:
        director.addRoom(r.Room(element["id"], element["Name"], element["Lore"]))
    for element in environment["Exits"]:
        newExit = element["id"].split(":") # From has index 0, To has index 1, Direction has index 2
        getRoomById(newExit[0], director.getRooms()).addExit(ex.Exit(getRoomById(newExit[1], director.getRooms()), e.Direction(getEnumByName(newExit[2], e.ShortDirection).value)))
    for element in gamestate["Items"]:
        if element["Start"] == "INVENTORY":
            if element["Location"] != 0:
                player.addItem(i.Wearable(element["id"], element["Name"], element["Lore"], element["Created"], e.WearableLoc(element["Location"]), element["Inspect"], element["Value"]))
            else:
                player.addItem(i.Item(element["id"], element["Name"], element["Lore"], element["Created"], element["Inspect"], element["Value"]))
        elif element["Start"] == "WEARING":
            if element["Location"] != 0:
                player.donItem(i.Wearable(element["id"], element["Name"], element["Lore"], e.WearableLoc(element["Location"]), element["Created"], element["Inspect"], element["Value"]))
        else:
            if element["Location"] != 0:
                getRoomById(element["Start"], director.getRooms()).addItem(i.Wearable(element["id"], element["Name"], element["Lore"], e.WearableLoc(element["Location"]), element["Created"], element["Inspect"], element["Value"]))
            else:
                getRoomById(element["Start"], director.getRooms()).addItem(i.Item(element["id"], element["Name"], element["Lore"], element["Created"], element["Inspect"], element["Value"]))
              
    for element in gamestate["NPCs"]:
        getRoomById(element["Current Room"], director.getRooms()).addNPC(n.NPC(element["id"], element["Name"], element["Dialogue"], element["AI"], element["Health"]))

    player.setRoom(getRoomById(gamestate["Current Room"], director.getRooms()))

    outputText = parsed.parse(inputText, player, director)
    newGamestate = generateSaveFile(player, director)
    newEnvironment = generateEnvironmentFile(player, director)
    return {"output": outputText, "gamestate": newGamestate, "environment": newEnvironment}

