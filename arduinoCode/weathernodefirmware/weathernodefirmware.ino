#include "DHT.h"
#include <Arduino.h>
#include <U8g2lib.h>
#include <Wire.h>
#include "RTClib.h"
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP085_U.h>

#ifdef U8X8_HAVE_HW_SPI
#include <SPI.h>
#endif
#ifdef U8X8_HAVE_HW_I2C
#include <Wire.h>
#endif

#define DHTPIN PB4   
#define DHTTYPE DHT22 

RTC_DS1307 rtc;
Adafruit_BMP085_Unified bmp = Adafruit_BMP085_Unified(10085);
//Use for SSD1306 based oled
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, LED_BUILTIN); 
//Use for SH1106 based oled
//U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, LED_BUILTIN);
DHT dht(DHTPIN, DHTTYPE);

char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
int UVOUT = PA0; //Output from the sensor
int REF_3V3 = PA1; //3.3V power on the STM32 Board

//Logo Bitmap Byte Array
#pragma once
#define JS2HF5_BMPWIDTH  80
#define JS2HF5_BMPHEIGHT  35

static const unsigned char bitmap_js2hf5[] PROGMEM = {
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7f, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
  0xff, 0xfe, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xf7, 0xff, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x68, 0x3f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0xf8, 0x00, 0x1f, 
  0xc0, 0x00, 0x00, 0x00, 0x00, 0x01, 0xe0, 0x07, 0x80, 0x03, 0xc0, 0x00, 0x00, 0x00, 0x00, 0xff, 
  0x00, 0x00, 0xe0, 0x0f, 0xc0, 0x00, 0x00, 0x00, 0x07, 0x8c, 0x00, 0x00, 0x38, 0x07, 0xe0, 0x00, 
  0x00, 0x00, 0x0c, 0x08, 0x00, 0x00, 0x7f, 0x07, 0xc0, 0x00, 0x00, 0x00, 0x18, 0x10, 0x00, 0x01, 
  0x81, 0xe1, 0xc0, 0x00, 0x00, 0x00, 0x68, 0x00, 0x00, 0x04, 0x00, 0x38, 0xc0, 0x00, 0x00, 0x01, 
  0xf8, 0x00, 0x00, 0x00, 0x00, 0x0e, 0x00, 0x00, 0x00, 0x03, 0x18, 0x00, 0x00, 0x00, 0x00, 0x07, 
  0x00, 0x00, 0x00, 0x06, 0x0c, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 
  0x00, 0x0c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x01, 0x80, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x04, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 
  0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x1c, 0x00, 0x00, 0x00, 0x00, 0xe0, 0x00, 
  0x00, 0x00, 0x00, 0x70, 0x00, 0x00, 0x00, 0x00, 0x3f, 0xff, 0xff, 0xff, 0xff, 0x80, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
};

void setup() {
  //DS3231 RTC module init
  while (!Serial); // for Leonardo/Micro/Zero
  Serial.begin(57600);
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  }
  // Remove the NOT symbol (!) in below 'if' condition if module was previously initialised so fresh date may be uploaded
  if (!rtc.isrunning()) {
    Serial.println("RTC is NOT running!");
    // Takes the time at which sketch was compiled
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    // For explicit time setting
    // rtc.adjust(DateTime(2021, 1, 26, 13,54, 0));
  }

  //BMP180/BMP280 init
  Serial.println("Pressure Sensor Test"); Serial.println("");
  if(!bmp.begin())
  {
    Serial.print("Ooops, no BMP085 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  
  //DHT22 init
  Serial.begin(9600);
  Serial.println(F("DHTxx test!"));
  dht.begin();

  //UV Sensor Init
  pinMode(UVOUT, INPUT);
  pinMode(REF_3V3, INPUT);
  Serial.println("ML8511 example");

  //U8G2 init
  u8g2.begin();
  u8g2.enableUTF8Print();
  u8g2.setFontDirection(0);
  displayLogo();
}

//Shows logo on bootup
void displayLogo(){
  u8g2.clearDisplay();
  u8g2.drawBitmap(25, 0, JS2HF5_BMPWIDTH/8, JS2HF5_BMPHEIGHT, bitmap_js2hf5);
  u8g2.setCursor(0, 50);
  u8g2.setFont(u8g2_font_unifont_t_latin);             
  u8g2.print("Weather Node V6");
  u8g2.sendBuffer();
  delay(3500);
}

int averageAnalogRead(int pinToRead)
{
  byte numberOfReadings = 8;
  unsigned int runningValue = 0; 
 
  for(int x = 0 ; x < numberOfReadings ; x++)
    runningValue += analogRead(pinToRead);
  runningValue /= numberOfReadings;
 
  return(runningValue);
}
 
float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void loop() {
 DateTime now = rtc.now();
  String yr = String(now.year());
  String mnth = String(now.month(),DEC);
  String dy = String(now.day());
  String hr = String(now.hour());
  String mn = String(now.minute());
  String sc = String(now.second());
  String dtme = dy + "/" + mnth + "/" + yr + " " + hr + ":" + mn + ":" + sc;
  String dt = dy + "/" + mnth + "/" + yr;
  String tm = " " + hr + ":" + mn + ":" + sc;
  Serial.println(dtme);
  Serial.println(dt);
  Serial.println(tm);

  float pres;
  float temperature;
  float slp;
  float alti;
  
  sensors_event_t event;
  bmp.getEvent(&event);
  if (event.pressure)
  {
    pres = event.pressure*0.000987;
    bmp.getTemperature(&temperature);
    slp = SENSORS_PRESSURE_SEALEVELHPA;
    alti = bmp.pressureToAltitude(slp,event.pressure);
  }
  else
  {
    Serial.println("Sensor error");
  }
  
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);
  
  int uvLevel = averageAnalogRead(UVOUT);
  int refLevel = averageAnalogRead(REF_3V3);
  float outputVoltage = 3.3 / refLevel * uvLevel;
  float uvIntensity = mapfloat(outputVoltage, 0.99, 2.8, 0.0, 15.0); //Convert the voltage to a UV intensity level
  Serial.print("UV Intensity (mW/cm^2): ");
  Serial.println(uvIntensity);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  //Display on oled Display
  u8g2.clearBuffer();                   
  u8g2.setFont(u8g2_font_6x12_tr);
  u8g2.setCursor(10, 10);
  u8g2.print(dt);
  u8g2.println(tm);
  
  u8g2.setCursor(0, 20);              
  u8g2.print("Temp: ");
  u8g2.print(temperature);
  u8g2.println(" C");
  
  u8g2.setCursor(0, 30);              
  u8g2.print("Pres: ");
  u8g2.print(pres);
  u8g2.println(" atm");
  
  u8g2.setCursor(0, 40); 
  u8g2.print("Humd: ");
  u8g2.print(h);
  u8g2.println(" %");
  
  u8g2.setCursor(0, 50); 
  u8g2.print("HIdx: ");
  u8g2.print(hic);
  u8g2.println(" C");
    
  u8g2.setCursor(0, 60); 
  u8g2.print("UVIN: ");
  u8g2.print(uvIntensity);
  u8g2.println(" mW/cm^2");
  u8g2.sendBuffer();

  delay(1000);
}
