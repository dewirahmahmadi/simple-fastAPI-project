from typing import List
import pydantic as _pydantic
import datetime as _dt
from enum import Enum

class Gender(str, Enum):
    FEMALE = "Female"
    MALE = "Male"

class _JobBase(_pydantic.BaseModel):
    title: str
    description: str
    deadline: _dt.datetime

class JobCreate(_JobBase):
    pass

class Job(_JobBase):
    """Used to reading data for Job"""
    id: int
    owner_id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True

class _UserBase(_pydantic.BaseModel):
    email: str
    first_name: str
    last_name: str
    gender: Gender

class UserCreate(_UserBase):
    pass

class User(_UserBase):
    """Used to reading data for User"""
    id: int
    is_active: bool
    jobs: List[Job] = []

    class Config:
        orm_mode = True