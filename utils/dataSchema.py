from pydantic import BaseModel
from typing import Tuple


class Metadata(BaseModel):
    deviceID:str
    
class Message(BaseModel):
    metadata: Metadata
    data: Tuple
    
    