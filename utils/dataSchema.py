from pydantic import BaseModel
from typing import Dict


class Metadata(BaseModel):
    deviceID:int
    
class Message(BaseModel):
    metadata: Metadata
    data: Dict
    
    