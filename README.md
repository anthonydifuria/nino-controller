# NINO — Node Interface for Networked Output

Progetto per il controller hardware NINO (Arduino) collegato ad ambienti di sintesi/programmazione audio.

## Struttura

- `firmware/` — sketch Arduino per la scheda NINO.
- `docs/diagrams/` — diagrammi concettuali e fisici del sistema.
- `mapping_layer/` — applicazione Python: legge la seriale e la traduce in OSC/MIDI.
- `prototyping/` — implementazioni native indipendenti (Max, Csound, SuperCollider) che parlano direttamente alla seriale.

## Requisiti

- Arduino IDE (per il firmware in `firmware/`)
- Python 3.9+ (per `mapping_layer/`, vedi il suo README)
