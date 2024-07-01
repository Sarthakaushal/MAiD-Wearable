import asyncio
from bleak import BleakScanner 
import paho.mqtt.client as mqtt
import time
from edge.conf import BT_Loc
from queue import Queue
from core import BleScanner
async def scan_devices():
    scanner = BleakScanner()

    devices = await scanner.discover()
    for device in devices:
        if device.name:
            print(f"Device: {device.name}, Address: {device.address}, RSSI: {device.rssi}")




async def scan_bluetooth_devices():
    devices = await BleakScanner.discover()
    rssi_values = {device.address: device.rssi for device in devices}
    devices = sorted(rssi_values.items(), key=lambda x:  x[1] , reverse=True)
    devices = dict([d for d in devices if BT_Loc.UUID in d[0]][:BT_Loc.TOP_N])
    return devices

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_message(client, userdata, message):
    if message.topic == BT_Loc.ACK:
        if message.payload.decode() == "200":
            print("Registration successful")
            userdata['registered'] = True
    else:
        print(message.payload.decode())

def register_device(client):
    while not client._userdata['registered']:
        client.publish(BT_Loc.REGISTER_TOPIC, BT_Loc.DEVICE_ID)
        print('publishing')
        time.sleep(5)  # Wait for 5 seconds before retrying

async def main():
    # MQTT connection and setup
    topics_to_subs = [BT_Loc.RSSI_TOPIC, BT_Loc.ACK]
    client = mqtt.Client(userdata={'registered': False})
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BT_Loc.MQTT_BROKER, BT_Loc.MQTT_PORT, BT_Loc.KEEPALIVE)
    client.loop_start()
    
    # Supscribe to topics
    for topic in topics_to_subs:
        client.subscribe(topic)
        
    # Try to register self to hub
    register_device(client)
    while not client._userdata['registered']:
        await asyncio.sleep(1)

    # Instantiate memory buffer & BleScanner
    mem_buff = Queue()
    scanner = BleScanner(mem_buff)
    scanner.start()
    
    
    #Send data packets to hub
    try:
        # first = True
        while True:
            if not mem_buff.empty():
                    device_address, rssi, name = mem_buff.get()
            # rssi_values = await scan_bluetooth_devices()
            # if first:
            print(device_address, rssi, name)
            payload = f"DeviceID:{BT_Loc.DEVICE_ID}\n"
            payload += f"{device_address}:{rssi}\n"
            client.publish(BT_Loc.RSSI_TOPIC, payload)
            # await asyncio.sleep(.1)
    except KeyboardInterrupt:
        print("Terminating...")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
