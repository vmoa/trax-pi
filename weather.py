# Weather sensor utilities
#
# Specific to the Boltwood Cloud Sensor III

import logging
import re
import threading
import time

# pip3 install alpyca
from alpaca.safetymonitor import *


def log(arg):
    print(arg)

class Weather:
    Type = 'Boltwood CSIII'
    device = '192.168.74.74:80' # host:port, override in __init__()
    unit = 0                    # which sensor on device (always 0)
    safetymonitor = None        # Alpaca SafetyMonitor() object
    IsSafe = None               # Cached SafetyMonitor.IsSafe result

    def __init__(self, device=None, unit=None):
        if device:
            self.device = device
        if unit:
            self.unit = unit
        self.safetymonitor = SafetyMonitor(self.device, self.unit)
        log(f'Connecting to weather sensor at {self.device}')
        if self.connect():
            log(f'Connected to {self.safetymonitor.Name}')
        else:
            log(f'Connect to {self.Device.name} failed')

        # Register callback? Or do that in perMinute()?

    def connect(self):
        '''Connect to the weather sensor.'''
        self.safetymonitor.Connected = True
        return self.connected()

    def connected(self):
        '''Return connected status.'''
        return self.safetymonitor.Connected

    def disconnect(self):
        '''Disconnect.'''
        if verbose:
            log(f'Disconnecting {self.Device.name}')
        self.safetymonitor.Connected = False

    def issafe(self, check=False):
        '''Return cached weather status. If check=True, queries device. Could block on result.'''
        if check:
            if not self.connected():
                self.connect()
            self.IsSafe = self.safetymonitor.IsSafe
        return(self.IsSafe)


if (__name__ == "__main__"):
    '''Stand-alone weather test.'''
    wx = Weather()
    if wx.issafe(check=True):
        print(f'{wx.safetymonitor.Name} reports sky is safe')
    else:
        print(f'{wx.safetymonitor.Name} reports sky is NOT SAFE')
