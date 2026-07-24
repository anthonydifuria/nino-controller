// NINO CONTROLLER
int analogPins[] = {0, 1, 2, 3, 4, 5};
int analogPinCount = 6;
int orangeLed[] = {5, 6 };
int ledCount = 2;
int onoff[] = {7, 8, 9, 10, 11, 12};
int onoffCount = 6;

// Variabili per il controllo connessione
bool connesso = false;
unsigned long ultimoPing = 0;

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
  // 1. CONTROLLO TIMEOUT (2 secondi)
  if (connesso && (millis() - ultimoPing > 2000)) {
    connesso = false;
    analogWrite(6, 0); // Spegne il LED se Max non si fa vivo
  }

  // 2. LETTURA SERIALE
  while (Serial.available() > 0) {
    int inByte = Serial.read();
    
    // Se riceve 200, è il "Ping" di Max
    if (inByte == 200) {
      connesso = true;
      ultimoPing = millis(); // Resetta il timer
      analogWrite(6, 255);   // Accende il LED
    } 
    // Altrimenti è un comando normale (2 byte: id e valore)
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
  
  // 3. INVIO DATI ANALOGICI
  for (int i = 0; i < analogPinCount; i++){
    float knobs = linearizza(analogRead(analogPins[i]) / 1020.0);
    Serial.print(knobs);
    Serial.print(" ");
  }
  
  // 4. INVIO DATI DIGITALI
  for (int i = 0; i < onoffCount; i++){
    Serial.print(digitalRead(onoff[i]));
    Serial.print(" ");
  }
  Serial.println("");
  
  delay(10);
}

float linearizza(float lettura) {
  static const float x[] = {0.00, 0.18, 0.37, 0.41, 0.51, 1.00};
  static const float y[] = {0.00, 0.25, 0.50, 0.75, 0.87, 1.00};
  
  int n_let = 5;
  if (lettura <= x[0]) return y[0];
  if (lettura >= x[n_let]) return y[n_let];
  
  int i = 0;
  while (lettura > x[i + 1]) i++;
  
  float frazione = (lettura - x[i]) / (x[i + 1] - x[i]);
  return y[i] + frazione * (y[i + 1] - y[i]);
}