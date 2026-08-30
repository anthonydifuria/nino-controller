import("stdfaust.lib");

vol0 = hslider("knob0[midi:ctrl 20]", 0, 0, 1, 0.01);
vol1 = hslider("knob1[midi:ctrl 21]", 0, 0, 1, 0.01);
vol2 = hslider("knob2[midi:ctrl 22]", 0, 0, 1, 0.01);
vol3 = hslider("knob3[midi:ctrl 23]", 0, 0, 1, 0.01);
vol4 = hslider("knob4[midi:ctrl 24]", 0, 0, 1, 0.01);
vol5 = hslider("knob5[midi:ctrl 25]", 0, 0, 1, 0.01);

on0 = hslider("btn0[midi:ctrl 30]", 0, 0, 1, 0.01);
on1 = hslider("btn1[midi:ctrl 31]", 0, 0, 1, 0.01);
on2 = hslider("btn2[midi:ctrl 32]", 0, 0, 1, 0.01);
on3 = hslider("btn3[midi:ctrl 33]", 0, 0, 1, 0.01);
on4 = hslider("btn4[midi:ctrl 34]", 0, 0, 1, 0.01);
on5 = hslider("btn5[midi:ctrl 35]", 0, 0, 1, 0.01);

osc0 = os.osc(110) * vol0 * on0;
osc1 = os.osc(220) * vol1 * on1;
osc2 = os.osc(330) * vol2 * on2;
osc3 = os.osc(440) * vol3 * on3;
osc4 = os.osc(550) * vol4 * on4;
osc5 = os.osc(660) * vol5 * on5;

mix = (osc0+osc1+osc2+osc3+osc4+osc5) * 0.15;

process = mix <: _,_;
