from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class BleBuffer:
    '''Class for saving the rssi values on edge'''
    uuids:List[str]
    buffer: Dict[str, List[int]] = field(default_factory=dict)
    
class SyncedData:
    '''Format for temporally synced dataset'''
    valid:bool
    data:Dict[str, int]
    