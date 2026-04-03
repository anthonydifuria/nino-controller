int redLed = 11;
int bluLed = 12;

int cnt = 0;

void setup() {
  Serial.begin(9600);
  pinMode(bluLed, OUTPUT); 
  pinMode(redLed, OUTPUT);

}

void loop() {

  int status = cnt % 4;
  if(status == 0){
    digitalWrite(redLed, LOW);
    digitalWrite(bluLed, HIGH);
  }
  else if(status == 1){
    digitalWrite(redLed, HIGH);
    digitalWrite(bluLed, LOW);
  }
  else if(status == 2){
    digitalWrite(redLed, HIGH);
    digitalWrite(bluLed, HIGH);
  }
  else{
    digitalWrite(bluLed, LOW);
    digitalWrite(redLed, LOW);
  }

  Serial.println(status);

  cnt++;
  delay(1000);

  // for (int i = 0; i < 4; i = i + 1) {
  //   digitalWrite(11 + (i % 2), int(i / 2.0));
  //   delay(1000);
  // } 

}


