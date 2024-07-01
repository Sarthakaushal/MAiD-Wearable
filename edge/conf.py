class BT_Loc:
    # Device Details
    DEVICE_ID = "maid-1"
    DEVICE_VERSION = 0.1
    
    # MQTT  Client Config
    MQTT_BROKER = "10.56.6.195"
    MQTT_PORT = 1883
    KEEPALIVE = 60
    
    # MQTT Topics
    REGISTER_TOPIC = "register"
    ACK = f'ack/{DEVICE_ID}'
    RSSI_TOPIC = f"device/seeker/{DEVICE_ID}"
    
    # BT device selection 
    UUID = "DD:34:02:0A:"
    LOCAL_NAME_ID = 'MAiD'
    
    # Num of devices to send to hub post ascending ordering of BLE sinals
    TOP_N = 10 # use -1 for all devices
    