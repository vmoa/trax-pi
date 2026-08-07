# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

1. Don't assume. Don't hide confusion. Surface tradeoffs.

2. Minimum code that solves the problem. Nothing speculative.

3. Touch only what you must. Clean up only your own mess.

4. Define success criteria. Loop until verified.

## What This Is

T-Rax is a Raspberry Pi Flask server that controls the roll-off roof at the Robert Ferguson Observatory (RFO). It manages GPIO-driven hardware (roof motor, mount power, weather sensor, park detector) and serves a browser UI with Server-Sent Events (SSE) for live updates. See `README.md` for hardware design details.

No test suite — testing is manual via the Flask debug server or `--test-mode`.

## Running Locally (non-Pi)

```bash
pip install flask   # gpiozero is Pi-only; test-mode stubs it out
python3 trax.py --test-mode   # simulates GPIO; safe on any machine
python3 trax.py --debug       # verbose logging
```

On a real Pi, it runs as a systemd service (`trax.service`). See `INSTALL.md` for setup and `doc/TestPlan.md` for the manual test plan.

## Architecture

The app is fully interrupt-driven — no main polling loop. GPIO state changes and browser HTTP requests each execute in separate threads. A 1 Hz update thread handles housekeeping (clock updates, heartbeat LED).

- **`trax.py`** — entry point; acquires lock file (`/tmp/trax.lock` — prevents duplicate instances), configures logging, starts the update thread, then hands off to Flask on port 5000
- **`device.py`** — GPIO abstraction via `gpiozero`; `newSensor()` / `newControl()` wrappers; safety interlock logic (weather, building power, park detector)
- **`browser.py`** — Flask route handlers; each UI button maps to a URI that checks safety interlocks, triggers GPIO outputs, then fires an SSE event
- **`alpaca.py`** — ASCOM Alpaca bridge for dome/shutter control; exposes `OpenShutter`/`CloseShutter`, `ShutterStatus`, discovery and status endpoints, and reuses the browser safety logic for roof motion
- **`sse.py`** — Server-Sent Events channel; browser connects to `/connect` and receives push updates; Flask handler threads write events that the SSE thread broadcasts
- **`test_mode.py`** — stubs for `gpiozero` that allow running on non-Pi hardware
- **`util.py`** — shared helpers

## GPIO Pin Assignments

**Inputs (sensors):** `weatherOK`=4, `bldgPowerIn`=17, `roofPowerIn`=27, `mountPowerIn`=22, `roofOpen`=23, `roofClosed`=24, `mountParked`=25

**Outputs (controls):** `roofPowerOut`=5, `mountPowerOut`=6, `fobOutput`=26, `heartLed`=13, `laserPowerOut`=16

## Production Deployment

Apache serves the static launcher page from `/var/www/html/`; trax.py runs on port 5000 via systemd. Logs to `/var/log/trax.log`.
