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


def _make_app():
    # Monkeypatch device.Gpio to avoid hardware dependency: roof reported CLOSED.
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

    # Do not bind a real UDP socket during tests
    alpaca.Alpaca._start_multicast_responder = lambda self: None

    app = Flask(__name__)
    alpaca.Alpaca(app, device_number=0, base_path='/api/v1')
    return app


def run_tests():
    app = _make_app()
    client = app.test_client()

    endpoints = [
        '/api/v1/dome/0/connected',
        '/api/v1/dome/0/name',
        '/api/v1/dome/0/description',
        '/api/v1/dome/0/driverinfo',
        '/api/v1/dome/0/driverversion',
        '/api/v1/discovery',
        '/api/v1/apiversion',
        '/management/apiversions',
        '/management/v1/description',
        '/management/v1/configureddevices',
        '/api/v1/dome/0/cansetshutter',
        '/api/v1/dome/0/cansyncazimuth',
        '/api/v1/dome/0/canrotate',
        '/api/v1/dome/0/canpark',
        '/api/v1/dome/0/canfindhome',
        '/api/v1/dome/0/shutterstatus',
    ]

    for e in endpoints:
        r = client.get(e)
        try:
            body = r.get_json()
        except Exception:
            body = r.data.decode('utf-8')
        print(e, '->', r.status_code, body)


def test_ascom_contract():
    """Assert the ASCOM-specific interface contract a client (e.g. NINA) relies on."""
    app = _make_app()
    client = app.test_client()

    # CanSetShutter must be True or a client will not offer shutter control.
    assert client.get('/api/v1/dome/0/cansetshutter').get_json()['Value'] is True

    # Roof is CLOSED in the fixture -> ASCOM ShutterState 1 (shutterClosed).
    status = client.get('/api/v1/dome/0/shutterstatus').get_json()
    assert status['Value'] == alpaca.SHUTTER_CLOSED == 1, status
    # Legacy alias resolves to the same handler/value.
    assert client.get('/api/v1/dome/0/shutterstate').get_json()['Value'] == 1

    # Management API returns the standard shapes.
    assert client.get('/management/apiversions').get_json()['Value'] == [1]
    devs = client.get('/management/v1/configureddevices').get_json()['Value']
    assert devs and devs[0]['DeviceType'] == 'Dome', devs

    # OpenShutter is an ASCOM method: invoked with PUT, parameters in the form
    # body, and the response carries no Value (only the transaction envelope).
    r = client.put('/api/v1/dome/0/openshutter', data={'ClientTransactionID': '42'})
    body = r.get_json()
    assert r.status_code == 200, r.status_code
    assert 'Value' not in body, body
    assert body['ErrorNumber'] == 0, body
    assert body['ClientTransactionID'] == 42, body

    # CloseShutter and AbortSlew are likewise PUT methods that succeed.
    assert client.put('/api/v1/dome/0/closeshutter').get_json()['ErrorNumber'] == 0
    assert client.put('/api/v1/dome/0/abortslew').get_json()['ErrorNumber'] == 0

    # Connected accepts a PUT to set the connection state.
    assert client.put('/api/v1/dome/0/connected', data={'Connected': 'true'}).status_code == 200

    print('ASCOM contract test passed')


def test_discovery_response_format():
    """The UDP discovery reply is JSON naming the Alpaca HTTP port."""
    original_start = alpaca.Alpaca._start_multicast_responder
    alpaca.Alpaca._start_multicast_responder = lambda self: None
    try:
        app = Flask(__name__)
        instance = alpaca.Alpaca(app, device_number=0, base_path='/api/v1')
        response = instance._format_discovery_response(('127.0.0.1', 65000))
        assert isinstance(response, bytes)
        payload = json.loads(response.decode('utf-8'))
        assert payload == {'AlpacaPort': alpaca.ALPACA_HTTP_PORT}, payload
    finally:
        alpaca.Alpaca._start_multicast_responder = original_start
    print('Discovery response format test passed')


if __name__ == '__main__':
    run_tests()
    test_ascom_contract()
    test_discovery_response_format()
