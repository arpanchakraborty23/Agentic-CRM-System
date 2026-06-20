# Phase 2: Lead Management & Sales Pipeline

## Objective
Track incoming leads through qualification stages and manage the sales pipeline with deal/opportunity records.

## Models
| Model | Table | Purpose |
|-------|-------|---------|
| `Lead` | `leads` | Unqualified inbound prospect |
| `Deal` | `deals` | Qualified opportunity in pipeline |
| `PipelineStage` | `pipeline_stages` | Configurable stage definitions |
| `LeadSource` | `lead_sources` | Source taxonomy (referral, website, call, etc.) |

## Tools to Create

### Lead Tools
| Tool | Description |
|------|-------------|
| `create_lead(company_name, contact_name, email, phone, source, notes)` | Capture an inbound lead |
| `qualify_lead(lead_id, deal_id, score)` | Convert lead → deal with qualification score |
| `list_leads(status, source, date_range, page, limit)` | Filter/sort leads |
| `get_lead(lead_id)` | Lead details + activity history |
| `update_lead(lead_id, **fields)` | Update lead properties |
| `disqualify_lead(lead_id, reason)` | Mark lead lost with reason code |

### Pipeline / Deal Tools
| Tool | Description |
|------|-------------|
| `create_deal(name, company_id, contact_id, stage_id, value, expected_close_date)` | Open a new opportunity |
| `move_deal_stage(deal_id, stage_id)` | Advance/regress deal stage |
| `list_deals(stage_id, user_id, date_range, page, limit)` | Pipeline view with filters |
| `get_deal(deal_id)` | Full deal details + stage history |
| `update_deal(deal_id, **fields)` | Update value, close date, owner |
| `close_deal_won(deal_id)` | Mark deal won, record close value |
| `close_deal_lost(deal_id, reason)` | Mark deal lost with reason |
| `get_pipeline_summary(user_id)` | Stage-by-stage counts + total value |

## Pipeline Stages (default seed)
1. Prospecting
2. Qualification
3. Needs Analysis
4. Proposal
5. Negotiation
6. Closed Won
7. Closed Lost

## Verification
```bash
uv run python -c "
import asyncio
from src.tools.pipeline_tools import create_lead, create_deal
async def test():
    lead = await create_lead('NewCo', 'John', 'john@newco.com', 'referral')
    print(lead)
asyncio.run(test())
"
```
