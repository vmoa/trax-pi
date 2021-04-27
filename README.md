# T-Rax Raspberry Pi Notes

This is the Raspberry Pi implementation of the T-Rax roof controller for the Robert Ferguson Observatory
[rfo.org](https://rfo.org).

This design is a logical follow-on to the [Arduino T-Rax](https://github.com/votmoa/trax-arduino) roof controller
created back in 2017 by Jim Finn, David Kensiski and Jay Pacheco.  The switch to the Raspberry Pi was driven by the desire
to implement an [ASCOM Alpaca](https://ascom-standards.org/Developer/Alpaca.htm) interface so that the roof
can be opened via automation through tools such as [ACP](https://acpx.dc3.com/).

Note that version 1 will simply replace the Arduino functionality.  The ASCOM Alpaca interface will not be
available unitl version 2.

# Theory of Operation

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
Hardware state changes trigger callbacks that execute in separate threads, and browser reqeusts trigger Flask
actions that execute in separte threads.  Finally an "update" thread executes every second to perform household chores.


Hardware Interrupt driven
Each input has a callback
Wrapper around gpiozero to track output changes

Static html launcher Apache page
Sets browser window size (can't figure out how else to do it) and calls trax:5000 to paint the canvas
On load, browser calls /connect to set up a SSE channel from server
Listens for events on channel and paints display appropriately
Buttons trigger async http calls to varioius uris that perform safety checks, actions, and send SSE in response

Update thread that rescheules itself every second to perform household chores and proactively update browser.
Clock is a heartbeat that confirms the server/browser SSE channel is active

# Detailed Operation

Browser
 calls links that trigger functions to perform operations
  Check safety logic, trigger outputs
  Send 
Javascript 

Update thread 


# Future Plans

* Use md5 hashed password instead of hard coding
* Implement all logging using Flask's logging wrapper (evaluate how useful)
* Switch from Flask web server to Apache/WCGI
* Implement ASCOM/Alpaca
* Make multi-user (eg: for emergency override, notifications)


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

# GPIO -- General Purpose Input/Output

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
