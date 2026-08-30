"""
OSC output/input for the NINO mapping layer.

Sends the state (6 knobs + 6 buttons) as a single OSC message:
    /nino/state  f f f f f f i i i i i i

Receives LED commands on:
    /nino/led  i(id) i(value 0-255)
"""

from __future__ import annotations

import threading
from typing import Callable, Optional

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient


class OSCOutput:
    def __init__(
        self,
        send_host: str = "127.0.0.1",
        send_port: int = 9000,
        recv_port: int = 9001,
        on_led_command: Optional[Callable[[int, int], None]] = None,
    ):
        self.send_host = send_host
        self.send_port = send_port
        self.recv_port = recv_port

        self._client = SimpleUDPClient(send_host, send_port)
        self._on_led_command = on_led_command
        self._server: Optional[ThreadingOSCUDPServer] = None
        self._server_thread: Optional[threading.Thread] = None

    def start(self) -> None:
        dispatcher = Dispatcher()
        dispatcher.map("/nino/led", self._handle_led)
        self._server = ThreadingOSCUDPServer(("0.0.0.0", self.recv_port), dispatcher)
        self._server_thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._server_thread.start()

    def stop(self) -> None:
        if self._server:
            self._server.shutdown()

    def send_state(self, knobs, buttons) -> None:
        self._client.send_message("/nino/state", list(knobs) + list(buttons))
        for i, v in enumerate(knobs):
            self._client.send_message(f"/nino/knob{i}", float(v))
        for i, v in enumerate(buttons):
            self._client.send_message(f"/nino/btn{i}", int(v))

    def _handle_led(self, address: str, id_, value) -> None:
        if self._on_led_command:
            self._on_led_command(int(id_), int(value))
