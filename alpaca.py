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

ROOF_STATE_TIMEOUT = 60
ROOF_STATE_POLL_INTERVAL = 0.5
ROOF_POWER_SETTLE_DELAY = 1.0
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
        # Tracked shutter motion. `_shutter_status` holds the in-flight
        # Opening/Closing direction (or a terminal value set by a watcher);
        # `_lock` serialises command acceptance and state transitions, and
        # `_motion_gen` tags each move so a superseded watcher goes inert.
        self._shutter_status = None
        self._lock = threading.Lock()
        self._motion_gen = 0
        # True while a move is reserved but its preflight (park check + toggle)
        # has not yet confirmed the roof is actually moving.
        self._move_pending = False
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
        # ASCOM common methods. Unsupported here, but they must return the
        # standard not-implemented envelope (not a bare 404) for conformance
        # tools and clients that probe them.
        for meth in ('action', 'commandblind', 'commandbool', 'commandstring'):
            app.add_url_rule(prefix + '/' + meth, endpoint=prefix + '_' + meth, view_func=self._not_impl_view(meth), methods=['GET', 'POST', 'PUT'])

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
        for prop in ('athome', 'atpark'):
            app.add_url_rule(prefix + '/' + prop, endpoint=prefix + '_' + prop, view_func=self._const_view(False), methods=['GET'])
        # Slewing is derived from the live shutter status (see _slewing).
        app.add_url_rule(prefix + '/slewing', endpoint=prefix + '_slewing', view_func=self._slewing, methods=['GET'])
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

    def _format_discovery_response(self):
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
                    response = self._format_discovery_response()
                    sock.sendto(response, addr)
            except Exception as e:
                logging.error('Alpaca multicast responder error: %s', e)

    def _start_multicast_responder(self):
        thread = threading.Thread(target=self._multicast_responder, daemon=True)
        thread.start()

    # Shutter state mapping
    def _get_shutter_state(self):
        # A tracked move in progress takes precedence over the end-stop sensors:
        # the origin sensor can stay asserted until the motor physically starts,
        # so reporting the sensor here would momentarily look like a completed
        # terminal state. While Opening/Closing the watcher owns the transition
        # to the terminal value once the target sensor asserts.
        status = self._shutter_status
        if status in (SHUTTER_OPENING, SHUTTER_CLOSING):
            return status
        # At rest the end-stop sensors are authoritative (this also reflects
        # motion started outside this Alpaca instance, e.g. via /startstop).
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
        # Neither sensor active and no tracked move: the roof is stuck midway.
        return SHUTTER_ERROR

    def _start_roof_state_watcher(self, gen, target_sensor, success_fn, action_name):
        # `gen` tags this watcher with the motion generation it belongs to. If a
        # newer move (or rollback) bumps self._motion_gen, this watcher becomes
        # stale and must not touch the shutter state -- otherwise a lingering
        # opening watcher could fire _on_open_complete during a later close,
        # cutting roof power and enabling mount power mid-close.
        def watcher():
            deadline = time.time() + ROOF_STATE_TIMEOUT
            try:
                while time.time() < deadline:
                    if self._motion_gen != gen:
                        return  # superseded by a newer move
                    if target_sensor.isOn():
                        with self._lock:
                            if self._motion_gen != gen:
                                return
                            success_fn()
                        return
                    time.sleep(ROOF_STATE_POLL_INTERVAL)
            except Exception as e:
                # A transient sensor/GPIO read (or completion callback) failure
                # must not leave the daemon thread dead with the status stuck
                # Opening/Closing forever. Fall through to the error transition.
                logging.error('Alpaca: roof %s watcher error: %s', action_name, e)
                with self._lock:
                    if self._motion_gen == gen:
                        self._shutter_status = SHUTTER_ERROR
                return
            with self._lock:
                if self._motion_gen != gen:
                    return
                self._shutter_status = SHUTTER_ERROR
            browser.browser.sendNotice(
                "Timeout waiting for roof {} after {} seconds".format(action_name, ROOF_STATE_TIMEOUT),
                log='ERROR'
            )

        thread = threading.Thread(target=watcher, daemon=True)
        thread.start()

    # Note: _on_open_complete / _on_close_complete run while self._lock is held
    # (called from the watcher) so the status update and GPIO actuation are
    # atomic with respect to command acceptance.
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

    def _slewing(self):
        # Slewing reports whether any dome component is moving. The roof only
        # moves while the shutter is opening or closing.
        return self._resp(self._get_shutter_state() in (SHUTTER_OPENING, SHUTTER_CLOSING))

    def _openshutter(self):
        logging.info("Alpaca: OpenShutter requested from %s", flask.request.remote_addr)
        return self._begin_move(
            moving_status=SHUTTER_OPENING, terminal_status=SHUTTER_OPEN,
            origin_sensor=device.Gpio.close, target_sensor=device.Gpio.open,
            success_fn=self._on_open_complete, action='open', origin_name='closed', err_no=1)

    def _closeshutter(self):
        logging.info("Alpaca: CloseShutter requested from %s", flask.request.remote_addr)
        return self._begin_move(
            moving_status=SHUTTER_CLOSING, terminal_status=SHUTTER_CLOSED,
            origin_sensor=device.Gpio.open, target_sensor=device.Gpio.close,
            success_fn=self._on_close_complete, action='close', origin_name='open', err_no=2)

    def _begin_move(self, moving_status, terminal_status, origin_sensor, target_sensor,
                    success_fn, action, origin_name, err_no):
        # Reserve the move atomically *before* any blocking work. The roof is a
        # single START/STOP toggle with no defined direction from a midway
        # position, so the acceptance decision and the Opening/Closing
        # reservation must be one critical section: otherwise an overlapping
        # retry could pass the guard (because the status was not yet set) and
        # fire a second toggle that stops the roof.
        with self._lock:
            # A matching move is already tracked.
            if self._shutter_status == moving_status:
                if self._move_pending:
                    # Reserved, but its preflight has not confirmed the roof is
                    # moving yet -- and it may still fail (unparked mount, failed
                    # toggle) and roll back. Do not acknowledge a duplicate as a
                    # started move; report that a command is already in progress.
                    return self._resp(
                        error_number=err_no,
                        error_message='Cannot {} shutter: a shutter move is already in progress'.format(action))
                return self._resp()  # confirmed in-flight -> idempotent success
            # Already resting at the target end stop -> success.
            if self._shutter_status not in (SHUTTER_OPENING, SHUTTER_CLOSING) and target_sensor.isOn():
                self._shutter_status = terminal_status
                return self._resp()
            # A move in the other direction is running, or the roof is not
            # resting at the origin end stop (midway / in motion / unknown):
            # refuse rather than fire the directionless toggle.
            if self._shutter_status in (SHUTTER_OPENING, SHUTTER_CLOSING) or not origin_sensor.isOn():
                return self._resp(
                    error_number=err_no,
                    error_message='Cannot {} shutter: roof is not {} (position unknown or in motion)'.format(action, origin_name))
            # Reserve the move (pending until actuation confirms) and open a new
            # motion generation, invalidating any earlier watcher, before
            # releasing the lock for the blocking work.
            self._shutter_status = moving_status
            self._move_pending = True
            self._motion_gen += 1
            gen = self._motion_gen

        # Blocking safety checks and actuation happen outside the lock so status
        # reads are not stalled by the (multi-second) park check. Failures *before*
        # the fob is toggled roll the reservation back; once startStop() has
        # actuated the roof we must not roll back (a rollback would let a retry
        # re-toggle and stop the moving roof).
        try:
            if device.Gpio.park.checkParked() != device.park.PARKED:
                return self._abort_move(gen, err_no, 'Cannot {} shutter: mount must be parked first'.format(action))

            # Ensure mount power is off and roof power is on before moving.
            device.Gpio.mntout.turnOff()
            device.Gpio.roofout.turnOn()
            if ROOF_POWER_SETTLE_DELAY > 0:
                logging.info('Alpaca: waiting %.1f seconds for roof power relays to settle before toggling roof', ROOF_POWER_SETTLE_DELAY)
                time.sleep(ROOF_POWER_SETTLE_DELAY)

            # Delegate to the same safety-checked toggle path used by the browser.
            if browser.browser.startStop(self.app) != 'OK':
                return self._abort_move(gen, err_no, 'Failed to {} shutter'.format(action))
        except Exception as e:
            logging.error('Alpaca: %s shutter failed before actuation: %s', action, e)
            return self._abort_move(gen, err_no, 'Failed to {} shutter: {}'.format(action, e))

        # startStop() has actuated the fob; browser.toggleFob() moves the roof
        # asynchronously, so from here the roof is committed to moving. Promote
        # the reservation to a confirmed move; any failure starting the watcher
        # leaves the move conservatively tracked (Opening/Closing) rather than
        # rolled back, so a retry cannot trigger a second, roof-stopping toggle.
        with self._lock:
            if self._motion_gen != gen:
                return self._resp()  # superseded during preflight
            self._move_pending = False
        try:
            self._start_roof_state_watcher(gen, target_sensor, success_fn, action)
        except Exception as e:
            logging.error('Alpaca: %s watcher failed to start; move left tracked: %s', action, e)
        return self._resp()

    def _abort_move(self, gen, err_no, message):
        # Roll back a reserved-but-unstarted move so the sensors re-derive the
        # resting state. Guarded by the generation so we never clobber a newer
        # move that raced in.
        with self._lock:
            if self._motion_gen == gen:
                self._shutter_status = None
                self._move_pending = False
        return self._resp(error_number=err_no, error_message=message)

    def _abortslew(self):
        # A roll-off roof cannot honour a remote mid-travel abort: stopping the
        # motor between end stops leaves the observatory exposed and defeats the
        # safety interlocks. Rather than falsely report that motion stopped,
        # return an explicit "not implemented" error so a caller cannot act on a
        # bogus success. Use the physical Emergency Stop control for a genuine
        # emergency halt.
        logging.info("Alpaca: AbortSlew requested from %s (not implemented for roll-off roof)", flask.request.remote_addr)
        return self._resp(error_number=NOT_IMPLEMENTED, error_message='AbortSlew is not implemented for a roll-off roof')


# If the module is imported, user can create an Alpaca instance. When run
# directly for quick smoke testing, create a Flask app and register the
# routes on it.
if (__name__ == '__main__'):
    from flask import Flask
    test_app = Flask(__name__)
    Alpaca(test_app)
    test_app.run('0.0.0.0', 8000)
