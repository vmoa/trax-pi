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

import browser
import device
import test_mode
import util
import sse

import flask
app = flask.Flask(__name__)

version = 'v0.9'        # T-Rax version
statusInterval = 60     # Seconds between status updates without input changes

# Hard coded GPIO setup
class TraxGpio:
    def __init__(self):
        self.wx = device.Sensor(pin=0, name='wx')           # weatherOk 
        self.bldg = device.Sensor(pin=17, name='bldg')      # bldgPowerIn 
        self.mntin = device.Sensor(pin=22, name='mntin')    # mountPowerIn 
        self.roofin = device.Sensor(pin=27, name='roofin')  # roofPowerIn 
        self.park = device.Sensor(pin=25, name='park')      # mountParked 
        self.open = device.Sensor(pin=23, name='open')      # roofOpen 
        self.close = device.Sensor(pin=24, name='close')    # roofClosed 

        self.heart = device.Control(pin=13, name='heart')                       # heartLed 
        self.mntout = device.Control(pin=6, name='mntout', active_high=False)   # mountPowerOut
        self.roofout = device.Control(pin=5, name='roofout', active_high=False) # roofPowerOut 
        self.laser = device.Control(pin=16, name='laser')                       # laserPowerOut 
        self.fob = device.Control(pin=26, name='fob')                           # fobOutput 


def initialize():
    default_logfile = '/var/log/trax.log'
    parser = argparse.ArgumentParser(description='T-Rax roof controller.')
    parser.add_argument('--test-mode', dest='test_mode', action='store_true', help='enter test mode')
    parser.add_argument('--log-file', '-L', dest='logfile', action='store', help='log filename (default {})'.format(default_logfile))
    args = parser.parse_args()

    loggingConfig = dict(
        format = "%(asctime)s [%(levelname)s] %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
        level = logging.INFO)
    if (sys.stdin.isatty() and not args.logfile):
        print("TTY detected; logging to stderr")
    else:
        loggingConfig['filename'] = args.logfile if args.logfile else default_logfile;
    logging.basicConfig(**loggingConfig)
    logging.info("Initializing T-Rax for the Raspberry Pi {}".format(version))
    # TODO consider using flask logging interface https://flask.palletsprojects.com/en/1.1.x/logging/

    global gpio
    gpio = TraxGpio()

    logging.info(device.printStatus())

    if (args.test_mode):
        # TODO: pass in gpio instead of using xxx.by_name
        test = test_mode.TestMode()


#
# Register URL callbacks
#

@app.route('/')
def top():
    return flask.render_template('trax.html')

@app.route('/connect', methods=['GET'])
def connect():
    """
    This function starts in a different thread (I think) for each browser that connects,
    listens on the `browser` queue in sse.py and sends any messages that are posted to it.
    """
    logging.info("Browser connected from {}".format(flask.request.remote_addr))
    threading.Timer(0.5, browser.browser.initialConnect).start()  # Dispatch our welcome connect function
    return flask.Response(sse.sse.stream(), mimetype='text/event-stream')

@app.route('/startstop', methods=['GET'])
def startStop():
    """User pressed the Start/Stop button"""
    return browser.browser.startStop(app)

@app.route('/roofpwr', methods=['GET'])
def roofPwrOff():
    return browser.browser.roofPower(app)
    return('OK')

@app.route('/mountpwr', methods=['GET'])
def mountPwrOn():
    return browser.browser.mountPower(app)
    return('OK')

@app.route('/STOP', methods=['GET'])
def emergencyStop():
    return browser.browser.emergencyStop(app)
    return('OK')


if __name__ == '__main__':
    initialize()
    device.perSecond()
    app.run('0.0.0.0', 5000)
