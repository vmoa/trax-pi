#!/usr/bin/python3
"""
Simple ASCOM Alpaca-compatible dome controller interface for T-Rax.

This implements a minimal subset of the Alpaca JSON HTTP API sufficient
to control the roll-off roof as a dome shutter: core info endpoints,
shutter Open/Close, and the ``Can...`` capability endpoints (we return
false for rotation-related capabilities since the roof does not rotate).

The class registers Flask routes on construction. It uses the existing
`browser` and `device` modules to perform actions and to check safety
conditions used elsewhere in the project.
"""

import json
import logging
import socket
import struct
import threading
import time

import flask

import browser
import device
import util

ROOF_STATE_TIMEOUT = 30
ROOF_STATE_POLL_INTERVAL = 0.5
DISCOVERY_MULTICAST_GROUP = '239.255.255.250'
DISCOVERY_MULTICAST_PORT = 32227
DISCOVERY_RESPONSE_ST = 'urn:schemas-upnp-org:device:Alpaca:1'


class Alpaca:
    """Register a minimal Alpaca dome controller on a Flask app.

    Example:
        Alpaca(app, device_number=0)
    """

    server_txid = 0

    def __init__(self, app, device_number=0, base_path='/api/v1'):
        self.app = app
        self.device_number = int(device_number)
        self.base = base_path.rstrip('/')
        # Register routes
        prefix = self._prefix()

        # Core device metadata
        app.add_url_rule(prefix + '/connected', endpoint=prefix + '_connected', view_func=self._connected, methods=['GET'])
        app.add_url_rule(prefix + '/name', endpoint=prefix + '_name', view_func=self._name, methods=['GET'])
        app.add_url_rule(prefix + '/description', endpoint=prefix + '_description', view_func=self._description, methods=['GET'])

        # Capability flags (we do not support rotation)
        app.add_url_rule(prefix + '/canrotate', endpoint=prefix + '_canrotate', view_func=self._canrotate, methods=['GET'])
        app.add_url_rule(prefix + '/canpark', endpoint=prefix + '_canpark', view_func=self._canpark, methods=['GET'])
        app.add_url_rule(prefix + '/canfindhome', endpoint=prefix + '_canfindhome', view_func=self._canfindhome, methods=['GET'])

        # Basic discovery / service info (rooted at the base path)
        app.add_url_rule(self.base + '/discovery', endpoint=prefix + '_discovery', view_func=self._discovery, methods=['GET'])
        app.add_url_rule(self.base + '/apiversion', endpoint=prefix + '_apiversion', view_func=self._apiversion, methods=['GET'])
        app.add_url_rule(self.base + '/configureddevices', endpoint=prefix + '_configureddevices', view_func=self._configureddevices, methods=['GET'])
        self._start_multicast_responder()

        # Shutter control
        app.add_url_rule(prefix + '/openshutter', endpoint=prefix + '_openshutter', view_func=self._openshutter, methods=['GET','POST'])
        app.add_url_rule(prefix + '/closeshutter', endpoint=prefix + '_closeshutter', view_func=self._closeshutter, methods=['GET','POST'])
        app.add_url_rule(prefix + '/shutterstate', endpoint=prefix + '_shutterstate', view_func=self._shutterstate, methods=['GET'])

    def _prefix(self):
        # e.g. /api/v1/dome/0
        return '{}/dome/{}'.format(self.base, self.device_number)

    def _next_txid(self):
        Alpaca.server_txid += 1
        return Alpaca.server_txid

    def _resp(self, value=None, error_number=0, error_message=''):
        resp = {
            'Value': value,
            'ClientTransactionID': int(flask.request.args.get('ClientTransactionID', 0)),
            'ServerTransactionID': self._next_txid(),
            'ErrorNumber': int(error_number),
            'ErrorMessage': error_message,
        }
        return flask.jsonify(resp)

    # Core info endpoints
    def _connected(self):
        return self._resp(True)

    def _name(self):
        return self._resp('T-Rax Roof Dome')

    def _description(self):
        return self._resp('T-Rax roll-off roof presented as an Alpaca dome (shutter only)')

    # Capability endpoints
    def _canrotate(self):
        return self._resp(False)

    def _canpark(self):
        # No dedicated park functionality for the roof
        return self._resp(False)

    def _canfindhome(self):
        return self._resp(False)

    def _discovery_data(self):
        ip_address = util.get_ip()
        return {
            'DeviceType': 'dome',
            'DeviceNumber': self.device_number,
            'DeviceName': 'T-Rax Roof Dome',
            'Connected': True,
            'BaseURL': self._prefix(),
            'APIVersion': 1,
            'ServerName': 'T-Rax',
            'Vendor': 'Robert Ferguson Observatory',
            'Manufacturer': 'Robert Ferguson Observatory',
            'IPAddress': ip_address,
            'HTTPPort': 5000,
            'SupportedApiVersions': [1],
            'Description': 'ASCOM Alpaca dome shutter interface',
        }

    def _discovery(self):
        return self._resp([self._discovery_data()])

    def _apiversion_data(self):
        return {
            'AlpacaVersion': 1,
            'CurrentApiVersion': 1,
            'SupportedApiVersions': [1],
            'ServerName': 'T-Rax',
            'Vendor': 'Robert Ferguson Observatory',
            'ServerBaseURL': self.base,
        }

    def _apiversion(self):
        return self._resp(self._apiversion_data())

    def _configureddevices(self):
        # Return list of configured devices on this server
        devices = [
            {
                'DeviceType': 'dome',
                'DeviceNumber': self.device_number,
                'DeviceName': 'T-Rax Roof Dome',
                'UniqueID': 'uuid:trax:dome:{}'.format(self.device_number),
            }
        ]
        return self._resp(devices)

    def _format_discovery_response(self, client_addr):
        # Return a JSON-encoded discovery payload per the Alpaca discovery specification.
        # Use the same structure as the HTTP discovery endpoint, but encoded as JSON
        # so UDP responders expecting Alpaca JSON will receive the expected format.
        try:
            # Per request, only advertise the Alpaca HTTP port in the UDP response
            payload = {'AlpacaPort': 5000}
            return json.dumps(payload).encode('utf-8')
        except Exception as e:
            logging.error('Failed to format JSON discovery response: %s', e)
            return b''

    def _multicast_responder(self):
        # Listen for UDP broadcast discovery probes on the discovery port.
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            if hasattr(socket, 'SO_REUSEPORT'):
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except Exception:
            pass
        # Allow receiving broadcasts
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        except Exception:
            pass
        try:
            sock.bind(('', DISCOVERY_MULTICAST_PORT))
        except OSError as e:
            logging.error('Alpaca broadcast bind failed: %s', e)
            return

        logging.info('Alpaca broadcast responder listening on port %s', DISCOVERY_MULTICAST_PORT)
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                if not data:
                    continue
                text = data.decode('utf-8', errors='ignore')
                # Respond to common discovery probes. Accept multicast-style M-SEARCH
                # as well as simple broadcast discovery strings.
                if 'M-SEARCH' in text or 'ALPACA_DISCOVERY' in text.upper() or 'DISCOVERY' in text.upper():
                    logging.info('Received discovery request from %s', addr)
                    response = self._format_discovery_response(addr)
                    sock.sendto(response, addr)
            except Exception as e:
                logging.error('Alpaca multicast responder error: %s', e)

    def _start_multicast_responder(self):
        thread = threading.Thread(target=self._multicast_responder, daemon=True)
        thread.start()

    # Shutter state mapping
    def _get_shutter_state(self):
        # Map existing roof indicators to simple shutter states:
        # 0 = ShutterUnknown, 1 = ShutterClosed, 2 = ShutterOpen, 3 = ShutterMoving
        try:
            if device.Gpio.close.isOn() and device.Gpio.open.isOn():
                return 0
            elif device.Gpio.close.isOn():
                return 1
            elif device.Gpio.open.isOn():
                return 2
            else:
                return 3
        except Exception:
            return 0

    def _start_roof_state_watcher(self, target_sensor, success_fn, action_name):
        def watcher():
            deadline = time.time() + ROOF_STATE_TIMEOUT
            while time.time() < deadline:
                if target_sensor.isOn():
                    success_fn()
                    return
                time.sleep(ROOF_STATE_POLL_INTERVAL)
            browser.browser.sendNotice(
                "Timeout waiting for roof {} after {} seconds".format(action_name, ROOF_STATE_TIMEOUT),
                log='ERROR'
            )

        thread = threading.Thread(target=watcher, daemon=True)
        thread.start()

    def _on_open_complete(self):
        browser.browser.sendNotice("Roof open; turning off roof power and enabling mount power", log='INFO')
        device.Gpio.roofout.turnOff()
        device.Gpio.mntout.turnOn()

    def _on_close_complete(self):
        browser.browser.sendNotice("Roof closed; turning off roof power", log='INFO')
        device.Gpio.roofout.turnOff()

    def _shutterstate(self):
        return self._resp(self._get_shutter_state())

    def _openshutter(self):
        logging.info("Alpaca: OpenShutter requested from %s", flask.request.remote_addr)
        # If already open, succeed
        if device.Gpio.open.isOn():
            return self._resp(True)

        # Require the telescope to be parked before cutting mount power.
        if (device.Gpio.park.checkParked() != device.park.PARKED):
            return self._resp(False, 1, 'Cannot open shutter: mount must be parked first')

        # Ensure mount power is off and roof power is on before opening.
        device.Gpio.mntout.turnOff()
        device.Gpio.roofout.turnOn()

        # Use the same safety checks as the browser/startStop path by
        # delegating to browser.startStop which toggles roof appropriately
        result = browser.browser.startStop(self.app)
        ok = (result == 'OK')
        if ok:
            self._start_roof_state_watcher(device.Gpio.open, self._on_open_complete, 'open')
        return self._resp(ok, 0 if ok else 1, '' if ok else 'Failed to open shutter')

    def _closeshutter(self):
        logging.info("Alpaca: CloseShutter requested from %s", flask.request.remote_addr)
        # If already closed, succeed
        if device.Gpio.close.isOn():
            return self._resp(True)

        # Require the telescope to be parked before cutting mount power.
        if (device.Gpio.park.checkParked() != device.park.PARKED):
            return self._resp(False, 2, 'Cannot close shutter: mount must be parked first')

        # Ensure mount power is off and roof power is on before closing.
        device.Gpio.mntout.turnOff()
        device.Gpio.roofout.turnOn()

        result = browser.browser.startStop(self.app)
        ok = (result == 'OK')
        if ok:
            self._start_roof_state_watcher(device.Gpio.close, self._on_close_complete, 'close')
        return self._resp(ok, 0 if ok else 2, '' if ok else 'Failed to close shutter')


# If the module is imported, user can create an Alpaca instance. When run
# directly for quick smoke testing, create a Flask app and register the
# routes on it.
if (__name__ == '__main__'):
    from flask import Flask
    test_app = Flask(__name__)
    Alpaca(test_app)
    test_app.run('0.0.0.0', 8000)
