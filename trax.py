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


def initialize():
    # Parse command line args
    default_logfile = '/var/log/trax.log'
    parser = argparse.ArgumentParser(description='T-Rax roof controller.')
    parser.add_argument('--test-mode', dest='test_mode', action='store_true', help='enter test mode')
    parser.add_argument('--simulator', dest='simulator', action='store_true', help='adjust timings for T-Rax simulator')
    parser.add_argument('--debug', dest='debug', action='store_true', help='include DEBUG messages in logs')
    parser.add_argument('--log-file', '-L', dest='logfile', action='store', help='log filename (default {})'.format(default_logfile))
    args = parser.parse_args()

    # Set up logging
    # TODO consider using flask logging interface https://flask.palletsprojects.com/en/1.1.x/logging/
    loggingConfig = dict(
        format = "%(asctime)s [%(levelname)s] %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
        level = logging.DEBUG if (args.debug) else logging.INFO)
    if (sys.stdin.isatty() and not args.logfile):
        print("TTY detected; logging to stderr")
    else:
        loggingConfig['filename'] = args.logfile if args.logfile else default_logfile;
    logging.basicConfig(**loggingConfig)
    logging.info("Initializing T-Rax for the Raspberry Pi {}".format(version))
    if (args.simulator):
        logging.info("Adjusting timings for simulator")

    # Initialize devices
    gpio = device.Gpio(args.simulator)
    logging.info(device.printStatus())

    # Enter test mode if requested
    if (args.test_mode):
        # TODO: pass in gpio instead of using xxx.by_name
        test = test_mode.TestMode()
        exit  # Test mode should not return, but just in case


#
# Register URL callbacks
#

@app.route('/')
def top():
    return flask.render_template('trax.html')

@app.route('/connect', methods=['GET'])
def connect():
    """Browser connected to T-Rax; dispatch welcome message and connect brower to SSE stream"""
    logging.info("Browser connected from {}".format(flask.request.remote_addr))
    threading.Timer(0.5, browser.browser.initialConnect).start()  # Dispatch our welcome connect function
    return flask.Response(sse.sse.stream(), mimetype='text/event-stream')

@app.route('/startstop', methods=['GET'])
def startStop():
    """User pressed the Start/Stop button"""
    return browser.browser.startStop(app)

@app.route('/roofpwr', methods=['GET'])
def roofPwrOnOff():
    return browser.browser.roofPower(app)

@app.route('/mountpwr', methods=['GET'])
def mountPwrOnOff():
    return browser.browser.mountPower(app)

@app.route('/checkmnt', methods=['GET'])
def checkMount():
    return browser.browser.checkMount(app)

@app.route('/STOP', methods=['GET'])
def emergencyStop():
    return browser.browser.emergencyStop(app)

@app.route('/override', methods=['GET'])
def doOverride():
    return browser.browser.doOverride(app)


if __name__ == '__main__':
    initialize()
    device.perSecond()
    app.run('0.0.0.0', 5000)
