#!/usr/bin/env python

import argparse
import sys
import time

import tellcore.telldus as td
import tellcore.constants as const

# Web
import HomeMonitorWebApi as web

if sys.version_info < (3, 0):
    import tellcore.library as lib
    lib.Library.DECODE_STRINGS = False

def print_devices(devices):
    print("Number of devices: {}\n".format(len(devices)))
    print("{:<5s} {:<25s} {:<10s} {:<20s} {}".format(
        "ID", "NAME", "STATE", "PROTOCOL", "MODEL", "PARAMTERS"))
    for device in devices:
        params_str = ""
        for name, value in device.parameters().items():
            params_str += " {}:{}".format(name, value)
            
        print("{:<5d} {:<25s} {:<10s} {:<20s}{}".format(
                device.id, device.name,
                device.protocol, device.model, params_str))

def print_sensors(sensors):
    print("Number of devices: {}\n".format(len(sensors)))

    for sensor in sensors:
        if sensor.has_value(const.TELLSTICK_TEMPERATURE) and sensor.has_value(const.TELLSTICK_HUMIDITY):
            print("Id: {} Temp: {}".format(sensor.id, sensor.value(const.TELLSTICK_TEMPERATURE).value))

                  
                            
    

def load_devices_from_file(filename):
    print("Loading devices from file")

core = td.TelldusCore()

print_sensors(core.sensors())



configs = web.get_sensor_configuration()
for config in configs:
    print ("{} {}".format(config.id, config.location))


web.save_sensor_reading(id, 23.3)


