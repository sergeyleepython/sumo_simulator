import time

import paho.mqtt.client as mqtt

from sumo_traci import make_step


def run():
    client = mqtt.Client()
    client.connect("35.189.64.191", 1883, 60)
    client.loop_start()

    proceed = input("Do you want to start?")

    while True:
        jsons = make_step()
        for json_data in jsons:
            client.publish("test", json_data, qos=2)
            time.sleep(2)


if __name__ == '__main__':
    run()
