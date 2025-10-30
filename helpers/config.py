from pydantic import BaseModel
from typing import List, Optional

class Inquiry(BaseModel):
    SPECIALTY: str
    DIAGNOSIS: str

class Doctor(BaseModel):
    NAME: str
    DEGREE: str
    SCOPE_OF_SERVICE: Optional[List]
    GENDER: str