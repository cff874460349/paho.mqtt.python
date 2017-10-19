#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as client

import json
from collections import OrderedDict

import pytest
from enum import Enum

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


class deviceType(Enum):
    IRT3122 = 1
    IRT3122CS = 2
    IRT3112 = 3

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
            topicHead='/Thingworx/IOP-'
            break
        if case(): 
            print "something else!"

    print topicHead


