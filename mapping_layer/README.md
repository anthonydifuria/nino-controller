# NINO Mapping Layer

Protocol converter / mapping layer: legge il flusso seriale del controller NINO
(Arduino) e lo traduce in OSC o MIDI classico, cosi' da poter essere ricevuto da
qualsiasi ambiente audio senza che ognuno debba reimplementare la lettura seriale.

STATO: nucleo funzionante (seriale + rilevamento USB + OSC + MIDI) da CLI,
nessuna interfaccia grafica/tray ancora, nessun installer ancora — fase di test.

## Setup ambiente (venv)

    cd mapping_layer
    python3 -m venv .venv
    source .venv/bin/activate        # su Windows: .venv\Scripts\activate
    pip install -r requirements.txt

## Uso (da dentro mapping_layer/src)

Elenca le porte seriali disponibili (segnala quelle che sembrano un Arduino):

    cd src
    python -m nino_mapping_layer --list-ports

Avvio con rilevamento automatico della porta, uscita OSC (default):

    python -m nino_mapping_layer --output osc

Avvio specificando la porta e l'uscita MIDI:

    python -m nino_mapping_layer --port /dev/cu.usbmodem14101 --output midi

Tutte le opzioni:

    python -m nino_mapping_layer --help

## Uscita OSC

- Manda `/nino/state` con 6 float (knob, 0.0-1.0) + 6 int (pulsanti, 0/1)
  sulla porta indicata da `--osc-send-port` (default 9000).
- Riceve comandi LED su `/nino/led` (id, valore 0-255) sulla porta indicata
  da `--osc-recv-port` (default 9001), e li inoltra all'Arduino.

## Risoluzione problemi

**macOS: `pip install -r requirements.txt` fallisce compilando `python-rtmidi`
con un errore su `sem_timedwait`.** Succede se hai JACK installato (es. via
Homebrew): il build system rileva JACK e prova a compilarne il supporto, ma
quel codice usa una funzione POSIX che macOS non implementa. A noi qui serve
solo CoreMIDI, quindi si disattiva JACK in fase di build:

    pip install pyserial python-osc mido
    pip install python-rtmidi --config-settings=setup-args="-Djack=false"

Se anche questo fallisse, prova a creare la venv con una versione di Python
leggermente piu' vecchia (es. `python3.12 -m venv .venv` se disponibile):
per alcune versioni recentissime di Python potrebbe non esistere ancora una
wheel precompilata, e allora pip prova a compilare da zero incontrando lo
stesso problema.

## Uscita MIDI

- Crea una porta MIDI virtuale (nome configurabile con `--midi-port-name`),
  visibile a qualsiasi DAW/software MIDI su Mac e Linux.
- I 6 knob diventano Control Change 20-25, i 6 pulsanti Control Change 30-35
  (0 o 127), sul canale scelto con `--midi-channel`.
- Il rilevamento/inoltro LED via MIDI non e' ancora implementato.


## Struttura

- `src/nino_mapping_layer/`
  - `serial_reader.py` — lettura/parsing seriale + rilevamento automatico USB
  - `osc_out.py` — invio/ricezione OSC
  - `midi_out.py` — invio MIDI
  - `__main__.py` — entry point CLI (fase di test)
  - `tray_app.py` — interfaccia a icona nella system tray (TODO, non ancora scritta)
- `build/` — script per compilare l'eseguibile nativo (PyInstaller) — TODO
- `tests/` — test automatici — TODO
- `receivers/` — esempi minimi di come ricevere i dati OSC/MIDI di questo
  progetto nei vari ambienti audio (Max, Csound, SuperCollider, Pure Data,
  plugdata, Faust) — TODO

## Prossimi passi

1. Testare a fondo la CLI (seriale, rilevamento USB, OSC, MIDI) su Mac e Linux.
2. Interfaccia a icona nella system tray (`tray_app.py`).
3. Build eseguibile nativo con PyInstaller (`build/`).
