#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

import json
from collections import OrderedDict

import pytest
#from enum import Enum

try:
    import paho

except ImportError:
    # This part is only required to run the examples from within the examples
    # directory when the module itself is not installed.
    import sys
    import os
    import inspect

    cmd_subfolder = os.path.realpath(
        os.path.abspath(
            os.path.join(
                os.path.split(
                    inspect.getfile(inspect.currentframe())
                )[0],
                "..",
                "src"
            )
        )
    )
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

    import paho
    import context  # Ensures paho is in PYTHONPATH
    import paho.mqtt.client as client


class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

def creat_topic(deviceType, deviceId, action):        
    for case in switch(deviceType):
        if case(1):
            break
        if case(2):
            break
        if case(3):
            topic = '/Thingworx/IOP-'+ deviceId + '/' + action
            topicRsp = '/Thingworx/IOP-'+ deviceId + '/' + action + '_rsp'
            break
        if case(): 
            print "something else!"

    print topic


def creat_message(deviceType, deviceId, action, messageId, message):
    dataJson = OrderedDict()
    for case in switch(deviceType):
        if case(1):
            break
        if case(2):
            break
        if case(3):
            for case in switch(action):
                if case('config_info'):                    
                    dataJson["tagType"]=2
                    dataJson["message_id"]=messageId
                    dataJson["message"]=message
                    dataJson["length"]=len(message)
                    break
                if case('firmware_update'):
                    dataJson["tagType"]=3
                    dataJson["message_id"]=messageId
                    dataJson["message"]=message
                    dataJson["length"]=len(message)
                    dataJson["fileLength"]=85
                    break
            break
        if case(): 
            print "something else!"
    payload_metaData = json.dumps(dataJson,sort_keys=False)
    print payload_metaData
    
if __name__ == '__main__':
    message = 'at+covrag=35\r\nat+sigprd=250\r\nat+sigramdly=50\r\nat+lcttype=2\r\nat+mqtthrtint=60\r\nat+led=on\r\nat+bt=on'
    creat_topic(3, '66-55-44-33-22-13', 'config_info')
    creat_message(3, '66-55-44-33-22-13', 'config_info', 1, message)


