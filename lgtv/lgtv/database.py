import simplejson as json
import os
import traceback

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')

def load_database_by_mac(mac):
    try:
        f = open(os.path.join(APP_STATIC,mac + '.json'), 'r')
        d = json.loads(f.read())
        f.close()
        return d
    except:
        print(traceback.format_exc())
        return None

def write_database_by_mac(mac, json_string):
    try:
        f = open(os.path.join(APP_STATIC,mac + '.json'), "w")
        f.write(json.dumps(json_string))
        f.close()
        return True
    except:
        print(traceback.format_exc())
        return False

def write_remote_belongs_to_mac(mac, remote):
    try:
        data = {}
        data[remote] = mac
        if os.path.exists(os.path.join(APP_STATIC,'remotes.json')):
            f = open(os.path.join(APP_STATIC,'remotes.json'),'r')
            try:
                data = json.loads(f.read())
                data[remote] = mac
                f.close()
            except:
                f.close()
        
        f = open(os.path.join(APP_STATIC,'remotes.json'), 'w')
        f.write(json.dumps(data))
        f.close()
        return True
    except:
        print(traceback.format_exc())
        return False
        
def load_mac_belongs_to_remote(remote):
    try:
        f = open(os.path.join(APP_STATIC,'remotes.json'),'r')
        mac = json.loads(f.read())[remote]
        f.close()
        return mac
    except:
        print(traceback.format_exc())
        return None

def load_macro(macro_name):
    try:
        f = open(os.path.join(APP_STATIC,'macros.json'),'r')
        macro_sequence = json.loads(f.read())
        f.close()
        return macro_sequence.get(macro_name)
    except:
        print(traceback.format_exc())
        return None
        
def write_macro(macro_name, sequence):
    try:
        data = {}
        data[macro_name] = sequence
        if os.path.exists(os.path.join(APP_STATIC,'macros.json')):
            f = open(os.path.join(APP_STATIC,'macros.json'),'r')
            try:
                data = json.loads(f.read())
                data[macro_name] = sequence
                f.close()
            except:
                f.close()
        
        f = open(os.path.join(APP_STATIC,'macros.json'),'w')
        f.write(json.dumps(data))
        f.close()
        return True
    except:
        print(traceback.format_exc())
        return False
