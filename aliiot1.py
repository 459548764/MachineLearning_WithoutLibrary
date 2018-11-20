
#! /usr/bin/python2
# coding = utf-8

import hmac
import hashlib
import paho.mqtt.client as mqtt
import random
import json
import time

productKey = "a1tJ24GnsQw"
deviceName = "16eThXqfQulErMbfpnzb"
deviceSecret = "yUHlM4JgG19AeVB2XjHWxr7V2Y5k6Pun"

device_data = {
    "IndoorTemperature": 12
}

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

iotSetup = AliIOT(productKey,
                  deviceName,
                  deviceSecret)

iotSetup.connect()

while(1):
    time.sleep(5)
    device_eval = json.dumps(device_data)
    device_msg = eval(device_eval)

    iotSetup.publish(device_msg)
    print("Message Sent!")
