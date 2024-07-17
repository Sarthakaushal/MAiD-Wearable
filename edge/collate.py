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
        if len(self.data.uuids) <3:
                return SyncedData(valid=False, data={})
        for key in self.data.uuids:
                rssi_data[key] = self.data.buffer[key].pop(-1)
        payload = SyncedData(valid=True, data=rssi_data)
        self.data.buffer = {}
        self.data.uuids = []
        # self.data = BleBuffer(uuids=[], buffer={})
        print(f'RSSI Data: {rssi_data}')
        
        return payload
    
    
                