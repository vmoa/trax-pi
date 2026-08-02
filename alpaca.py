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

Interface notes (ASCOM Alpaca compliance)
-----------------------------------------
A real ASCOM/Alpaca client (e.g. NINA) requires a specific contract that
the earlier version of this file did not fully satisfy.  The pieces that
were folded in from the reference driver (`ALPACA_Dome_Driver-c.py`) are:

* ``CanSetShutter`` returns ``True`` -- a client will not expose the
  Open/Close Shutter buttons unless the driver advertises this.
* ``ShutterStatus`` uses the real ASCOM ``ShutterState`` enumeration
  (0=Open, 1=Closed, 2=Opening, 3=Closing, 4=Error).  The previous code
  used a home-grown mapping (2=Open) that collides with the ASCOM value
  for "Opening".
* ``OpenShutter``/``CloseShutter`` (and ``Connected``/``AbortSlew``) are
  ASCOM *methods*, invoked with HTTP ``PUT``; parameters such as
  ``ClientTransactionID`` arrive in the form body rather than the query
  string.
* The standard Alpaca management API (``/management/apiversions``,
  ``/management/v1/description``, ``/management/v1/configureddevices``).

Unlike the reference driver -- which blocks the request with ``sleep()``
while it fakes roof motion -- ASCOM methods must return promptly and let
the client poll ``ShutterStatus``.  We keep the project's existing
non-blocking design: the command starts the roof and a background watcher
thread updates the tracked status when the roof reaches its end stop.
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

# HTTP port the Flask app (and therefore the Alpaca API) listens on. This is
# what the UDP discovery responder advertises to clients.
ALPACA_HTTP_PORT = 5000

DRIVER_VERSION = '1.1.0'

# ASCOM error number for a property/method that is part of the interface but
# not implemented by this driver (e.g. dome rotation on a shutter-only roof).
NOT_IMPLEMENTED = 0x400

