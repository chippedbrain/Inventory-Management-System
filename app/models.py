from sqlmodel import Field, SQLModel
from datetime import datetime

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    hashed_password: str
    admin: bool = False

class GearItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    manufacturer: str
    model : str
    
class Job(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    start_date: datetime
    end_date: datetime
    
class JobGearItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    job_id: int | None = Field(default=None, foreign_key="job.id")
    gear_item_id: int | None = Field(default=None, foreign_key="gearItem.id")
    status = 
    checked_out: bool