# Interactive browser callbacks
#
# Callbacks are registered in trax.py because it just makes flask cleaner

import flask
import logging
import re
import threading
import time

import device
import sse


class Browser:

    emergencyOverride = 0
    version = "unknown"  # Will be set at startup

    def setVersion(self, version):
        """Set the version so browser callbacks can report it"""
        self.version = version

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

    def startStop(self, app):
        """Process START/STOP button"""
        logging.info("Click: START/STOP from {}".format(flask.request.remote_addr))

        if (self.emergencyOverride):
            self.sendNotice("EMERGENCY OVERRIDE: Toggling fob", log='INFO')
            device.Gpio.fob.toggle()
            return "OK"

        # Open logic -- roof is closed
        if (device.Gpio.close.isOn()):
            if (device.Gpio.bldg.isOn()):
                if (device.Gpio.roofin.isOn()):
                    if (device.Gpio.park.checkParked() == device.park.PARKED):
                        if (device.Gpio.mntin.isOff()):
                            if (device.Gpio.wx.isOn()):
                                self.sendNotice("Toggling fob (opening roof)", log='INFO')
                                device.Gpio.fob.toggleFob()
                                return "OK"
                            else:
                                self.sendNotice("Cannot open roof: Weather not OK", log='ERROR')
                                return "ERROR"
                        else:
                            self.sendNotice("Cannot open roof: Mount power is on", log='ERROR')
                            return "ERROR"
                    else:
                        self.sendNotice("Cannot open roof: Mount must be parked first", log='ERROR')
                        return "ERROR"
                else:
                    self.sendNotice("Cannot open roof: roof power is not on", log='ERROR')
                    return "ERROR"
            else:
                self.sendNotice("Cannot open roof: building power has failed", log='ERROR')
                return "ERROR"

        # Close logic -- roof is open
        elif (device.Gpio.open.isOn()):
            if (device.Gpio.roofin.isOn()):
                if (device.Gpio.park.checkParked() == device.park.PARKED):
                    if (device.Gpio.mntin.isOff()):
                        self.sendNotice("Toggling fob (closing roof)", log='INFO')
                        device.Gpio.fob.toggleFob()
                        return "OK"
                    else:
                        self.sendNotice("Cannot close roof: mount power is on", log='ERROR')
                        return "ERROR"
                else:
                    self.sendNotice("Cannot close roof: mount must be parked first", log='ERROR')
                    return "ERROR"
            else:
                self.sendNotice("Cannot close roof: roof power is not on", log='ERROR')
                return "ERROR"

        # Midway logic -- neither open nor closed
        else:
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
                device.Gpio.roofout.turnOn()
                return "OK"
            else:
                self.sendNotice("Turning on roof power", log='INFO')
                device.Gpio.roofout.turnOn()
                return 'OK'

        else:    # action == 'OFF'
            if (self.emergencyOverride):
                self.sendNotice("EMERGENCY OVERRIDE: Turning off roof power", log='INFO')
                device.Gpio.roofout.turnOff()
                return "OK"
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
                device.Gpio.mntout.turnOn()
                return "OK"
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
                device.Gpio.mntout.turnOff()
                return "OK"
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
        logging.info("checkPassword({})".format(password))
        if (password == "password"):  # TODO: compare to md5 from a file
            return True
        else:
            return False

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
