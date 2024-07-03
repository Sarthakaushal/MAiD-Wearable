class CONFIG:
    
    # Path-loss exponent
    N = 2 # used in rssi to distance conversion can vary from 2 to 4
    
    # RSSI_0 values
    DEVICE_RSSI = {
        "C2:15:B9:9A:1B:36":-59,
        "31:E5:9E:3B:BF:67": -61} # Readings for RSSI at 1 meter
    
    # Time for the old values to persist in the system
    DATA_EXPIRY_TIME = 1
    
    VERBOSE = 2
    
    DEVICE_COORDINATES = {
        'C2:15:B9:9A:1B:36': (0,0)
    }
    
    
    