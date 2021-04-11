# Interactive browser callbacks
#
# Callbacks are registered in trax.py because it just makes flask cleaner

import logging
import threading

import device
import flask
import sse


class Browser:

    def sendNotice(self, msg):
        """Update the notice area on the browser"""
        sse.sse.send(id='notice', type='innerHTML', data=msg)

    def sendTicker(self, msg):
        """Update the ticker on the browser"""
        sse.sse.send(id='ticker', type='innerHTML', data=msg)


    # TODO: make this a callback for any sensor change
    # TODO: (maybe) optimize to only send updates for changes?
    def updateBrowser(self):
        """Decorate the indicators on the web browser"""
        if (device.Sensor.by_name['close'].isOn()):
            sse.sse.send(type='indicator', id='roof_position', status='closed')
        elif (device.Sensor.by_name['open'].isOn()):
            sse.sse.send(type='indicator', id='roof_position', status='open')
        else:
            sse.sse.send(type='indicator', id='roof_position', status='midway')

        if (device.Sensor.by_name['park'].isOn()):
            sse.sse.send(type='indicator', id='mount_position', status='parked')
        else:
            sse.sse.send(type='indicator', id='mount_position', status='notparked')

        if (device.Sensor.by_name['bldg'].isOn()):
            sse.sse.send(type='indicator', id='building_pwr', status='on')
        else:
            sse.sse.send(type='indicator', id='building_pwr', status='off')

        if (device.Sensor.by_name['roofin'].isOn()):
            sse.sse.send(type='indicator', id='roof_pwr', status='on')
        else:
            sse.sse.send(type='indicator', id='roof_pwr', status='off')

        if (device.Sensor.by_name['mntin'].isOn()):
            sse.sse.send(type='indicator', id='mount_pwr', status='on')
        else:
            sse.sse.send(type='indicator', id='mount_pwr', status='off')


    def initialConnect(self):
        """Send intial connect message to browser"""
        self.sendNotice("Connected!<br/>Welcome to T-Rax!")
        self.updateBrowser()

    def startStop(self, app):
        """Process START/STOP button"""
        logging.info("Click: START/STOP from {}".format(flask.request.remote_addr))
        # TODO: put safety logic here!
        device.Control.by_name['fob'].toggle()
        return "Toggle"

    def roofPower(self, app):
        """Process Roof Power ON or OFF button"""
        # TODO: put safety logic here!
        if ('on' in flask.request.args):
            logging.info("Click: Roof Power ON from {}".format(flask.request.remote_addr))
            device.Control.by_name['roofout'].turnOn()
            return "Roof on OK"
        elif ('off' in flask.request.args):
            logging.info("Click: Roof Power OFF from {}".format(flask.request.remote_addr))
            device.Control.by_name['roofout'].turnOff()
            return "Roof on OK"
        else:
            logging.error("Click: Mount Power <invalid> from {} [request:{}]".format(
                flask.request.remote_addr, flask.request))
            return "Invalid roof request"

    def mountPower(self, app):
        """Porcess Mount Power ON or OFF button"""
        # TODO: put safety logic here!
        if ('on' in flask.request.args):
            logging.info("Click: Mount Power ON from {}".format(flask.request.remote_addr))
            device.Control.by_name['mntout'].turnOn()
            return "Mount on OK"
        elif ('off' in flask.request.args):
            logging.info("Click: Mount Power OFF from {}".format(flask.request.remote_addr))
            device.Control.by_name['mntout'].turnOff()
            return "Mount off OK"
        else:
            logging.error("Click: Mount Power <invalid> from {} [request:{}]".format(
                flask.request.remote_addr, flask.request))
            return "Invalid mount request"

    def emergencyStop(self, app):
        """Process EMERGENCY STOP button"""
        logging.info("User pressed EMERGENCY STOP from {}".format(flask.request.remote_addr))
        device.Control.by_name['roofout'].turnOff()
        self.sendNotice("EMERGENCY STOP!<br/>Turning off roof power")
        return "Emergency Stop OK"

    def test(self, app):
        """Test request components; can probably delete"""
        logging.info("User pressed Test from {}".format(flask.request.remote_addr))
        print("request: ", flask.request)
        print("  .path: ", flask.request.path)
        print("  .args: ", flask.request.args)
        return("Test OK")

# Instantiate a browser object
browser = Browser()
