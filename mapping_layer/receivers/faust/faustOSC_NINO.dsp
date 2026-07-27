import("stdfaust.lib");

vol0 = hslider("knob0[osc:/nino/knob0]", 0, 0, 1, 0.01);
vol1 = hslider("knob1[osc:/nino/knob1]", 0, 0, 1, 0.01);
vol2 = hslider("knob2[osc:/nino/knob2]", 0, 0, 1, 0.01);
vol3 = hslider("knob3[osc:/nino/knob3]", 0, 0, 1, 0.01);
vol4 = hslider("knob4[osc:/nino/knob4]", 0, 0, 1, 0.01);
vol5 = hslider("knob5[osc:/nino/knob5]", 0, 0, 1, 0.01);

on0 = checkbox("btn0[osc:/nino/btn0]");
on1 = checkbox("btn1[osc:/nino/btn1]");
on2 = checkbox("btn2[osc:/nino/btn2]");
on3 = checkbox("btn3[osc:/nino/btn3]");
on4 = checkbox("btn4[osc:/nino/btn4]");
on5 = checkbox("btn5[osc:/nino/btn5]");

osc0 = os.osc(110) * vol0 * on0;
osc1 = os.osc(220) * vol1 * on1;
osc2 = os.osc(330) * vol2 * on2;
osc3 = os.osc(440) * vol3 * on3;
osc4 = os.osc(550) * vol4 * on4;
osc5 = os.osc(660) * vol5 * on5;

mix = (osc0+osc1+osc2+osc3+osc4+osc5) * 0.15;

process = mix <: _,_;