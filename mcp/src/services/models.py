from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False
    )
    name: str
    email: str = Field(unique=True)
    role: str 


class Company(SQLModel, table=True):
    __tablename__ = "companies"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False
    )
    company_name: str
    industry: Optional[str] = None
    employee_count: Optional[int] = None
    location: str 


class Contact(SQLModel, table=True):

    __tablename__ = "contacts"

    id: Optional[int] = Field(default=None, primary_key=True)

    company_id: uuid.UUID = Field(
        foreign_key="companies.id"
    )

    first_name: str
    last_name: str

    email: str
    phone: Optional[str] = None
    job_title: Optional[str] = None


class Meeting(SQLModel, table=True):
    __tablename__ = "meetings"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False
    )
    title: str
    description: Optional[str] = None
    scheduled_at: datetime
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    status: str = Field(default="scheduled")
    organizer_id: uuid.UUID = Field(foreign_key="users.id")
    contact_id: Optional[int] = Field(default=None, foreign_key="contacts.id")
    company_id: Optional[uuid.UUID] = Field(default=None, foreign_key="companies.id")


class Campaign(SQLModel, table=True):
    __tablename__ = "campaigns"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False
    )
    name: str
    description: Optional[str] = None
    type: str
    status: str = Field(default="draft")
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = None
    company_id: Optional[uuid.UUID] = Field(default=None, foreign_key="companies.id")
    created_by: uuid.UUID = Field(foreign_key="users.id")