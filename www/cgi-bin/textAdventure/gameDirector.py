#!/usr/local/bin/python3

# The GameDirector class file
from . import commands as com
from . import player as plr
from . import enums
from . import room as r

class GameDirector:
    def __init__(self):
        self.rooms = []
        self.players = []

    def getRooms(self):
        return self.rooms
    def getPlayers(self):
        return self.players
    def getNPCs(self):
        return self.npcs

    def addRoom(self, newRoom):
        self.rooms.append(newRoom)
    def addPlayer(self, newPlayer):
        self.players.append(newPlayer)

    def storeLast(self, command, player):
        if isinstance(command, com.Command) and isinstance(player, plr.Player):
            player.storeLast(command)

    def returnLast(self, player):
        return player.getLastMove()

    def movePlayer(self, player, room):
        player.setRoom(room)

    def getItemByName(self, player, name):
        for item in player.getCurrentRoom().getItems():
            if item.getName().lower() == name:
                return item

