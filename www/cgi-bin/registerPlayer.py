#!/usr/local/bin/python3

import cgi
import cgitb
import json
import psycopg2
import psycopg2.extras
import hashlib
cgitb.enable()

form = cgi.FieldStorage()

def encrypt(inputString):
    m = hashlib.sha256()
    m.update(inputString.encode('utf-8'))
    return m.hexdigest()

def createPlayer(firstname, lastname, gradeLevel, username, password):
  try:
    password = encrypt(password)

    connection = psycopg2.connect("dbname=quarantine user=sebastian")
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''insert into players (id, username, password, firstname, lastname, grade_level) values (default, '{}', '{}', '{}', '{}', {});'''.format(username, password, firstname, lastname, gradeLevel))
    connection.commit()
    connection.close()
    return {"success": True}
  except Exception as e:
    print(e)
    return {"success": False}

print("Content-Type: application/json")
print()
print(json.dumps({"message": createPlayer(form["firstname"].value, form["lastname"].value, form["grade-level"].value, form["username"].value, form["password"].value)}))
