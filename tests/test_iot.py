#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

import json
from collections import OrderedDict

import pytest
import Queue
#from enum import Enum
import paho.mqtt.client as mqtt
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
    return topic, topicRsp


def creat_message(deviceType, deviceId, action, messageId, message):
    dataJson = OrderedDict()
    for case in switch(deviceType):
        if case(1):
            break
        if case(2):
            break
        if case(3):#case IRT3112
            for case in switch(action):
                if case('config_info'):#配置
                    dataJson["tagType"]=2
                    dataJson["message_id"]=messageId
                    dataJson["message"]=message
                    dataJson["length"]=len(message)
                    break
                if case('firmware_update'):#升级
                    dataJson["tagType"]=3
                    dataJson["message_id"]=messageId
                    dataJson["message"]=message
                    dataJson["length"]=len(message)
                    dataJson["fileLength"]=85
                    break
            break
        if case(): 
            print "something else!"
    payload_metaData = json.dumps(dataJson, sort_keys=False)
    print payload_metaData
    return payload_metaData

def subscribe_callback(mqttc, obj, msg):
    print( "topic:" + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    return msg.topic, msg.payload

mqttc = mqtt.Client()
mqttc.on_message = subscribe_callback

def connet_mqtt_server(host):
    a=mqttc.connect(host, port=1883, keepalive=60)
    
def disconnet_mqtt_server():
    mqttc.disconnect()

def subscribe_topic(deviceType, deviceIdArray, action):
    for deviceId in deviceIdArray:
        topic, topic_rsp = creat_message(deviceType, deviceId, action)
        mqttc.subscribe(topic_rsp, 0)

def publish_topic(deviceType, deviceIdArray, action, testTimes, message):
    for messageid in range(0, testTimes):
        for deviceId in deviceIdArray:
            topic, topic_rsp = creat_topic(deviceType, deviceId, action)
            payload = creat_message(deviceType, deviceId, action, messageId, message)
            (rc, mid) = mqttc.publish(topic, payload, qos=1)
        
        

if __name__ == '__main__':
    connet_mqtt_server('192.168.202.172')
    message = 'at+covrag=35\r\nat+sigprd=250\r\nat+sigramdly=50\r\nat+lcttype=2\r\nat+mqtthrtint=60\r\nat+led=on\r\nat+bt=on'
    creat_topic(3, '66-55-44-33-22-13', 'config_info')
    creat_message(3, '66-55-44-33-22-13', 'config_info', 1, message)
    publish_topic(3, '66-55-44-33-22-13', 'config_info', 1, message)


