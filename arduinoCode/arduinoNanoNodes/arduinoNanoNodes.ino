#include <Wire.h>
#include <Adafruit_BMP085.h>
#include <SPI.h>
#include <SD.h>
#include <SimpleDHT.h>
#include "SSD1306Ascii.h"
#include "SSD1306AsciiWire.h"

#define pinDHT11 8
#define I2C_ADDRESS 0x3C
#define RST_PIN -1

SimpleDHT11 dht11(pinDHT11);
Adafruit_BMP085 bmp;
SSD1306AsciiWire oled;

void setup() {
  Serial.begin(9600);

  //All init code in this block

  //BMP180 INIT
  if (!bmp.begin()) {
  Serial.println("Could not find a valid BMP085 sensor, check wiring!");
  while (1) {}
  }
  
  //OLED INIT
  Wire.begin();
  Wire.setClock(400000L);
  #if RST_PIN >= 0
  oled.begin(&Adafruit128x32, I2C_ADDRESS, RST_PIN);
  #else // RST_PIN >= 0
  oled.begin(&Adafruit128x32, I2C_ADDRESS);
  #endif // RST_PIN >= 0

 //SD Card init
 Serial.print("Initializing SD card...");

 // See if the card is present and can be initialized:
 if (!SD.begin(10)) {
   Serial.println("Card failed, or not present");
   // don't do anything more:
   while (1);
 }
  Serial.println("card initialized.");
  
}

void loop() {

  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(NULL, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT11 failed, err="); Serial.println(err);delay(1000);
    return;
  }
  
  float temp,pres,alti,humd;
  temp = bmp.readTemperature();
  pres = bmp.readPressure()/1000;
  alti = bmp.readAltitude(101500);
  humd = float(humidity);

  String fin = String(temp)+","+String(pres)+","+String(alti)+","+String(humd)+"\n";
  Serial.println(fin);

  //OLED starts
  oled.setFont(Adafruit5x7);
  uint32_t m = micros();
  oled.clear();
  oled.print("Temp:");
  oled.print(temp);
  oled.println(" 'C");
  oled.print("Pres:");
  oled.print(pres);
  oled.println(" KPa");
  oled.print("Alti:");
  oled.print(alti);
  oled.println(" mtrs");
  oled.print("Humd:");
  oled.print(humd);
  oled.println(" g/m-3");
//OLED ends

//SD Card
  File DataFile = SD.open("datalog.txt", FILE_WRITE);
  if(DataFile){
    DataFile.println(fin);
    DataFile.close();
  }
//SD Card Code ends
  delay(1000);
}
