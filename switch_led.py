#!/usr/bin/env python3.6
import time
import gpio
import logging
import paho.mqtt.client as mqtt


class Switcher:
    def __init__(self):
        self.local_client = mqtt.Client()
        self.local_client.on_connect = self.local_on_connect
        self.local_client.connect("localhost", 1883, 60)
        self.local_client.on_message = self.local_on_message

        self.ref_client = mqtt.Client()
        self.ref_client.on_connect = self.ref_on_connect
        self.ref_client.connect("192.168.51.239", 1883, 60)
        self.ref_client.on_message = self.ref_on_message

    def local_on_connect(self, client, userdata, flags, rc):
        print("Local connected with result code "+str(rc))
        client.subscribe("gpio/#")

    def local_on_message(self, client, userdata, msg):
        print(f"Local received msg: {msg.payload}, propagate to led/504")
        client.publish("led/504", msg.payload)

    def ref_on_connect(self, client, userdata, flags, rc):
        print("Ref connected with result code "+str(rc))
        client.subscribe("gpio/#")

    def ref_on_message(self, client, userdata, msg):
        print(f"Ref received msg: {msg.payload}, propagate to led/504 and led/505")
        client.publish("led/504", msg.payload)
        client.publish("led/505", msg.payload)

    def ref_publish_payload(self, payload):
        self.ref_client.publish("led/504", payload)
        self.ref_client.publish("led/505", payload)

    def loop(self):
        while True:
            self.local_client.loop()
            self.ref_client.loop()

    # def local_on_message_mixed(self, client, userdata, msg):
    #     self.local_on_message(client, userdata, msg)
    #     self.ref_publish_payload(msg.payload)

    def option_1(self):
        def local_on_message(client, userdata, msg):
            client.publish("led/490", msg.payload)
            self.ref_client.publish("led/504", msg.payload)

        self.local_client.on_message = local_on_message

    def option_2(self):
        def ref_on_message(client, userdata, msg):
            print("Message from NUC9")
            self.local_client.publish("led/504", msg.payload)
        
        self.ref_client.on_message = ref_on_message

    def option_3(self):
        self.option_1()
        self.option_2()

    def option_4(self):
        base_address_common_part = "192.168.51."
        last_octets = [
            231,
            232,
            233,
            234,
            235,
            237,
            238
        ]
        clients = []
        for octet in last_octets:
            client = mqtt.Client()
            try:
                client.connect(f"{base_address_common_part}{octet}", 1883, 60)
                clients.append(client)
            except ConnectionRefusedError as e:
                print(f"Octet - {octet} is broken")
        
        clients.append(self.local_client)
        clients.append(self.ref_client)

        def local_on_message(client, userdata, msg):
            # client.publish("led/490", msg.payload)
            print("Received")
            for other_client in clients:
                other_client.publish("led/504", msg.payload)
            # self.ref_client.publish("led/504", msg.payload)

        print(f"Connected clients:{len(clients)}")
        self.local_client.on_message = local_on_message




# def create_switcher_for_local_led():
#     def on_connect(client, userdata, flags, rc):
#         print("Local connected with result code "+str(rc))
#         client.subscribe("gpio/#")

#     def on_message(client, userdata, msg):
#         # print(msg.topic+" "+str(msg.payload))
#         print(f"Local received msg: {msg.payload}, propagate to led/504")
#         client.publish("led/504", msg.payload)

#     client = mqtt.Client()
#     client.on_connect = on_connect
#     client.on_message = on_message
#     client.connect("localhost", 1883, 60)

#     return client

# def create_switchef_for_ref_led():
#     def on_connect(client, userdata, flags, rc):
#         print("Ref connected with result code "+str(rc))
#         client.subscribe("gpio/#")

#     def on_message(client, userdata, msg):
#         # print(msg.topic+" "+str(msg.payload))
#         print(f"Ref received msg: {msg.payload}, propagate to led/504 and led/505")
#         client.publish("led/504", "0")#msg.payload)
#         client.publish("led/505", "0")#msg.payload)

#     client = mqtt.Client()
#     client.on_connect = on_connect
#     client.on_message = on_message
#     client.connect("192.168.51.239", 1883, 60)

#     return client

if __name__ == "__main__":
    switcher = Switcher()
    # switcher.option_4()
    switcher.loop()
    # local_client = create_switcher_for_local_led()
    # ref_client = create_switchef_for_ref_led()
    # while True:
    #     local_client.loop()
    #     ref_client.loop()


# client.loop_forever()