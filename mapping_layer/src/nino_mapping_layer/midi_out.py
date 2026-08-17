"""
Uscita e ingresso MIDI classico per il mapping layer NINO.

Usa DUE porte MIDI virtuali distinte, per non confondere le due direzioni:
    - "NINO"      (uscita dal bridge)  -> gli altri software la vedono come INPUT,
                    riceve i 6 knob (CC 20-25) e i 6 pulsanti (CC 30-35)
    - "NINO LED"  (ingresso al bridge) -> gli altri software la vedono come OUTPUT,
                    ci mandano CC 40 per pilotare il LED sul pin 5 (0-127 -> 0-255)

Manda un messaggio in uscita solo quando il valore 7-bit cambia davvero, per
non intasare inutilmente il canale MIDI.
"""

from __future__ import annotations

import threading
from typing import Callable, List, Optional

import mido


class MIDIOutput:
    def __init__(
        self,
        port_name: str = "NINO",
        led_port_name: str = "NINO LED",
        channel: int = 0,
        knob_ccs: Optional[List[int]] = None,
        button_ccs: Optional[List[int]] = None,
        led_cc: int = 40,
        on_led_command: Optional[Callable[[int, int], None]] = None,
    ):
        self.port_name = port_name
        self.led_port_name = led_port_name
        self.channel = channel
        self.knob_ccs = knob_ccs or [20, 21, 22, 23, 24, 25]
        self.button_ccs = button_ccs or [30, 31, 32, 33, 34, 35]
        self.led_cc = led_cc
        self._on_led_command = on_led_command

        self._out_port: Optional["mido.ports.BaseOutput"] = None
        self._in_port: Optional["mido.ports.BaseInput"] = None
        self._in_thread: Optional[threading.Thread] = None
        self._stop = threading.Event()

        self._last_knob_7bit: List[Optional[int]] = [None] * 6
        self._last_button_val: List[Optional[int]] = [None] * 6

    def start(self) -> None:
        # porta virtuale in uscita: gli altri software la vedono come INPUT
        self._out_port = mido.open_output(self.port_name, virtual=True)
        # porta virtuale in ingresso: gli altri software la vedono come OUTPUT
        self._in_port = mido.open_input(self.led_port_name, virtual=True)

        self._stop.clear()
        self._in_thread = threading.Thread(target=self._listen_led, daemon=True)
        self._in_thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._in_port:
            self._in_port.close()
        if self._out_port:
            self._out_port.close()

    def send_state(self, knobs, buttons) -> None:
        for i, v in enumerate(knobs):
            v7 = max(0, min(127, int(round(v * 127))))
            if v7 != self._last_knob_7bit[i]:
                self._last_knob_7bit[i] = v7
                self._out_port.send(
                    mido.Message("control_change", channel=self.channel, control=self.knob_ccs[i], value=v7)
                )

        for i, v in enumerate(buttons):
            v7 = 127 if v else 0
            if v7 != self._last_button_val[i]:
                self._last_button_val[i] = v7
                self._out_port.send(
                    mido.Message("control_change", channel=self.channel, control=self.button_ccs[i], value=v7)
                )

    def _listen_led(self) -> None:
        for msg in self._in_port:
            if self._stop.is_set():
                break
            if msg.type == "control_change" and msg.control == self.led_cc:
                value = max(0, min(255, int(round(msg.value * (255 / 127)))))
                if self._on_led_command:
                    self._on_led_command(0, value)