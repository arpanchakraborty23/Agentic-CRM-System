# Phase 3: Activities, Meetings & Tasks

## Objective
Track every sales interaction — calls, emails, meetings, and follow-up tasks — with full calendar and time management.

## Models
| Model | Table | Purpose |
|-------|-------|---------|
| `Meeting` | `meetings` | Scheduled meetings (internal & client) |
| `Activity` | `activities` | Logged interactions (call, email, note) |
| `Task` | `tasks` | Assignable follow-up items |
| `CalendarEvent` | `calendar_events` | Integrated calendar entries |

## Tools to Create

### Meeting Tools
| Tool | Description |
|------|-------------|
| `schedule_meeting(title, scheduled_at, organizer_id, contact_id, company_id, duration, location)` | Book a meeting |
| `list_meetings(date_range, user_id, status, page, limit)` | Calendar view |
| `get_meeting(meeting_id)` | Meeting details + attendees |
| `update_meeting(meeting_id, **fields)` | Reschedule / change details |
| `cancel_meeting(meeting_id, reason)` | Cancel with notification |
| `get_meeting_slots(date, user_id)` | Find free time slots |

### Activity Tools
| Tool | Description |
|------|-------------|
| `log_activity(type, subject, description, contact_id, deal_id, user_id)` | Log call, email, or note |
| `list_activities(entity_type, entity_id, date_range, page, limit)` | Activity feed for a contact/deal |
| `get_activity(activity_id)` | Full activity details |

### Task Tools
| Tool | Description |
|------|-------------|
| `create_task(title, assigned_to, due_date, priority, related_to_type, related_to_id)` | Create follow-up task |
| `list_tasks(assigned_to, status, priority, due_date_range, page, limit)` | Task dashboard |
| `update_task(task_id, **fields)` | Update status, priority, due date |
| `complete_task(task_id)` | Mark task done |
| `get_task_overview(user_id)` | Overdue, today, upcoming counts |

### Calendar Tools
| Tool | Description |
|------|-------------|
| `get_calendar(user_id, start_date, end_date)` | Combined meetings + tasks view |
| `sync_calendar(provider, credentials)` | External calendar sync (Google/Outlook) |

## Verification
```bash
uv run python -c "
import asyncio
from src.tools.activity_tools import log_activity, create_task
async def test():
    a = await log_activity('call', 'Follow-up call', 'Discussed proposal', contact_id=1)
    print(a)
asyncio.run(test())
"
```
