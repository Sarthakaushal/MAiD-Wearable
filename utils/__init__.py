from config import CONFIG as cfg
from utils.dataSchema import Message, Metadata
import time
import numpy as np

class BLE_Conversions:
    @staticmethod
    def rssi_to_dist(rssi, name):
        rssi_0 = cfg.DEVICE_RSSI[name]
        return 10**((rssi_0- rssi)/(10*cfg.N))
    
    @staticmethod
    def trilaterate(p1, p2, p3, r1, r2, r3):
        """
        Desc: Takes coordinates and distances as inputs, returns (X,Y) of object
        Args:   p1 - coordinate (x1,y1)
                p2 - coordinate (x2,y2)
                p3 - coordinate (x3,y3)
        Returns : x,y()
        """
        P1 = np.array(p1)
        P2 = np.array(p2)
        P3 = np.array(p3)
        
        # Transform to a system where P1 is at the origin
        ex = (P2 - P1) / np.linalg.norm(P2 - P1)
        i = np.dot(ex, P3 - P1)
        ey = (P3 - P1 - i * ex) / np.linalg.norm(P3 - P1 - i * ex)
        d = np.linalg.norm(P2 - P1)
        j = np.dot(ey, P3 - P1)
        
        # Coordinates in the new system
        x = (r1**2 - r2**2 + d**2) / (2 * d)
        y = (r1**2 - r3**2 + i**2 + j**2 - 2 * i * x) / (2 * j)
        
        # Transform back to the original system
        final_pos = P1 + x * ex + y * ey
        return final_pos
    

class MsgProcessing:
    @staticmethod
    def process_msg_data(payload):
        data = {}
        data = payload.split('\n') 
        id = data[0].split(':')[-1]
        bt_data = data[1].split(':')
        key = ':'.join(bt_data[:-1])
        data= (key, bt_data[-1])
        # print(data ,id)
        
        out = {
            'metadata': Metadata(deviceID=id),
            'data':data} 
        return Message(**out)

    @staticmethod
    def get_old_keys(bt_devices:dict):
        output = []
        current_time = time.time()
        for bt_add in bt_devices.keys():
            if current_time - bt_devices[bt_add]['last_updated']>= cfg.data_expiry_time:
                output.append(bt_add)
        return output