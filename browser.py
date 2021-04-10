# Interactive browser callbacks
#
# Callbacks are registered in trax.py because it just makes flask cleaner

import threading

import device
import sse


class Browser:

    def sendNotice(self, msg):
        """Update the notice area on the browser"""
        sse.sse.send(id='notice', type='innerHTML', data=msg)


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


# Instantiate a browser object
browser = Browser()
