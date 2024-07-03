import paho.mqtt.client as mqtt
from utils import MsgProcessing, BLE_Conversions
from config import CONFIG as cfg
import copy
import time
# Define the MQTT broker details
BROKER = '0.0.0.0'
PORT = 1883
KEEPALIVE = 60

# Define the topics
TOPIC_SEEKER = 'device/seeker/#'
TOPIC_GOAL_STATE = 'devices/goal_device'
REGISTRATION = 'register'
ACK = 'ack'

# Tuning params
update_delta = cfg.DATA_EXPIRY_TIME

# Connected Devices mapping
connectedDevices = []
# live dict of devices around different devices 
live_rssi_vals = {}

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
    global live_rssi_vals
    # Update the live dict with the RSSI ßvals
    # print(f"Received seeker message")
    obj = MsgProcessing.process_msg_data(payload)
    dev_id = obj.metadata.deviceID
    
    live_rssi_vals[dev_id] =live_rssi_vals.get(dev_id,{})
    # print(live_rssi_vals[dev_id][obj.data[0]] 
    live_rssi_vals[dev_id][obj.data[0]] = {'rssi':obj.data[1],
                                           'last_updated':time.time()}

def handle_goal_state_message(payload):
    print(f"Received goal state message: {payload}")
    # Process the goal state message here
    # For example, update the goal state information

def device_registration(payload):
    global connectedDevices
    # print(f'Received registration request from {payload}')
    connectedDevices.append(payload)
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
client.loop_start()
start_time = time.time()
while True:
    if live_rssi_vals!={} and cfg.VERBOSE>=3:
        print(live_rssi_vals)
        
    # Get the most relevant data from the live rssi dict
    now_time = time.time()
    if now_time - start_time >= update_delta:
        start_time = now_time
        # remove unwanted keys from the livedict and data
        for dev_id in live_rssi_vals:
            old_keys = MsgProcessing.get_old_keys(live_rssi_vals[dev_id])
            if len(old_keys)!=0:
                # remove keys
                print(f'---- Removing device from live_rssi_dict----  \n\tNames: {old_keys}\n\t')
                for k in old_keys:
                    live_rssi_vals[dev_id].pop(k, None)
            
                # Calc the distances for the devices
            for bt_id in live_rssi_vals[dev_id]:
                dist =  BLE_Conversions.rssi_to_dist(
                        int(live_rssi_vals[dev_id][bt_id]['rssi']), bt_id)
                live_rssi_vals[dev_id][bt_id]['dist'] = dist
        data = copy.copy(live_rssi_vals)
        
        print("Data", data)
        
    


    time.sleep(0.05)
        
        
        
        