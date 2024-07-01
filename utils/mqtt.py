import paho.mqtt.client as mqtt
from typing import List

class MQTT():
    def __init__(self) -> None:
        self.client = mqtt.Client(userdata={'registered': False})
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
    
    def connect(self, host='localhost', port='1883', keepalive=60):
        self.client.connect(host, port, keepalive)
        
    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}, {userdata}")
    
    def on_message(self, client, userdata, message):
        pass
    
    def subscribe(self, topics:List[str]):
        for topic in topics:
            self.client.subscribe(topic)

    def publish(self, topic, payload, qos=0, retain = False):
        self.client.publish(topic=topic, payload=payload, qos=qos,
                            retain=retain)
    
    def loop(self):
        self.client.loop_forever()
        