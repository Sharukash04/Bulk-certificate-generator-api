from pydantic import BaseModel,EmailStr,Field
from typing import List


class Recipient(BaseModel):
    name:str=Field(...,min_length=2,max_length=100)
    email:EmailStr


class GenerationRequest(BaseModel):
    event_name:str=Field(...,min_length=2,max_length=200)
    organization:str=Field(...,min_length=2,max_length=200)
    recipients:List[Recipient]=Field(...,min_length=1)


    