#!/usr/bin/python3
#
# TraxTester class for T-Rax roof controller
#
# This is to verify that all the pins are connected as designed, and a validation
# of the interrupt driven mechanism.

from datetime import datetime
from gpiozero import DigitalInputDevice, DigitalOutputDevice
import os
import re
import signal
import socket
import sys
from time import sleep

from device import Sensor, Control
import util

class TestMode:

    def blinkOnce(self, output=0):
        util.printStatus()
        output.on()
        sleep(0.25)
        output.off()

    def blinkTwice(self, output=0):
        if (output != Control.by_name['heart'].device):
            util.printStatus()
        output.on()
        sleep(0.1)
        output.off()
        sleep(0.05)
        output.on()
        sleep(0.1)
        output.off()

    def __init__(self):
        print("TEST MODE: Entering test mode")
        if (re.match('^172\.19\.9\.', util.get_ip())):
            # Make life easy for Dave
            print("TEST MODE: Welcome back, Dave")
        else:
            print()
            print("****************************************************************")
            print("**** DANGER: Test mode must NOT be run on the real roof!!!  ****") 
            print("****        Physical damage will surely ensue               ****")
            print("****   It is intended for being run ONLY on the test rig    ****")
            print("****************************************************************")
            print()
            answer = input("Confirm you are connected to the test rig by typing TEST RIG now: ")
            if (answer == 'TEST RIG'):
                print("It's a fair cop.")
            else:
                print("Abort.")
                exit(1)

        # Set up testing triggers
        Sensor.by_name['mntin'].device.when_activated  = lambda: self.blinkOnce(Control.by_name['mntout'].device)
        Sensor.by_name['roofin'].device.when_activated = lambda: self.blinkOnce(Control.by_name['roofout'].device)
        Sensor.by_name['park'].device.when_activated   = lambda: self.blinkOnce(Control.by_name['laser'].device)
        Sensor.by_name['close'].device.when_activated  = lambda: self.blinkOnce(Control.by_name['fob'].device)
        Sensor.by_name['wx'].device.when_activated     = lambda: self.blinkTwice(Control.by_name['laser'].device)
        Sensor.by_name['bldg'].device.when_activated   = lambda: self.blinkTwice(Control.by_name['mntout'].device)
        Sensor.by_name['open'].device.when_activated   = lambda: self.blinkTwice(Control.by_name['fob'].device)

        Sensor.by_name['mntin'].device.when_deactivated  = util.printStatus
        Sensor.by_name['roofin'].device.when_deactivated = util.printStatus
        Sensor.by_name['park'].device.when_deactivated   = util.printStatus
        Sensor.by_name['close'].device.when_deactivated  = util.printStatus
        Sensor.by_name['wx'].device.when_deactivated     = util.printStatus
        Sensor.by_name['bldg'].device.when_deactivated   = util.printStatus
        Sensor.by_name['open'].device.when_deactivated   = util.printStatus

# This allows the class to be tested locally or be used as an 'include' target
def main():
    weatherOk = Sensor(pin=4, name='wx');
    bldgPowerIn = Sensor(pin=17, name='bldg');
    mountPowerIn = Sensor(pin=22, name='mntin');
    roofPowerIn = Sensor(pin=27, name='roofin');
    mountParked = Sensor(pin=25, name='park');
    roofOpen = Sensor(pin=23, name='open');
    roofClosed = Sensor(pin=24, name='close');

    heartLed = Control(pin=13, name='heart')
    mountPowerOut = Control(pin=6, name='mntout', active_high=False)
    roofPowerOut = Control(pin=5, name='roofout', active_high=False)
    laserPowerOut = Control(pin=16, name='laser')
    fobOutput = Control(pin=26, name='fob')

    foo = TestMode()
    util.printStatus();
    heartInterval = 1

    # Interrupt loop
    while True:
        signal.pause()
        signal.alarm(heartInterval)

# Execute only if run as a script
if __name__ == "__main__":
    print("TEST MODE: running as a stand alone script")
    main()
