int sensorValue = 0; // variabile per memorizzare il valore

void setup() {
  Serial.begin(9600); 
}

void loop() {
  sensorValue = analogRead(A0); 
  Serial.println(sensorValue);   
  delay(500);                    
}
