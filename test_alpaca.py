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
    inst = alpaca.Alpaca(app, device_number=0, base_path='/api/v1')
    return app, inst


def run_tests():
    app, _ = _make_app()
    client = app.test_client()

    endpoints = [
        '/api/v1/dome/0/connected',
        '/api/v1/dome/0/name',
        '/api/v1/dome/0/description',
        '/api/v1/dome/0/driverinfo',
        '/api/v1/dome/0/driverversion',
        '/api/v1/dome/0/interfaceversion',
        '/api/v1/dome/0/supportedactions',
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
    app, inst = _make_app()
    client = app.test_client()

    # CanSetShutter must be True or a client will not offer shutter control.
    assert client.get('/api/v1/dome/0/cansetshutter').get_json()['Value'] is True

    # ASCOM common properties queried on connect must not 404.
    assert client.get('/api/v1/dome/0/interfaceversion').get_json()['Value'] == 2
    assert client.get('/api/v1/dome/0/supportedactions').get_json()['Value'] == []

    # Advertising InterfaceVersion 2 requires the full IDomeV2 surface to
    # exist. Capability/state flags respond (false) rather than 404...
    for cap in ('cansetaltitude', 'cansetazimuth', 'cansetpark', 'canslave',
                'athome', 'atpark', 'slewing', 'slaved'):
        body = client.get('/api/v1/dome/0/' + cap).get_json()
        assert body['ErrorNumber'] == 0 and body['Value'] is False, (cap, body)
    # ...and the unsupported rotation/park members return a proper ASCOM
    # "not implemented" error (0x400) instead of a bare Flask 404.
    for name in ('altitude', 'azimuth'):
        body = client.get('/api/v1/dome/0/' + name).get_json()
        assert body['ErrorNumber'] == alpaca.NOT_IMPLEMENTED and 'Value' not in body, (name, body)
    for name in ('findhome', 'park', 'setpark', 'slewtoaltitude', 'slewtoazimuth', 'synctoazimuth'):
        body = client.put('/api/v1/dome/0/' + name).get_json()
        assert body['ErrorNumber'] == alpaca.NOT_IMPLEMENTED, (name, body)
    # ASCOM common methods respond with the not-implemented envelope, not 404.
    for name in ('action', 'commandblind', 'commandbool', 'commandstring'):
        body = client.put('/api/v1/dome/0/' + name).get_json()
        assert body['ErrorNumber'] == alpaca.NOT_IMPLEMENTED, (name, body)

    # Slaved rejects a slave-enable but accepts the no-op disable.
    assert client.put('/api/v1/dome/0/slaved', data={'Slaved': 'true'}).get_json()['ErrorNumber'] == alpaca.NOT_IMPLEMENTED
    assert client.put('/api/v1/dome/0/slaved', data={'Slaved': 'false'}).get_json()['ErrorNumber'] == 0

    # Roof is CLOSED in the fixture -> ASCOM ShutterState 1 (shutterClosed).
    status = client.get('/api/v1/dome/0/shutterstatus').get_json()
    assert status['Value'] == alpaca.SHUTTER_CLOSED == 1, status

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

    # While the move is reserved, status reports Opening and Slewing is true
    # even though the origin (closed) end stop may still be asserted.
    assert client.get('/api/v1/dome/0/shutterstatus').get_json()['Value'] == alpaca.SHUTTER_OPENING
    assert client.get('/api/v1/dome/0/slewing').get_json()['Value'] is True

    # Reset the tracked move to exercise CloseShutter from the resting state.
    inst._shutter_status = None
    # CloseShutter is likewise a PUT method that succeeds.
    assert client.put('/api/v1/dome/0/closeshutter').get_json()['ErrorNumber'] == 0
    # AbortSlew cannot be honoured on a roll-off roof, so it must report an
    # explicit not-implemented error rather than a false success.
    abort = client.put('/api/v1/dome/0/abortslew').get_json()
    assert abort['ErrorNumber'] == alpaca.NOT_IMPLEMENTED and 'Value' not in abort, abort

    # Connected accepts a PUT to set the connection state.
    assert client.put('/api/v1/dome/0/connected', data={'Connected': 'true'}).status_code == 200

    print('ASCOM contract test passed')


def test_shutter_command_guards():
    """A move already in flight must not be stopped by a repeated/opposite command."""
    # Roof midway: neither end-stop sensor active.
    device.Gpio = SimpleNamespace(
        open=DummySensor(False),
        close=DummySensor(False),
        park=SimpleNamespace(checkParked=(lambda: device.park.PARKED)),
        mntout=SimpleNamespace(turnOff=(lambda: None), turnOn=(lambda: None)),
        roofout=SimpleNamespace(turnOn=(lambda: None), turnOff=(lambda: None)),
    )
    calls = {'n': 0}
    browser.browser.startStop = lambda app: calls.__setitem__('n', calls['n'] + 1) or 'OK'
    alpaca.Alpaca._start_multicast_responder = lambda self: None

    app = Flask(__name__)
    inst = alpaca.Alpaca(app, device_number=0, base_path='/api/v1')
    client = app.test_client()

    # An open is already in progress (tracked by this instance).
    inst._shutter_status = alpaca.SHUTTER_OPENING
    # Repeated OpenShutter is idempotent success and does NOT re-toggle the fob.
    assert client.put('/api/v1/dome/0/openshutter').get_json()['ErrorNumber'] == 0
    # Opposite CloseShutter is refused rather than stopping the roof mid-travel.
    assert client.put('/api/v1/dome/0/closeshutter').get_json()['ErrorNumber'] == 2

    # Untracked midway state: motion started outside this instance (e.g. via
    # trax.py's /startstop, after a restart, or after a watcher timeout) leaves
    # _shutter_status None/ERROR. A command must be refused, never toggled.
    for state in (None, alpaca.SHUTTER_ERROR):
        inst._shutter_status = state
        assert client.put('/api/v1/dome/0/openshutter').get_json()['ErrorNumber'] == 1, state
        assert client.put('/api/v1/dome/0/closeshutter').get_json()['ErrorNumber'] == 2, state

    assert calls['n'] == 0, 'startStop must not be invoked from a non-terminal roof position'

    print('Shutter command guard test passed')


def test_motion_generation():
    """Each accepted move opens a new generation so a stale watcher goes inert."""
    device.Gpio = SimpleNamespace(
        open=DummySensor(False), close=DummySensor(True),
        park=SimpleNamespace(checkParked=(lambda: device.park.PARKED)),
        mntout=SimpleNamespace(turnOff=(lambda: None), turnOn=(lambda: None)),
        roofout=SimpleNamespace(turnOn=(lambda: None), turnOff=(lambda: None)),
    )
    browser.browser.startStop = lambda app: 'OK'
    alpaca.Alpaca._start_multicast_responder = lambda self: None
    # Capture the generation each watcher would be tagged with (no threads).
    started = []
    alpaca.Alpaca._start_roof_state_watcher = lambda self, gen, *a: started.append(gen)

    app = Flask(__name__)
    inst = alpaca.Alpaca(app, device_number=0, base_path='/api/v1')
    client = app.test_client()

    # Open from the closed state: accepted, generation 1, status reserved as
    # Opening *before* the response returns.
    assert client.put('/api/v1/dome/0/openshutter').get_json()['ErrorNumber'] == 0
    assert inst._shutter_status == alpaca.SHUTTER_OPENING
    assert started == [1] and inst._motion_gen == 1

    # Simulate the open completing and the roof now reading open.
    device.Gpio.open._v = True
    device.Gpio.close._v = False
    inst._shutter_status = alpaca.SHUTTER_OPEN

    # Close from the open state opens a NEW generation, so the earlier watcher
    # (gen 1) is superseded and cannot later apply _on_open_complete.
    assert client.put('/api/v1/dome/0/closeshutter').get_json()['ErrorNumber'] == 0
    assert inst._shutter_status == alpaca.SHUTTER_CLOSING
    assert started == [1, 2] and inst._motion_gen == 2

    print('Motion generation test passed')


def test_reservation_rollback_and_pending():
    """A reserved move must roll back on failure and not ack duplicates while pending."""
    device.Gpio = SimpleNamespace(
        open=DummySensor(False), close=DummySensor(True),
        park=SimpleNamespace(checkParked=(lambda: device.park.PARKED)),
        mntout=SimpleNamespace(turnOff=(lambda: None), turnOn=(lambda: None)),
        roofout=SimpleNamespace(turnOn=(lambda: None), turnOff=(lambda: None)),
    )
    alpaca.Alpaca._start_multicast_responder = lambda self: None
    alpaca.Alpaca._start_roof_state_watcher = lambda self, gen, *a: None
    browser.browser.startStop = lambda app: 'OK'

    app = Flask(__name__)
    inst = alpaca.Alpaca(app, device_number=0, base_path='/api/v1')
    client = app.test_client()

    # A duplicate arriving while the first move is still pending (preflight not
    # confirmed) must NOT be acknowledged as a started move.
    inst._shutter_status = alpaca.SHUTTER_OPENING
    inst._move_pending = True
    assert client.put('/api/v1/dome/0/openshutter').get_json()['ErrorNumber'] == 1
    inst._shutter_status = None
    inst._move_pending = False

    # A failed startStop rolls the reservation back so status is not stuck Opening.
    browser.browser.startStop = lambda app: 'ERROR'
    body = client.put('/api/v1/dome/0/openshutter').get_json()
    assert body['ErrorNumber'] == 1, body
    assert inst._shutter_status is None and inst._move_pending is False

    # An exception during preflight also rolls back rather than leaking state.
    def boom():
        raise RuntimeError('gpio fault')
    device.Gpio.park = SimpleNamespace(checkParked=boom)
    body = client.put('/api/v1/dome/0/openshutter').get_json()
    assert body['ErrorNumber'] == 1, body
    assert inst._shutter_status is None and inst._move_pending is False

    print('Reservation rollback/pending test passed')


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
    test_shutter_command_guards()
    test_motion_generation()
    test_reservation_rollback_and_pending()
    test_discovery_response_format()
