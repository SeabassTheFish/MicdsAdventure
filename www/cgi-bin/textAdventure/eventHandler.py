#!/usr/local/bin/python3

from . import exit as e
from . import enums
from . import utils

# This is the event handler stuff

def onRoomEntry(player, director):
    room = player.getCurrentRoom()
    outstring = str(player.getCurrentRoom())
    if room.getId() == "ALT-FGP":
        return outstring + "#You are at the flagpole."
    if room.getId() == "ALT-ASW":
        return outstring + "#You are in the southwest of A lot."
    return outstring

def useItem(player, director, item):
    item = utils.getItemByName(" ".join(item), director)
    if item is not None:
        return "You slightly lucky dog"
        if item.getId() == "IPR":
            return "You lucky dog"
    return "You unlucky dog"

def onShout(player, director, words):
    room = player.getCurrentRoom()
    
    if room.getId() == "ALT-FGP":
        if len(words) == 1 and words[0].lower() == "rainey":
            room.addExit(e.Exit(utils.getRoomById("ALT-ANE", director.getRooms()), enums.Direction(6)))
            return "Jaysus smiles upon you"

    return " ".join(words).upper()
