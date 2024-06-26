from pydantic import BaseModel
from typing import Dict
class Metadata(BaseModel):
    deviceID:str
    
class Message(BaseModel):
    metadata: Metadata
    data: Dict
    
    