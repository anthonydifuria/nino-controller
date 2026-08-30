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
;  "NINO controller" UDO - copy this block to the top of
;  any project, without touching it
; ============================================================

; global arrays: 6 knobs (0.0-1.0) and 6 buttons (0/1)
gkKnob[] init 6
gkBtn[]  init 6

; --- NinoUpdate: reads the serial port and updates gkKnob[]/gkBtn[] ---
; usage: NinoUpdate iPort
opcode NinoUpdate, 0, i
    iPort xin

    kPingTime init 0
    kField    init 0
    kValue    init 0
    kDivisor  init 1
    kInFrac   init 0
    kSawDigit init 0

    ; periodic ping (must arrive within 2s or the Arduino "disconnects")
    kNow timeinsts
    if (kNow - kPingTime >= 0.5) then
        serialWrite iPort, 200
        kPingTime = kNow
    endif

    ; byte-by-byte serial read
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

; --- NinoLed: turns an LED on/dims it (id 0 = pin5, id 1 = pin6) ---
; usage: NinoLed iPort, iId, kValue   (kValue 0-255)
; only sends the command when the value changes, so as not to flood the serial port
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
;  INSTRUMENT - use the two UDOs here
; ============================================================
instr 1
    ; REPLACE WITH YOUR MAC PORT (in Terminal: ls /dev/cu.*)
    iPort serialBegin "/dev/cu.usbmodem14101", 115200

    NinoUpdate iPort

    ; debug print (uncomment to enable)
     printks "K0=%.2f K1=%.2f K2=%.2f K3=%.2f K4=%.2f K5=%.2f | B0=%d B1=%d B2=%d B3=%d B4=%d B5=%d\n", 0.2, gkKnob[0], gkKnob[1], gkKnob[2], gkKnob[3], gkKnob[4], gkKnob[5], gkBtn[0], gkBtn[1], gkBtn[2], gkBtn[3], gkBtn[4], gkBtn[5]

    ; example: dim the LED on pin5 based on knob 0
    ; NinoLed iPort, 0, gkKnob[0] * 255

endin
</CsInstruments>
<CsScore>
i 1 0 3600
</CsScore>
</CsoundSynthesizer>
