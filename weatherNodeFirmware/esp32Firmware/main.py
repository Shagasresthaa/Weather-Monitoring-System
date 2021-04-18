from machine import Pin, SoftI2C, ADC, SPI
from ds3231_port import DS3231
import urequests as requests
import sdcard, os
import nodeConf
import network
import ssd1306
import bmp280
import dht
import time
import ujson

node_id = nodeConf.nodeId
mac_id = nodeConf.macId
loct = nodeConf.loc
wlan = nodeConf.wlanId
wlanpass = nodeConf.wlanPass

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect(wlan, wlanpass)
    while not sta_if.isconnected():
        pass
print('network config:', sta_if.ifconfig())

#SD Card Init
spi = SPI(sck=Pin(18),miso=Pin(19),mosi=Pin(23))
spi.init()
sd = sdcard.SDCard(spi, Pin(2))
vfs = os.VfsFat(sd)
os.mount(vfs, "/fc")
print("Filesystem check")
print(os.listdir("/fc"))


#oled init
i2c = SoftI2C(scl=Pin(22),sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128,64,i2c,addr=0x3C)
oled.fill(0)

#DHT init
sensor = dht.DHT22(Pin(5))

#BMP280 init
bmp=bmp280.BMP280(i2c,addr=0x76)
bmp.use_case(bmp280.BMP280_CASE_WEATHER)

#ML8511 init
def mapfloat(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#DS3131 init
ds3231 = DS3231(i2c)
#ds3231.save_time()

#ML8511 init
uvLevel = ADC(Pin(34))
refLevel = ADC(Pin(35))
uvLevel.atten(ADC.ATTN_11DB)
refLevel.atten(ADC.ATTN_11DB)

def writeDataToSDCard(data):
    logPath = "/fc/dataCollected.log"
    dataPath = "/fc/datalog.csv"

    with open(logPath,'a') as file1:
        file1.write(data)
        file1.close()
    with open(dataPath,'a') as file2:
        file2.write(data)
        file2.close()

def getRequestIdAuth():
    requrl = "https://weather-main17.herokuapp.com/getReqIdAuth/" + node_id + "/" + mac_id
    res = requests.get(requrl)
    respdata = ujson.dumps(res.json())
    fin = ujson.loads(respdata)
    return fin["reqid"]

def sendDataToApi(wdata):
    data = wdata
    rqid = getRequestIdAuth()
    requrl = "https://weather-main17.herokuapp.com/postData/" + rqid + "/" + mac_id + "/" + node_id + "/" + loct + "/" + wdata
    res = requests.get(requrl)
    respdata = ujson.dumps(res.json())
    fin = ujson.loads(respdata)
    
    respCode = fin["status_code"]
    
    if respCode == 201:
        print("successful")
    else:
        print("retrying")
        sendDataToApi(data)

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
    except OSError as e:
        print('Failed to read sensor.')
    
    ref3v3 = refLevel.read()
    uvinten = uvLevel.read()
    outputVoltage = 3.3 / ref3v3 * uvinten
    uvIntensity = mapfloat(outputVoltage, 0.99, 2.8, 0.0, 15.0)
    
    bmp.oversample(bmp280.BMP280_OS_HIGH)
    T = "Temp: " + str(temp) + " C"
    H = "Humd: " + str(hum) + " %"
    P = "Pres: " + str(str(round(bmp.pressure/101325,2))) + " atm"
    uvin = "UVIn: " + str(round(uvIntensity,2))
    
    Y, Mon, D, Hr, M, S = ds3231.get_time()[0], ds3231.get_time()[1], ds3231.get_time()[2], ds3231.get_time()[3], ds3231.get_time()[4], ds3231.get_time()[5]
    cDate = str(Y) + "-" + str(Mon) + "-" + str(D)
    cTime = str(Hr) + ":" + str(M) + ":" + str(S)
    timeStamp = cDate + "+" + cTime
    ts1 = cDate + " " + cTime
    print(ts1)
    data = ts1 + "/" + str(temp) + "/" + str(bmp.pressure/101325) + "/" + str(hum) + "/" + str(abs(round(uvIntensity,2))) + "\n"
    dt1 = timeStamp + "/" + str(temp) + "/" + str(bmp.pressure/101325) + "/" + str(hum) + "/" + str(abs(round(uvIntensity,2)))
    
    oled.fill(0)
    oled.text(cDate,30,0)
    oled.text(cTime,36,10)
    oled.text(T,0,20)
    oled.text(H,0,30)
    oled.text(P,0,40)
    oled.text(uvin,0,50)
    oled.show()
    
    writeDataToSDCard(data)
    sendDataToApi(dt1)
    time.sleep(30)