import time

import paho.mqtt.client as mqtt

from sumo_traci import make_step

client = mqtt.Client()
client.connect("mqtt-broker.ru", 1883, 60)
client.loop_start()

proceed = input("Do you want to start?")

while True:
    json_data = make_step()
    client.publish("test", json_data, qos=2)
    # time.sleep(1)
