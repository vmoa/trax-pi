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

import device
import util

class TestMode:

    def blinkOnce(self, output=0):
        device.printStatus()
        output.on()
        sleep(0.25)
        output.off()

    def blinkTwice(self, output=0):
        if (output != device.Control.by_name['heart'].device):
            device.printStatus()
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
        device.Sensor.by_name['mntin'].device.when_activated  = lambda: self.blinkOnce(device.Control.by_name['mntout'].device)
        device.Sensor.by_name['roofin'].device.when_activated = lambda: self.blinkOnce(device.Control.by_name['roofout'].device)
        device.Sensor.by_name['park'].device.when_activated   = lambda: self.blinkOnce(device.Control.by_name['laser'].device)
        device.Sensor.by_name['close'].device.when_activated  = lambda: self.blinkOnce(device.Control.by_name['fob'].device)
        device.Sensor.by_name['wx'].device.when_activated     = lambda: self.blinkTwice(device.Control.by_name['laser'].device)
        device.Sensor.by_name['bldg'].device.when_activated   = lambda: self.blinkTwice(device.Control.by_name['mntout'].device)
        device.Sensor.by_name['open'].device.when_activated   = lambda: self.blinkTwice(device.Control.by_name['fob'].device)

# This allows the class to be tested locally or be used as an 'include' target
def main():
    weatherOk = device.Sensor(pin=4, name='wx');
    bldgPowerIn = device.Sensor(pin=17, name='bldg');
    mountPowerIn = device.Sensor(pin=22, name='mntin');
    roofPowerIn = device.Sensor(pin=27, name='roofin');
    mountParked = device.Sensor(pin=25, name='park');
    roofOpen = device.Sensor(pin=23, name='open');
    roofClosed = device.Sensor(pin=24, name='close');

    heartLed = device.Control(pin=13, name='heart')
    mountPowerOut = device.Control(pin=6, name='mntout', active_high=False)
    roofPowerOut = device.Control(pin=5, name='roofout', active_high=False)
    laserPowerOut = device.Control(pin=16, name='laser')
    fobOutput = device.Control(pin=26, name='fob')

    foo = TestMode()
    device.printStatus();
    heartInterval = 1

    # Interrupt loop
    while True:
        signal.pause()
        signal.alarm(heartInterval)

# Execute only if run as a script
if __name__ == "__main__":
    print("TEST MODE: running as a stand alone script")
    main()
