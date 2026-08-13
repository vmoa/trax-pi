# Boltwood III weather sensor observing conditions
#
# Description
# Connects to Boltwood III weather sensor via IP and port
# Queries current weather data
# Prints weather data out and ends
#
# 2025-04-24 George Loyer

# pip3 install alpyca
from alpaca.observingconditions import *
import time
import logging

def log(arg):
    print(arg)

def wait_until(condition, timeout=None, interval=0.1, *args, **kwargs):
    start_time = time.time()
    while True:
        if condition(*args, **kwargs):
            return True
        if timeout and time.time() - start_time > timeout:
            return False  # or raise an exception
        time.sleep(interval)

class Weather:
    Type = 'Boltwood CSIII'
    device = '192.168.74.74:80' # host:port, override in __init__()
    unit = 0                    # which sensor on device (always 0)
    obscond = None              # Alpaca ObservingConditions object
    IsSafe = None               # Cached SafetyMonitor.IsSafe result

    def __init__(self, device=None, unit=None):
        if device:
            self.device = device
        if unit:
            self.unit = unit
        self.obscond = ObservingConditions(self.device, self.unit)
        log(f'Connecting to weather sensor at {self.device}')
        if self.connect():
            log(f'Connected to {self.obscond.Name}')
        else:
            log(f'Connect to {self.device} failed')

        # Register callback? Or do that in perMinute()?

    def connect(self):
        '''Connect to the weather sensor.'''
        self.obscond.Connected = True
        return self.connected()

    def connected(self):
        '''Return connected status.'''
        return self.obscond.Connected

    def disconnect(self):
        '''Disconnect.'''
        if verbose:
            log(f'Disconnecting {self.Device.name}')
        self.obscond.Connected = False

    def issafe(self, check=False):
        '''Return cached weather status. If check=True, queries device. Could block on result.'''
        if check:
            if not self.connected():
                self.connect()
            self.IsSafe = self.safetymonitor.IsSafe
        return(self.IsSafe)

    def weatherdata(self, check=False):
        '''Return cached weather data. If check=True, queries device, Could block on result.'''
        if check:
            if not self.connected():
                self.connect()
            self.humidity = self.obscond.Humidity
            self.pressure = self.obscond.Pressure
            self.temperature = self.obscond.Temperature
            self.dewpoint = self.obscond.DewPoint
        return(self.humidity, self.pressure, self.temperature, self.dewpoint)


def get_boltwood_conditions(host):
    """
    Connects to a Boltwood Cloud Sensor III via ASCOM Alpaca and retrieves
    observing conditions.

    Args:
        host (str): The IP address and port of the Boltwood Cloud Sensor III.
    """
    try:
        # Create an Alpaca client for ObservingConditions
        observing_conditions = ObservingConditions(host, 0, "http")
        observing_conditions.Connect()
        while observing_conditions.Connecting:
            time.sleep(0.5)
        print(f'Connected to {observing_conditions.Name}')
        print(observing_conditions.Description)

        # Retrieve sensor data (example properties, adjust based on your sensor)
        cloud_cover = observing_conditions.CloudCover()
        temperature = observing_conditions.Temperature()
        dew_point = observing_conditions.DewPoint()
        wind_speed = observing_conditions.WindSpeed()
        # Add more properties based on available sensor data

        # Print the retrieved values
        print(f"Cloud Cover: {cloud_cover}")
        print(f"Temperature: {temperature} degrees C")
        print(f"Dew Point: {dew_point} degrees C")
        print(f"Wind Speed: {wind_speed} m/s")
        # Print other properties as needed

    except Exception as e:  # Catch general exceptions
        print(f"Error communicating with the sensor: {e}")

    finally:
        # Disconnect the device
        if observing_conditions.Connected:
            observing_conditions.Disconnect()
        while not observing_conditions.Connected:
            time.sleep(0.5)
        print(f'Disconnected from Boltwood III')

if __name__ == "__main__":
    # Replace with your sensor's IP address or hostname and port
    # host = "192.168.74.74:80"

    # get_boltwood_conditions(host)

    wx = Weather()
    (humidity, pressure, temperature, dewpoint) = wx.weatherdata(True)
    print(f'Weather data: ')
    print(f'Humidity:       {humidity}')
    print(f'Pressure:       {pressure}')
    print(f'Temperature:    {temperature}')
    print(f'Dewpoint:       {dewpoint}')
