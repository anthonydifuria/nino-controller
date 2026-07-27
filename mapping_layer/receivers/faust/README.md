# Faust — ricevitori NINO

Due DSP minimi che ricevono i 6 knob + 6 pulsanti del mapping layer NINO e li
usano per pilotare il volume/on-off di 6 oscillatori a frequenze diverse
(110-660 Hz), cosi' si sente il risultato invece di dover guardare una GUI.

## MIDI (`faustMIDI_NINO.dsp`)

Testabile subito nel browser, senza installare nulla:

1. Vai su [faustide.grame.fr](https://faustide.grame.fr)
2. Incolla il contenuto del file
3. Attiva il MIDI dalle impostazioni dell'IDE (usa la WebMIDI del browser)
4. Gira i knob/pulsanti sul NINO (con il mapping layer in `--output midi`)

Oppure in locale, senza GUI:

    faust2caconsole -midi faustMIDI_NINO.dsp
    ./faustMIDI_NINO

## OSC (`faustOSC_NINO.dsp`)

L'OSC non e' testabile nel browser (i browser non hanno accesso a socket UDP
per motivi di sicurezza) — serve compilarlo in locale. Usiamo
`faust2caconsole`, che compila un eseguibile da riga di comando senza bisogno
di nessuna libreria grafica (niente Qt, niente GTK):

    faust2caconsole -osc faustOSC_NINO.dsp
    ./faustOSC_NINO -port 9000

Il `-port 9000` e' necessario: Faust di default ascolta sulla porta 5510,
il mapping layer manda invece sulla 9000.

### Risoluzione problemi

**`ld: library 'OSCFaust' not found`** in fase di compilazione: capita quando
Homebrew ha installato `libOSCFaust` (verificabile con
`find /opt/homebrew -iname "*OSCFaust*"`) ma il compilatore non sa dove
cercarla, di solito perche' il setup standard di Homebrew
(`eval "$(/opt/homebrew/bin/brew shellenv)"` in `~/.zshrc`) manca o non e'
stato ricaricato in questa sessione di terminale. Fix rapido per la sessione
corrente:

    export LIBRARY_PATH="/opt/homebrew/lib:$LIBRARY_PATH"
    faust2caconsole -osc faustOSC_NINO.dsp

Per renderlo permanente (evita di doverlo rifare ad ogni nuovo terminale),
verifica se manca dal profilo shell:

    grep brew ~/.zshrc

Se non stampa nulla, aggiungilo:

    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc