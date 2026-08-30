# NINO — Node Interface for Networked Output

Project for the NINO hardware controller (Arduino) connected to audio synthesis/programming environments.

## Background

The project started by prototyping directly against the serial port: `prototyping/` holds a Max patch, a SuperCollider script and a Csound orchestra that each open the NINO's serial connection themselves and parse the 12-field line the Arduino sends (6 knobs + 6 buttons), plus the ping/timeout housekeeping that keeps the connection alive. `prototyping/csound/NINO.csd` is the most explicit example: it implements the whole parser as a Csound UDO, byte by byte.

Every new environment meant rewriting that same logic from scratch, in whatever way that language talks to a serial port — a different API, different string/byte handling, the same bugs to work out again. `mapping_layer/` exists to do that work exactly once: a small Python bridge reads the serial port and re-broadcasts the state as OSC and/or MIDI, two protocols almost every audio environment already understands natively.

The payoff shows up in `mapping_layer/receivers/`: compare `csoundOSC_NINO.csd` there (a dozen lines, just an `OSClisten`) to `prototyping/csound/NINO.csd` (the full serial parser) — once the bridge is running, supporting a new environment means "listen for OSC or MIDI", not "parse the serial protocol again". `prototyping/` stays in the repo as the earlier, dependency-free approach: useful if you want to wire one specific environment straight to the serial port without running the Python bridge.

## Graphical interface (demo)

Stylized preview of the Python graphical panel (`mapping_layer`, demo mode, simulated values):

![Preview of the NINO graphical panel](docs/nino_gui_preview.png)

## Structure

- `firmware/` — Arduino sketch for the NINO board.
- `docs/diagrams/` — conceptual and physical diagrams of the system.
- `mapping_layer/` — Python application: reads the serial data and translates it into OSC/MIDI.
- `prototyping/` — standalone native implementations (Max, Csound, SuperCollider) that talk directly to the serial port.

## Requirements

- Arduino IDE (for the firmware in `firmware/`)
- Python 3.9+ (for `mapping_layer/`, see its README)

## Credits

Developed by Anthony Di Furia during the electroacoustic music courses
with maestro Alessandro Fiordelmondo at the Conservatorio di Cesena.
