#!/usr/local/bin/python3

# This program checks for differences between an established save file and the master save
# and merges the two into one coherent save file

import json
import psycopg2
import psycopg2.extras
import copy
from datetime import datetime
from textAdventure.utils import stringNow, stringDate, unstringDate

def checkDiff(player_id):
    
    diffFile = json.loads(open("diff.json", "r").read())

    add = {
        "rooms": [],
        "exits": [],
        "items": [],
        "containers": [],
        "npcs": []
    }
    modify = {
        "rooms": [],
        "exits": [],
        "items": [],
        "containers": [],
        "npcs": []
    }
    delete = {
        "rooms": [],
        "exits": [],
        "items": [],
        "containers": [],
        "npcs": []
    }

    for element in diffFile:
        if element["action"] == "add":
            element["addition"].update({"entry-made": element["entry-made"]})
            add[str(element["type"] + "s")].append(element["addition"])
            continue
        if element["action"] == "modify":
            element["modification"].update({"entry-made": element["entry-made"]})
            modify[str(element["type"] + "s")].append(element["modification"])
            continue
        if element["action"] == "delete":
            element["deletion"].update({"entry-made": element["entry-made"]})
            delete[str(element["type"] + "s")].append(element["deletion"])
            continue
        raise Exception("An element doesn't have a correct action")

    connection = psycopg2.connect("dbname=quarantine user=sebastian")
    c = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    c.execute('''select gamestate, environment from gamestates where player_id = {};'''.format(player_id))
    fetched = c.fetchone()
    
    oldGamestate = fetched["gamestate"]
    oldGamestateUpdate = unstringDate(oldGamestate["Last Update"])
    oldEnvironment = fetched["environment"]
    oldEnvironmentUpdate = unstringDate(oldEnvironment["Last Update"])

    newGamestate = copy.deepcopy(oldGamestate) # Ensures that these return values are separate from the originals, so changing the new one leaves the old intact
    newEnvironment = copy.deepcopy(oldEnvironment)

    fileSorter = {
        "room": {"old": oldEnvironment, "new": newEnvironment, "dest": "Rooms"},
        "exit": {"old": oldEnvironment, "new": newEnvironment, "dest": "Exits"},
        "item": {"old": oldGamestate, "new": newGamestate, "dest": "Items"},
        "container": {"old": oldGamestate, "new": newGamestate, "dest": "Containers"},
        "npc": {"old": oldGamestate, "new": newGamestate, "dest": "NPCs"}
    }

    for key, value in add.items():
        for addElement in value:
            relevantInfo = fileSorter[key[:-1]]
            if unstringDate(addElement["entry-made"]) > unstringDate(relevantInfo["old"]["Last Update"]):
                addElement.update({"Created": stringNow()})
                relevantInfo["new"][relevantInfo["dest"]].append(addElement)

    for key, value in modify.items():
        for modElement in value:
            relevantInfo = fileSorter[key[:-1]]
            if unstringDate(modElement["entry-made"]) > unstringDate(relevantInfo["old"]["Last Update"]):
                destArray = relevantInfo["new"][relevantInfo["dest"]]
                for element in destArray:
                    if element["id"] == modElement["id"]:
                        for key, value in modElement.items():
                            element["key"] = value

    for key, value in delete.items():
        for delElement in value:
            relevantInfo = fileSorter[key[:-1]]
            if key == "rooms":
                exitsToDelete = []
                for exit in oldEnvironment["Exits"]:
                    delExit = exit["id"].split(":")
                    if delExit[0] == delElement["id"] or delExit[1] == delElement["id"]:
                        exit.update({"entry-made": stringNow()})
                        exitsToDelete.append(exit)
                delete["exits"].extend(exitsToDelete)
            if unstringDate(delElement["entry-made"]) > unstringDate(relevantInfo["old"]["Last Update"]):
                destArray = relevantInfo["new"][relevantInfo["dest"]]
                for element in destArray:
                    if element["id"] == delElement["id"]:
                        destArray.remove(element)

    newGamestate.update({"Last Update": stringNow()})
    newEnvironment.update({"Last Update": stringNow()})

    c.execute('''update gamestates set environment = %s, gamestate = %s where player_id = %s''', (json.dumps(newEnvironment), json.dumps(newGamestate), player_id))

    connection.commit()
    connection.close()
