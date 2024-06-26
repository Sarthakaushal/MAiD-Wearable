import asyncio
from bleak import BleakScanner 
import paho.mqtt.client as mqtt
import time

async def scan_devices():
    scanner = BleakScanner()

    devices = await scanner.discover()
    for device in devices:
        if device.name:
            print(f"Device: {device.name}, Address: {device.address}, RSSI: {device.rssi}")



DEVICE_ID = "maid-1"
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
REGISTER_TOPIC = "register"
ACK = f'ack/{DEVICE_ID}'
RSSI_TOPIC = f"device/seeker/{DEVICE_ID}"
KEEPALIVE = 60
TOP_N = -1
async def scan_bluetooth_devices():
    devices = await BleakScanner.discover()
    rssi_values = {device.address: device.rssi for device in devices}
    devices = dict(sorted(rssi_values.items(), key=lambda x: x[1], reverse=True)[:TOP_N])
    return devices

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_message(client, userdata, message):
    if message.topic == ACK:
        if message.payload.decode() == "200":
            print("Registration successful")
            userdata['registered'] = True
    else:
        print(message.payload.decode())

def register_device(client):
    while not client._userdata['registered']:
        client.publish(REGISTER_TOPIC, DEVICE_ID)
        print('publishing')
        time.sleep(5)  # Wait for 5 seconds before retrying

async def main():
    topics_to_subs = [RSSI_TOPIC, ACK]
    client = mqtt.Client(userdata={'registered': False})
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, KEEPALIVE)
    
    client.loop_start()
    for topic in topics_to_subs:
        client.subscribe(topic)
    register_device(client)

    while not client._userdata['registered']:
        await asyncio.sleep(1)

    try:
        while True:
            rssi_values = await scan_bluetooth_devices()
            payload = f"DeviceID:{DEVICE_ID}\n"
            for addr, rssi in rssi_values.items():
                payload += f"{addr}:{rssi}\n"
            client.publish(RSSI_TOPIC, payload)
            # await asyncio.sleep(.1)
    except KeyboardInterrupt:
        print("Terminating...")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
