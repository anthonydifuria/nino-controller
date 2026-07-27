(
~knob = Array.fill(6, 0.0);
~btn = Array.fill(6, 0);

OSCdef(\ninoState, { |msg|
    ~knob = msg[1..6];
    ~btn = msg[7..12];
}, '/nino/state');

~printRoutine = fork {
    loop {
        [~knob, ~btn].postln;
        0.2.wait;
    };
};
)

// per fermare: ~printRoutine.stop; OSCdef(\ninoState).free;