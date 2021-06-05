#!/usr/bin/python3 URL callbacks
#
# Message queue implementation of Server Send Events (SSE)
# cobbled from https://maxhalford.github.io/blog/flask-sse-no-deps/

import datetime
import json
import queue
import signal
import sys
import threading

import flask


class MessageAnnouncer:
    """Implement a queue and dispatch SSE events to connected browsers"""

    def __init__(self):
        self.listeners = []

    def listen(self):
        """Consumers of the queue listen() for queue updates"""
        q = queue.Queue(maxsize=32)
        self.listeners.append(q)
        return q

    def send(self, **kwargs):
        """Producers of queue messages send() them here"""
        if ('msg' in kwargs):
            msg = kwargs['msg']
        else:
            msg = self.format_sse(event=kwargs['type'], data=json.dumps(kwargs))
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

    def format_sse(self, data: str, event=None) -> str:
        """Format `data` with optional `event` as a Server Side Event"""
        # Consider putting this in send() above?
        msg = f'data: {data}\n\n'
        if event is not None:
            msg = f'event: {event}\n{msg}'
        return msg

    def count(self):
        """Return the number of active connections"""
        return len(self.listeners)

# Instantiate the queue
sse = MessageAnnouncer()
