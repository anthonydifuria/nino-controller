// C++ code
//

float sensorValue = 0.0;

int orangeLed = 3;
int knobDig = 5;

void setup()
{
  Serial.begin(9600);
  
  pinMode(orangeLed, OUTPUT);
  pinMode(knobDig, INPUT);
  
}

void loop()
{
  sensorValue = analogRead(A0); 

  //Serial.println(sensorValue);
  //digitalWrite();
  
  analogWrite(orangeLed, analogRead(knobDig));
  Serial.println(analogRead(knobDig));
  delay(100);
}