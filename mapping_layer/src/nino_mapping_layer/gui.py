"""
Stylized graphical panel for the NINO controller (tkinter, no extra
dependency beyond what the mapping layer already requires).

This isn't a realistic rendering: it's a stylized/schematic version of the
physical panel (dark case, knobs and sliders, status LEDs), useful as a
visual monitor of what's coming in over serial while coding or debugging,
even without a Max/OSC/MIDI patch open.

If it doesn't find an Arduino connected it starts in demo mode, with
simulated values, so the interface can be tried out even without hardware.

Usage:
    python -m nino_mapping_layer.gui
    python -m nino_mapping_layer.gui --port /dev/cu.usbmodem14101
    python -m nino_mapping_layer.gui --demo
"""

from __future__ import annotations

import argparse
import math
import queue
import random
import tkinter as tk
from typing import Optional

from .serial_reader import NinoState, SerialReader, autodetect_port

# --- palette inspired by the photographed panel: dark case, amber accents ---
BG_WINDOW = "#0b0b0c"
BG_PANEL = "#161616"
PANEL_OUTLINE = "#2b2b2b"
KNOB_BODY = "#c97a1f"
KNOB_BODY_DARK = "#7a4a12"
KNOB_INDICATOR = "#fff2d6"
CAP_OFF = "#4a2f10"
CAP_ON = "#ffb347"
LED_RED_OFF = "#3a0f0f"
LED_RED_ON = "#ff2b1f"
LED_AMBER_ON = "#ffb020"
LED_AUX = "#7a4a12"
SWITCH_TRACK = "#3a3a3a"
SWITCH_CURSOR = KNOB_BODY
SCREW = "#2f2f2f"
LABEL_FG = "#8a8a8a"
TITLE_FG = "#cfcfcf"

N_KNOBS = 6
N_SWITCHES = 6


class NinoPanel(tk.Frame):
    """Canvas that draws the stylized panel and updates via update_state()."""

    def __init__(self, master: tk.Misc, width: int = 620, height: int = 400):
        super().__init__(master, bg=BG_WINDOW)
        self.width = width
        self.height = height

        title = tk.Label(self, text="NINO", fg=TITLE_FG, bg=BG_WINDOW, font=("Menlo", 13, "bold"))
        title.pack(pady=(14, 0))

        self.canvas = tk.Canvas(self, width=width, height=height, bg=BG_WINDOW, highlightthickness=0)
        self.canvas.pack(padx=16, pady=10)

        self.status_var = tk.StringVar(value="waiting...")
        tk.Label(self, textvariable=self.status_var, fg=LABEL_FG, bg=BG_WINDOW, font=("Menlo", 10)).pack(
            pady=(0, 14)
        )

        self._draw_static_panel()
        self._knob_ids = [self._draw_knob(cx, cy) for cx, cy in self._knob_positions()]
        self._switch_ids = [self._draw_switch(cx, cy) for cx, cy in self._switch_positions()]
        # two LEDs top-right, like in the photo: one small (decorative,
        # always dim amber) and one big that reflects the connection state.
        self._draw_led(width - 100, 55, r=7, color=LED_AUX)
        self._led_id = self._draw_led(width - 55, 55, r=12, color=LED_RED_OFF)

    # --- layout: knobs on the left (2x3), sliders on the right (2x3), LED top-right ---

    def _knob_positions(self):
        cols = [140, 290]
        rows = [110, 205, 300]
        return [(c, r) for r in rows for c in cols]

    def _switch_positions(self):
        cols = [440, 530]
        rows = [130, 220, 310]
        return [(c, r) for r in rows for c in cols]

    # --- static drawing ---

    def _draw_static_panel(self):
        pad = 20
        self.canvas.create_rectangle(
            pad, pad, self.width - pad, self.height - pad,
            fill=BG_PANEL, outline=PANEL_OUTLINE, width=2,
        )
        corners = (
            (pad + 16, pad + 16),
            (self.width - pad - 16, pad + 16),
            (pad + 16, self.height - pad - 16),
            (self.width - pad - 16, self.height - pad - 16),
        )
        for x, y in corners:
            self._draw_screw(x, y)

    def _draw_screw(self, x, y, r=6):
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=SCREW, outline="#111")
        self.canvas.create_line(x - r + 2, y, x + r - 2, y, fill="#5a5a5a")

    # --- dynamic elements ---

    def _draw_knob(self, cx, cy, r=32):
        self.canvas.create_oval(cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3, outline="#000", width=1)
        body = self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=KNOB_BODY, outline=KNOB_BODY_DARK, width=3)
        indicator = self.canvas.create_line(cx, cy, cx, cy - r + 6, fill=KNOB_INDICATOR, width=3)
        cap = self.canvas.create_oval(cx - 5, cy - r - 15, cx + 5, cy - r - 5, fill=CAP_OFF, outline="")
        return {"body": body, "indicator": indicator, "cap": cap, "cx": cx, "cy": cy, "r": r}

    def _draw_switch(self, cx, cy, w=54, r=10):
        # simple cursor that slides left (off) / right (on) along a track.
        x_off, x_on = cx - w / 2, cx + w / 2
        track = self.canvas.create_line(x_off, cy, x_on, cy, fill=SWITCH_TRACK, width=4, capstyle=tk.ROUND)
        cursor = self.canvas.create_oval(x_off - r, cy - r, x_off + r, cy + r, fill=SWITCH_CURSOR, outline=KNOB_BODY_DARK, width=2)
        return {"track": track, "cursor": cursor, "x_off": x_off, "x_on": x_on, "cy": cy, "r": r}

    def _draw_led(self, cx, cy, r=12, color=LED_RED_OFF):
        return self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=color, outline="#200")

    # --- update from a NinoState ---

    def update_state(self, state: NinoState, mode: str = "connected") -> None:
        """mode: 'connected' (real data), 'demo' (simulated), 'waiting' (waiting for data)."""
        for i, v in enumerate(state.knobs[:N_KNOBS]):
            self._set_knob(i, v)
        for i, v in enumerate(state.buttons[:N_SWITCHES]):
            self._set_switch(i, v)

        led_color = {"connected": LED_RED_ON, "demo": LED_AMBER_ON, "waiting": LED_RED_OFF}[mode]
        self.canvas.itemconfig(self._led_id, fill=led_color)

        status_text = {
            "connected": "NINO connected",
            "demo": "demo mode (no Arduino found)",
            "waiting": "waiting for data...",
        }[mode]
        self.status_var.set(status_text)

    def _set_knob(self, i, value):
        value = max(0.0, min(1.0, value))
        k = self._knob_ids[i]
        angle = math.radians(-135 + value * 270)  # -135 to +135 degrees
        x2 = k["cx"] + (k["r"] - 6) * math.sin(angle)
        y2 = k["cy"] - (k["r"] - 6) * math.cos(angle)
        self.canvas.coords(k["indicator"], k["cx"], k["cy"], x2, y2)
        self.canvas.itemconfig(k["cap"], fill=CAP_ON if value > 0.05 else CAP_OFF)

    def _set_switch(self, i, value):
        s = self._switch_ids[i]
        x = s["x_on"] if value else s["x_off"]
        r, cy = s["r"], s["cy"]
        self.canvas.coords(s["cursor"], x - r, cy - r, x + r, cy + r)


