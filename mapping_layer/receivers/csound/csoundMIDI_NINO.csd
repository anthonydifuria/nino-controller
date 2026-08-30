<CsoundSynthesizer>
<CsOptions>
-Ma -odac -m0d
</CsOptions>
<CsInstruments>
sr = 44100
ksmps = 64
nchnls = 2
0dbfs = 1

instr 1
    ; knob 1-6 -> CC 20-25, buttons 1-6 -> CC 30-35, channel 1
    kK0 ctrl7 1, 20, 0, 1
    kK1 ctrl7 1, 21, 0, 1
    kK2 ctrl7 1, 22, 0, 1
    kK3 ctrl7 1, 23, 0, 1
    kK4 ctrl7 1, 24, 0, 1
    kK5 ctrl7 1, 25, 0, 1
    kB0 ctrl7 1, 30, 0, 1
    kB1 ctrl7 1, 31, 0, 1
    kB2 ctrl7 1, 32, 0, 1
    kB3 ctrl7 1, 33, 0, 1
    kB4 ctrl7 1, 34, 0, 1
    kB5 ctrl7 1, 35, 0, 1

    printks "knob: %.2f %.2f %.2f %.2f %.2f %.2f | buttons: %.0f %.0f %.0f %.0f %.0f %.0f\n", 0.2, kK0, kK1, kK2, kK3, kK4, kK5, kB0, kB1, kB2, kB3, kB4, kB5
endin
</CsInstruments>
<CsScore>
i 1 0 3600
</CsScore>
</CsoundSynthesizer>
