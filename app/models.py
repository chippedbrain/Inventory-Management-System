from sqlmodel import Field, SQLModel
from datetime import datetime
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, DateTime

class CheckoutStatus(str, Enum):
    reserved = "reserved"
    checked_out = "checked_out"
    returned = "returned"

class GearUnitStatus(str, Enum):
    available = "available"
    damaged = "damaged"
    retired = "retired"

class JobStatus(str, Enum):
    planned =  "planned"
    active = "active"
    completed= "completed"

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    hashed_password: str
    admin: bool = False

class GearUnit(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    gear_item_id: int | None = Field(default=None, foreign_key="gearitem.id")
    serial_number: str
    status: GearUnitStatus = GearUnitStatus.available


class GearItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    manufacturer: str
    model : str
    
class Job(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    client_name: str
    start_date: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    end_date: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    status: JobStatus = JobStatus.planned

    
class JobGearUnit(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    job_id: int | None = Field(default=None, foreign_key="job.id")
    gear_unit_id: int | None = Field(default=None, foreign_key="gearunit.id")
    status: CheckoutStatus = CheckoutStatus.reserved

# Pydantic models for request validation
class GearUnitCreate(SQLModel):
    gear_item_id: int
    serial_number: str
    status: GearUnitStatus = GearUnitStatus.available

class GearItemCreate(SQLModel):
    name: str
    manufacturer: str
    model : str

class JobCreate(SQLModel):
    name: str
    client_name: str
    start_date: datetime
    end_date: datetime
    status: JobStatus = JobStatus.planned

class JobGearUnitCreate(SQLModel):
    job_id: int
    gear_unit_id: int
    status: CheckoutStatus = CheckoutStatus.reserved
    
class UserCreate(SQLModel):
    email: str
    password: str
    
class UserLogin(SQLModel):
    email: str
    password: str