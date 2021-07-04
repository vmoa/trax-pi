# Instructions for Testing T-Rax

This is a test suite to run through to check for regressions when making
changes to the T-Rax code.  This requires the simulator and should work
with it either connected through the RJ11 cables or directly to the
controller board.
(Note that instrucitons were initally written using the sensor cables and
have not yet been tested with the direct controller connection.)

_TODO_: Add wiring details and options

Note on `BldgPwr`: The pushbutton switch is used when connecting directly to the controller board;
the toggle is used when connecting via sensor cables.

1. Start the version of trax.py you wish to test.
   * This might require stopping the auto-boot version:
      `sudo systemctl stop trax`
   * Simulator mode gives you more time to push buttons:
      `sudo ./trax.py --simulator`

1. Set all simulator buttons and switches to __OFF__ (including `BldgPwr` toggle)

1. Point a browser to http://trax (or via IP) and click the image to open T-Rax browser window
   * Notice briefly reads `Connecting to T-Rax`, then `Connected!` and a welcome and version number
   * Roof position reads `MIDWAY`
   * Mount position reads `UNKNOWN`
   * All status indicators read `OFF`
   * Time should be incrementing

1. Depress "Close" button
   * ROOF POSITION reads `CLOSED`

1. Turn `BldgPwr` __ON__
   * BUILDING PWR reads `ON`

1. Click MOUNT POSITION `UNKNOWN` indicator
   * Notice reads `Laser ON checking park`
   * Park LED (red) illuminates briefly
   * After _simulatordelay_ seconds, LED turns off and
     * Notice reads `Not parked`
     * MOUNT POSITION reads `NOT PARKED`
   * After _shortdelay_ seconds, MOUNT POSITION background changes to orange
   * After _longdelay_ seconds, MOUNT POSITION changes to `UNKNOWN`

1. Click MOUNT POSITION `UNKNOWN` indicator
   * Notice reads `Laser ON checking park`
   * Park LED (red) illuminates briefly
   * While LED illuminated, depress "Park" button (repeat if you missed it)
     * Park LED turns off
     * Notice reads `Parked`
     * MOUNT POSITION reads `PARKED`
   * After _shortdelay_ seconds, MOUNT POSITION background changes to pale yellow
   * After _longdelay_ seconds, MOUNT POSITION changes to `UNKNOWN`

1. Click `START STOP`
   * Noice reads `Cannot open roof: roof power is not on`

1. Click Roof Power `ON`
   * Notice reads `Turning on roof power`
   * RoofPwr LED (yellow) illuminates

1. Depress "RoofPwr" button
   * ROOF PWR reads `ON`

1. Click Mount Power `ON`
   * Notice reads `Cannot turn on mount: roof is not open`

1. Click `START STOP`
   * Notice reads `Cannot open roof: Weather not OK`

1. Depress "WX" button

1. Click `START STOP`
   * Notice flashes `Laser ON checking park` and Park LED (red) illuminates briefly
     (might be too fast to notice, but we tested above)
   * MOUNT POSITION reads `PARKED`
   * Noitce reads `Toggling fob (opening roof)`
   * FOB LED (blue) illuminates briefly
   * A lot of things happen at once -- repeat this step as necessary to confirm operation

1. Undpress "Close" button
   * ROOF POSITION reads `MIDWAY`

1. Click `START STOP`
   * Notice reads `Toggling fob (roof midway)`
   * FOB LED (blue) illuminates briefly

1. Click `EMERGENCY STOP`
   * Notice reads `EMERGENCY STOP! Turning off roof power`
   * RoofPwr LED (red) extinguishes

1. Undepress RoofPwr button
   * ROOF PWR reads `OFF`

1. Click Roof Power `ON`
   * Notice reads `Turning on roof power`
   * RoofPwr LED (red) extinguishes

1. Depress RoofPwr button
   * ROOF PWR reads `ON`

1. Depress "Open" button
   * ROOF POSITION reads `OPEN`

1. Click Mount Power `ON`
   * Notice reads `Turning on mount power`
   * MntPwr LED (green) illuminates

1. Depress "MntPwr" button
   * MOUNT PWR reads `ON`

1. Undepress "Park" button

1. Click `START STOP`
   * Notice reads `Laser ON checking park` and Park LED (red) illuminates
   * After _shortdelay_ seconds, MOUNT POSITION reads `NOT PARKED`
   * Notice reads `Cannot close roof: mount must be parked first`

1. Depress "Park" button

1. Click `START STOP`
   * Notice flashes `Laser ON checking park` and Park LED (red) illuminates briefly, MOUNT POSITION reads `PARKED`
   * Notice reads `Cannot close roof: mount power is on`

1. Click Mount Power `OFF`
   * MntPwr LED (yellow) turns off

1. Undepress "MntPwr" button

1. Click `START STOP`
   * Notice flashes `Laser ON checking park` and Park LED (red) illuminates briefly,  MOUNT POSITION reads `PARKED`
   * Noitce reads `Toggling fob (closing roof)`
   * FOB LED (blue) illuminates briefly

1. Undepress "Open" button
   * ROOF POSITION reads `MIDWAY`

1. Depress "Close" button
   * ROOF POSITION reads `CLOSED`

1. Click Roof Power `OFF`
   * RoofPwr LED extinguishes

1. Undepress "RoofPwr" button
   * ROOF PWR read `OFF`

1. Stop the test version of the software by typing Ctrl-C in the shell where you started it
   * Restart the auto-start version if stopped above: 
      `sudo systemctl start trax`
