#!/usr/bin/env python
"""Main module for monitoring sensors"""

import threading
import time
import datetime

import TellStick as tellstick_module

# import SunSettingService
# Web
import HomeMonitorWebApi as web

# CONFIGS = web.get_sensor_configuration()
# for config in CONFIGS:
#     print("{} {}".format(config.identity, config.location))

TELLSTICK = tellstick_module.Tellstick()



# class TandLyset(threading.Thread):
#     """Thread that turns light on"""
#     light_is_lit = False

#     def __init__(self, thread_id, tellstick):
#         threading.Thread.__init__(self)
#         self.thread_id = thread_id
#         self.tellstick = tellstick

#     def run(self):
#         while True:
#             time.sleep(60)
#             try:
#                 sunset = SunSettingService.get_sunset_for_today()
#                 is_after_sunset = sunset < (datetime.datetime.now() - datetime.time.minute(40))
#                 is_night_time = datetime.datetime.now().time > datetime.time.hour(23).minute(30)

#                 if is_after_sunset and not self.light_is_lit:
#                     self.tellstick.tand_lyset()
#                     self.light_is_lit = True
#                 elif is_night_time and self.light_is_lit:
#                     self.tellstick.slack_lyset()
#                     self.light_is_lit = False

#             except:
#                 print("oops in TandLyset")


class ReadSensorData(threading.Thread):
    """Thread class that reads sensor data and delivers info to web."""
    import tellcore.constants as const
    configurations = []
    def __init__(self, tellstick):
        threading.Thread.__init__(self)
        self.tellstick = tellstick

    def run(self):

        while True:
            try:
                results = []
                configurations = web.get_sensor_configuration()

                for sensor in self.tellstick.get_sensors():
                    if any(sensor.id == config.identity for config in configurations):
                        has_temp = sensor.has_value(self.const.TELLSTICK_TEMPERATURE)
                        has_humidity = sensor.has_value(self.const.TELLSTICK_HUMIDITY)

                        if has_temp and has_humidity:
                            temp = sensor.value(self.const.TELLSTICK_TEMPERATURE)
                            humid = sensor.value(self.const.TELLSTICK_HUMIDITY)
                            results.append(web.SensorMessurement(sensor.id, \
                                temp, \
                                humid, \
                                humid.timestamp))

                if any(results):
                    web.save_sensor_readings(results[1])

            except Exception as e:
                print("oops in readSensorData! {}".format(e))
                time.sleep(10)
                continue

            time.sleep(60*5)

## Main
try:
    # T1 = TandLyset(1, TELLSTICK)
    T2 = ReadSensorData(TELLSTICK)
    # T1.start()
    T2.start()
except:
    print("Error unable to start thread")

TELLSTICK.run_loop()





# web.save_sensor_reading(id, 23.3)




# if sys.version_info < (3, 0):
#     import tellcore.library as lib
#     lib.Library.DECODE_STRINGS = False

# def print_devices(devices):
#     print("Number of devices: {}\n".format(len(devices)))
#     print("{:<5s} {:<25s} {:<10s} {:<20s} {}".format(
#         "ID", "NAME", "STATE", "PROTOCOL", "MODEL", "PARAMTERS"))
#     for device in devices:
#         params_str = ""
#         for name, value in device.parameters().items():
#             params_str += " {}:{}".format(name, value)

#         print("{:<5d} {:<25s} {:<10s} {:<20s}{}".format(device.id, device.name, \
#                 device.protocol, device.model, params_str))

# def print_sensors(sensors):
#     print("Number of devices: {}\n".format(len(sensors)))

#     for sensor in sensors:
#         if sensor.has_value(const.TELLSTICK_TEMPERATURE) \
#             and sensor.has_value(const.TELLSTICK_HUMIDITY):
#             print("Id: {} Temp: {}".format(sensor.id, sensor.value(const.TELLSTICK_TEMPERATURE).value))


