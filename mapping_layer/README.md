# NINO mapping layer

Python application that reads the NINO controller's serial data and
translates it into OSC and/or MIDI, so the knob and switch values become
usable in Max, Csound, SuperCollider, a DAW, or any software that speaks
OSC/MIDI.

## Quick start

Every command below assumes the repo lives at
`~/Documents/GitHub/nino-controller` — adjust the first `cd` if yours is
somewhere else. Two folders matter and it's easy to mix them up:
`mapping_layer/` (has `requirements.txt`) and `mapping_layer/src/` (has the
`nino_mapping_layer` package you actually run).

```bash
# 1. Go to mapping_layer/ — this is where requirements.txt lives
cd ~/Documents/GitHub/nino-controller/mapping_layer

# 2. Create and activate a virtual environment (recommended, keeps
#    dependencies isolated from the rest of your system)
python3 -m venv venv
source venv/bin/activate

# 3. Install the dependencies — run from mapping_layer/, NOT from src/
python3 -m pip install -r requirements.txt

# 4. Move into src/ — the nino_mapping_layer package lives here, and every
#    `python -m nino_mapping_layer...` command must be run from inside it
cd src

# 5. Plug in the Arduino, then find its serial port
python3 -m nino_mapping_layer --list-ports

# 6. Start the bridge (replace the port with the one --list-ports gave you)
python3 -m nino_mapping_layer --port /dev/cu.usbmodemXXXXX --output osc
```

`nino_mapping_layer` is a plain Python package under `src/`, not installed
system-wide — that's why `cd src` matters, and why it's run with
`python3 -m nino_mapping_layer` rather than `python3 some_file.py`.

Each new terminal session needs `source venv/bin/activate` again (run from
`mapping_layer/`, where the `venv` folder lives) before step 4 onward.

On macOS, if you have JACK installed (e.g. via Homebrew), installing
`python-rtmidi` from `requirements.txt` can fail to compile (a known RtMidi
bug with the JACK backend on Darwin). If that happens, temporarily
uninstall/disable JACK before installing the requirements, or install
`python-rtmidi` from a precompiled wheel.

## More usage examples

```
python -m nino_mapping_layer --port /dev/ttyACM0 --output midi   # MIDI instead of OSC
python -m nino_mapping_layer --output osc                        # skip --port, try automatic detection
```

See `python -m nino_mapping_layer --help` for all the options (OSC
host/ports, MIDI port name and channel, etc.).

## Graphical panel

A stylized visual monitor of the panel (knobs, switches, status LEDs),
useful while testing/debugging even without a Max/OSC/MIDI patch open. Run
it from `mapping_layer/src` just like the bridge above:

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
