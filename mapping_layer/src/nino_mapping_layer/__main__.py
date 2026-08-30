"""
CLI entry point for the NINO mapping layer (testing phase, no GUI/installer).

Examples:
    python -m nino_mapping_layer --list-ports
    python -m nino_mapping_layer --port /dev/cu.usbmodem14101 --output osc
    python -m nino_mapping_layer --port /dev/ttyACM0 --output midi
    python -m nino_mapping_layer --output osc          (automatic detection)
"""

from __future__ import annotations

import argparse
import sys
import time

from .serial_reader import SerialReader, autodetect_port, list_serial_ports


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="NINO mapping layer: serial -> OSC/MIDI")
    p.add_argument("--list-ports", action="store_true", help="list the available serial ports and exit")
    p.add_argument("--port", help="serial port (if omitted, tries automatic detection)")
    p.add_argument("--baud", type=int, default=115200)
    p.add_argument("--output", choices=["osc", "midi"], default="osc")
    p.add_argument("-v", "--verbose", action="store_true", help="print received values to the terminal (useful while testing)")

    osc = p.add_argument_group("OSC")
    osc.add_argument("--osc-send-host", default="127.0.0.1")
    osc.add_argument("--osc-send-port", type=int, default=9000)
    osc.add_argument("--osc-recv-port", type=int, default=9001)

    midi = p.add_argument_group("MIDI")
    midi.add_argument("--midi-port-name", default="NINO")
    midi.add_argument("--midi-channel", type=int, default=1, help="MIDI channel 1-16")

    return p


def main() -> None:
    args = build_parser().parse_args()

    if args.list_ports:
        candidates = list_serial_ports()
        if not candidates:
            print("No serial ports found.")
            return
        for c in candidates:
            tag = "  <-- likely Arduino" if c.likely_arduino else ""
            print(f"{c.device}  ({c.description}){tag}")
        return

    port = args.port or autodetect_port()
    if not port:
        print("Could not automatically detect the port.")
        print("Use --list-ports to see them all, then pass the right one with --port.")
        sys.exit(1)

    print(f"Connecting to {port} @ {args.baud} baud...")

    reader = SerialReader(port, baudrate=args.baud)

    if args.output == "osc":
        from .osc_out import OSCOutput

        output = OSCOutput(
            send_host=args.osc_send_host,
            send_port=args.osc_send_port,
            recv_port=args.osc_recv_port,
            on_led_command=reader.send_led,
        )
        output.start()
        print(f"OSC: sending to {args.osc_send_host}:{args.osc_send_port}  address /nino/state")
        print(f"OSC: receiving LED commands on port {args.osc_recv_port}  address /nino/led")
    else:
        from .midi_out import MIDIOutput

        output = MIDIOutput(
            port_name=args.midi_port_name,
            channel=args.midi_channel - 1,
            on_led_command=reader.send_led,
        )
        output.start()
        print(f"MIDI: virtual port '{args.midi_port_name}' created (output), channel {args.midi_channel}")
        print(f"MIDI: virtual port '{output.led_port_name}' created (input) for the LED, CC {output.led_cc}")
        print("      (make it show up as a MIDI input in your DAW/software)")

    last_print = [0.0]

    def on_update(state):
        output.send_state(state.knobs, state.buttons)
        if args.verbose:
            now = time.monotonic()
            if now - last_print[0] > 0.2:  # no more than 5 prints per second
                last_print[0] = now
                knobs_str = " ".join(f"{v:.2f}" for v in state.knobs)
                buttons_str = " ".join(str(v) for v in state.buttons)
                print(f"knob: {knobs_str}  |  buttons: {buttons_str}")

    reader.on_update = on_update
    reader.start()

    print("Running. Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        reader.stop()
        output.stop()


if __name__ == "__main__":
    main()
