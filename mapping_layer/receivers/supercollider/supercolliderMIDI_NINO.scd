(
MIDIClient.init;
MIDIIn.connectAll;

~knob = Array.fill(6, 0.0);
~btn = Array.fill(6, 0);
~midiFuncs = List.new;

~knobCCs = [20, 21, 22, 23, 24, 25];
~btnCCs = [30, 31, 32, 33, 34, 35];

~knobCCs.do { |cc, i|
    ~midiFuncs.add(
        MIDIFunc.cc({ |val, num, chan, src|
            ~knob[i] = val / 127.0;
        }, cc, 0)  // canale 0 in SC = canale MIDI 1
    );
};

~btnCCs.do { |cc, i|
    ~midiFuncs.add(
        MIDIFunc.cc({ |val, num, chan, src|
            ~btn[i] = if(val > 63) { 1 } { 0 };
        }, cc, 0)
    );
};

~printRoutine = fork {
    loop {
        [~knob, ~btn].postln;
        0.2.wait;
    };
};
)

// per fermare: ~printRoutine.stop; ~midiFuncs.do(_.free);