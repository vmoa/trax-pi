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
        q = queue.Queue(maxsize=10)
        self.listeners.append(q)
        colorUp()
        return q

    def announce(self, msg):
        """Producers of queue messages announce() them here"""
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]

def format_sse(data: str, event=None) -> str:
    """Format `data` with optional `event` as a Server Side Event"""
    # Consider putting this in announce() above?
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg


# Silly loop to send something every second
def perSecond():
    msg = json.dumps( { 'tag':'notice', 'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") } )
    fmsg = format_sse(data=msg, event='innerHTML')
    #print(fmsg)
    announcer.announce(fmsg)
    threading.Timer(1.0, perSecond).start()  # Redispatch self


#
# Register URL callbacks
#

app = flask.Flask(__name__)

@app.route('/')
def top():
    return flask.render_template('trax.html')

# Sample SSE from the example; delete
@app.route('/ping')
def ping():
    msg = format_sse(data='pong')
    announcer.announce(msg=msg)
    return {}, 200

@app.route('/connect', methods=['GET'])
def connect():
    """
    This function starts in a different thread (I think) for each browser that connects,
    listens on the `announcer` queue and sends any messages that are posted on it.
    """

    def stream():
        """Loop on the `announcer` queue and "yields" any message posted to the queue."""
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return flask.Response(stream(), mimetype='text/event-stream')



# Instantiate the message queue
announcer = MessageAnnouncer()

back_on_green = "background-color:#00FF00; color:black"
yellow_on_red = "background-color:#FF0800; color:yellow"

def colorUp():
    print("colorUp")
    announcer.announce(format_sse(event='innerHTML', data=json.dumps( { 'tag':'notice', 'data':'Connected!' } )))
    announcer.announce(format_sse(event='bgcolor', data=json.dumps( { 'tag':'roof_position', 'data':'#00FF00' } )))
    announcer.announce(format_sse(event='fgcolor', data=json.dumps( { 'tag':'roof_position', 'data':'black' } )))
    announcer.announce(format_sse(event='innerHTML', data=json.dumps( { 'tag':'roof_position', 'data':'OPEN' } )))

    announcer.announce(format_sse(event='bgcolor', data=json.dumps( { 'tag':'mount_position', 'data':'#FF0800' } )))
    announcer.announce(format_sse(event='fgcolor', data=json.dumps( { 'tag':'mount_position', 'data':'yellow' } )))
    announcer.announce(format_sse(event='innerHTML', data=json.dumps( { 'tag':'mount_position', 'data':'PARKED' } )))

#threading.Timer(2.4, colorUp).start()  # Set colors

# Start it all up
perSecond()
