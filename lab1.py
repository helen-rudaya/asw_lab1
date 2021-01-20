#!/usr/bin/env python3.6
import time
import gpio
import logging
import paho.mqtt.client as mqtt


client = mqtt.Client()
client.connect("localhost", 1883, 60)

gpio.setup(504, gpio.OUT)
gpio.setup(488, gpio.IN)
gpio.log.setLevel(logging.INFO)
current_state = gpio.read(488)
while(True):
    new_state = gpio.read(488)
    if current_state != new_state:
        current_state = new_state
        print(f"Button pressed, change to {'ENABLED' if current_state == 1 else 'DISABLED'}")
        client.publish("gpio/488", current_state)
        # gpio.set(504, current_state)
        #gpio/488,:0 / gpio/488,:1