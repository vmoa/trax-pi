#
# Class Sensor to extend DigitalInputDevice for T-Rax
#

from gpiozero import DigitalInputDevice, DigitalOutputDevice
import logging
from time import sleep
import threading

import util

class Sensor:
    sensors = []    # array of all sensor instances (in order of creation for status printout)
    by_name = {}    # dict of all sensors by name
    by_pin = {}     # dict of all sensors by pin
    names = []      # array of sensor names (in order of creation for status printout)

    def __init__(self, pin, name, pull_up=False, active_state=True, bounce_time=0.1, when_activated=0, when_deactivated=0):
        # TODO throw exception if pin not set
        self.name = name
        self.device = DigitalInputDevice(pin=pin, pull_up=pull_up, bounce_time=bounce_time)
        self.device.when_activated = when_activated if (when_activated) else self.activated
        self.device.when_deactivated = when_deactivated if (when_deactivated) else self.deactivated
        Sensor.sensors.append(self)
        Sensor.by_name[name] = self
        Sensor.by_pin[pin] = self
        Sensor.names.append(name)

    def is_active(self):
        return(self.device.is_active)

    def isOn(self):
        return(self.device.value == 1)

    def isOff(self):
        return(self.device.value == 0)

    # Default callbacks; override at instance creation or by setting <var>.device.when_[de]activated
    def activated(self):
        logging.info(printStatus())

    def deactivated(self):
        logging.info(printStatus())


class Control:
    controls = []   # array of all sensor instances (in order of creation for status printout)
    by_name = {}    # dict of all controls by name
    by_pin = {}     # dict of all controls by pin
    names = []      # array of control names (in order of creation for status printout)

    def __init__(self, pin, name, active_high=True, initial_value=False):
        # TODO throw exception if pin not set
        self.name = name
        self.device = DigitalOutputDevice(pin=pin, active_high=active_high, initial_value=initial_value)
        Control.controls.append(self)
        Control.by_name[name] = self
        Control.by_pin[pin] = self
        Control.names.append(name)

    def turnOn(self):
        return(self.device.on())

    def turnOff(self):
        return(self.device.off())

    def is_active(self):
        return(self.device.value == 1)

    def isOn(self):
        return(self.device.value == 1)

    def isOff(self):
        return(self.device.value == 0)


def printStatus():
    status = ''
    ### print(util.timestamp(), threading.get_ident(), end=' ')
    for sensor in Sensor.sensors:
        if (sensor.is_active()):
            status += "[{}] ".format(sensor.name.upper())
        else:
            status += "({}) ".format(sensor.name)
    for control in Control.controls:
        if (control.is_active()):
            status += "[{}] ".format(control.name.upper())
        else:
            status += "({}) ".format(control.name)
    return(status)
