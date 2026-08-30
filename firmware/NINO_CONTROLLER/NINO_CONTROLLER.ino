// NINO CONTROLLER
int analogPins[] = {0, 1, 2, 3, 4, 5};
int analogPinCount = 6;
int orangeLed[] = {5, 6};
int ledCount = 2;
int togglePins[] = {7, 8, 9, 10, 11, 12};
int toggleCount = 6;

// Connection tracking
bool connected = false;
unsigned long lastPing = 0;

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < toggleCount; i++) {
    pinMode(togglePins[i], INPUT_PULLUP);
  }
  for (int i = 0; i < ledCount; i++) {
    pinMode(orangeLed[i], OUTPUT);
  }
}

void loop() {
  // 1. TIMEOUT CHECK (2 seconds)
  if (connected && (millis() - lastPing > 2000)) {
    connected = false;
    analogWrite(6, 0); // Turn off the LED if the host stops pinging
  }

  // 2. SERIAL READ
  while (Serial.available() > 0) {
    int inByte = Serial.read();

    // A value of 200 is the "ping" from the host software
    if (inByte == 200) {
      connected = true;
      lastPing = millis(); // Reset the timeout timer
      analogWrite(6, 255);  // Turn on the LED
    }
    // Otherwise it's a normal command (2 bytes: id and value)
    else {
      if (Serial.available() > 0) {
        int val = Serial.read();
        if (inByte == 0) {
          analogWrite(5, val);
        }
        if (inByte == 1) {
          analogWrite(6, val);
        }
      }
    }
  }

  // 3. SEND ANALOG DATA
  for (int i = 0; i < analogPinCount; i++) {
    float knobs = linearize(analogRead(analogPins[i]) / 1020.0);
    Serial.print(knobs);
    Serial.print(" ");
  }

  // 4. SEND DIGITAL DATA
  for (int i = 0; i < toggleCount; i++) {
    Serial.print(digitalRead(togglePins[i]));
    Serial.print(" ");
  }
  Serial.println("");

  delay(10);
}

float linearize(float reading) {
  static const float x[] = {0.00, 0.18, 0.37, 0.41, 0.51, 1.00};
  static const float y[] = {0.00, 0.25, 0.50, 0.75, 0.87, 1.00};

  int n = 5;
  if (reading <= x[0]) return y[0];
  if (reading >= x[n]) return y[n];

  int i = 0;
  while (reading > x[i + 1]) i++;

  float fraction = (reading - x[i]) / (x[i + 1] - x[i]);
  return y[i] + fraction * (y[i + 1] - y[i]);
}
