#!/usr/bin/python3
#
# T-Rax roof controller for the Raspberry Pi
#
# This is a roll-off roof controller specifically designed and built for
# Robert Ferguson Observatory (https://rfo.org) but the code will hopefully
# be generic enough that it can be adapted for other roll-off roofs.
# See README.md for details.

import argparse
import datetime
from gpiozero import DigitalInputDevice, DigitalOutputDevice
import logging
import os
import signal
import sys
import threading

import device
import test_mode
import util
import web

import flask

version = 'v0.9'        # T-Rax version
heartInterval = 1       # Seconds between heartbeats (drives SIGALRM)
statusInterval = 60     # Seconds between status updates without input changes

# Hard coded GPIO setup -- should these be in a dict?
class TraxGpio:
    def __init__(self):
        self.weatherOk = device.Sensor(pin=4, name='wx');
        self.bldgPowerIn = device.Sensor(pin=17, name='bldg');
        self.mountPowerIn = device.Sensor(pin=22, name='mntin');
        self.roofPowerIn = device.Sensor(pin=27, name='roofin');
        self.mountParked = device.Sensor(pin=25, name='park');
        self.roofOpen = device.Sensor(pin=23, name='open');
        self.roofClosed = device.Sensor(pin=24, name='close');

        self.heartLed = device.Control(pin=13, name='heart')
        self.mountPowerOut = device.Control(pin=6, name='mntout', active_high=False)
        self.roofPowerOut = device.Control(pin=5, name='roofout', active_high=False)
        self.laserPowerOut = device.Control(pin=16, name='laser')
        self.fobOutput = device.Control(pin=26, name='fob')

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
    web.browser.send(id='notice', type='innerHTML', data=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    if (int(datetime.datetime.now().second) % 2 == 0):
        beatHeart(gpio.heartLed.device)
    if (int(datetime.datetime.now().second) % statusInterval == 0):
        logging.info(device.printStatus())
    threading.Timer(1.0, perSecond).start()  # Redispatch self


#def main():

default_logfile = '/var/log/trax.log'

#parser = argparse.ArgumentParser(description='T-Rax roof controller.')
#parser.add_argument('--test-mode', dest='test_mode', action='store_true', help='enter test mode')
#parser.add_argument('--log-file', '-L', dest='logfile', action='store', help='log filename (default {})'.format(default_logfile))
#args = parser.parse_args()

loggingConfig = dict(format = "%(asctime)s [%(levelname)s] %(message)s", datefmt = "%Y-%m-%d %H:%M:%S", level = logging.INFO)
#if (sys.stdin.isatty() and not args.logfile):
if (sys.stdin.isatty()):
    print("TTY detected; logging to stdout")
else:
    loggingConfig['filename'] = default_logfile;
logging.basicConfig(**loggingConfig)
logging.info("Initializing T-Rax for the Raspberry Pi {}".format(version))

global gpio
gpio = TraxGpio()

logging.info(device.printStatus())

#if (args.test_mode):
#    test = test_mode.TestMode()

# Loop forever
#while True:
#    signal.pause()

#
# Register URL callbacks
#

# Instantiate the message queue

color = { 'black':'black', 'yellow':'yellow', 'green':'#00FF00', 'red':'#FF0800' }

def colorUp():
    """Decorate the indicators on the web browser"""
    print("colorUp")
    web.browser.send(id='notice', type='innerHTML', data='Connected!')

    if (gpio.roofClosed.isOn()):
        web.browser.send(type='indicator', id='roof_position', status='closed')
    elif (gpio.roofOpen.isOn()):
        web.browser.send(type='indicator', id='roof_position', status='open')
    else:
        web.browser.send(type='indicator', id='roof_position', status='midway')

    if (gpio.mountParked.isOn()):
        web.browser.send(type='indicator', id='mount_position', status='parked')
    else:
        web.browser.send(type='indicator', id='mount_position', status='notparked')

    if (gpio.bldgPowerIn.isOn()):
        web.browser.send(type='indicator', id='building_pwr', status='on')
    else:
        web.browser.send(type='indicator', id='building_pwr', status='off')

    if (gpio.roofPowerIn.isOn()):
        web.browser.send(type='indicator', id='roof_pwr', status='on')
    else:
        web.browser.send(type='indicator', id='roof_pwr', status='off')

    if (gpio.mountPowerIn.isOn()):
        web.browser.send(type='indicator', id='mount_pwr', status='on')
    else:
        web.browser.send(type='indicator', id='mount_pwr', status='off')

web.browser.setWelcome(colorUp)

app = flask.Flask(__name__)

@app.route('/')
def top():
    return flask.render_template('trax.html')

@app.route('/connect', methods=['GET'])
def connect():
    """
    This function starts in a different thread (I think) for each browser that connects,
    listens on the `browser` queue and sends any messages that are posted to it.
    """
    return flask.Response(web.browser.stream(), mimetype='text/event-stream')

# Start the self perpetuating per second timer
perSecond()


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
