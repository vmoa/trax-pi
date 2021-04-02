#!/usr/bin/python3
#
# Flask based web frontend for trax

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def top():
    return render_template('trax.html')
