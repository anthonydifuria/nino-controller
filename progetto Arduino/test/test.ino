//blocco di codice globale, in cui mettiamo variabili globli e funzioni globali
//poi all'interno di {} ci sono le vabiabili e funzioni locali - quindi locali all'interno delle funzioni

//da chiarire: potrebbe essere possibile fare un codice ardunio senza  utilizzare setup o loop
int myLed = 8;
float pi = 3.14;




int add(int num1,int num2) {
return num1 + num2;
}


int x = 0;

void increaseX(){
 x = x + 1;
 return;
}

void setup() {
  //gestione degli stati inziali di varibili funzioni o altro, esempio che tipo di pin ho o altro
  Serial.begin(9600);
  
  int result = add(1,2);
  //increaseX();

}

void loop() {
  //è il proceswso che continua ad essere eseguito in loop a runtime
  
}


