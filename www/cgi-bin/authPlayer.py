#!/usr/local/bin/python3

import psycopg2
import psycopg2.extras
import json
import cgi
import cgitb
import random
import hashlib
cgitb.enable()

form = cgi.FieldStorage()

def randomString(length):
    acceptableChars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',\
    'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'\
    '1','2','3','4','5','6','7','8','9','0'];
    outstring = ""
    for i in range(length):
        randomNum = int(random.random() * len(acceptableChars))
        outstring = outstring + acceptableChars[randomNum]
    return outstring

def encrypt(inputString):
    m = hashlib.sha256()
    m.update(inputString.encode('utf-8'))
    return m.hexdigest()

def authPlayer(username, password):
    try:
        connection = psycopg2.connect("dbname=quarantine user=sebastian")
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('''select id, password from players where username='{}';'''.format(username))
        fetched = cursor.fetchone()

        returnDict = {"session": "", "status": False}
        if fetched["password"] == encrypt(password):
            returnDict["session"] = randomString(30)
            returnDict["status"] = True
            cursor.execute('''insert into sessions values (default, '{}', '{}', now(), now())'''.format(fetched["id"], returnDict["session"])) 
            cursor.execute('''delete from sessions where last_used < now() - interval '24 hours\';''')

            defaultSave = open('defaultSave.json', 'r').read()
            defaultEnvironment = open('./textAdventure/environmentSave.json', 'r').read()
            cursor.execute('''select g.* from gamestates g, players p where p.id='{}' and g.player_id=p.id'''.format(fetched["id"]))
            fetchedOne = cursor.fetchone()
            if fetchedOne is None:
                cursor.execute('''insert into gamestates values (default, {}, '{}', '{}');'''.format(fetched["id"], defaultSave.replace("'", r"''"), defaultEnvironment.replace("'", r"''")))

        connection.commit()
        connection.close()
    except Exception as e:
        returnDict = {"message": "Middle level exception: " + str(e), "status": False, "session": ""}

    return returnDict 

print('Content-Type: application/json')
print()
try:
    print(json.dumps({"response": authPlayer(form["username"].value, form["password"].value)}))
except Exception as ex:
    print('''{"response": {"message": "Top level exception: {}"}}'''.format(str(ex)))
