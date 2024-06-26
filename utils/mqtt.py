import paho.mqtt.client as mqtt


class MQTT:
    def __init__(self, host='localhost', port='1883') -> None:
        self.client = mqtt.Client(userdata={'registered': False})
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
    
    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}, {userdata}")
    
    def on_message(self, client, userdata, message):
        pass
    
    def publish(self, topic, payload, qos=0, retain = False):
        self.client.publish(topic=topic, payload=payload, qos=qos,
                            retain=retain)
        