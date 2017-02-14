# -*- coding: utf-8 -*- 

from flask import Flask
from flask_ask import Ask, statement, question, session
import logging
import time
import bmdevices as bm
import database as js
import traceback
import re
from string import digits

app = Flask(__name__)
ask = Ask(app, "/")

RE_D = re.compile('\d+')

logging.getLogger("flask_ask").setLevel(logging.DEBUG)
logging.basicConfig(filename='static/error.log',level=logging.DEBUG)

def has_number(s):
    return bool(RE_D.search(s))

@app.route('/')
def index():
    return 'This is Alexa LGTV Skill'

@ask.launch
def launch():
    return question("Hallo, was möchstest du tun?")

@ask.intent("ActionIntent")
def action(action):
    try:
        action = action.replace(".","").replace(" ","")
	if action == "aus":
            action = "power"
        elif action == "an":
            action = "up"

        device = bm.load_device_for_remote("tv", debug=False)
        if device != None:
            macro_code = js.load_macro(action)
            macro_send = True
            if macro_code != None:
                for c in macro_code.split("|"):
                    macro_send &= device.send_code(str(c),"tv")
                    time.sleep(0.1)
                time.sleep(0.1)
                if macro_send:
                    return statement("Ok... ").simple_card(title="Du sagtest...",content=str(action))
            else:
                send_code = device.send_code(str(action),"tv")
                time.sleep(0.1)
                if send_code:
                    return statement("Ok... ").simple_card(title="Du sagtest...",content=str(action))
                else:
                    return statement((u"Befehl " + unicode(action) + u" existiert nicht.").encode('utf-8')).simple_card(title="Du sagtest...",content=str(action))
        else:
            return statement((u"Leider ging etwas schief bei dem Befehl " + unicode(action) + u"!").encode('utf-8')).simple_card(title="Du sagtest...",content=str(action))
    except:
        return statement("Es ist ein Ausnahmefehler aufgetreten Tobias. Bitte debugen!" + str(traceback.format_exc())).simple_card(title="Du sagtest...",content=str(action))

@ask.intent("DoubleActionIntent")
def double_action(number, action):
    try:
        action = action.replace(".","").replace(" ","")
        number = int(number)
        device = bm.load_device_for_remote("tv")
        if device != None:
            macro_code = js.load_macro(action)
            macro_send = True
            if macro_code != None:
                for c in macro_code.split("|"):
                    macro_send &= device.send_code(str(c),"tv")
                    time.sleep(0.1)
                time.sleep(0.1)
                if macro_send:
                    return statement("Ok... ").simple_card(title="Du sagtest...",content=str(number) + " " + str(action))
            else:
                send_code = True
                while number > 0 and send_code:
                    print(action)
                    send_code &= device.send_code(str(action),"tv")
                    number -= 1
                    time.sleep(0.1)
                if send_code:
                    return statement("Ok... ").simple_card(title="Du sagtest...",content=str(number) + " " + str(action))
                else:
                    return statement((u"Befehl " + unicode(action) + u" existiert nicht.").encode('utf-8')).simple_card(title="Du sagtest...",content=str(number) + " " + str(action))
        else:
            return statement((u"Leider ging etwas schief bei dem Befehl " + unicode(action) + u"!").encode('utf-8')).simple_card(title="Du sagtest...",content=str(number) + " " + str(action))
    except:
        return statement("Es ist ein Ausnahmefehler aufgetreten Tobias. Bitte debugen!" + str(traceback.format_exc())).simple_card(title="Du sagtest...",content=str(number) + " " + str(action))

if __name__ == '__main__':
    app.run(debug=True)

#action("an")
