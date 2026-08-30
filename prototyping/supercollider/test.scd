// --- includes the file next to it, regardless of where you launch SC from ---
(
~herePath = thisProcess.nowExecutingPath.dirname;
(~herePath +/+ "nino.scd").load;
)

// --- create the instance ---
(
n = ~nino.value("/dev/cu.usbmodem14101", 115200);
n.action = { |me| [me.knob, me.btn].postln };
)

// read a value at any time
n.knob[0];
n.btn[3];

// drive the LED on pin5
n.led.(0, 255);

// at the end of the session (or just with Cmd+.)
n.free.();
