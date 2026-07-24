# NINO Mapping Layer

Protocol converter / mapping layer: legge il flusso seriale del controller NINO
(Arduino) e lo ritraduce in OSC (e, in futuro, MIDI) su rete locale, cosi' da poter
essere ricevuto da qualsiasi ambiente audio senza che ognuno debba reimplementare
la lettura seriale.

STATO: scheletro del progetto, implementazione in corso.

## Setup ambiente (venv)

    python3 -m venv .venv
    source .venv/bin/activate        # su Windows: .venv\Scripts\activate
    pip install -r requirements.txt

## Struttura

- `src/nino_mapping_layer/` — codice sorgente dell'applicazione
  - `serial_reader.py` — lettura e parsing del protocollo seriale NINO
  - `osc_out.py` — invio/ricezione OSC
  - `tray_app.py` — interfaccia a icona nella system tray
- `build/` — script per compilare l'eseguibile nativo (PyInstaller)
- `tests/` — test automatici
- `receivers/` — esempi minimi di come ricevere i dati OSC di questo progetto
  nei vari ambienti audio (Max, Csound, SuperCollider, Pure Data, plugdata, Faust)

## Build eseguibile nativo

    bash build/build_mac.sh      # su macOS
    bash build/build_linux.sh    # su Linux
