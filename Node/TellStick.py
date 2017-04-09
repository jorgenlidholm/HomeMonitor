
"""Modul som tänder lyset när det blir mörkt"""

import time
import datetime
import threading
import SunSettingService
import HomeMonitorWebApi as web
import tellcore.constants as const

METHODS = {const.TELLSTICK_TURNON: 'turn on',
           const.TELLSTICK_TURNOFF: 'turn off',
           const.TELLSTICK_BELL: 'bell',
           const.TELLSTICK_TOGGLE: 'toggle',
           const.TELLSTICK_DIM: 'dim',
           const.TELLSTICK_LEARN: 'learn',
           const.TELLSTICK_EXECUTE: 'execute',
           const.TELLSTICK_UP: 'up',
           const.TELLSTICK_DOWN: 'down',
           const.TELLSTICK_STOP: 'stop'}

EVENTS = {const.TELLSTICK_DEVICE_ADDED: "added",
          const.TELLSTICK_DEVICE_REMOVED: "removed",
          const.TELLSTICK_DEVICE_CHANGED: "changed",
          const.TELLSTICK_DEVICE_STATE_CHANGED: "state changed"}

CHANGES = {const.TELLSTICK_CHANGE_NAME: "name",
           const.TELLSTICK_CHANGE_PROTOCOL: "protocol",
           const.TELLSTICK_CHANGE_MODEL: "model",
           const.TELLSTICK_CHANGE_METHOD: "method",
           const.TELLSTICK_CHANGE_AVAILABLE: "available",
           const.TELLSTICK_CHANGE_FIRMWARE: "firmware"}

TYPES = {const.TELLSTICK_CONTROLLER_TELLSTICK: 'tellstick',
         const.TELLSTICK_CONTROLLER_TELLSTICK_DUO: "tellstick duo",
         const.TELLSTICK_CONTROLLER_TELLSTICK_NET: "tellstick net"}



class Tellstick():
    """Tellstick main class"""
    loop = None
    core = None

    def __init__(self):
        import tellcore.telldus as td
        try:
            import asyncio
            self.loop = asyncio.get_event_loop()
            dispatcher = td.AsyncioCallbackDispatcher(self.loop)
        except ImportError:
            self.loop = None
            dispatcher = td.QueuedCallbackDispatcher()

        self.core = td.TelldusCore(callback_dispatcher=dispatcher)

        self.core.register_device_change_event(self.device_change_event_handler)
        self.core.register_device_event(self.device_event)
        self.core.register_controller_event(self.controller_event)

    def get_sensors(self):
        """Returns the core object"""
        return self.core.sensors()

    def tand_lyset(self):
        """Tänder lyset"""
        devices = self.core.devices()
        for device in devices:
            device.turn_on()

    def device_event(self, id_, method, data, cid):
        """Hantera device events"""
        method_string = METHODS.get(method, "UNKNOWN METHOD {0}".format(method))
        string = "[DEVICE] {0} -> {1}".format(id_, method_string)
        if method == const.TELLSTICK_DIM:
            string += " [{0}]".format(data)
        print(string)

    def device_change_event_handler(self, id_, event, type_, cid):
        """Hantera events från enheter."""
        event_string = EVENTS.get(event, "UNKNOWN EVENT {0}".format(event))
        string = "[DEVICE_CHANGE] {0} {1}".format(event_string, id_)
        if event == const.TELLSTICK_DEVICE_CHANGED:
            type_string = CHANGES.get(type_, "UNKNOWN CHANGE {0}".format(type_))
            string += " [{0}]".format(type_string)
        print(string)

    def controller_event(self, id_, event, type_, new_value, cid):
        """Hantera events från controller"""
        event_string = EVENTS.get(event, "UNKNOWN EVENT {0}".format(event))
        string = "[CONTROLLER] {0} {1}".format(event_string, id_)
        if event == const.TELLSTICK_DEVICE_ADDED:
            type_string = TYPES.get(type_, "UNKNOWN TYPE {0}".format(type_))
            string += " {0}".format(type_string)
        elif event == const.TELLSTICK_DEVICE_CHANGED \
            or event == const.TELLSTICK_DEVICE_STATE_CHANGED:
            type_string = CHANGES.get(type_, "UNKNOWN CHANGE {0}".format(type_))
            string += " [{0}] -> {1}".format(type_string, new_value)
        print(string)


    def run_loop(self):
        """Event loop runner"""
        try:
            if self.loop:
                self.loop.run_forever()
            else:
                while True:
                    self.core.callback_dispatcher().process_pending_callbacks()
                    time.sleep(0.5)
        except KeyboardInterrupt:
            pass


class TandLyset(threading.Thread):
    """Thread that turns light on"""

    def __init__(self, thread_id, tellstick):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.tellstick = tellstick

    def run(self):
        while True:
            try:
                sunset = SunSettingService.get_sunset_for_today()
                if sunset > datetime.datetime.now(): #- datetime.time.minute(10):
                    continue
                self.tellstick.tand_lyset()
            except:
                print("oops in TandLyset")

            time.sleep(60)

class ReadSensorData(threading.Thread):
    """Thread class that reads sensor data and delivers info to web."""
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
                        has_temp = sensor.has_value(const.TELLSTICK_TEMPERATURE)
                        has_humidity = sensor.has_value(const.TELLSTICK_HUMIDITY)
                        if has_temp and has_humidity:
                            results.append(web.SensorMessurement(sensor.id, \
                                sensor.value(const.TELLSTICK_TEMPERATURE), \
                                sensor.value(const.TELLSTICK_HUMIDITY)))
            except:
                print("{}".format('oops in readSensorData!'))

            time.sleep(60*10)




