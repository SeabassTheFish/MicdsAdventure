#!/usr/local/bin/python3

from . import room
from . import enums
from . import item as i
from datetime import datetime
import json
import cgi
import cgitb
cgitb.enable()

def getRoomById(roomId, list):
    for item in list:
        if item.getId() == roomId:
            return item

def getItemByName(name, director):
    for room in director.getRooms():
        for item in room.getItems():
            if item.getName() == name:
                return item

def getEnumByName(name, enum):
    for item in enum:
        if name == item.name:
            return item

def generateEnvironmentFile(player, director):
    saveRooms = []
    saveExits = []

    for room in director.getRooms():
        saveRooms.append({
            "id": room.getId(),
            "Name": room.getName(),        
            "Lore": room.getLore(),
        })
        for exit in room.getExits():
            saveExits.append({
                "id": ":".join([room.getId(), exit.getLeadsTo().getId(), exit.getShortDirection().name])
            })
    return {"Rooms": saveRooms, "Exits": saveExits, "Last Update": stringNow()}

def generateSaveFile(player, director):
    saveItems = []
    saveNPCs = []
    saveContainers = []
    for item in player.getInventory():
        saveItems.append({
            "id": item.getId(),
            "Name": item.getName(),
            "Lore": item.getLore(),
            "Start": "INVENTORY",
            "Inspect": item.getInspect(),
            "Value": item.getValue(),
            "Location": item.getLocation().value if isinstance(item, i.Wearable) else 0,
            "Created": stringDate(item.getDate())
        })
    for item in player.getWearing():
        if item != 0:
            saveItems.append({
                "id": item.getId(),
                "Name": item.getName(),
                "Lore": item.getLore(),
                "Start": "WEARING",
                "Inspect": item.getInspect(),
                "Value": item.getValue(),
                "Location": item.getLocation().value,
                "Created": stringDate(item.getDate())
            })

    for room in director.getRooms():
        for item in room.getItems():
            if isinstance(item, i.Wearable):
                location = enums.WearableLoc(item.getLocation()).value
            else:
                location = 0
            saveItems.append({
                "id": item.getId(),
                "Name": item.getName(),
                "Lore": item.getLore(),
                "Start": room.getId(),
                "Inspect": item.getInspect(),
                "Value": item.getValue(),
                "Location": location,
                "Created": stringDate(item.getDate())
            })
        for npc in room.getNPCs():
            saveNPCs.append({
                "id": npc.getId(),
                "Name": npc.getName(),
                "Dialogue": npc.getDialogue(),
                "AI": npc.getAI(),
                "Health": npc.getHealth(),
                "CurrentRoom": room.getId()
            })
        for container in room.getContainers():
            saveContainers.append({
                "id": container.getId(),
                "items": container.getItems(),
            })
    
    returnJson = {
        "Items": saveItems,
        "NPCs": saveNPCs,
        "Containers": saveContainers,
    	"Current Room": director.getPlayers()[0].getCurrentRoom().getId(),
        "Last Update": stringNow()
    }
    return returnJson

def stringNow():
    return str(datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"))

def stringDate(dateObject):
    return str(datetime.strftime(dateObject, "%Y-%m-%d %H:%M:%S.%f"))

def unstringDate(stringDate):
    return datetime.strptime(stringDate, "%Y-%m-%d %H:%M:%S.%f")


