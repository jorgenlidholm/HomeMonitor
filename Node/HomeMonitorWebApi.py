#!/usr/bin/env python


# Web
import json

import datetime

class SensorConfiguration(object):
    """Configuration object"""
    identity = 0,
    location = ""

    def __init__(self, identity, location):
        self.identity = identity
        self.location = location

    def get_configuration(self):
        """json string"""
        return {'identity' : self.identity, 'location': self.location}

    def set_location(self, location):
        """set location of sensor"""
        self.location = location



class SensorMessurement(object):
    """Sensor messurement object"""
    identity = 0,
    temperature = 0.0
    humidity = 0.0

    def __init__(self, identity, temperature, humidity):
        self.identity = identity
        self.temperature = temperature
        self.humidity = humidity

#BASE_URL = "http://homemonitorweb.azurewebsites.net"
BASEURL = "http://localhost:51895"
SENSORCONFIGROUTE = "/api/sensorconfigurations"
LIGHTINGCONFIGROUTE = "/api/lightingconfigurations"
SENSORDATAROUTE = "/api/sensordate"

def get_sensor_configuration():
    """Reads sensor configuration from web."""
    import requests
    response = requests.get(BASEURL+SENSORCONFIGROUTE, headers=get_headers())

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
        configurations.append(SensorConfiguration(**item))

    return configurations

def save_sensor_reading(sensorid, value):
    """Some info"""
    import requests
    query = BASEURL + SENSORDATAROUTE + '/{}'.format(sensorid)
    result = requests.put(query, data={"value":'{}'.format(value)}, headers=get_headers())

    if not result.ok:
        print('Response is not ok')

def get_authentication_token(key):
    """Creates security token."""
    import hashlib
    hash_content = hashlib.sha256()
    secret = '{}{}'.format("Äpplen, bananer och andra frukter", key)

    hash_content.update(secret.encode())
    return hash_content.hexdigest()

def get_headers():
    """Get header for authentication"""
    current_time = datetime.datetime.now().isoformat(timespec='seconds')
    return {'X-HomeMonitor-Secret': '{},{}'.format(current_time, \
        	get_authentication_token(current_time))}


def get_lighting_configuration():
    """Reads lighting configuration from web."""
    import requests
    response = requests.get(BASEURL+LIGHTINGCONFIGROUTE, headers=get_headers())

    if not response.ok:
        print('Response is not ok')
        return

    if not response.headers.get('content-type').__contains__('application/json'):
        print('Wrong content type {}'.format(response.headers.get('content-type')))
        return

    configurations = []
    j = json.loads(response.content)
    # for item in j:
    #     print("Adding: {}\n".format(item))
    #     configurations.append(sensor_configuration(**item))

    print('{}'.format(j))
    return configurations

# c0da4c400404034fd83a03500544272d2c35d25197fcf02b5c9fff49ede0c2e4

#get_lighting_configuration()

