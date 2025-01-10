from pydantic import BaseModel

class FireType():
    NONE = 0
    ORDINARY = "ORDINARY"
    ELECTRICAL = "ELECTRICAL"
    GAS = "GAS"

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