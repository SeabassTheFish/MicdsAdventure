#!/usr/local/bin/python3

import cgi
import cgitb
import json
from .imports import *
cgitb.enable()

parser = pr.P()
player = p.Player()
director = g.GameDirector()

player.setRoom(getRoomById("ALT-ANE", director.getRooms()))

def returnGet(inputText=""):
  return {"message": parser.parse(inputText, player, director)}

print('Content-Type: application/json')
print()
form = cgi.FieldStorage()
print(json.dumps(returnGet(form.getvalue("text"))))
