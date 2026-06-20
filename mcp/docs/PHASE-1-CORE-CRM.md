# Phase 1: Core CRM Foundation — Contact & Company Management

## Objective
Build the foundational CRM layer — companies and contacts — that every other feature plugs into.

## Models
| Model | Table | Purpose |
|-------|-------|---------|
| `Company` | `companies` | Organization / account record |
| `Contact` | `contacts` | Individual person tied to a company |
| `User` | `users` | Internal CRM user (sales rep, admin) |

## Tools to Create

### Company Tools
| Tool | Description |
|------|-------------|
| `create_company(name, industry, location, employee_count, domain, phone, website)` | Create a new company account |
| `list_companies(search, industry, page, limit)` | List/search companies with filters |
| `get_company(company_id)` | Full company details |
| `update_company(company_id, **fields)` | Patch company fields |
| `delete_company(company_id)` | Soft-delete a company |

### Contact Tools
| Tool | Description |
|------|-------------|
| `create_contact(first_name, last_name, email, company_id, phone, job_title, linkedin_url)` | Add a contact to a company |
| `list_contacts(company_id, search, page, limit)` | List/search contacts |
| `get_contact(contact_id)` | Full contact profile |
| `update_contact(contact_id, **fields)` | Patch contact details |
| `delete_contact(contact_id)` | Soft-delete a contact |
| `merge_duplicate_contacts(source_id, target_id)` | Merge duplicate records |

### User Tools
| Tool | Description |
|------|-------------|
| `create_user(name, email, role, team)` | Add a CRM user |
| `list_users(role, page, limit)` | List users by role |
| `get_user(user_id)` | User details + recent activity |

## DB Config Pattern
```python
# db_config.py — swap DATABASE_URL for any DB:
#   PostgreSQL: postgresql+asyncpg://user:pass@host/db
#   MySQL:      mysql+asyncmy://user:pass@host/db
#   SQLite:     sqlite+aiosqlite:///local.db
DATABASE_URL = "postgresql+asyncpg://..."
```

## Verification
```bash
uv run python -c "
import asyncio
from src.tools.crm_tools import create_company, create_contact
async def test():
    c = await create_company('Acme Corp', 'Tech', 'NY')
    print(c)
asyncio.run(test())
"
```
