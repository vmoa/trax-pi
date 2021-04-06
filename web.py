#!/usr/bin/python3 URL callbacks
#
# Flask based web frontend for trax

# One shot:
# FLASK_APP=web.py flask run --host=0.0.0.0 &
# Auto-reloading:
# FLASK_ENV=development FLASK_APP=web.py flask run --host=0.0.0.0 &


import datetime
import json
import queue
import signal
import sys
import threading

import flask

# Message queue cobbled from https://maxhalford.github.io/blog/flask-sse-no-deps/

class MessageAnnouncer:
    """Implement a queue for messages to be sent to connected browsers"""

    def __init__(self):
        self.listeners = []

    def listen(self):
        """Consumers of the queue listen() for queue updates"""
        q = queue.Queue(maxsize=32)
        self.listeners.append(q)
        threading.Timer(1.0, colorUp).start()  # Dispatch
        return q

    def send(self, msg='', id='', type='', data=''):
        """Producers of queue messages send() them here"""
        if (not msg):
            msg = format_sse(data=json.dumps( { 'id':id, 'data':data } ), event=type)
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]

    def stream(self):
        """Loops on the `browser` queue and "yields" any message posted to the queue."""
        messages = self.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            # print("Yielding", msg)
            yield msg

def format_sse(data: str, event=None) -> str:
    """Format `data` with optional `event` as a Server Side Event"""
    # Consider putting this in send() above?
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg


# Silly loop to send something every second
def perSecond():
    browser.send(id='notice', type='innerHTML', data=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    threading.Timer(1.0, perSecond).start()  # Redispatch self

def fizzbin(id, type, data):
    msg = format_sse(data=json.dumps( { 'id':id, 'data':data } ), event=type)
    return msg

#
# Register URL callbacks
#

# Instantiate the message queue
browser = MessageAnnouncer()

app = flask.Flask(__name__)

@app.route('/')
def top():
    return flask.render_template('trax.html')

# Sample SSE from the example; delete
@app.route('/ping')
def ping():
    msg = format_sse(data='pong')
    browser.send(msg=msg)
    return {}, 200

@app.route('/connect', methods=['GET'])
def connect():
    """
    This function starts in a different thread (I think) for each browser that connects,
    listens on the `browser` queue and sends any messages that are posted to it.
    """
    return flask.Response(browser.stream(), mimetype='text/event-stream')



back_on_green = "background-color:#00FF00; color:black"
yellow_on_red = "background-color:#FF0800; color:yellow"
color = { 'black':'black', 'yellow':'yellow', 'green':'#00FF00', 'red':'#FF0800' }

def colorUp():
    print("colorUp")
    browser.send(id='notice', type='innerHTML', data='Connected!')
    browser.send(id='roof_position', type='bgcolor', data=color['green'])
    browser.send(id='roof_position', type='fgcolor', data=color['black'])
    browser.send(id='roof_position', type='innerHTML', data='OPEN')

    browser.send(id='mount_position', type='bgcolor', data=color['red'])
    browser.send(id='mount_position', type='fgcolor', data=color['yellow'])
    browser.send(id='mount_position', type='innerHTML', data='PARKED')

# Start it all up
perSecond()
