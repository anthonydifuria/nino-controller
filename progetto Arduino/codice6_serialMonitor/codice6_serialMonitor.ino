//Serial Monitor TEST

/*
Cichi [while e for]
il while è un ciclo

counter = 0
while (counter < 10){
  //excute code
  counter++
}
*/

int buttonPin = 2;
int redLed = 11;
int bluLed = 12;

bool butPress = false;
int cnt = 0;

void setup() {
  Serial.begin(9600); // attivo la porta seriale e gli do la velocità (baud rate) cioè la velocità di bit al secondo che può trasmettere e leggere sulla prota 
  while(!Serial);     // blocca il codice se non è attivo il seriale
  //Serial.println("Hello World");

  pinMode(bluLed,    OUTPUT); 
  pinMode(redLed,    OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);

  Serial.println("HELLO");
  
  // int array[5] = {1,2,3,4,5};
  // for(int i = 0; i < 5; i++){

  //     Serial.println(i);

  // }
;}

void loop() {

  int buttonStatus = digitalRead(buttonPin);
  //Serial.println(buttonStatus);
  //delay(100);
  int buttonON = 1 - buttonStatus;

  // if(buttonON == 1){
  //     if(butPress == false){
  //       cnt++;
  //       switchLed(cnt);
  //       butPress = true;
  //     }
  //     else{}
  //   }
  //   else{
  //     if(butPress == true){
  //       butPress = false;
  //     }
  //   }
  
  if (buttonON && !butPress) {
  cnt++;
  switchLed(cnt);
  }
  butPress = buttonON;

  Serial.println(int((cnt % 2) / 2.0));  
}


void switchLed(int status){
  digitalWrite(11 + (status % 2), int((status % 4) / 2.0));
}


