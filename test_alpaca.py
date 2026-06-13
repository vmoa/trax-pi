#!/usr/bin/python3
"""Quick functional test for the minimal Alpaca interface using Flask test client."""

from types import SimpleNamespace
from flask import Flask
import json

import util

# Provide a minimal gpiozero stub for non-Pi test environments
import sys
import types
if 'gpiozero' not in sys.modules:
    gpio_stub = types.SimpleNamespace()
    def _make_input(*a, **k):
        obj = types.SimpleNamespace(value=0)
        obj.on = lambda : setattr(obj, 'value', 1)
        obj.off = lambda : setattr(obj, 'value', 0)
        obj.is_active = False
        return obj
    def _make_output(*a, **k):
        obj = types.SimpleNamespace(value=0)
        obj.on = lambda : setattr(obj, 'value', 1)
        obj.off = lambda : setattr(obj, 'value', 0)
        return obj
    gpio_stub.DigitalInputDevice = _make_input
    gpio_stub.DigitalOutputDevice = _make_output
    sys.modules['gpiozero'] = gpio_stub

import alpaca
import device
import browser


class DummySensor:
    def __init__(self, val=False):
        self._v = val

    def isOn(self):
        return self._v

    def isOff(self):
        return not self._v


def run_tests():
    # Monkeypatch device.Gpio to avoid hardware dependency
    dummyGpio = SimpleNamespace(
        open=DummySensor(False),
        close=DummySensor(True),
        park=SimpleNamespace(checkParked=(lambda: device.park.PARKED), isOn=(lambda : True)),
        mntout=SimpleNamespace(turnOff=(lambda : None), turnOn=(lambda : None)),
        roofout=SimpleNamespace(turnOn=(lambda : None), turnOff=(lambda : None)),
    )
    device.Gpio = dummyGpio

    # Monkeypatch browser startStop to simulate successful toggles
    browser.browser.startStop = lambda app: 'OK'

    app = Flask(__name__)
    alpaca.Alpaca(app, device_number=0, base_path='/api/v1')
    client = app.test_client()

    endpoints = [
        '/api/v1/dome/0/connected',
        '/api/v1/dome/0/name',
        '/api/v1/dome/0/description',
        '/api/v1/discovery',
        '/api/v1/apiversion',
        '/api/v1/dome/0/canrotate',
        '/api/v1/dome/0/canpark',
        '/api/v1/dome/0/canfindhome',
        '/api/v1/dome/0/shutterstate',
        '/api/v1/dome/0/openshutter',
        '/api/v1/dome/0/closeshutter',
    ]

    for e in endpoints:
        r = client.get(e)
        try:
            body = r.get_json()
        except Exception:
            body = r.data.decode('utf-8')
        print(e, '->', r.status_code, body)


def test_multicast_response_format():
    # Prevent the actual responder thread from binding in test mode
    original_start = alpaca.Alpaca._start_multicast_responder
    original_get_ip = util.get_ip
    alpaca.Alpaca._start_multicast_responder = lambda self: None
    util.get_ip = lambda: '127.0.0.1'
    try:
        app = Flask(__name__)
        client_app = alpaca.Alpaca(app, device_number=0, base_path='/api/v1')
        response = client_app._format_discovery_response(('127.0.0.1', 65000))
        assert isinstance(response, bytes)
        text = response.decode('utf-8')
        assert 'HTTP/1.1 200 OK' in text
        assert 'LOCATION: http://127.0.0.1:5000/api/v1/discovery' in text
        assert 'ST: urn:schemas-upnp-org:device:Alpaca:1' in text
        assert 'USN: uuid:trax:dome:0' in text
    finally:
        alpaca.Alpaca._start_multicast_responder = original_start
        util.get_ip = original_get_ip
    print('Multicast response format test passed')


if __name__ == '__main__':
    run_tests()
    test_multicast_response_format()
