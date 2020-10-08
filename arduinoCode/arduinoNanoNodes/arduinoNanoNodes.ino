#include <Wire.h>
#include <Adafruit_BMP085.h>

#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels

//DHT11 config
#include <SimpleDHT.h>
#define pinDHT11 8
SimpleDHT11 dht11(pinDHT11);

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET     4 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

Adafruit_BMP085 bmp;

void setup() {
  Serial.begin(9600);
  if (!bmp.begin()) {
  Serial.println("Could not find a valid BMP085 sensor, check wiring!");
  while (1) {}
  }

  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3C for 128x32
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }
}

void loop() {

  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT11 failed, err="); Serial.println(err);delay(1000);
    return;
  }
  
  float temp,pres,alti,humd;
  temp = bmp.readTemperature();
  pres = bmp.readPressure()/1000;
  alti = bmp.readAltitude(101500);
  humd = float(humidity);
  
  display.clearDisplay();
  display.setTextSize(1);      // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE); // Draw white text
  display.setCursor(0, 0);     // Start at top-left corner
  display.print("Temp = ");
  display.print(temp);
  display.println(" C");
  display.print("Pres = ");
  display.print(pres);
  display.println(" KPa");
  display.print("Alti = ");
  display.print(alti);
  display.println(" meters");
  display.print("Humd = ");
  display.print(humd);
  display.println(" g/m-3");
  display.display();
  delay(2000);

    
  Serial.print("Temperature = ");
  Serial.print(temp);
  Serial.println(" *C");

  Serial.print("Pressure = ");
  Serial.print(pres);
  Serial.println(" KPa");

  Serial.print("Real altitude = ");
  Serial.print(alti);
  Serial.println(" meters");

  Serial.print("Humidity = ");
  Serial.println(humd);
  Serial.println(" meters");
    
  Serial.println();
  delay(500);
}
