import paho.mqtt.client as mqtt
from utils import process_msg_data

# Define the MQTT broker details
BROKER = '127.0.0.1'
PORT = 1883
KEEPALIVE = 60

# Define the topics
TOPIC_SEEKER = 'device/seeker/#'
TOPIC_GOAL_STATE = 'devices/goal_device'
REGISTRATION = 'register'
ACK = 'ack'

# Connected Devices mapping
connectedDevices = {}

# Define the callback function for when a message is received
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode('utf-8')
    
    if 'device/seeker' in topic:
        handle_seeker_message(payload)
    elif topic == TOPIC_GOAL_STATE:
        handle_goal_state_message(payload)
    elif topic == REGISTRATION:
        is_registered = device_registration(payload)
        if is_registered:
            client.publish(f'{ACK}/{payload}', '200')

def handle_seeker_message(payload):
    print(f"Received seeker message")
    obj = process_msg_data(payload)
    print(obj)
    # Process the seeker message here
    # For example, update the state of the seeker

def handle_goal_state_message(payload):
    print(f"Received goal state message: {payload}")
    # Process the goal state message here
    # For example, update the goal state information

def device_registration(payload):
    global connectedDevices
    print(f'Received registration request from {payload}')
    connectedDevices = {payload:True}
    return True


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    
# Create the MQTT client
client = mqtt.Client()

# Assign the on_message callback function
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(BROKER, PORT, KEEPALIVE)

# Subscribe to the relevant topics
client.subscribe(TOPIC_SEEKER)
client.subscribe(TOPIC_GOAL_STATE)
client.subscribe(REGISTRATION)

# Start the MQTT client loop
client.loop_forever()