(
~nino = { |portName, baud = 115200|
    var port, knob, btn, readRoutine, pingRoutine, cmdPeriodFunc, api, parseLine;

    knob = Array.fill(6, 0.0);
    btn  = Array.fill(6, 0);
    port = SerialPort(portName, baudrate: baud, crtscts: true);

    parseLine = { |line|
        var tokens = line.split($ ).reject(_.isEmpty);
        tokens.do { |tok, i|
            if (i < 6) {
                knob[i] = tok.asFloat;
            } {
                if (i < 12) { btn[i - 6] = tok.asInteger };
            };
        };
        if (api.action.notNil) { api.action.value(api) };
    };

    // --- ping periodico (deve arrivare entro 2s o Arduino si "disconnette") ---
    pingRoutine = fork {
        loop { port.put(200); 0.5.wait; };
    };

    // --- lettura continua, ricompone le righe e le spacchetta ---
    readRoutine = fork {
        var byte, line;
        loop {
            byte = port.read;
            if (byte == 10) {
                line = "";
                while ({ byte = port.read; byte != 13 }) {
                    line = line ++ byte.asAscii;
                };
                parseLine.(line);
            };
        };
    };

    // chiude la porta anche se premi Cmd+. (buona pratica con l'hardware)
    cmdPeriodFunc = { port.close };
    CmdPeriod.add(cmdPeriodFunc);

    api = (
        knob: knob,
        btn: btn,
        port: port,
        action: nil,
        led: { |id, value| port.put(id); port.put(value.asInteger.clip(0, 255)) },
        free: {
            readRoutine.stop;
            pingRoutine.stop;
            CmdPeriod.remove(cmdPeriodFunc);
            if (port.isOpen) { port.close };
        }
    );

    api;
};
)