# --- data source: real serial, marshalled to the tkinter thread via a queue ---

class LiveSource:
    def __init__(self, port: str, baudrate: int, update_queue: "queue.Queue[NinoState]"):
        self.reader = SerialReader(port, baudrate=baudrate, on_update=self._on_update)
        self._queue = update_queue

    def _on_update(self, state: NinoState) -> None:
        # called from the serial thread: don't touch tkinter from here,
        # just pass a copy of the state through the queue.
        self._queue.put(NinoState(knobs=list(state.knobs), buttons=list(state.buttons)))

    def start(self) -> None:
        self.reader.start()

    def stop(self) -> None:
        self.reader.stop()


# --- simulated data source, to try the interface without hardware ---

class DemoSource:
    def __init__(self):
        self._t = 0.0
        self._buttons = [0] * N_SWITCHES
        self._next_toggle = [random.uniform(1, 4) for _ in range(N_SWITCHES)]

    def tick(self, dt: float) -> NinoState:
        self._t += dt
        knobs = [
            0.5 + 0.5 * math.sin(self._t * (0.5 + 0.15 * i) + i)
            for i in range(N_KNOBS)
        ]
        for i in range(N_SWITCHES):
            self._next_toggle[i] -= dt
            if self._next_toggle[i] <= 0:
                self._buttons[i] = 1 - self._buttons[i]
                self._next_toggle[i] = random.uniform(1, 4)
        return NinoState(knobs=knobs, buttons=list(self._buttons))


def run(port: Optional[str], baudrate: int, force_demo: bool, selftest: bool = False) -> None:
    root = tk.Tk()
    root.title("NINO - panel")
    root.configure(bg=BG_WINDOW)
    root.resizable(False, False)

    panel = NinoPanel(root)
    panel.pack()

    update_queue: "queue.Queue[NinoState]" = queue.Queue()
    live: Optional[LiveSource] = None
    demo: Optional[DemoSource] = None
    mode = "waiting"

    chosen_port = None if force_demo else (port or autodetect_port())

    if chosen_port:
        try:
            live = LiveSource(chosen_port, baudrate, update_queue)
            live.start()
            mode = "waiting"  # becomes "connected" on the first packet received
        except Exception:
            live = None

    if live is None:
        demo = DemoSource()
        mode = "demo"

    def poll():
        nonlocal mode
        if live is not None:
            got_update = False
            try:
                while True:
                    state = update_queue.get_nowait()
                    panel.update_state(state, mode="connected")
                    got_update = True
            except queue.Empty:
                pass
            if not got_update and mode != "connected":
                panel.update_state(NinoState(), mode="waiting")
        elif demo is not None:
            state = demo.tick(0.03)
            panel.update_state(state, mode="demo")

        root.after(30, poll)

    poll()

    def on_close():
        if live is not None:
            live.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    if selftest:
        # starts and closes itself: checks that the interface launches
        # without exceptions even without hardware connected (useful for
        # CI/debugging).
        root.after(300, on_close)

    root.mainloop()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="NINO - stylized graphical panel (tkinter)")
    p.add_argument("--port", help="serial port (if omitted, tries automatic detection)")
    p.add_argument("--baud", type=int, default=115200)
    p.add_argument("--demo", action="store_true", help="force demo mode (simulated values)")
    p.add_argument("--selftest", action="store_true", help="start and immediately close the window (for automated checks)")
    return p


def main() -> None:
    args = build_parser().parse_args()
    run(port=args.port, baudrate=args.baud, force_demo=args.demo, selftest=args.selftest)


if __name__ == "__main__":
    main()
