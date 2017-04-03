#!/usr/bin/env python


# Web
import json
import requests

class sensor_configuration(object):
    id = 0,
    location = ""

    def __init__(self, id, location):
        self.id = id
        self.location = location

class sensor_messurement(object):
    id = 0,
    temperature = 0.0

    def __init__(self, id, temperature):
        self.id = id
        self.temperature = temperature

#base_url = "http://homemonitorweb.azurewebsites.net"
base_url = "http://localhost:51895"
controller = "/api/sensorconfigurations"

def get_sensor_configuration():
    response = requests.get(base_url+controller)

    if not response.ok:
        print('Response is not ok')
        return

    if not response.headers.get('content-type').__contains__('application/json'):
        print('Wrong content type {}'.format(response.headers.get('content-type')))
        return

    configurations = []
    j = json.loads(response.content)
    for item in j:
        print("Adding: {}\n".format(item))
        configurations.append(sensor_configuration(**item))

    return configurations

def save_sensor_reading(sensorid, value):
    query = base_url + controller + '/{}'.format(sensorid)
    result = requests.put(query, data={"value":'{}'.format(value)})

    if not result.ok:
        print('Response is not ok')
