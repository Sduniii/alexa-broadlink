# coding: utf8

import re
from string import digits

action = u"10 lauter"

RE_D = re.compile('\d')
def has_number(s):
    return bool(RE_D.search(s))
number = 0
if ("lauter" in action or "leiser" in action) and has_number(action):
    number = [int(s) for s in action.split() if s.isdigit()][0]
    action = action.strip().replace(" ","").replace(".","")
    action = action.translate({ord(k): None for k in digits})

while number > 0:
    print(action + " ---- " + str(number))
    number -= 1
