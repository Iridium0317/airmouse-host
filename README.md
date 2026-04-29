# AirMouse Host

Mac-side BLE host for the [AirMouse](https://github.com/Iridium0317/AirMouse) firmware. Receives gyroscope-derived cursor deltas over BLE and translates them into macOS cursor movement.

## Architecture

```text
Nano 33 BLE Sense Rev2         Mac
──────────────────────         ───────────────────
BMI270 IMU (200Hz)             bleak (BLE central)
↓                              ↓
LPF / deadband / gain          parse 4-byte packet
↓                              ↓
int16 dx / dy packed           pynput.mouse.move()
↓
ArduinoBLE NUS notify ──BLE──>
```

## Protocol

Connects to a BLE peripheral named AirMouse exposing the Nordic UART Service. Subscribes to the TX characteristic (`6E400003-B5A3-F393-E0A9-E50E24DCCA9E`) and decodes 4-byte notifications:

| Byte | Field | Type      |
| ---- | ----- | --------- |
| 0–1  | dx    | int16, LE |
| 2–3  | dy    | int16, LE |

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install bleak pynput
python airmouse_host.py
```

Requires macOS Bluetooth and Accessibility permissions for the terminal.

## Status

Working end-to-end: cursor moves in response to board orientation changes. Tuning IMU calibration, filtering, and gain mapping is ongoing.
