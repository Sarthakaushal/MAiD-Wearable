from data_classes import BleBuffer, SyncedData

class TemporalDataCollator:
    def __init__(self) -> None:
        self.data = BleBuffer()
    
    def insert(self,uuid:str, rssi:int)->None:
        if uuid in self.uuids:
            self.data.buffer[uuid].append(rssi)
        else:
            self.data.uuids.append(uuid)
            self.data.buffer[uuid].append(rssi)
    
    def get(self)->SyncedData:
        rssi_data = {}
        for key in self.data.buffer:
            if len(self.data.buffer[key]) ==0:
                return SyncedData(valid=False, data={})
            else:
                rssi_data[key] = self.data.buffer[key]
        self.data = BleBuffer()
        return SyncedData(valid=True, data=rssi_data)
    
    
                