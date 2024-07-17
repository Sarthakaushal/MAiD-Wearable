class CONFIG:
    
    # Path-loss exponent
    N = 2 # used in rssi to distance conversion can vary from 2 to 4
    
    # RSSI_0 values
    DEVICE_RSSI = {
        "DD:34:02:0A:4B:98": -57.56, # Billy
        "DD:34:02:0A:4C:3F": -60.05, # Jimmy
        "DD:34:02:0A:4D:2B": -57.94, # # Maurice
        "DD:34:02:0A:4D:0B": -58.17 # Timmy
        } # Readings for RSSI at 1 meter
    
    # Time for the old values to persist in the system
    DATA_EXPIRY_TIME = 1
    
    VERBOSE = 2
    
    DEVICE_COORDINATES = {
        "DD:34:02:0A:4B:98": (0,0), # Billy
        "DD:34:02:0A:4C:3F": (0,23), # Jimmy
        "DD:34:02:0A:4D:2B": (23,0), # # Maurice
        "DD:34:02:0A:4D:0B": (23,23) # Timmy
        }
    
    
    