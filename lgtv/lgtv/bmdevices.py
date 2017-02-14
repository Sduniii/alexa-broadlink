# -*- coding: utf-8 -*-

import time
import broadlink
import sys
import os
import database as js
import traceback
import socket

def scan_for_devices(timeout):
    devices = broadlink.discover(timeout=timeout)
    return devices
    
def load_device_for_remote(remote, debug=False):
    mac = js.load_mac_belongs_to_remote(remote)
    if debug:
        print mac
    if mac == None:
        return None
    try:
        device = BroadlinkDevice(mac=mac, debug=debug)
        return device
    except socket.timeout:
        host = check_device(mac)
        print(host)
        if host == None:
            return None
        try:
            device = BroadlinkDevice(mac=mac,host=host,debug=debug)
            device.save()
            return device
        except:
            return None
def check_device(mac):
    devices = broadlink.discover(timeout=5)
    for index, item in enumerate(devices):
        print(mac)
        mac2 = ''.join(format(x, '02x') for x in item.mac[::-1])
        print(mac2)
        if mac2 == mac:
            return item.host
    return None

class BroadlinkDevice(object):
    def __init__(self, device = None, mac = None, host = None, debug = False):
        try:
            self.debug = debug
            self.name = None
            self.code_database = {}
            self.mac = mac
            self.device_id = None
            self.device = device
            self.host = host
            self.auth = False
            
            if self.debug:
                print("Init BroadlinkDevice: (mac: {}, device: {})".format(mac,device))
            
            if device == None and mac != None and host == None:
                db = js.load_database_by_mac(self.mac)
                if db != None:
                    self.device = broadlink.gendevice(devtype=db['deviceId'],host=(db['ip'],db['port']),mac=bytearray.fromhex(self.mac),timeout=1)
                    self.code_database = db.get('codes')
                    self.name = db.get('name')
                    self.device_id = self.device.devtype
                    self.host = self.device.host
            elif device == None and mac != None and host != None:
                db = js.load_database_by_mac(self.mac)
                if db != None:
                    self.device = broadlink.gendevice(devtype=db['deviceId'],host=self.host,mac=bytearray.fromhex(self.mac),timeout=1)
                    self.code_database = db.get('codes')
                    self.name = db.get('name')
                    self.device_id = self.device.devtype
            elif device != None:
                self.mac = str(''.join(format(x, '02x') for x in self.device.mac[::-1]))
                db = js.load_database_by_mac(self.mac)
                if db != None:
                    self.code_database = db.get('codes')
                    self.name = db.get('name')
                    self.device_id = self.device.devtype
                    self.host = self.device.host
                        
            if self.device != None:
                if self.debug:
                    print("auth...")
                self.auth = self.device.auth()
                if self.debug:
                    print("auth: " + str(self.auth))
        except:
            if debug:
                print(traceback.format_exc())
            raise          
        
    def learn_code(self, codename, remote):
        try:
            self.device.enter_learning()
            if self.debug:
                print("warte 10 sec auf Code")
            i = 0
            code = self.device.check_data()
            while code == None and i < 21:
                time.sleep(0.5)
                code = self.device.check_data()
                i+=1
            code_in_hex = str(code).encode('hex')
            if code != None:
                if self.code_database.get(remote) == None:
                    self.code_database[remote] = {}
                self.code_database[remote][codename] = code_in_hex
            js.write_remote_belongs_to_mac(self.mac,remote)
            return True
        except:
            print(traceback.format_exc())
            return False

    def send_code(self, codename, remote):
        try:
            if self.debug:
                print("send_code("+codename+", "+remote+")")
                print("Code: " + self.code_database.get(remote).get(codename))
            code = self.code_database.get(remote).get(codename).decode('hex')
            self.device.send_data(code)
            return True
        except:
            print(traceback.format_exc())
            return False

    def save(self):        
        json = {'ip':self.host[0], 'port':self.host[1], 'name':self.name, 'deviceId':self.device_id, 'codes':self.code_database}
        return js.write_database_by_mac(self.mac, json)
