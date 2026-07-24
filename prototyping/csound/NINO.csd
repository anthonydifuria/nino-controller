<CsoundSynthesizer>
<CsOptions>
-odac -m0d
</CsOptions>
<CsInstruments>
sr = 44100
ksmps = 64
nchnls = 2
0dbfs = 1

; ============================================================
;  UDO "NINO controller" - copia questo blocco in cima a
;  qualsiasi progetto, senza toccarlo
; ============================================================

; array globali: 6 potenziometri (0.0-1.0) e 6 pulsanti (0/1)
gkKnob[] init 6
gkBtn[]  init 6

; --- NinoUpdate: legge la seriale e aggiorna gkKnob[]/gkBtn[] ---
; uso: NinoUpdate iPort
opcode NinoUpdate, 0, i
    iPort xin

    kPingTime init 0
    kField    init 0
    kValue    init 0
    kDivisor  init 1
    kInFrac   init 0
    kSawDigit init 0

    ; ping periodico (deve arrivare entro 2s o Arduino si "disconnette")
    kNow timeinsts
    if (kNow - kPingTime >= 0.5) then
        serialWrite iPort, 200
        kPingTime = kNow
    endif

    ; lettura seriale byte per byte
    kMoreData = 1
    while (kMoreData == 1) do
        kByte serialRead iPort
        if (kByte == -1) then
            kMoreData = 0
        elseif (kByte >= 48 && kByte <= 57) then
            kValue = kValue * 10 + (kByte - 48)
            if (kInFrac == 1) then
                kDivisor = kDivisor * 10
            endif
            kSawDigit = 1
        elseif (kByte == 46) then
            kInFrac = 1
        elseif (kByte == 32 || kByte == 10 || kByte == 13) then
            if (kSawDigit == 1) then
                kResult = kValue / kDivisor
                if (kField < 6) then
                    gkKnob[kField] = kResult
                elseif (kField < 12) then
                    gkBtn[kField - 6] = kResult
                endif
                kField = kField + 1
            endif
            kValue = 0
            kDivisor = 1
            kInFrac = 0
            kSawDigit = 0
            if (kByte == 10 || kByte == 13) then
                kField = 0
            endif
        endif
    od
endop

; --- NinoLed: accende/dimmerra un LED (id 0 = pin5, id 1 = pin6) ---
; uso: NinoLed iPort, iId, kValore   (kValore 0-255)
; manda il comando solo quando il valore cambia, per non intasare la seriale
opcode NinoLed, 0, iik
    iPort, iId, kVal xin
    kVal limit kVal, 0, 255
    kChanged changed kVal
    if (kChanged == 1) then
        serialWrite iPort, iId
        serialWrite iPort, kVal
    endif
endop

; ============================================================
;  ISTRUMENTO - qui usi le due UDO
; ============================================================
instr 1
    ; SOSTITUISCI CON LA TUA PORTA MAC (nel Terminale: ls /dev/cu.*)
    iPort serialBegin "/dev/cu.usbmodem14101", 115200

    NinoUpdate iPort

    ; stampa di controllo (scommenta per debug)
     printks "K0=%.2f K1=%.2f K2=%.2f K3=%.2f K4=%.2f K5=%.2f | B0=%d B1=%d B2=%d B3=%d B4=%d B5=%d\n", 0.2, gkKnob[0], gkKnob[1], gkKnob[2], gkKnob[3], gkKnob[4], gkKnob[5], gkBtn[0], gkBtn[1], gkBtn[2], gkBtn[3], gkBtn[4], gkBtn[5]

    ; esempio: dimmerare il LED sul pin5 in base al knob 0
    ; NinoLed iPort, 0, gkKnob[0] * 255

endin
</CsInstruments>
<CsScore>
i 1 0 3600
</CsScore>
</CsoundSynthesizer>