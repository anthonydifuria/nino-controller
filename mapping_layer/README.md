# NINO mapping layer

Python application that reads the NINO controller's serial data and
translates it into OSC and/or MIDI, so the knob and switch values become
usable in Max, Csound, SuperCollider, a DAW, or any software that speaks
OSC/MIDI.

## Installation

```
pip install -r requirements.txt
```

On macOS, if you have JACK installed (e.g. via Homebrew), installing
`python-rtmidi` can fail to compile (a known RtMidi bug with the JACK
backend on Darwin). If that happens, temporarily uninstall/disable JACK
before installing the requirements, or install `python-rtmidi` from a
precompiled wheel.

## Usage — serial -> OSC/MIDI bridge

```
python -m nino_mapping_layer --list-ports
python -m nino_mapping_layer --port /dev/cu.usbmodem14101 --output osc
python -m nino_mapping_layer --port /dev/ttyACM0 --output midi
python -m nino_mapping_layer --output osc          # automatic detection
```

See `python -m nino_mapping_layer --help` for all the options (OSC
host/ports, MIDI port name and channel, etc.).

## Usage — graphical panel

A stylized visual monitor of the panel (knobs, switches, status LEDs),
useful while testing/debugging even without a Max/OSC/MIDI patch open:

```
python -m nino_mapping_layer.gui
python -m nino_mapping_layer.gui --port /dev/cu.usbmodem14101
python -m nino_mapping_layer.gui --demo   # simulated values, no hardware
```

Requires tkinter (included with most standard Python installs; on some
Linux distributions it needs to be installed separately, e.g.
`sudo apt install python3-tk`).

## Structure

- `src/nino_mapping_layer/serial_reader.py` — serial read/parsing, automatic port detection.
- `src/nino_mapping_layer/osc_out.py` — OSC output/input.
- `src/nino_mapping_layer/midi_out.py` — MIDI output/input (virtual ports).
- `src/nino_mapping_layer/gui.py` — stylized graphical panel (monitor).
- `src/nino_mapping_layer/tray_app.py` — system tray icon (not implemented yet).
- `receivers/` — ready-made patches/examples for Csound, Faust, Max, SuperCollider that receive OSC/MIDI from this bridge.
- `build/` — scripts to build a standalone executable (macOS/Linux).
