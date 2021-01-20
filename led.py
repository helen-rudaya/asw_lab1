#!/usr/bin/env python3.6
import time
import gpio
import logging
import paho.mqtt.client as mqtt

gpio.setup(504, gpio.OUT)
gpio.log.setLevel(logging.INFO)

import paho.mqtt.client as mqtt
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("led/#")

def on_message(client, userdata, msg):
    print(f"Received msg: {msg.payload}, switching setting LED to state: {int(msg.payload)}")
    gpio.set(504, int(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)

client.loop_forever()