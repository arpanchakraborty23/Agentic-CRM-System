from fastmcp import FastMCP
from datetime import datetime, timedelta
from sqlalchemy import select
from src.services.db import get_db
from src.services.models import Contact, Meeting

mcp = FastMCP("CRM Server")

@mcp.tool()
async def create_contact(first_name: str, last_name: str, email: str, company_id: str) -> dict:
    """Create a new CRM contact."""
    async for session in get_db():
        contact = Contact(
            first_name=first_name,
            last_name=last_name,
            email=email,
            company_id=company_id,
        )
        session.add(contact)
        await session.commit()
        await session.refresh(contact)
        return {"id": contact.id, "email": contact.email}

@mcp.tool()
async def list_contacts() -> list[dict]:
    """List all CRM contacts."""
    async for session in get_db():
        result = await session.execute(select(Contact))
        contacts = result.scalars().all()
        return [
            {
                "id": c.id,
                "name": f"{c.first_name} {c.last_name}",
                "email": c.email,
            }
            for c in contacts
        ]


@mcp.tool()
async def get_contact_details(contact_id : int):
    """Get detailed information about a contact."""
    async for session in get_db():
        result = await session.execute(select(Contact).where(Contact.id == contact_id))
        contact = result.scalar_one_or_none()
        if contact:
            return {
                "id": contact.id,
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "email": contact.email,
                "company_id": contact.company_id,
            }
        
        return {}
    
##########################
# Meeting Tools
##########################

@mcp.tool()
async def schedule_meeting(title: str,  scheduled_at: datetime, organizer_id: str, description: str = None, contact_id: int = None, company_id: str = None):
    """Schedule a new meeting in the CRM"""
    async for session in get_db():
        meeting = Meeting(
            id=contact_id,
            title= title,
            scheduled_at=scheduled_at,
            description=description,
            company_id=company_id,
            organizer_id=organizer_id
        )

        session.add(meeting)
        await session.commit()
        await session.refresh(meeting)
    return {
        "scheduled_at": scheduled_at
    }

@mcp.tool()
async def get_meeting_slot(date: datetime, time: str):
    """Search Meeting Slot"""
    async for session in get_db():
       # This finds everything between 00:00:00 and 23:59:59 of that day
        stmt = select(Meeting).where(
            Meeting.scheduled_at >= date.replace(hour=0, minute=0, second=0),
            Meeting.scheduled_at <= date.replace(hour=23, minute=59, second=59)
        )

        result = await session.execute(stmt)
        meetings = result.scalars().all()
        
        if not meetings:
            return "No meetings found for this slot."
            
        # 3. Format the results into a readable list
        return [
            {"title": m.title, "time": m.scheduled_at, "status": m.status} 
            for m in meetings
        ]
    
@mcp.tool()
async def update_meeting(meeting_id: str, title: str = None, scheduled_at: datetime = None, description: str = None, status: str = None) -> dict:
    """Update an existing meeting's details."""
    async for session in get_db():
        result = await session.execute(select(Meeting).where(Meeting.id == meeting_id))
        meeting = result.scalar_one_or_none()
        
        if not meeting:
            return {"error": "Meeting not found"}
        if title is not None:
            meeting.title = title
        if scheduled_at is not None:
            meeting.scheduled_at = scheduled_at
        if description is not None:
            meeting.description = description
        if status is not None:
            meeting.status = status

        # 3. Commit and Refresh
        await session.commit()
        await session.refresh(meeting)
        
        return {"status": "success", "meeting_id": meeting.id}