# ASCOM ShutterState enumeration (Dome.ShutterStatus). These values are part
# of the wire protocol -- clients interpret them literally, so they must match
# the ASCOM standard exactly.
SHUTTER_OPEN = 0
SHUTTER_CLOSED = 1
SHUTTER_OPENING = 2
SHUTTER_CLOSING = 3
SHUTTER_ERROR = 4


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
        # Last direction the roof was commanded to move. Used to report
        # Opening/Closing while the roof is between its end-stop sensors.
        self._shutter_status = None
        # Register routes
        prefix = self._prefix()

        # Core device metadata
        app.add_url_rule(prefix + '/connected', endpoint=prefix + '_connected', view_func=self._connected, methods=['GET', 'PUT'])
        app.add_url_rule(prefix + '/name', endpoint=prefix + '_name', view_func=self._name, methods=['GET'])
        app.add_url_rule(prefix + '/description', endpoint=prefix + '_description', view_func=self._description, methods=['GET'])
        app.add_url_rule(prefix + '/driverinfo', endpoint=prefix + '_driverinfo', view_func=self._driverinfo, methods=['GET'])
        app.add_url_rule(prefix + '/driverversion', endpoint=prefix + '_driverversion', view_func=self._driverversion, methods=['GET'])
        # ASCOM common properties a compliant client queries on connect.
        app.add_url_rule(prefix + '/interfaceversion', endpoint=prefix + '_interfaceversion', view_func=self._interfaceversion, methods=['GET'])
        app.add_url_rule(prefix + '/supportedactions', endpoint=prefix + '_supportedactions', view_func=self._supportedactions, methods=['GET'])

        # Capability flags. The roof is a shutter-only dome: it can set the
        # shutter but cannot rotate, slave, park or find home.
        app.add_url_rule(prefix + '/cansetshutter', endpoint=prefix + '_cansetshutter', view_func=self._cansetshutter, methods=['GET'])
        app.add_url_rule(prefix + '/cansyncazimuth', endpoint=prefix + '_cansyncazimuth', view_func=self._cansyncazimuth, methods=['GET'])
        app.add_url_rule(prefix + '/canrotate', endpoint=prefix + '_canrotate', view_func=self._canrotate, methods=['GET'])
        app.add_url_rule(prefix + '/canpark', endpoint=prefix + '_canpark', view_func=self._canpark, methods=['GET'])
        app.add_url_rule(prefix + '/canfindhome', endpoint=prefix + '_canfindhome', view_func=self._canfindhome, methods=['GET'])

        # Advertising InterfaceVersion 2 promises the whole IDomeV2 contract, so
        # the remaining rotation/park members must exist rather than 404. For a
        # shutter-only roof the capability flags are all false, the boolean
        # state properties report false, and the numeric position properties
        # and rotation/park methods return a proper ASCOM "not implemented"
        # error (better than a bare Flask 404 a strict client may reject on).
        for cap in ('cansetaltitude', 'cansetazimuth', 'cansetpark', 'canslave'):
            app.add_url_rule(prefix + '/' + cap, endpoint=prefix + '_' + cap, view_func=self._const_view(False), methods=['GET'])
        for prop in ('athome', 'atpark', 'slewing'):
            app.add_url_rule(prefix + '/' + prop, endpoint=prefix + '_' + prop, view_func=self._const_view(False), methods=['GET'])
        for prop in ('altitude', 'azimuth'):
            app.add_url_rule(prefix + '/' + prop, endpoint=prefix + '_' + prop, view_func=self._not_impl_view(prop), methods=['GET'])
        for meth in ('findhome', 'park', 'setpark', 'slewtoaltitude', 'slewtoazimuth', 'synctoazimuth'):
            app.add_url_rule(prefix + '/' + meth, endpoint=prefix + '_' + meth, view_func=self._not_impl_view(meth), methods=['GET', 'POST', 'PUT'])
        # Slaved is readable (always false) and writable only to false.
        app.add_url_rule(prefix + '/slaved', endpoint=prefix + '_slaved', view_func=self._slaved, methods=['GET', 'PUT'])

        # Basic discovery / service info (rooted at the base path)
        app.add_url_rule(self.base + '/discovery', endpoint=prefix + '_discovery', view_func=self._discovery, methods=['GET'])
        app.add_url_rule(self.base + '/apiversion', endpoint=prefix + '_apiversion', view_func=self._apiversion, methods=['GET'])

        # Standard Alpaca management API (server-global, rooted at /management)
        app.add_url_rule('/management/apiversions', endpoint=prefix + '_management_apiversions', view_func=self._management_apiversions, methods=['GET'])
        app.add_url_rule('/management/v1/description', endpoint=prefix + '_management_description', view_func=self._management_description, methods=['GET'])
        app.add_url_rule('/management/v1/configureddevices', endpoint=prefix + '_management_configureddevices', view_func=self._configureddevices, methods=['GET'])
        # Backward-compatible aliases some clients probe under the API base
        app.add_url_rule(self.base + '/management/apiversions', endpoint=prefix + '_management_apiversions_prefixed', view_func=self._management_apiversions, methods=['GET'])
        app.add_url_rule(self.base + '/configureddevices', endpoint=prefix + '_configureddevices', view_func=self._configureddevices, methods=['GET'])
        self._start_multicast_responder()

        # Shutter control. Open/Close are ASCOM methods invoked with PUT; we
        # also accept GET/POST so the endpoints can be exercised from a browser.
        app.add_url_rule(prefix + '/openshutter', endpoint=prefix + '_openshutter', view_func=self._openshutter, methods=['GET', 'POST', 'PUT'])
        app.add_url_rule(prefix + '/closeshutter', endpoint=prefix + '_closeshutter', view_func=self._closeshutter, methods=['GET', 'POST', 'PUT'])
        app.add_url_rule(prefix + '/abortslew', endpoint=prefix + '_abortslew', view_func=self._abortslew, methods=['GET', 'POST', 'PUT'])
        app.add_url_rule(prefix + '/shutterstatus', endpoint=prefix + '_shutterstatus', view_func=self._shutterstatus, methods=['GET'])
        # Retain the previously-used name as an alias for existing callers.
        app.add_url_rule(prefix + '/shutterstate', endpoint=prefix + '_shutterstate', view_func=self._shutterstatus, methods=['GET'])

    def _prefix(self):
        # e.g. /api/v1/dome/0
        return '{}/dome/{}'.format(self.base, self.device_number)

    def _next_txid(self):
        Alpaca.server_txid += 1
        return Alpaca.server_txid

    def _client_txid(self):
        """Read ClientTransactionID from the query string (GET) or form (PUT)."""
        for src in (flask.request.args, flask.request.form):
            raw = src.get('ClientTransactionID')
            if raw is not None:
                try:
                    return int(raw)
                except (TypeError, ValueError):
                    return 0
        return 0

    def _resp(self, value=None, error_number=0, error_message=''):
        resp = {
            'ClientTransactionID': self._client_txid(),
            'ServerTransactionID': self._next_txid(),
            'ErrorNumber': int(error_number),
            'ErrorMessage': error_message,
        }
        # ASCOM property reads carry a Value; method (PUT) responses do not.
        if value is not None:
            resp['Value'] = value
        return flask.jsonify(resp)

    def _const_view(self, value):
        """Build a zero-arg GET handler that always returns a constant value."""
        return lambda: self._resp(value)

    def _not_impl_view(self, name):
        """Build a handler for an interface member this driver does not implement."""
        return lambda: self._resp(error_number=NOT_IMPLEMENTED, error_message='{} is not implemented'.format(name))

    def _slaved(self):
        # A roll-off roof cannot slave to the telescope. Report false, and
        # accept a PUT only when it sets Slaved=false (a no-op).
        if flask.request.method == 'PUT':
            want = flask.request.form.get('Slaved', 'false').lower() == 'true'
            if want:
                return self._resp(error_number=NOT_IMPLEMENTED, error_message='Slaving is not implemented')
            return self._resp()
        return self._resp(False)

    # Core info endpoints
    def _connected(self):
        # A client "connects" by PUTting Connected=true. We are stateless and
        # always available, so we simply acknowledge the request.
        if flask.request.method == 'PUT':
            state = flask.request.form.get('Connected', 'false').lower() == 'true'
            logging.info('Alpaca: client set Connected=%s', state)
            return self._resp()
        return self._resp(True)

    def _name(self):
        return self._resp('T-Rax Roof Dome')

    def _description(self):
        return self._resp('T-Rax roll-off roof presented as an Alpaca dome (shutter only)')

    def _driverinfo(self):
        return self._resp('T-Rax Alpaca dome bridge to the roll-off roof controller')

    def _driverversion(self):
        return self._resp(DRIVER_VERSION)

    def _interfaceversion(self):
        # We implement the classic IDomeV2 property/method set.
        return self._resp(2)

    def _supportedactions(self):
        # No device-specific custom actions are exposed.
        return self._resp([])

    # Capability endpoints
    def _cansetshutter(self):
        # The roof *is* the shutter, so we can open and close it.
        return self._resp(True)

    def _cansyncazimuth(self):
        return self._resp(False)

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
            'HTTPPort': ALPACA_HTTP_PORT,
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

    def _management_apiversions(self):
        """Return list of supported Alpaca API versions (management discovery)."""
        return self._resp([1])

    def _management_description(self):
        """Return the server description block for management discovery."""
        return self._resp({
            'ServerName': 'T-Rax',
            'Manufacturer': 'Robert Ferguson Observatory',
            'ManufacturerVersion': DRIVER_VERSION,
            'Location': 'RFO, Kenwood CA',
        })

    def _configureddevices(self):
        # Return list of configured devices on this server
        devices = [
            {
                'DeviceName': 'T-Rax Roof Dome',
                'DeviceType': 'Dome',
                'DeviceNumber': self.device_number,
                'UniqueID': 'uuid:trax:dome:{}'.format(self.device_number),
            }
        ]
        return self._resp(devices)

    def _format_discovery_response(self, client_addr):
        # Per the Alpaca discovery specification the UDP reply is a small JSON
        # document naming the HTTP port the Alpaca API is served on.
        try:
            payload = {'AlpacaPort': ALPACA_HTTP_PORT}
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
                # The official Alpaca discovery probe is the ASCII string
                # "alpacadiscovery1". Also accept the legacy SSDP-style probes.
                upper = text.upper()
                if 'ALPACADISCOVERY' in upper or 'M-SEARCH' in upper or 'DISCOVERY' in upper:
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
        # Map the roof end-stop sensors to the ASCOM ShutterState enum. The
        # sensors are authoritative for the terminal Open/Closed states; while
        # the roof is between them we report the direction of the move in
        # progress (tracked in self._shutter_status).
        try:
            open_on = device.Gpio.open.isOn()
            close_on = device.Gpio.close.isOn()
        except Exception:
            return SHUTTER_ERROR

        if open_on and close_on:
            # Both sensors active is a fault ("confused") condition.
            return SHUTTER_ERROR
        if open_on:
            return SHUTTER_OPEN
        if close_on:
            return SHUTTER_CLOSED
        # Neither sensor active: the roof is midway. Report the in-progress
        # direction if a command is running, otherwise flag it as an error.
        if self._shutter_status in (SHUTTER_OPENING, SHUTTER_CLOSING):
            return self._shutter_status
        return SHUTTER_ERROR

    def _start_roof_state_watcher(self, target_sensor, success_fn, action_name):
        def watcher():
            deadline = time.time() + ROOF_STATE_TIMEOUT
            while time.time() < deadline:
                if target_sensor.isOn():
                    success_fn()
                    return
                time.sleep(ROOF_STATE_POLL_INTERVAL)
            self._shutter_status = SHUTTER_ERROR
            browser.browser.sendNotice(
                "Timeout waiting for roof {} after {} seconds".format(action_name, ROOF_STATE_TIMEOUT),
                log='ERROR'
            )

        thread = threading.Thread(target=watcher, daemon=True)
        thread.start()

    def _on_open_complete(self):
        self._shutter_status = SHUTTER_OPEN
        browser.browser.sendNotice("Roof open; turning off roof power and enabling mount power", log='INFO')
        device.Gpio.roofout.turnOff()
        device.Gpio.mntout.turnOn()

    def _on_close_complete(self):
        self._shutter_status = SHUTTER_CLOSED
        browser.browser.sendNotice("Roof closed; turning off roof power", log='INFO')
        device.Gpio.roofout.turnOff()

    def _shutterstatus(self):
        return self._resp(self._get_shutter_state())

    def _openshutter(self):
        logging.info("Alpaca: OpenShutter requested from %s", flask.request.remote_addr)
        # If already open, succeed
        if device.Gpio.open.isOn():
            self._shutter_status = SHUTTER_OPEN
            return self._resp()

        # The roof is driven by a single START/STOP toggle, so a second command
        # while it is moving would stop (not continue/reverse) it. Treat a
        # repeated open as idempotent, and refuse to open while it is closing
        # rather than halting it mid-travel.
        if self._shutter_status == SHUTTER_OPENING:
            return self._resp()
        if self._shutter_status == SHUTTER_CLOSING:
            return self._resp(error_number=1, error_message='Cannot open shutter: roof is closing; wait for it to finish')

        # Require the telescope to be parked before cutting mount power.
        if (device.Gpio.park.checkParked() != device.park.PARKED):
            return self._resp(error_number=1, error_message='Cannot open shutter: mount must be parked first')

        # Ensure mount power is off and roof power is on before opening.
        device.Gpio.mntout.turnOff()
        device.Gpio.roofout.turnOn()

        # Use the same safety checks as the browser/startStop path by
        # delegating to browser.startStop which toggles roof appropriately
        result = browser.browser.startStop(self.app)
        ok = (result == 'OK')
        if ok:
            self._shutter_status = SHUTTER_OPENING
            self._start_roof_state_watcher(device.Gpio.open, self._on_open_complete, 'open')
            return self._resp()
        return self._resp(error_number=1, error_message='Failed to open shutter')

    def _closeshutter(self):
        logging.info("Alpaca: CloseShutter requested from %s", flask.request.remote_addr)
        # If already closed, succeed
        if device.Gpio.close.isOn():
            self._shutter_status = SHUTTER_CLOSED
            return self._resp()

        # Mirror OpenShutter: a repeated close while already closing is
        # idempotent, and closing while the roof is opening is refused rather
        # than stopping it mid-travel (single START/STOP toggle hardware).
        if self._shutter_status == SHUTTER_CLOSING:
            return self._resp()
        if self._shutter_status == SHUTTER_OPENING:
            return self._resp(error_number=2, error_message='Cannot close shutter: roof is opening; wait for it to finish')

        # Require the telescope to be parked before cutting mount power.
        if (device.Gpio.park.checkParked() != device.park.PARKED):
            return self._resp(error_number=2, error_message='Cannot close shutter: mount must be parked first')

        # Ensure mount power is off and roof power is on before closing.
        device.Gpio.mntout.turnOff()
        device.Gpio.roofout.turnOn()

        result = browser.browser.startStop(self.app)
        ok = (result == 'OK')
        if ok:
            self._shutter_status = SHUTTER_CLOSING
            self._start_roof_state_watcher(device.Gpio.close, self._on_close_complete, 'close')
            return self._resp()
        return self._resp(error_number=2, error_message='Failed to close shutter')

    def _abortslew(self):
        # A roll-off roof should not be halted mid-travel from a remote client:
        # stopping the motor between end stops leaves the observatory exposed
        # and defeats the safety interlocks. We acknowledge the ASCOM method so
        # clients do not error, but take no action. Use the physical Emergency
        # Stop control for a genuine emergency halt.
        logging.info("Alpaca: AbortSlew requested from %s (no-op for roll-off roof)", flask.request.remote_addr)
        return self._resp()


# If the module is imported, user can create an Alpaca instance. When run
# directly for quick smoke testing, create a Flask app and register the
# routes on it.
if (__name__ == '__main__'):
    from flask import Flask
    test_app = Flask(__name__)
    Alpaca(test_app)
    test_app.run('0.0.0.0', 8000)
