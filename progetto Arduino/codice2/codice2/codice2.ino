//primo codice 
//prima cosa dobbiamo definire la board per definire una serie di cose all'interno della board.
//andiamo a recuperare quella varibile e proviamo ad accendere e spegnere quel led
//le variabili in maiuscolo sono tutte costanti

//cercare elettronica per maker libro
//the art of electronics cercare libro


void setup() {
  // Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT); 

}

void loop() {

  digitalWrite(LED_BUILTIN,HIGH); //stiamo accendendo il led
  delay(1000);
  digitalWrite(LED_BUILTIN,LOW);
  delay(1000);

}


