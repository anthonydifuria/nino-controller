"""
Entry point CLI del mapping layer NINO (fase di test, senza GUI/installer).

Esempi:
    python -m nino_mapping_layer --list-ports
    python -m nino_mapping_layer --port /dev/cu.usbmodem14101 --output osc
    python -m nino_mapping_layer --port /dev/ttyACM0 --output midi
    python -m nino_mapping_layer --output osc          (rilevamento automatico)
"""

from __future__ import annotations

import argparse
import sys
import time

from .serial_reader import SerialReader, autodetect_port, list_serial_ports


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="NINO mapping layer: seriale -> OSC/MIDI")
    p.add_argument("--list-ports", action="store_true", help="elenca le porte seriali disponibili ed esce")
    p.add_argument("--port", help="porta seriale (se omessa, prova il rilevamento automatico)")
    p.add_argument("--baud", type=int, default=115200)
    p.add_argument("--output", choices=["osc", "midi"], default="osc")
    p.add_argument("-v", "--verbose", action="store_true", help="stampa a terminale i valori ricevuti (utile in fase di test)")

    osc = p.add_argument_group("OSC")
    osc.add_argument("--osc-send-host", default="127.0.0.1")
    osc.add_argument("--osc-send-port", type=int, default=9000)
    osc.add_argument("--osc-recv-port", type=int, default=9001)

    midi = p.add_argument_group("MIDI")
    midi.add_argument("--midi-port-name", default="NINO")
    midi.add_argument("--midi-channel", type=int, default=1, help="canale MIDI 1-16")

    return p


def main() -> None:
    args = build_parser().parse_args()

    if args.list_ports:
        candidates = list_serial_ports()
        if not candidates:
            print("Nessuna porta seriale trovata.")
            return
        for c in candidates:
            tag = "  <-- probabile Arduino" if c.likely_arduino else ""
            print(f"{c.device}  ({c.description}){tag}")
        return

    port = args.port or autodetect_port()
    if not port:
        print("Impossibile rilevare automaticamente la porta.")
        print("Usa --list-ports per vederle tutte, poi passa quella giusta con --port.")
        sys.exit(1)

    print(f"Connessione a {port} @ {args.baud} baud...")

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
        print(f"OSC: invio su {args.osc_send_host}:{args.osc_send_port}  indirizzo /nino/state")
        print(f"OSC: ricevo comandi LED sulla porta {args.osc_recv_port}  indirizzo /nino/led")
    else:
        from .midi_out import MIDIOutput

        output = MIDIOutput(port_name=args.midi_port_name, channel=args.midi_channel - 1)
        output.start()
        print(f"MIDI: porta virtuale '{args.midi_port_name}' creata, canale {args.midi_channel}")
        print("      (falla comparire come input MIDI nella tua DAW/software)")

    last_print = [0.0]

    def on_update(state):
        output.send_state(state.knobs, state.buttons)
        if args.verbose:
            now = time.monotonic()
            if now - last_print[0] > 0.2:  # non piu' di 5 stampe al secondo
                last_print[0] = now
                knobs_str = " ".join(f"{v:.2f}" for v in state.knobs)
                buttons_str = " ".join(str(v) for v in state.buttons)
                print(f"knob: {knobs_str}  |  pulsanti: {buttons_str}")

    reader.on_update = on_update
    reader.start()

    print("Attivo. Ctrl+C per fermare.")
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
