# Faust — NINO receivers

Two minimal DSPs that receive the NINO mapping layer's 6 knobs + 6 buttons
and use them to drive the volume/on-off of 6 oscillators at different
frequencies (110-660 Hz), so you can hear the result instead of having to
look at a GUI.

## MIDI (`faustMIDI_NINO.dsp`)

Testable right away in the browser, no install needed:

1. Go to [faustide.grame.fr](https://faustide.grame.fr)
2. Paste the file's content
3. Enable MIDI in the IDE's settings (uses the browser's WebMIDI)
4. Turn the knobs/buttons on the NINO (with the mapping layer in `--output midi`)

Or locally, without a GUI:

    faust2caconsole -midi faustMIDI_NINO.dsp
    ./faustMIDI_NINO

## OSC (`faustOSC_NINO.dsp`)

OSC can't be tested in the browser (browsers don't have access to UDP
sockets for security reasons) — it needs to be compiled locally. We use
`faust2caconsole`, which compiles a command-line executable without needing
any graphical library (no Qt, no GTK):

    faust2caconsole -osc faustOSC_NINO.dsp
    ./faustOSC_NINO -port 9000

The `-port 9000` is required: Faust listens on port 5510 by default, while
the mapping layer sends on 9000.

### Troubleshooting

**`ld: library 'OSCFaust' not found`** at compile time: happens when
Homebrew has installed `libOSCFaust` (check with
`find /opt/homebrew -iname "*OSCFaust*"`) but the compiler doesn't know
where to look for it, usually because the standard Homebrew setup
(`eval "$(/opt/homebrew/bin/brew shellenv)"` in `~/.zshrc`) is missing or
hasn't been reloaded in this terminal session. Quick fix for the current
session:

    export LIBRARY_PATH="/opt/homebrew/lib:$LIBRARY_PATH"
    faust2caconsole -osc faustOSC_NINO.dsp

To make it permanent (so you don't have to redo it in every new terminal),
check if it's missing from the shell profile:

    grep brew ~/.zshrc

If it prints nothing, add it:

    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
