from config import CONFIG as cfg
from utils.dataSchema import Message, Metadata

class BLE_Conversions:
    def rssi_to_dist(self, rssi, rssi_0 = cfg.RSSI_0):
        return 10**((rssi_0- rssi)/(10*cfg.N))

def process_msg_data(payload):
    data = {}
    print(payload)
    for line in payload.split('\n')[:-2]:
        m = line.split(':')
        if m[0] == 'DeviceID':
            id = 1
            key = ':'.join(m[:-1])
            data[key] = m[-1]
    out = {
        'metadata': Metadata(deviceID=id),
        'data':data} 
    return Message(**out)
    