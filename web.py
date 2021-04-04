#!/usr/bin/python3
#
# Flask based web frontend for trax

from flask import Flask, render_template
app = Flask(__name__)

import queue
from time import sleep
import signal

@app.route('/')
def top():
    return render_template('trax.html')

# Cobbled from https://maxhalford.github.io/blog/flask-sse-no-deps/
class MessageAnnouncer:

    def __init__(self):
        self.listeners = []

    def listen(self):
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        return q

    def announce(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]

announcer = MessageAnnouncer()

def format_sse(data: str, event=None) -> str:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg

@app.route('/ping')
def ping():
    msg = format_sse(data='pong')
    announcer.announce(msg=msg)
    return {}, 200

@app.route('/connect', methods=['GET'])
def connect():

    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return flask.Response(stream(), mimetype='text/event-stream')



notice = "Connecting to T-Rax...<br/>\
1 3 5 7 9 1 3 5 7 9 1 <br/>\
&nbsp;2 4 6 8 0 2 4 6 8 0 2<br/>"

back_on_green = "background-color:#00FF00; color:black"
yellow_on_red = "background-color:#FF0800; color:yellow"

announcer.announce(msg="Connected")

def alarmHandler(signum,frame):
    announcer.announce(msg="Connected")

signal.signal(signal.SIGALRM, alarmHandler)
signal.alarm(heartInterval)
while True:
    signal.pause()
    signal.alarm(1)
