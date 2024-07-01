from config import CONFIG as cfg
from utils.dataSchema import Message, Metadata

class BLE_Conversions:
    def rssi_to_dist(self, rssi, rssi_0 = cfg.RSSI_0):
        return 10**((rssi_0- rssi)/(10*cfg.N))

def process_msg_data(payload):
    data = {}
    data = payload.split('\n') 
    id = data[0].split(':')[-1]
    bt_data = data[1].split(':')
    key = ':'.join(bt_data[:-1])
    data= (key, bt_data[-1])
    print(data ,id)
    
    out = {
        'metadata': Metadata(deviceID=id),
        'data':data} 
    return Message(**out)
    