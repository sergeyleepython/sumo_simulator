import paho.mqtt.publish as publish


def publish_to_mqtt(topic, data, hostname="mqtt-broker.ru", port=1883):
    publish.single(topic="test", payload=data, qos=2, hostname=hostname, port=port)
