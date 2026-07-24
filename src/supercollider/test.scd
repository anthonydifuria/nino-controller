// --- include il file accanto, indipendentemente da dove lanci SC ---
(
~herePath = thisProcess.nowExecutingPath.dirname;
(~herePath +/+ "nino.scd").load;
)

// --- crea l'istanza ---
(
n = ~nino.value("/dev/cu.usbmodem14101", 115200);
n.action = { |me| [me.knob, me.btn].postln };
)

// leggi un valore in qualsiasi momento
n.knob[0];
n.btn[3];

// comanda il LED sul pin5
n.led.(0, 255);

// a fine sessione (o anche solo con Cmd+.)
n.free.();