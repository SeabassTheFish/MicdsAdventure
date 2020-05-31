#!/usr/local/bin/python3

import sys
import cgi
import cgitb
import json
import psycopg2
import psycopg2.extras
import traceback
from datetime import datetime
from textAdventure.main import runAdventure
from checkDiff import checkDiff
cgitb.enable()

def main():
    output = { 'error': True }
    try:
        def stringDivider(inputString, chopLength):
            outArray = []
            inputArray = inputString.split("#")

            for i in range(len(inputArray)):
                latestSpace = chopLength
                while len(inputArray[i]) > chopLength:
                    for j in range(chopLength, -1, -1):
                        if inputArray[i][j] == "@" or inputArray[i][j] == " ":
                            latestSpace = j
                            break;

                    outArray.append(inputArray[i][:latestSpace])
                    inputArray[i] = inputArray[i][latestSpace:]
            outArray.extend(inputArray)

            for i in range(len(outArray)):
                outArray[i] = outArray[i].replace("@", "&nbsp")

            return outArray

        def run(inputText, session_id):
            outlines = []
            try:
                connection = psycopg2.connect("dbname=quarantine user=sebastian")
                cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute('''select g.gamestate, p.id, g.environment from players p, sessions s, gamestates g where s.session_token = '{}' and s.player_id = p.id and p.id = g.player_id'''.format(session_id))
                fetched = cursor.fetchone()
                gamestate = fetched["gamestate"]
                player_id = fetched["id"]
                environment = fetched["environment"]

                try:
                    adventure = runAdventure(gamestate, environment, inputText)
                    output['message'] = stringDivider(adventure["output"], 80)

                    checkDiff(player_id)
                    cursor.execute('''update players set current_room = '{}';'''.format(gamestate["Current Room"]))
                    output['error'] = False
                except Exception as ex:
                    output['message'] = [ 'Error in runAdventure', traceback.format_exc() ]

                connection.commit()
                connection.close()

            except Exception as e:
                output['message'] = [ "Mid level error:", str(e), traceback.format_exc() ]

        form = cgi.FieldStorage()
        try:
            run(form["input_text"].value, form["session_id"].value)
        except Exception as ex:
            output['message'] = [ "Top Level Error:", str(ex), traceback.format_exc() ]

    except Exception as topLevelException:
        output['message'] = [ 'Mega Error:', str(topLevelException), traceback.format_exc() ]

    print('Content-Type: application/json')
    print()
    print(json.dumps(output))

if __name__ == "__main__":
    main()
