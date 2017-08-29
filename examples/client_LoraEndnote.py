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


def on_connect(mqttc, userdata, flags, rc):
    print("rc: " + str(rc))
    client.subscribe("0CB16D62C9FB5828/devices/0000000022000003/up", 0)


def on_message(mqttc, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obuserdataj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, userdata, level, string):
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
    client = mqtt.Client()
    client.on_connect = on_connect    
    client.on_message = on_message

    try:
        client.connect('172.18.33.194', port=1883)        
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()