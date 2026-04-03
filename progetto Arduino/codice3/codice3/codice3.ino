int redLed = 11;
int bluLed = 12;

void setup() {
  // Serial.begin(9600);
  pinMode(bluLed, OUTPUT); 
  pinMode(redLed, OUTPUT);

}

void loop() {

  // int onoff = 0;
  // for (int i = 0; i < 10; i = i + 1){

  //   digitalWrite(11 + (i % 2),i % 1);
  //   delay(1000);
    
  // };


  // // if (){


  // // }
  // // else
  // // {


  // // }
  
  digitalWrite(bluLed,HIGH);
  delay(1000);
  digitalWrite(redLed,HIGH);
  digitalWrite(bluLed,LOW);
  delay(1000); 
  digitalWrite(redLed,LOW);
  delay(1000);

}


