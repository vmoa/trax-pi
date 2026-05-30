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
import threading

import flask

import browser
import device


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

    def _shutterstate(self):
        return self._resp(self._get_shutter_state())

    def _openshutter(self):
        logging.info("Alpaca: OpenShutter requested from %s", flask.request.remote_addr)
        # If already open, succeed
        if device.Gpio.open.isOn():
            return self._resp(True)

        # Use the same safety checks as the browser/startStop path by
        # delegating to browser.startStop which toggles roof appropriately
        result = browser.browser.startStop(self.app)
        ok = (result == 'OK')
        return self._resp(ok, 0 if ok else 1, '' if ok else 'Failed to open shutter')

    def _closeshutter(self):
        logging.info("Alpaca: CloseShutter requested from %s", flask.request.remote_addr)
        # If already closed, succeed
        if device.Gpio.close.isOn():
            return self._resp(True)

        result = browser.browser.startStop(self.app)
        ok = (result == 'OK')
        return self._resp(ok, 0 if ok else 2, '' if ok else 'Failed to close shutter')


# If the module is imported, user can create an Alpaca instance. When run
# directly for quick smoke testing, create a Flask app and register the
# routes on it.
if (__name__ == '__main__'):
    from flask import Flask
    test_app = Flask(__name__)
    Alpaca(test_app)
    test_app.run('0.0.0.0', 8000)
