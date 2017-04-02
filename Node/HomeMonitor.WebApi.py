#!/usr/bin/env python


# Web
import requests
import json

class sensor_configuration(object):
    id = 0,
    location = ""

    def __init__(self, id, location)
        self.id = id
        self.location = location
        
base_url = "http://homemonitorweb.azurewebsites.net"
controller = "/api/sensorconfiguration"
    
def get_sensor_configuration():
    sensors = requests.get(base_url+controller)
    print(sensors.text)
    
    
    
