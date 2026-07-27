<CsoundSynthesizer>
<CsOptions>
-odac -m0d
</CsOptions>
<CsInstruments>
sr = 44100
ksmps = 64
nchnls = 2
0dbfs = 1

giOSC OSCinit 9000

instr 1
    kK0, kK1, kK2, kK3, kK4, kK5, kB0, kB1, kB2, kB3, kB4, kB5 init 0

    kk OSClisten giOSC, "/nino/state", "ffffffiiiiii", kK0, kK1, kK2, kK3, kK4, kK5, kB0, kB1, kB2, kB3, kB4, kB5

    printks "knob: %.2f %.2f %.2f %.2f %.2f %.2f | pulsanti: %.0f %.0f %.0f %.0f %.0f %.0f\n", 0.2, kK0, kK1, kK2, kK3, kK4, kK5, kB0, kB1, kB2, kB3, kB4, kB5
endin
</CsInstruments>
<CsScore>
i 1 0 3600
</CsScore>
</CsoundSynthesizer>