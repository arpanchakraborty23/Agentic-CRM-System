from fastmcp import FastMCP
from sqlalchemy import select
from src.services.db import get_db
from src.services.models import Contact, 

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