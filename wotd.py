#!flask/bin/python
from flask import Flask, jsonify, request
import requests
import json
import re
from requests.packages import urllib3
urllib3.disable_warnings()
 
app = Flask(__name__)
 
BASE_URL = "http://api.wordnik.com:80/v4/words.json/wordOfTheDay"
API_KEY = 'a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5'
payload = {'api_key': API_KEY}
 
@app.route('/wotd', methods=['GET', 'POST'])
def wordsmith():
    message = ""
    colour = "green"
    # args = request.get_json()
    # date = args["item"]["message"]["date"]
    # date_spliced = date[:10]
    # print(date_spliced)
    r = requests.get(BASE_URL, params=payload, verify=False)
    r.encoding = "utf-8"
    try:
        if r.status_code != 200:
            raise UserWarning
        try:
            content = r.json()
            # word = unicode(content['word'], 'utf-8')
            message += "Today's word of the day is: <br><b>" + content['word'] + "</b><br>Definition(s):<br> <ul>"
            for definition in content['definitions']:
                message += "<li>" + definition['partOfSpeech'] + " - " + definition['text'] + "</li>"
            message += "</ul>"
        except ValueError:
            raise ValueError
    except ValueError:
        message += "Error! No json data could be retrieved."
        colour = "red"
    except UserWarning:
        message += "Error! Either server didn't respond or has resulted in zero results.<br>" \
                   "Status code: " + str(r.status_code)
        colour = "red"
    except Exception:
        message += "Error!"
        colour = "red"
    res = {"message": message, "color": colour, "message_format": "html"}
    return jsonify(res)
 
 
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)