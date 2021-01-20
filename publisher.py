import paho.mqtt.client as mqtt
import time
client = mqtt.Client()
client.connect("localhost", 1883, 60)
while(True):
    client.publish("led/504", "1")
    time.sleep(0.5)
    client.publish("led/504", "0")
    time.sleep(0.5)