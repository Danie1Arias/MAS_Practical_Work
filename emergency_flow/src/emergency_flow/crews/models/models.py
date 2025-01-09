from pydantic import BaseModel

class FireType():
    NONE = 0
    ORDINARY = 1
    ELECTRICAL = 2
    GAS = 3

class Severity():
    HIGH = 1
    MEDIUM = 2
    LOW = 3

class PhoneCallDetails(BaseModel):
    longitude: float
    latitude: float
    fire_type: str
    severity: int 
    people_in_danger: int 