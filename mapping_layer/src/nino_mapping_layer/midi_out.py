"""
Uscita MIDI classica per il mapping layer NINO.

Crea una porta MIDI virtuale (visibile a DAW e altri software su Mac e Linux
tramite CoreMIDI/ALSA) e manda:
    - i 6 knob come Control Change continui (0-127)
    - i 6 pulsanti come Control Change binari (0 o 127)

Manda un messaggio solo quando il valore 7-bit cambia davvero, per non
intasare inutilmente il canale MIDI.
"""

from __future__ import annotations

from typing import List, Optional

import mido


class MIDIOutput:
    def __init__(
        self,
        port_name: str = "NINO",
        channel: int = 0,
        knob_ccs: Optional[List[int]] = None,
        button_ccs: Optional[List[int]] = None,
    ):
        self.port_name = port_name
        self.channel = channel
        self.knob_ccs = knob_ccs or [20, 21, 22, 23, 24, 25]
        self.button_ccs = button_ccs or [30, 31, 32, 33, 34, 35]

        self._port: Optional["mido.ports.BaseOutput"] = None
        self._last_knob_7bit: List[Optional[int]] = [None] * 6
        self._last_button_val: List[Optional[int]] = [None] * 6

    def start(self) -> None:
        # virtual=True crea una porta MIDI nuova invece di collegarsi a una
        # esistente: e' quella che poi scegli come "input" nella tua DAW.
        self._port = mido.open_output(self.port_name, virtual=True)

    def stop(self) -> None:
        if self._port:
            self._port.close()

    def send_state(self, knobs, buttons) -> None:
        for i, v in enumerate(knobs):
            v7 = max(0, min(127, int(round(v * 127))))
            if v7 != self._last_knob_7bit[i]:
                self._last_knob_7bit[i] = v7
                self._port.send(
                    mido.Message("control_change", channel=self.channel, control=self.knob_ccs[i], value=v7)
                )

        for i, v in enumerate(buttons):
            v7 = 127 if v else 0
            if v7 != self._last_button_val[i]:
                self._last_button_val[i] = v7
                self._port.send(
                    mido.Message("control_change", channel=self.channel, control=self.button_ccs[i], value=v7)
                )
