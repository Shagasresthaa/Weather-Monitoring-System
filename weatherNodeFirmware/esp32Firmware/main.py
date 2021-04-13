from machine import SPI, I2C, Pin, ADC
from ssd1306 import SSD1306_I2C
from DHT22 import DHT22
from ds3231_port import DS3231
import os, sdcard
import bmp280
import eepromLib
import time

#SD Card init
spi = SPI(1,sck=machine.Pin(10),miso=machine.Pin(12),mosi=machine.Pin(11))
spi.init()
sd = sdcard.SDCard(spi, machine.Pin(13))
vfs = os.VfsFat(sd)
os.mount(vfs, "/fc")
print("Filesystem check")
print(os.listdir("/fc"))

#ML8511 init
def mapfloat(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
uvLevel = ADC(Pin(26))
refLevel = ADC(Pin(27)) 

#Oled init
i2c = I2C(1,sda=Pin(14),scl=Pin(15))
oled = SSD1306_I2C(128, 64, i2c,addr=0x3C)
oled.fill(0)

#DHT22 init
dht22 = DHT22(Pin(28,Pin.IN,Pin.PULL_UP))

#BMP280 init
bmp=bmp280.BMP280(i2c,addr=0x76)
bmp.use_case(bmp280.BMP280_CASE_WEATHER)

#DS3131 init
ds3231 = DS3231(i2c)

#EEPROM init
epromI2C = I2C(0,sda=Pin(4),scl=Pin(5))
epromI2Caddr = 80
eeprom = eepromLib.CAT24C32(epromI2C,epromI2Caddr)

tempList = []
presList = []
humdList = []
uvinList = []
count = 0

def writeDataToSDCard(data):
    logPath = "/fc/dataCollected.log"
    dataPath = "/fc/datalog.csv"
    
    with open(logPath,'a') as file1:
        file1.write(data)
        file1.close()
    with open(dataPath,'a') as file2:
        file2.write(data)
        file2.close()
        
def writeDataToEEPROM():
    print("TBA")
        
while True:
    T, H = dht22.read()
    ref3v3 = refLevel.read_u16()
    uvinten = uvLevel.read_u16()
    outputVoltage = 3.3 / ref3v3 * uvinten
    uvIntensity = mapfloat(outputVoltage, 0.99, 2.8, 0.0, 15.0)
    bmp.oversample(bmp280.BMP280_OS_HIGH)
    Y, Mon, D, Hr, M, S = ds3231.get_time()[0], ds3231.get_time()[1], ds3231.get_time()[2], ds3231.get_time()[3], ds3231.get_time()[4], ds3231.get_time()[5]
    cDate = str(D) + "-" + str(Mon) + "-" + str(Y)
    cTime = str(Hr) + ":" + str(M) + ":" + str(S)
    timeStamp = cDate + " " + cTime
    data = timeStamp + "," + str(T) + "," + str(round(bmp.pressure/101325,2)) + "," + str(H) + "," + str(round(uvIntensity,2)) + "\n"
    writeDataToSDCard(data)
    if T is None:
        print("Sensor Error")
        
    temp = "Temp: " + str(T) + " C"
    pres = "Pres: " + str(round(bmp.pressure/101325,2)) + " atm"
    humd = "Humd: " + str(H) + " %"
    uvin = "UVIn: " + str(round(uvIntensity,2))
        
    #oled display code
    
    oled.fill(0)
    oled.text(cDate,30,0)
    oled.text(cTime,36,10)
    oled.text(temp,0,20)
    oled.text(pres,0,30)
    oled.text(humd,0,40)
    oled.text(uvin,0,50)
    oled.show()
    
    
    if(count == 59):
        tsum = sum(tempList)
        psum = sum(presList)
        hsum = sum(humdList)
        usum = sum(uvinList)
        tavg = tsum/60
        pavg = psum/60
        havg = hsum/60
        uavg = usum/60
        dt = timeStamp + "," + str(tavg) + "," + str(pavg) + "," + str(havg) + "," + str(uavg)
        print(dt)
        tempList.clear()
        presList.clear()
        humdList.clear()
        uvinList.clear()
        count = 0
    else:
        tempList.append(T)
        presList.append(bmp.pressure/101325)
        humdList.append(H)
        uvinList.append(round(uvIntensity,2))
        count+=1
    
    time.sleep_ms(1000)

'''
#write data
fn = "/fc/rats.txt"
with open(fn, "w") as f:
    n = f.write(lines)
'''