# Phase 7: Integrations & Automation

## Objective
Connect the CRM to external tools (email, calendar, telephony, Slack) and enable workflow automation via webhooks + triggers.

## Models
| Model | Table | Purpose |
|-------|-------|---------|
| `Webhook` | `webhooks` | Outbound event notifications |
| `WebhookEvent` | `webhook_events` | Delivery log |
| `Integration` | `integrations` | Connected third-party services |
| `AutomationRule` | `automation_rules` | When-this-then-that rules |
| `ApiKey` | `api_keys` | External API access credentials |

## Tools to Create

### Webhook Tools
| Tool | Description |
|------|-------------|
| `register_webhook(url, events, secret)` | Subscribe to CRM events |
| `list_webhooks(page, limit)` | Active webhooks |
| `delete_webhook(webhook_id)` | Remove webhook |
| `get_webhook_logs(webhook_id, page, limit)` | Delivery success/failure history |
| `replay_webhook_event(event_id)` | Retry failed delivery |

### Integration Tools
| Tool | Description |
|------|-------------|
| `connect_email(provider, credentials)` | Gmail / Outlook sync |
| `connect_calendar(provider, credentials)` | Google Calendar / Outlook Calendar sync |
| `connect_telephony(provider, credentials)` | Twilio / Zoom Phone integration |
| `connect_slack(workspace, channel, token)` | Slack notifications |
| `list_integrations(user_id)` | Connected services |
| `disconnect_integration(integration_id)` | Remove integration |

### Automation Rule Tools
| Tool | Description |
|------|-------------|
| `create_rule(name, trigger_event, conditions, actions)` | Build if-this-then-that |
| `list_rules(active, page, limit)` | Automation rules library |
| `toggle_rule(rule_id, active)` | Enable/disable rule |
| `update_rule(rule_id, **fields)` | Edit conditions or actions |
| `delete_rule(rule_id)` | Remove rule |

### Trigger Events Available
- `contact.created`, `contact.updated`, `contact.deleted`
- `deal.created`, `deal.stage_changed`, `deal.closed_won`, `deal.closed_lost`
- `meeting.created`, `meeting.cancelled`
- `activity.logged`
- `task.completed`
- `lead.created`, `lead.qualified`, `lead.disqualified`
- `order.created`, `order.status_changed`

### Example Automation Rules
| Rule | Trigger | Action |
|------|---------|--------|
| Notify on hot lead | `lead.created` (score > 80) | Slack message to sales channel |
| Follow-up after meeting | `meeting.completed` | Create task assigned to organizer |
| Welcome email | `contact.created` | Send email via template |
| Stage-advance alert | `deal.stage_changed` (to Negotiation) | Notify manager |

### API Key Tools
| Tool | Description |
|------|-------------|
| `create_api_key(name, scopes, expires_at)` | Generate API key |
| `list_api_keys(page, limit)` | Active keys (masked) |
| `revoke_api_key(key_id)` | Immediately invalidate key |

## Verification
```bash
uv run python -c "
import asyncio
from src.tools.integration_tools import register_webhook, create_rule
async def test():
    w = await register_webhook('https://myapp.com/webhook', ['deal.closed_won', 'lead.created'], 'my-secret')
    print(w)
asyncio.run(test())
"
```
