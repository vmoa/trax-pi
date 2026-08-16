# Interactive browser callbacks
#
# Callbacks are registered in trax.py because it just makes flask cleaner

import flask
import hashlib
import logging
import re
import threading
import time

import device
import sse

OVERRIDE_PASSWD_FILE = 'override.passwd'

ROOF_POWER_SETTLE_DELAY = 1.0   # seconds to wait after turning on roof power relays
ROOF_MOVE_TIMEOUT = 60          # seconds before giving up on a roof move
ROOF_MOVE_POLL = 0.5            # seconds between sensor polls during a move

# True while any roof move (browser-initiated or Alpaca-initiated) is in progress.
# Prevents concurrent /startstop, /open, /close from interfering.
# Emergency override mode bypasses this gate, as it bypasses all interlocks.
roof_move_active = False


class Browser:

    emergencyOverride = 0
    version = "unknown"  # Will be set at startup
    _override_hash = None  # SHA-256 hex digest loaded from OVERRIDE_PASSWD_FILE

    def setVersion(self, version):
        """Set the version so browser callbacks can report it"""
        self.version = version
        self._init_override_password()

    def _init_override_password(self):
        """Load the override password hash from OVERRIDE_PASSWD_FILE.

        The file must contain a single SHA-256 hex digest (64 lowercase hex chars).
        Generate one with:
            python3 -c "import hashlib; print(hashlib.sha256(b'yourpassword').hexdigest())"
        If the file is absent or malformed, override mode is disabled entirely.
        """
        try:
            with open(OVERRIDE_PASSWD_FILE) as f:
                h = f.read().strip().lower()
            if len(h) == 64 and all(c in '0123456789abcdef' for c in h):
                Browser._override_hash = h
                logging.info('Override password loaded from %s', OVERRIDE_PASSWD_FILE)
            else:
                logging.warning('Override password file %s is malformed; override disabled', OVERRIDE_PASSWD_FILE)
        except FileNotFoundError:
            logging.warning('Override password file %s not found; override disabled', OVERRIDE_PASSWD_FILE)
        except OSError as e:
            logging.warning('Cannot read override password file: %s; override disabled', e)

    def sendNotice(self, msg, log=''):
        """Update the notice area on the browser and optionally log the message"""
        if (log == 'ERROR'):
            logging.error(msg)
        elif (log == 'INFO'):
            logging.info(msg)
        sse.sse.send(id='notice', type='innerHTML', data=re.sub(r': +', ':<br/>', msg))

    def sendTicker(self, msg):
        """Update the ticker on the browser"""
        sse.sse.send(id='ticker', type='innerHTML', data=msg)

    # TODO: (maybe) optimize to only send updates for changes?
    def updateBrowser(self):
        """Decorate the indicators on the web browser"""
        if (device.Gpio.close.isOn() and device.Gpio.open.isOn()):
            sse.sse.send(type='indicator', id='roof_position', status='confused')
        elif (device.Gpio.close.isOn()):
            sse.sse.send(type='indicator', id='roof_position', status='closed')
        elif (device.Gpio.open.isOn()):
            sse.sse.send(type='indicator', id='roof_position', status='open')
        else:
            sse.sse.send(type='indicator', id='roof_position', status='midway')

        if (browser.emergencyOverride):
            # Emergency override reports actual park sensor status
            if (device.Gpio.park.isOn()):
                sse.sse.send(type='indicator', id='mount_position', status='parked')
            else:
                sse.sse.send(type='indicator', id='mount_position', status='notparked')
        else:
            parkState = device.Gpio.park.isParked()
            if (parkState == device.park.PARKED_PROBABLY):
                sse.sse.send(type='indicator', id='mount_position', status='parked_probably')
            elif (parkState == device.park.PARKED):
                sse.sse.send(type='indicator', id='mount_position', status='parked')
            elif (parkState == device.park.UNPARKED):
                sse.sse.send(type='indicator', id='mount_position', status='notparked')
            elif (parkState == device.park.UNPARKED_PROBABLY):
                sse.sse.send(type='indicator', id='mount_position', status='notparked_probably')
            else:
                sse.sse.send(type='indicator', id='mount_position', status='unknown')

        if (device.Gpio.bldg.isOn()):
            sse.sse.send(type='indicator', id='building_pwr', status='on')
        else:
            sse.sse.send(type='indicator', id='building_pwr', status='off')

        if (device.Gpio.roofin.isOn()):
            sse.sse.send(type='indicator', id='roof_pwr', status='on')
        else:
            sse.sse.send(type='indicator', id='roof_pwr', status='off')

        if (device.Gpio.mntin.isOn()):
            sse.sse.send(type='indicator', id='mount_pwr', status='on')
        else:
            sse.sse.send(type='indicator', id='mount_pwr', status='off')


    def initialConnect(self):
        """Send intial connect message to browser and make sure indicators are colored"""
        self.sendNotice("Connected!<br/>Welcome to T-Rax!<br/>Version %s" % self.version)
        self.updateBrowser()
        if (self.emergencyOverride):
            self.enterOverrideMode()

    def doOpen(self, skip_park_check=False):
        """Execute the full roof-open sequence: safety checks, power management, fob toggle, watcher.

        Manages power automatically: turns mount power off and roof power on as needed.
        Returns 'OK' on success or an error message string on failure.
        """
        global roof_move_active
        if roof_move_active:
            msg = "Cannot open roof: a roof move is already in progress"
            self.sendNotice(msg, log='ERROR')
            return msg
        if not device.Gpio.close.isOn():
            msg = "Cannot open roof: roof is not closed"
            self.sendNotice(msg, log='ERROR')
            return msg
        if not device.Gpio.bldg.isOn():
            msg = "Cannot open roof: building power has failed"
            self.sendNotice(msg, log='ERROR')
            return msg
        if not skip_park_check and device.Gpio.park.checkParked() != device.park.PARKED:
            msg = "Cannot open roof: Mount must be parked first"
            self.sendNotice(msg, log='ERROR')
            return msg
        if not device.Gpio.wx.isOn():
            msg = "Cannot open roof: Weather not OK"
            self.sendNotice(msg, log='ERROR')
            return msg

        # Power management: ensure mount off and roof on before moving.
        device.Gpio.mntout.turnOff()
        if not device.Gpio.roofout.isOn():
            device.Gpio.roofout.turnOn()
            time.sleep(ROOF_POWER_SETTLE_DELAY)

        self.sendNotice("Toggling fob (opening roof)", log='INFO')
        device.Gpio.fob.toggleFob()
        self._start_move_watcher(device.Gpio.open, self._on_open_complete, 'open')
        return "OK"

    def doClose(self, skip_park_check=False):
        """Execute the full roof-close sequence: safety checks, fob toggle, watcher.

        Does NOT auto-manage mount power — mount must be off before calling.
        Returns 'OK' on success or an error message string on failure.
        """
        global roof_move_active
        if roof_move_active:
            msg = "Cannot close roof: a roof move is already in progress"
            self.sendNotice(msg, log='ERROR')
            return msg
        if not device.Gpio.open.isOn():
            msg = "Cannot close roof: roof is not open"
            self.sendNotice(msg, log='ERROR')
            return msg
        if not skip_park_check and device.Gpio.park.checkParked() != device.park.PARKED:
            msg = "Cannot close roof: mount must be parked first"
            self.sendNotice(msg, log='ERROR')
            return msg
        if not device.Gpio.mntin.isOff():
            msg = "Cannot close roof: mount power is on"
            self.sendNotice(msg, log='ERROR')
            return msg
        if not device.Gpio.roofout.isOn():
            device.Gpio.roofout.turnOn()
            time.sleep(ROOF_POWER_SETTLE_DELAY)

        self.sendNotice("Toggling fob (closing roof)", log='INFO')
        device.Gpio.fob.toggleFob()
        self._start_move_watcher(device.Gpio.close, self._on_close_complete, 'close')
        return "OK"

    def _on_open_complete(self):
        """Called by the move watcher when the roof finishes opening."""
        self.sendNotice("Roof open; turning off roof power and enabling mount power", log='INFO')
        device.Gpio.roofout.turnOff()
        device.Gpio.mntout.turnOn()

    def _on_close_complete(self):
        """Called by the move watcher when the roof finishes closing."""
        self.sendNotice("Roof closed; turning off roof power", log='INFO')
        device.Gpio.roofout.turnOff()

    def _start_move_watcher(self, target_sensor, complete_fn, action_name):
        """Start a daemon thread that waits for target_sensor then calls complete_fn.

        Sets roof_move_active=True immediately and clears it via finally when done.
        """
        global roof_move_active

        def watcher():
            global roof_move_active
            try:
                deadline = time.time() + ROOF_MOVE_TIMEOUT
                while time.time() < deadline:
                    if target_sensor.isOn():
                        complete_fn()
                        return
                    time.sleep(ROOF_MOVE_POLL)
                self.sendNotice(
                    "Timeout waiting for roof {} after {} seconds".format(action_name, ROOF_MOVE_TIMEOUT),
                    log='ERROR'
                )
            except Exception as e:
                logging.error('Browser: roof %s watcher error: %s', action_name, e)
            finally:
                roof_move_active = False

        roof_move_active = True
        threading.Thread(target=watcher, daemon=True).start()

    def startStop(self, app):
        """Process START/STOP button — delegates to doOpen/doClose for terminal positions."""
        logging.info("Click: START/STOP from {}".format(flask.request.remote_addr))

        if (self.emergencyOverride):
            self.sendNotice("EMERGENCY OVERRIDE: Toggling fob", log='INFO')
            device.Gpio.fob.toggle()
            return "OK"

        if (device.Gpio.close.isOn()):
            return self.doOpen()
        elif (device.Gpio.open.isOn()):
            return self.doClose()
        else:
            # Midway: no directional safety checks; just toggle
            self.sendNotice("Toggling fob (roof midway)", log='INFO')
            device.Gpio.fob.toggle()
            return "OK"


    def roofPower(self, app):
        """Process Roof Power ON or OFF button"""
        if ('on' in flask.request.args):
            action = 'ON'
        elif ('off' in flask.request.args):
            action = 'OFF'
        else:
            logging.error("Click: Roof Power UNKNOWN from {}".format(flask.request.remote_addr))
            return 'ERROR'
        logging.info("Click: Roof Power {} from {}".format(action, flask.request.remote_addr))

        if (action == 'ON'):
            if (self.emergencyOverride):
                self.sendNotice("EMERGENCY OVERRIDE: Turning on roof power", log='INFO')
            else:
                self.sendNotice("Turning on roof power", log='INFO')
            device.Gpio.roofout.turnOn()
            return 'OK'

        else:    # action == 'OFF'
            if (self.emergencyOverride):
                self.sendNotice("EMERGENCY OVERRIDE: Turning off roof power", log='INFO')
            else:
                self.sendNotice("Turning off roof power", log='INFO')
            device.Gpio.roofout.turnOff()
            return 'OK'

    def mountPower(self, app):
        """Porcess Mount Power ON or OFF button"""
        if ('on' in flask.request.args):
            action = 'ON'
        elif ('off' in flask.request.args):
            action = 'OFF'
        else:
            logging.error("Click: Mount Power UNKNOWN from {}".format(flask.request.remote_addr))
            return 'ERROR'
        logging.info("Click: Mount Power {} from {}".format(action, flask.request.remote_addr))

        if (action == 'ON'):
            if (self.emergencyOverride):
                self.sendNotice("EMERGENCY OVERRIDE: Turning on mount power", log='INFO')
            elif (device.Gpio.open.isOff()):
                self.sendNotice("Cannot turn on mount: roof is not open", log='ERROR')
                return 'ERROR'
            else:
                self.sendNotice("Turning on mount power", log='INFO')
            device.Gpio.mntout.turnOn()
            return 'OK'

        else:    # action == 'OFF'
            if (self.emergencyOverride):
                self.sendNotice("EMERGENCY OVERRIDE: Turning off mount power", log='INFO')
            else:
                self.sendNotice("Turning off mount power", log='INFO')
            device.Gpio.mntout.turnOff()
            return 'OK'

    def checkPark(self, app):
        """Actively check the mount park status"""
        logging.info("Click: Check Mount from {}".format(flask.request.remote_addr))
        if (self.emergencyOverride):
            # Toggle laser on/off; let updateBrowser report status
            if (device.Gpio.laser.isOff()):
                self.sendNotice("EMERGENCY OVERRIDE: Turning on laser (pew, pew) for a while", log='INFO')
                device.Gpio.laser.turnOn()
                device.Gpio.laser.timeOut = int(time.time()) + device.Gpio.laser.defaultTimeOut
            else:
                self.sendNotice("EMERGENCY OVERRIDE: Turning off laser", log='INFO')
                device.Gpio.laser.turnOff()
                device.Gpio.laser.timeOut = 0
        else:
            device.Gpio.park.checkParked()
        return 'OK'

    def emergencyStop(self, app):
        """Process EMERGENCY STOP button"""
        logging.info("Click: EMERGENCY STOP from {}".format(flask.request.remote_addr))
        device.Gpio.roofout.turnOff()
        self.sendNotice("EMERGENCY STOP!<br/>Turning off roof power")
        return "Emergency Stop OK"

    def enterOverrideMode(self):
        logging.info("Entering emergency override mode")
        self.sendNotice(" EMERGENCY OVERRIDE!!<br/>Be vewwy vewwy careful")
        sse.sse.send(type='override', mode='on')
        self.emergencyOverride = 1

    def exitOverrideMode(self):
        logging.info("Exiting emergency override mode")
        self.sendNotice("Restoring normal mode")
        sse.sse.send(type='override', mode='off')
        self.emergencyOverride = 0

    def checkPassword(self, password):
        if self._override_hash is None:
            logging.warning('Override attempted but override is disabled (no password file)')
            return False
        return hashlib.sha256(password.encode()).hexdigest() == self._override_hash

    def doOverride(self, app):
        """Process override actions (hidden modal from clicking ticker)"""
        if ('on' in flask.request.args):
            logging.info("Click: Override ON from {}".format(flask.request.remote_addr))
            if ('password' in flask.request.args):
                if (self.checkPassword(flask.request.args['password'])):
                    self.enterOverrideMode()
                    return 'OK'
                else:
                    logging.error("doOverride() bad password")
                    self.sendNotice("Incorrect password")
                    return 'ERROR'
            else:
                return 'OK'  # Silently ignore no password

        elif ('off' in flask.request.args):
            logging.info("Click: Override OFF from {}".format(flask.request.remote_addr))
            self.exitOverrideMode()
            return 'OK'

        else:
            logging.error("Click: Override mode UNKNOWN (or missing) from {}".format(flask.request.remote_addr))
            return 'ERROR'

        logging.error("doOverride() executed unreachable code!")
        return 'ERROR'

    def test(self, app):
        """Test request components; can probably delete"""
        logging.info("User pressed Test from {}".format(flask.request.remote_addr))
        print("request: ", flask.request)
        print("  .path: ", flask.request.path)
        print("  .args: ", flask.request.args)
        return("Test OK")

# Instantiate a browser object
browser = Browser()
