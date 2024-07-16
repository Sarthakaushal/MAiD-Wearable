from .data_classes import BleBuffer, SyncedData

class TemporalDataCollator:
    def __init__(self) -> None:
        self.data = BleBuffer(uuids=[], buffer={})
    
    def insert(self,uuid:str, rssi:int)->None:
        if uuid in self.data.uuids:
            self.data.buffer[uuid].append(rssi)
        else:
            self.data.uuids.append(uuid)
            self.data.buffer[uuid]=[rssi]
    
    def get(self)->SyncedData:
        rssi_data = {}
        for key in self.data.uuids:
            if len(self.data.uuids) <3:
                return SyncedData(valid=False, data={})
            else:
                rssi_data[key] = self.data.buffer[key].pop(-1)
        
        self.data.buffer = rssi_data
        for key in self.data.uuids:
            self.data.buffer[key] = [rssi_data[key]]
        self.data.uuids = list(rssi_data.keys())
        # self.data = BleBuffer(uuids=[], buffer={})
        print(f'RSSI Data: {rssi_data}')
        payload = SyncedData(valid=True, data=rssi_data)
        return payload
    
    
                