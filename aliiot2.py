
#! /usr/bin/python2
# coding = utf-8

import hmac
import hashlib
import paho.mqtt.client as mqtt
import random
import json
import time
import queue
import serial
import threading

productKey = "a1tJ24GnsQw"
deviceName = "9QFzxApnsiQX0Yyebzua"
deviceSecret = "ICYe4YefN0YhFF19EQk4pY289MiXd2eg"

class AliIOT():
    host = ".iot-as-mqtt.cn-shanghai.aliyuncs.com"
    propertyTopic = "/sys/%s/%s/thing/event/property/post"

    def __init__(self,
                 productKey,
                 deviceName,
                 deviceSecret):
        self._productKey = productKey
        self._deviceName = deviceName
        self._deviceSecret = deviceSecret

        self._hostId = self._productKey + self.host
        self._propertyTopic = self.propertyTopic % (self._productKey, self._deviceName)
        self._clientId = "%s&&&%s|securemode=3,signmethod=hmacsha1,gw=1|" % (self._productKey, self._deviceName)

        self._mqttUsername = self._deviceName + "&" + self._productKey
        signContent = "clientId%sdeviceName%sproductKey%s" % (self._productKey + "&&&" + self._deviceName,
                                                              self._deviceName,
                                                              self._productKey)
        self._mqttPassword = hmac.new(str.encode(self._deviceSecret),
                                      str.encode(signContent),
                                      hashlib.sha1).hexdigest()

    def connect(self):
        self.mqttc = mqtt.Client(client_id = self._clientId,
                                 clean_session=True)
        self.mqttc.username_pw_set(self._mqttUsername,
                                   self._mqttPassword)

        mqttc_state = self.mqttc.on_connect
        mqttc_state = self.mqttc.on_disconnect
        mqttc_state = self.mqttc.on_message

        self.mqttc.connect(host = self._hostId,
                           port=1883,
                           keepalive=60)
        self.mqttc.loop_start()

    def publish(self,index):
        payload = {
            "id": random.randint(100, 100000),
            "version": "1.0",
            "params": index,
            "method": "thing.event.property.post"
        }
        self.mqttc.publish(self._propertyTopic,json.dumps(payload),qos=1)

serial01 = serial.Serial('/dev/ttyUSB0',115200,timeout = 0.5)
q = queue.Queue()
iotSetup = AliIOT(productKey,
                  deviceName,
                  deviceSecret)

iotSetup.connect()

device_data = {
    "IndoorTemperature": 12
}

def Produce():
    while(1):
        cnt = serial01.inWaiting()
        if(cnt != 0):
            pipe1 = serial01.read(cnt)
            message1 = pipe1.decode('ISO-8859-1')
            if(q.full() == False):
                q.put(message1)
        serial01.flushInput()
        time.sleep(0.1)
    
def Analysis():
    while(1):
        time.sleep(5)
        recv = q.get()
        print(recv[0:3])
        device_data['IndoorTemperature'] = int(recv[0:3])
        device_eval = json.dumps(device_data)
        device_msg = eval(device_eval)

        iotSetup.publish(device_msg)
        print("Message Sent!")

first = threading.Thread(target=Produce,name='')
second = threading.Thread(target=Analysis,name='')
first.start()
second.start()

