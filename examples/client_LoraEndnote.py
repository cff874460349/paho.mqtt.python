#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2010-2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# Copyright (c) 2010,2011 Roger Light <roger@atchoo.org>
# All rights reserved.

# This shows a simple example of an MQTT subscriber.

import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    


def on_message(mqttc, obj, msg):
    print( "topic:" + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
#mqttc = mqtt.Client()
#mqttc.on_message = on_message
#mqttc.on_connect = on_connect
#mqttc.on_publish = on_publish
#mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
#mqttc.connect("172.18.33.194", 1883, 60)
#mqttc.subscribe("0CB16D62C9FB5828/devices/0000000022000003/up", 0)

if __name__ == '__main__':
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    print("Inited!")
  

    try:
        a=100
        a=mqttc.connect("192.168.202.172", port=1883, keepalive=60)
        print("a=%d" %a)
        #mqttc.subscribe("574023A670C500A3/devices/0000000000220103/up", 0)
        mqttc.subscribe("/Thingworx/IOP-88-88-88-88-88-10/config_info", 0)
        print("Publish")
        topic = "/Thingworx/IOP-88-88-88-88-88-10/meta_data"
        payload = ("type": 2,
            "deviceType": 3,
            "ipAddr": "1.2.3.4",
            "macAddr": "00-00-00-00-00-01",
            "serialNum": "1234942570010",
            "softWareVer": "AP_RGOS 11.1(5)B39, Release(04181200)",
            "hardwareType":"IOP-WA(EDU) 1.00",
            "softwareNumber":"M00173906122017",
            "apMode":-1)

        (rc, mid) = mqttc.publish(topic, payload, qos=1)
        mqttc.loop_forever()
    except KeyboardInterrupt:
        mqttc.disconnect()