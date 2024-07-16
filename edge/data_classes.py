from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class BleBuffer:
    '''Class for saving the rssi values on edge'''
    uuids:List[str] = field(default_factory='')
    buffer: Dict[str, List[int]] = field(default_factory={})

@dataclass
class SyncedData:
    '''Format for temporally synced dataset'''
    valid:bool = field(default_factory='')
    data:Dict[str, int] = field(default_factory={})
    