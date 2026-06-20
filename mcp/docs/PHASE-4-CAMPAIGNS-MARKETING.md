# Phase 4: Campaigns & Marketing Automation

## Objective
Plan, execute, and measure marketing campaigns — email drips, events, and outbound sequences — tracked back to pipeline influence.

## Models
| Model | Table | Purpose |
|-------|-------|---------|
| `Campaign` | `campaigns` | Marketing campaign record |
| `CampaignMember` | `campaign_members` | Contacts associated with a campaign |
| `EmailTemplate` | `email_templates` | Reusable email/sms templates |
| `Sequence` | `sequences` | Automated follow-up steps |

## Tools to Create

### Campaign Tools
| Tool | Description |
|------|-------------|
| `create_campaign(name, type, status, budget, company_id, created_by, start_date, end_date)` | Launch a campaign |
| `list_campaigns(type, status, date_range, page, limit)` | Campaign dashboard |
| `get_campaign(campaign_id)` | Full campaign + member stats |
| `update_campaign(campaign_id, **fields)` | Budget, dates, status |
| `end_campaign(campaign_id)` | Close campaign, record ROI |

### Campaign Member Tools
| Tool | Description |
|------|-------------|
| `add_campaign_member(campaign_id, contact_id)` | Enroll a contact |
| `add_campaign_members_bulk(campaign_id, contact_ids)` | Bulk enroll from list/segment |
| `list_campaign_members(campaign_id, status, page, limit)` | Member list + engagement |
| `update_member_status(campaign_id, contact_id, status)` | Track response (sent, opened, replied) |

### Email Template Tools
| Tool | Description |
|------|-------------|
| `create_template(name, subject, body_html, variables)` | Design a template |
| `list_templates(category, page, limit)` | Template library |
| `update_template(template_id, **fields)` | Edit template |

### Sequence Tools
| Tool | Description |
|------|-------------|
| `create_sequence(name, steps, trigger_condition)` | Build an automation sequence |
| `enroll_in_sequence(sequence_id, contact_id)` | Start a contact in a sequence |
| `list_sequences(status, page, limit)` | Active/paused sequences |
| `get_sequence_progress(sequence_id)` | Step-by-step completion stats |

## Verification
```bash
uv run python -c "
import asyncio
from src.tools.campaign_tools import create_campaign
async def test():
    c = await create_campaign('Summer Sale', 'email', 'active', 5000, company_id='...', created_by='...')
    print(c)
asyncio.run(test())
"
```
