# Weather-Monitoring-System
A simple weather monitoring system using arduino, raspberry pi,Mobile application and a Python Flask based REST API

Mobile Login Authentication system uses Firebase.

Working on an SMD version of the node. Components for this will be marked with "*".

ATMEGA2560 16 AU will be used for this version due to more SRAM and program memory bypassing the memory restrictions due to an Arduino Nano running ATMEGA328P AU.

The bootloader burner to be used for this is also included in project including schematics, gerber files.

Arduino bootloader will be used for this ATMEGA2560.

# This is project is work in progress
All the work is licensed under GNU General Public License V3 which can be found in the project

This is a simple weather monitoring project for monitoring temperature, preasure and humidity using arduino nano nodes and a raspbery pi to upload the data to a custom REST API from which data can be retreived to a mobile application for remote monitoring

## Arduino Libraries Used

1. Adafruit GFX library
2. Adafruit SSD1306
3. Adafruit ESP8266
4. AdaFruit BMP085
5. Simple DHT11
6. Software Serial
7. Wire.h

## Components Used

1. Arduino Nano V3
2. Arduino Uno R3 (For receiving data from nodes)
3. Raspbery Pi 4 Model B (4GB) (Any raspbery pi can be used. I used 4 gb version in view of other personal uses)
4. 0.91 inch oled display (Used SSD1306 driver)
5. MicroSD Card Module (For backup data logging and logging node error events)
6. BMP180 sensor (Uses Adafruit BMP085 library)
7. DHT11 sensor (Uses Simple DHT Library)
8. 3 resistors (1k,2/2.2k,10k for ESP8266)
9. A 3S Lipo Battery (Not finalized as of yet)
10. ATMEGA 2560 16 AU *
11. 16MHz Crystal Oscilator *
12. Blue 0805 package LED x2 *
13. 22pf 0603 package capacitor x2 *
14. 1K resistors 0603 package x2 *
15. AMS1117 5V SMD package *
16. 100nf(0.1uf) 0402 package capacitor x2 *
17. 10uf 0805 package capacitor x2 *
18. DHT22 sensor *
19. Micro SD card module *

Components marked with * are to be used in the SMD Edition of the monitoring node.

## More to be added as project progresses
