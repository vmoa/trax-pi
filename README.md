# T-Rax Raspberry Pi Notes

This is the Raspberry Pi implementation of the T-Rax roof controller for the Robert Ferguson Observatory
[rfo.org](https://rfo.org).

This design is a logical follow-on to the [Arduino T-Rax](https://github.com/votmoa/trax-arduino) roof controller
created back in 2017 by Jim Finn, David Kensiski and Jay Pacheco.  The switch to the Raspberry Pi was driven by the desire
to implement an [ASCOM Alpaca](https://ascom-standards.org/Developer/Alpaca.htm) interface so that the roof
can be opened via automation through tools such as [ACP](https://acpx.dc3.com/).

Note that version 1 will simply replace the Arduino functionality.  The ASCOM Alpaca interface will not be
available unitl version 2.

# Table of Contents

1. [Theory of Operation](#general-theory-of-operation)
1. [Detailed Operation](#detailed-operation)
1. [Future Plans](#future-plans)
1. [Installation](#installation)
1. [GPIO Notes](#gpio-notes)


# General Theory of Operation

The server is written in Python 3 and utilizes only two external libraries:
[GPI Zero](https://gpiozero.readthedocs.io/en/stable/) to control the Raspberry Pi GPIO ports, and
[Flask](https://flask.palletsprojects.com/en/1.1.x/) to manage the web interface.  (Though Flask
has a bunch of prerequisites that also need to be loaded.)
The Browser panel is written in [HTML](https://www.w3schools.com/html/default.asp) using
Cascading Style Sheets ([CSS](https://www.w3schools.com/css/default.asp)) to control the apperance of the page, and
[Javascript](https://www.w3schools.com/js/default.asp) to handle communication and control the modal dialogs.

The overall software design is driven through interrupts -- there is no "main loop" as there was in the Arduino.
On start, the server sets  up logging, initializes each of the
GPIO pins, registers the web interface callbacks, then hands operation over to Flask to listen for incoming requests.
There are three flavors of threads:

* Hardware input state changes trigger GPI Zero callbacks that execute in individual threads.
* Browser reqeusts trigger Flask actions that execute in separte threads.
* Finally an "update" thread executes every second to perform household chores.

There is a static html launcher page that is currently served directly by Apache.  This sets browser window size
(I don't think a window can reliably change its size once launched) and points it at http://trax:5000 which is where
trax.py is listening (by way of Flask).  This sends a template web page to paint the browser.  Once painted,
Javascript in the browser connects back to trax and and set up a server-sent events channel
([SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events))
so the server can pro-actively update the browser.  Browser javascript listens on this channel and paints the
display appropriately.  Browser buttons trigger async HTTP calls to varioius
trax URIs that perform an appropriate action, which in turn triggers an SSE response.

Breaking this down, the connection flow is as follows:

1. User connects to http://trax and clicks the "Launch" button
1. Browser launches the T-Rax browser window pointing to http://trax:5000
1. Server sends static HTML, CSS and Javascript to paint the browser
1. After panting, browser javascript connects to http://trax:5000/connect to set up SSE channel

Then in normal operation:

* Server sends events via SSE when something changes
  * Browser executes javascript to handle the event
* Browser buttons send HTTP asynchronous requests to http://trax:5000/{whatever} to trigger actions
  * Sever performs the actions and responsds via SSE

The update thread is simply a thread that runs on startup to perform household chores and proactively update the
browser.  It then reschedules itself to run again one second later.  This thread updates the clock on the T-Rax
page to act as a hardbeat to confirm the server/browser SSE channel is active

# Detailed Operation

* Hardware Interrupt driven
* Each input has a callback
* Wrapper around gpiozero to track output changes

* Browser
* calls links that trigger functions to perform operations
* Check safety logic, trigger outputs
* Send SSE
* Javascript paints browser

* Buttons are (actually `<DIV>` onClick actions)

* Update thread 

# Hardware Design

* Raspberry Pi 3+
* Outputs: GPIO --> 6-pin header --> Relay board --> Relays supply 12v signal to (all?) devices (fob), roofPower, mountPower, laser
* Inputs: 8-pin header --> low pass RC filter, current limiter --> optocoupler 4N25 --> GPIO
* BldgPower: 2-pin header --> (same path) except that return is direct, not grounded
* Heartbeat: GPIO --> current limiter --> Green LED
* Power: 3.3v --> current limiter --> Red LED

# Future Plans

- [ ] Use md5 hashed password instead of hard coding
- [ ] Implement all logging using Flask's logging wrapper (evaluate how useful)
- [ ] Switch from Flask web server to Apache/WCGI
- [ ] Implement ASCOM/Alpaca
- [ ] Make multi-user (eg: for emergency override, notifications)


# Installation

* Python modules?
* Clone code (TBD)
* Configure systemd (TBD)
* Configure Apache

```
sudo apt-get install apach2
sudo a2enmod cgi
sudo systemctl restart apache2
```

# GPIO Notes

General Purpose Input/Output

![GPIO Pinout Diagram](GPIO-Pinout-Diagram-2.png)

## Input GPIO ports (sensors)

* GPIO4: weatherOK = newSensor(pin=4);
* GPIO17: bldgPowerIn = newSensor(pin=17);
* GPIO27: roofPowerIn = newSensor(pin=27);
* GPIO22: mountPowerIn = newSensor(pin=22);
* GPIO23: roofOpen = newSensor(pin=23);
* GPIO24: roofClosed = newSensor(pin=24);
* GPIO25: mountParked = newSensor(pin=25);

## Output GPIO ports (controls)

* GPIO5: roofPowerOut = newControl(pin=5)
* GPIO6: mountPowerOut = newControl(pin=6)
* GPIO26: fobOutput = newControl(pin=26)
* GPIO13: heartLed = newControl(pin=13)
* GPIO16: laserPowerOut = newControl(pin=16)

| GPIO | Function | T-Rax |
| ---- | -------- | ----- |
| 2    | I2C      | LCD   |
| 3    | I2C      | LCD   |
| 4    |          | weatherOK |
| 17   | SPI1     | bldgPowerIn |
| 27   |          | roofPowerIn |
| 22   |          | mountPowerIn |
| 10   | SPI0     |  |
| 9    | SPI0     |  |
| 11   | SPI0     |  |
| 0    | I2C      | LCD   |
| 5   |           | roofPowerOut |
| 6   |           | mountPowerOut |
| 13   | PWM      | Heart LED |
| 19   | PWM,SPI1 |  |
| 26   |          | fobOutput |
| | | |
| 14   | Serial   |  |
| 15   | Serial   |  |
| 18   | PWM,SPI1 |  |
| 23   |          | roofOpen |
| 24   |          | roofClosed |
| 25   |          | mountParked |
| 8    | SPI0     |  |
| 7    | SPI0     |  |
| 1    | I2C      | LCD   |
| 12   | PWM      |  |
| 16   | SPI1     | laserPowerOut |
| 20   | SPI1     |  |
| 21   | SPI1     |  |
