#include <WiFiS3.h>
#include <Wire.h>
#include "ICM_20948.h"
#include <ArduinoOSCWiFi.h>

//SENSORE
ICM_20948_I2C imu;

//WIFI
char ssid[] = "TP-LINK_36A8";
char pass[] = "81515431";

//OSC
char hostIP[] = "192.168.0.104";
int hostPort = 8000;

//per printare in modo concatenato
char print_buffer[200]; 

void setup() {
  //init SERIAL 
  Serial.begin(115200);
  while(!Serial);

  //init WIFI
  WiFi.begin(ssid, pass);
  Serial.print("Connection WiFi ");
  while(WiFi.status() != WL_CONNECTED){
    Serial.print(".");
  }
  Serial.println();
  Serial.print("IP host: ");
  Serial.println(WiFi.localIP());

  //init SENSOR
  Wire.begin();
  Serial.println("IMU is starting...");
  while(imu.begin(Wire, 0x68) != ICM_20948_Stat_Ok){
    Serial.println("ERROR: Check the IMU connection...");
    delay(1000);
  }
  Serial.println("IMU detected!");
}

void loop() {
  if(imu.dataReady()){
    imu.getAGMT();

    OscWiFi.send(hostIP, hostPort, "/imu/accData", imu.accX(), imu.accY(), imu.accZ());
    OscWiFi.send(hostIP, hostPort, "/imu/gyrData", imu.gyrX(), imu.gyrY(), imu.gyrZ());
    OscWiFi.send(hostIP, hostPort, "/imu/magData", imu.magX(), imu.magY(), imu.magZ());

    // sprintf(print_buffer,
    //   "accX: %f, accY: %f, accZ: %f\n"
    //   "gyroX: %f, gyroY: %f, gyroZ: %f\n"
    //   "magX: %f, magY: %f, magZ: %f\n",
    //   imu.accX(), imu.accY(), imu.accZ(),
    //   imu.gyrX(), imu.gyrY(), imu.gyrZ(),
    //   imu.magX(), imu.magY(), imu.magZ());
    // Serial.println(print_buffer);
    // delay(100); 
  }
}



