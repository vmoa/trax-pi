#
# Class Sensor to extend DigitalInputDevice for T-Rax
#

from gpiozero import DigitalInputDevice, DigitalOutputDevice

class Sensor:
    sensors = []    # array of all sensor instances (in order of creation for status printout)
    by_name = {}    # dict of all sensors by name
    by_pin = {}     # dict of all sensors by pin
    names = []      # array of sensor names (in order of creation for status printout)

    def __init__(self, pin, name, pull_up=False, active_state=True, bounce_time=0.1):
        # TODO throw exception if pin not set
        self.device = DigitalInputDevice(pin=pin, pull_up=pull_up, bounce_time=bounce_time)
        self.name = name
        Sensor.sensors.append(self)
        Sensor.by_name[name] = self
        Sensor.by_pin[pin] = self
        Sensor.names.append(name)

    def is_active(self):
        return(self.device.is_active)



class Control:
    controls = []   # array of all sensor instances (in order of creation for status printout)
    by_name = {}    # dict of all controls by name
    by_pin = {}     # dict of all controls by pin
    names = []      # array of control names (in order of creation for status printout)

    def __init__(self, pin, name, active_high=True, initial_value=False):
        # TODO throw exception if pin not set
        self.device = DigitalOutputDevice(pin=pin, active_high=active_high, initial_value=initial_value)
        self.name = name
        Control.controls.append(self)
        Control.by_name[name] = self
        Control.by_pin[pin] = self
        Control.names.append(name)

    def is_active(self):
        return(self.device.is_active)

    def on(self):
        return(self.device.on)

    def off(self):
        return(self.device.off)

