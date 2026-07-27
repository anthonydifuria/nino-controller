"""
Lettura e parsing del protocollo seriale del controller NINO, piu'
rilevamento automatico della porta USB (Mac e Linux).

Protocollo atteso dall'Arduino (vedi firmware/NINO_CONTROLLER):
    - riga di testo terminata da \\n, 12 campi separati da spazi:
      6 float (0.0-1.0, i potenziometri) + 6 int (0/1, i pulsanti)
    - risponde al ping (byte 200) restando "connesso"
    - accetta comandi LED come coppia di byte: (id, valore 0-255)
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Callable, List, Optional

import serial
from serial.tools import list_ports

# VID (vendor id) USB piu' comuni per Arduino e cloni compatibili.
# Il rilevamento resta euristico: molti cloni economici usano chip
# USB-seriale generici, non necessariamente un VID "Arduino" ufficiale.
KNOWN_VIDS = {
    0x2341,  # Arduino SA
    0x2A03,  # Arduino.org
    0x1A86,  # QinHeng Electronics (CH340, cloni economici)
    0x0403,  # FTDI
    0x10C4,  # Silicon Labs (CP210x)
}

KEYWORD_HINTS = ("arduino", "usbmodem", "usbserial", "ch340", "cp210", "wchusbserial")


@dataclass
class PortCandidate:
    device: str
    description: str
    likely_arduino: bool


def list_serial_ports() -> List[PortCandidate]:
    """Elenca le porte seriali disponibili, segnalando quelle che sembrano un Arduino."""
    candidates = []
    for p in list_ports.comports():
        likely = p.vid in KNOWN_VIDS
        desc = (p.description or "").lower()
        if any(k in desc for k in KEYWORD_HINTS):
            likely = True
        if any(k in p.device.lower() for k in KEYWORD_HINTS):
            likely = True
        candidates.append(PortCandidate(device=p.device, description=p.description or "", likely_arduino=likely))
    return candidates


def autodetect_port() -> Optional[str]:
    """
    Ritorna la porta se ce n'e' esattamente una che sembra un Arduino.
    Se sono zero o piu' di una, ritorna None (serve una scelta esplicita
    con --port, tramite l'elenco di --list-ports).
    """
    likely = [c for c in list_serial_ports() if c.likely_arduino]
    if len(likely) == 1:
        return likely[0].device
    return None


@dataclass
class NinoState:
    knobs: List[float] = field(default_factory=lambda: [0.0] * 6)
    buttons: List[int] = field(default_factory=lambda: [0] * 6)


class SerialReader:
    """
    Gestisce la connessione seriale con il controller NINO:
      - manda un ping periodico (byte 200) per tenere viva la connessione
      - legge il flusso ascii e lo spacchetta in 6 knob + 6 pulsanti
      - invoca on_update(state) ogni volta che arriva una riga completa
      - espone send_led(id, valore) per pilotare i LED sull'Arduino
    """

    PING_BYTE = 200
    PING_INTERVAL = 0.5  # secondi; deve restare sotto i 2s previsti dal firmware

    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        on_update: Optional[Callable[[NinoState], None]] = None,
    ):
        self.port_name = port
        self.baudrate = baudrate
        self.on_update = on_update
        self.state = NinoState()

        self._ser: Optional[serial.Serial] = None
        self._stop = threading.Event()
        self._threads: List[threading.Thread] = []

    def start(self) -> None:
        self._ser = serial.Serial(self.port_name, self.baudrate, timeout=1)
        self._stop.clear()

        t_ping = threading.Thread(target=self._ping_loop, daemon=True)
        t_read = threading.Thread(target=self._read_loop, daemon=True)
        self._threads = [t_ping, t_read]
        for t in self._threads:
            t.start()

    def stop(self) -> None:
        self._stop.set()
        for t in self._threads:
            t.join(timeout=2)
        if self._ser and self._ser.is_open:
            self._ser.close()

    def send_led(self, led_id: int, value: int) -> None:
        """Manda un comando LED: id (0=pin5, 1=pin6) + valore 0-255, come da firmware."""
        value = max(0, min(255, int(value)))
        if self._ser and self._ser.is_open:
            self._ser.write(bytes([int(led_id), value]))

    # --- interno ---

    def _ping_loop(self) -> None:
        while not self._stop.is_set():
            try:
                self._ser.write(bytes([self.PING_BYTE]))
            except serial.SerialException:
                pass
            self._stop.wait(self.PING_INTERVAL)

    def _read_loop(self) -> None:
        buffer = ""
        while not self._stop.is_set():
            try:
                raw = self._ser.read(self._ser.in_waiting or 1)
            except serial.SerialException:
                time.sleep(1)
                continue

            if not raw:
                continue

            buffer += raw.decode("ascii", errors="ignore")

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if not line:
                    continue
                tokens = line.split()
                if len(tokens) < 12:
                    continue
                try:
                    knobs = [float(t) for t in tokens[0:6]]
                    buttons = [int(t) for t in tokens[6:12]]
                except ValueError:
                    continue
                self.state.knobs = knobs
                self.state.buttons = buttons
                if self.on_update:
                    self.on_update(self.state)
