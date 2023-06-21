#
# Class Sensor to extend DigitalInputDevice for T-Rax
#

import enum
import datetime
from gpiozero import DigitalInputDevice, DigitalOutputDevice
import logging
import threading
import time

import browser
import sse
import util

statusInterval = 60     # Seconds between status updates without input changes

# Define an enum with possible park states
class park(enum.Enum):
    PARKED = enum.auto()
    UNPARKED = enum.auto()
    PARKED_PROBABLY = enum.auto()
    UNPARKED_PROBABLY = enum.auto()
    UNKNOWN = enum.auto()

# Define an enum with possible roof positions
class roof(enum.Enum):
    OPEN = enum.auto()
    CLOSED = enum.auto()
    MIDWAY = enum.auto()
    CONFUSED = enum.auto()  # When reporting both open and closed

# Define a dict of strings for roof position
roofString = {
    roof.OPEN     : 'OPEN',
    roof.CLOSED   : 'CLOSED',
    roof.MIDWAY   : 'MIDWAY',
    roof.CONFUSED : 'CONFUSED',
}


class Gpio:

    def __init__(self, simulator=0):
        """Connect all our devices. Set `simulator` to increase timings so a human can respond."""
        Gpio.simulator = simulator  
        Gpio.wx = self.Sensor(pin=4, name='wx')           # weatherOk
        Gpio.bldg = self.Sensor(pin=17, name='bldg')      # bldgPowerIn
        Gpio.mntin = self.Sensor(pin=22, name='mntin')    # mountPowerIn
        Gpio.roofin = self.Sensor(pin=27, name='roofin')  # roofPowerIn
        Gpio.park = self.Sensor(pin=25, name='park')      # mountParked
        Gpio.open = self.Sensor(pin=23, name='open')      # roofOpen
        Gpio.close = self.Sensor(pin=24, name='close')    # roofClosed

        Gpio.heart = self.Control(pin=13, name='heart')    # heartLed
        Gpio.mntout = self.Control(pin=6, name='mntout')   # mountPowerOut
        Gpio.roofout = self.Control(pin=5, name='roofout') # roofPowerOut
        Gpio.laser = self.Control(pin=16, name='laser')    # laserPowerOut
        Gpio.fob = self.Control(pin=26, name='fob')        # fobOutput


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

            # Park sensor magic
            if (name == 'park'):
                self.parkLastCheck = 0           # Time of last actual laser-on check of park state
                self.parkSensorDelay = 5         # Seconds to wait for park sensor after turing on laser
                self.park_report_last_state = 10 # Seconds to believe last park state
                self.park_report_unknown = 60    # Seconds after which we admit we've been guessing at park state
                if (Gpio.simulator):
                    self.parkSensorDelay = 15    # Give human more time to simulate park


        def is_active(self):
            return(self.device.is_active)

        def isOn(self):
            return(self.device.value == 1)

        def isOff(self):
            return(self.device.value == 0)

        def checkParked(self):
            """Check and report park status. Turn on laser and give park sensor time to activate."""
            browser.browser.sendNotice('Laser ON checking park')
            Gpio.laser.device.on()
            countdown = self.parkSensorDelay
            logging.info("Laser activated; waiting up to {} seconds for park sensor".format(countdown))
            while (self.isOff() and countdown > 0):
                time.sleep(0.1)  # Does not block other threads, yay!
                countdown = countdown - 0.1
            Gpio.laser.device.off()
            logging.info("Laser active for {:0.1f} seconds".format(self.parkSensorDelay - countdown))
            if (self.device.value == 1):
                browser.browser.sendNotice('Parked')
                self.parkLastState = park.PARKED
            else:
                browser.browser.sendNotice('Not parked')
                self.parkLastState = park.UNPARKED
            self.parkLastCheck = int(time.time())  # Track time of check so user can "see" how fresh it is
            browser.browser.updateBrowser()
            logging.info(printStatus())
            return(self.parkLastState);

        def isParked(self):
            """Report on park status, modified by length of time since last check."""
            age = int(time.time()) - self.parkLastCheck
            if (age < self.park_report_last_state):
                return(self.parkLastState)  # We still "believe"
            elif (age > self.park_report_unknown):
                return(park.UNKNOWN)  # Just too long to wager a guess
            else:
                if (self.parkLastState == park.PARKED):
                    return(park.PARKED_PROBABLY)
                else:
                    return(park.UNPARKED_PROBABLY)

        def roofPosition(self):
            """Return roof position."""
            if (Gpio.open.isOn() and Gpio.close.isOn()):
                logging.error("Roof is CONFUSED; reporting both open and closed")
                return roof.CONFUSED
            if (Gpio.open.isOn()):
                return roof.OPEN
            elif (Gpio.close.isOn()):
                return roof.CLOSED
            else:
                return roof.MIDWAY

        # Default callbacks; override at instance creation or by setting <var>.device.when_[de]activated
        def activated(self):
            browser.browser.updateBrowser()
            logging.info(printStatus())
            if (self.name in ('open', 'close')):
                browser.browser.sendNotice('Roof is {}'.format(roofString[self.roofPosition()]))

        def deactivated(self):
            browser.browser.updateBrowser()
            logging.info(printStatus())
            if (self.name in ('open', 'close')):
                browser.browser.sendNotice('Roof is {}'.format(roofString[self.roofPosition()]))


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

            # Fob control magic
            if (name == 'fob'):
                self.fob_wait = self.toggle_delay + 3.0    # Delay after toggle to check for roof motion
                self.fob_tries = 3                         # How many times we try toggling before we give up
                self.togglingFob = 0                       # Flag to track when we're toggling

            # Laser timeOut for emergency override
            if (name == 'laser'):
                self.laser.timeOut = 0                      # Turn off the laser after this time()
                self.laser.defaultTimeOut = 120             # Seconds to leave the laser on before timing out

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
            """Toggle the control ouput on then off"""
            if (step == 0):
                logging.info("Toggle {}".format(self.name))
                self.turnOn();
                threading.Timer(self.toggle_delay, self.toggle, [1]).start()
            elif (step == 1):
                self.turnOff();
            else:
                logging.error("WTF? toggle() called with step %".format(step))

        # Fob has speical toggle magic to ensure the roof starts moving
        def toggleFob(self, step=0):
            """Toggle fob and check for roof movement, retrying up to fob_tries times"""
            if (self.name != 'fob'):
                logging.error("toggleFob() called for {}".format(self.name))
                return(-1)
            if (step == 0 and self.togglingFob):
                logging.error("toggleFob() called while toggling already in progress")
                return(-1)
            # If roof is middle just revert to toggle
            if (step == 0 and Gpio.open.roofPosition() == roof.MIDWAY):
                self.togglingFob = 0
                self.toggle()
                return(0)

            # If we're a scheduled callback check for status
            if (step > 0 and Gpio.open.roofPosition() == roof.MIDWAY):
                browser.browser.sendNotice("Roof is midway")
                logging.info("toggleFob() detected roof movement")
                self.togglingFob = 0
                return(0)

            # Bail after x tries
            if (step >= self.fob_tries):
                browser.browser.sendNotice("No roof movement; giving up")
                logging.error("toggleFob() failed to detect movement after {} tries; giving up".format(step))
                self.togglingFob = 0
                return(1)

            # Toggle and schedule a callback to check for movement
            if (step > 0):
                browser.browser.sendNotice("Retrying fob ({}/{})".format(step+1, self.fob_tries))
            self.togglingFob = 1  # Should we use a timestamp so we can "expire" just in case?
            self.toggle()
            logging.info("toggleFob({}) waiting {} seconds".format(step, self.fob_wait))
            threading.Timer(self.fob_wait, self.toggleFob, [step+1]).start()
            return(0)


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

def timeOutLaser(laser):
    '''Time out and turn off the laser.'''
    browser.browser.sendNotice("Laser timeout")
    logging.info("Timing out laser")
    laser.timeOut = 0
    laser.off()

def perSecond():
    """Callback that runs every second to perform housekeeping duties"""
    browser.browser.sendTicker("%s&nbsp;&nbsp;&nbsp;%s" % (
        "[%d connection%s]" %(sse.sse.count(), "" if sse.sse.count()==1 else "s"),
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    if (int(datetime.datetime.now().second) % 2 == 0):
        beatHeart(Gpio.heart.device)
        browser.browser.updateBrowser()
    if (int(datetime.datetime.now().second) % statusInterval == 0):
        logging.info(printStatus())
    if (Gpio.laser.timeOut > 0 and int(time.time()) > Gpio.laser.timeOut):
        timeOutLaser(Gpio.laser)
    threading.Timer(1.0, perSecond).start()  # Redispatch self

