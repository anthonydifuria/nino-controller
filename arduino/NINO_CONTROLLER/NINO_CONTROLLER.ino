// NINO CONTROLLER
int analogPins[] = {0, 1, 2, 3, 4, 5}; 
int analogPinCount = 6;
int orangeLed[] = {5, 6 }; 
int ledCount = 2;
int onoff[] = {7, 8, 9, 10, 11, 12};
int onoffCount = 6;

void setup() {
  Serial.begin(115200);

  for (int i = 0; i < onoffCount; i++){
    pinMode(onoff[i], INPUT_PULLUP);
  }
  for (int i = 0; i < ledCount; i++){
    pinMode(orangeLed[i], OUTPUT);
  }
}

void loop() {
  while (Serial.available() >= 2) {
    int id = Serial.read();
    int val = Serial.read();
    if (val != -1) { // Protezione contro letture fallite
      if (id == 0) { 
        analogWrite(5, val);
      }
      if (id == 1) {
        analogWrite(6, val);
      }
    }
  }

  for (int i = 0; i < analogPinCount; i++){
    Serial.print(analogRead(analogPins[i]) / 1020.0);
    Serial.print(" ");
  }
  for (int i = 0; i < analogPinCount; i++){
    Serial.print(digitalRead(onoff[i]));
    Serial.print(" ");
  }
  Serial.println("");
  delay(10);
}
