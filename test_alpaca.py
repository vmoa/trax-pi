#!/usr/bin/python3
"""Quick functional test for the minimal Alpaca interface using Flask test client."""

from types import SimpleNamespace
from flask import Flask
import json

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
    dummyGpio = SimpleNamespace(open=DummySensor(False), close=DummySensor(True))
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


if __name__ == '__main__':
    run_tests()
