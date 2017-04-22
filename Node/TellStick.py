
"""Modul som skickar sensordata till webtjänst och tänder lyset när det blir mörkt"""

import time
import datetime
import threading
import SunSettingService
import HomeMonitorWebApi as web
import tellcore.telldus as td
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
    light_is_lit = False
    def __init__(self):
        try:
            import asyncio
            self.loop = asyncio.get_event_loop()
            dispatcher = td.AsyncioCallbackDispatcher(self.loop)
        except ImportError:
            self.loop = None
            dispatcher = td.QueuedCallbackDispatcher()
        self.core = td.TelldusCore(callback_dispatcher=dispatcher)
        self.core.register_device_event(self.device_event)

    def device_event(self, id_, method, data, cid):
        """Hantera device events"""
        method_string = METHODS.get(method, "UNKNOWN METHOD {0}".format(method))
        string = "[DEVICE] {0} -> {1}".format(id_, method_string)
        if method == const.TELLSTICK_DIM:
            string += " [{0}]".format(data)
        print(string)
        if method == const.TELLSTICK_TURNOFF:
            self.light_is_lit = False
        elif method == const.TELLSTICK_TURNON:
            self.light_is_lit = True

    def get_sensors(self):
        """Returns the core object"""
        return self.core.sensors()

    def tand_lyset(self):
        """Tänder lyset"""
        devices = self.core.devices()
        for device in devices:
            device.turn_on()

    def slack_lyset(self):
        """Släcker lyset"""
        devices = self.core.devices()
        for device in devices:
            device.turn_off()

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

