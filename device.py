#
# Class Sensor to extend DigitalInputDevice for T-Rax
#

import datetime
from gpiozero import DigitalInputDevice, DigitalOutputDevice
import logging
from time import sleep
import threading

import browser
import util

statusInterval = 60     # Seconds between status updates without input changes

class Gpio:

    def __init__(self, simulator=0):
        Gpio.wx = self.Sensor(pin=4, name='wx')           # weatherOk
        Gpio.bldg = self.Sensor(pin=17, name='bldg')      # bldgPowerIn
        Gpio.mntin = self.Sensor(pin=22, name='mntin')    # mountPowerIn
        Gpio.roofin = self.Sensor(pin=27, name='roofin')  # roofPowerIn
        Gpio.park = self.Sensor(pin=25, name='park')      # mountParked
        Gpio.open = self.Sensor(pin=23, name='open')      # roofOpen
        Gpio.close = self.Sensor(pin=24, name='close')    # roofClosed

        Gpio.heart = self.Control(pin=13, name='heart')                       # heartLed
        Gpio.mntout = self.Control(pin=6, name='mntout', active_high=False)   # mountPowerOut
        Gpio.roofout = self.Control(pin=5, name='roofout', active_high=False) # roofPowerOut
        Gpio.laser = self.Control(pin=16, name='laser')                       # laserPowerOut
        Gpio.fob = self.Control(pin=26, name='fob')                           # fobOutput

        Gpio.simulator = simulator


    class Sensor:
        sensors = []    # array of all sensor instances (in order of creation for status printout)
        by_name = {}    # dict of all sensors by name
        by_pin = {}     # dict of all sensors by pin
        names = []      # array of sensor names (in order of creation for status printout)

        def __init__(self, pin, name, pull_up=False, active_state=True, bounce_time=0.1, when_activated=0, when_deactivated=0):
            # TODO throw exception if pin not set
            self.name = name
            self.isSensor = True
            self.device = DigitalInputDevice(pin=pin, pull_up=pull_up, bounce_time=bounce_time)
            self.device.when_activated = when_activated if (when_activated) else self.activated
            self.device.when_deactivated = when_deactivated if (when_deactivated) else self.deactivated
            Gpio.Sensor.sensors.append(self)
            Gpio.Sensor.by_name[name] = self
            Gpio.Sensor.by_pin[pin] = self
            Gpio.Sensor.names.append(name)

        def is_active(self):
            return(self.device.is_active)

        def isOn(self):
            return(self.device.value == 1)

        def isOff(self):
            return(self.device.value == 0)

        # Default callbacks; override at instance creation or by setting <var>.device.when_[de]activated
        def activated(self):
            browser.browser.updateBrowser()
            logging.info(printStatus())

        def deactivated(self):
            browser.browser.updateBrowser()
            logging.info(printStatus())


    class Control:
        controls = []   # array of all sensor instances (in order of creation for status printout)
        by_name = {}    # dict of all controls by name
        by_pin = {}     # dict of all controls by pin
        names = []      # array of control names (in order of creation for status printout)

        def __init__(self, pin, name, active_high=True, initial_value=False, toggle_delay=0.5):
            # TODO throw exception if pin not set
            self.name = name
            self.isControl = True
            self.device = DigitalOutputDevice(pin=pin, active_high=active_high, initial_value=initial_value)
            self.toggle_delay = toggle_delay
            Gpio.Control.controls.append(self)
            Gpio.Control.by_name[name] = self
            Gpio.Control.by_pin[pin] = self
            Gpio.Control.names.append(name)

        def turnOn(self):
            self.device.on()
            browser.browser.updateBrowser()
            logging.info(printStatus())

        def turnOff(self):
            self.device.off()
            browser.browser.updateBrowser()
            logging.info(printStatus())

        def is_active(self):
            return(self.device.value == 1)

        def isOn(self):
            return(self.device.value == 1)

        def isOff(self):
            return(self.device.value == 0)

        def toggle(self, step=0):
            if (step == 0):
                logging.info("Toggle {}".format(self.name))
                self.turnOn();
                threading.Timer(self.toggle_delay, self.toggle, [1]).start()
            elif (step == 1):
                self.turnOff();
            else:
                logging.error("WTF? toggle() called with step %".format(step))


def printStatus():
    status = ''
    ### print(util.timestamp(), threading.get_ident(), end=' ')
    for sensor in Gpio.Sensor.sensors:
        if (sensor.is_active()):
            status += "[{}] ".format(sensor.name.upper())
        else:
            status += "({}) ".format(sensor.name)
    for control in Gpio.Control.controls:
        if (control.is_active()):
            status += "[{}] ".format(control.name.upper())
        else:
            status += "({}) ".format(control.name)
    return(status)

def beatHeart(output=0, step=0):
    if (step == 0):
        output.on()
        threading.Timer(0.1, beatHeart, [output,1]).start()
    elif (step == 1):
        output.off()
        threading.Timer(0.05, beatHeart, [output,2]).start()
    elif (step == 2):
        output.on()
        threading.Timer(0.1, beatHeart, [output,3]).start()
    elif (step == 3):
        output.off()
    else:
        logging.error("WTF? beatHeart() called with step %".format(step))


def perSecond():
    """Callback that runs every second to perform housekeeping duties"""
    browser.browser.sendTicker(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    if (int(datetime.datetime.now().second) % 2 == 0):
        beatHeart(Gpio.heart.device)
        browser.browser.updateBrowser()
    if (int(datetime.datetime.now().second) % statusInterval == 0):
        logging.info(printStatus())
    threading.Timer(1.0, perSecond).start()  # Redispatch self

