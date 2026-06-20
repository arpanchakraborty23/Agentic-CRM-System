# Agentic CRM System — MCP Server for Sales Management

A production-ready [MCP](https://modelcontextprotocol.io) server for sales CRM management. Swap the database connection and plug it into any MCP client — opencode, Claude Desktop, Cline, Continue, or custom apps.

---

## Architecture

```
┌──────────────────────────────────────┐
│         MCP Client                   │  opencode, Claude, Cline, Continue
└──────────┬───────────────────────────┘
           │  stdio / SSE
┌──────────▼───────────────────────────┐
│      MCP Server (fastmcp)           │  mcp/server.py
│  ┌────────────────────────────────┐  │
│  │  src/tools/  (per-phase files) │  │
│  │  ├─ core.py         (Phase 1)  │  │
│  │  ├─ pipeline.py     (Phase 2)  │  │
│  │  ├─ activities.py   (Phase 3)  │  │
│  │  ├─ campaigns.py    (Phase 4)  │  │
│  │  ├─ reporting.py    (Phase 5)  │  │
│  │  ├─ commerce.py     (Phase 6)  │  │
│  │  └─ integrations.py (Phase 7)  │  │
│  └────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │
│  │  src/services/                 │  │
│  │  ├─ db.py         (pool+retry) │  │
│  │  ├─ models.py     (21 tables)  │  │
│  │  └─ logfire.py    (observ.)    │  │
│  └────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │
│  │  src/config/db_config.py       │  │  ← swap DB here
│  └────────────────────────────────┘  │
└──────────┬───────────────────────────┘
           │
┌──────────▼───────────────────────────┐
│   PostgreSQL / MySQL / SQLite        │
└──────────────────────────────────────┘
```

**Key design:** Only the `.env` `DATABASE_URL` changes between environments. Everything else stays the same.

| Database | Connection String |
|----------|-----------------|
| PostgreSQL | `postgresql+asyncpg://user:pass@host/db` |
| MySQL | `mysql+asyncmy://user:pass@host/db` |
| SQLite | `sqlite+aiosqlite:///local.db` |

---

## Database Models (13 tables)

| Phase | Tables | Purpose |
|-------|--------|---------|
| **1 — Core CRM** | `users`, `companies`, `contacts` | Foundation records |
| **2 — Pipeline** | `leads`, `lead_sources`, `deals`, `pipeline_stages`, `deal_stage_history` | Lead → deal tracking |
| **3 — Activities** | `meetings`, `activities`, `tasks`, `calendar_events` | Sales interactions |
| **4 — Campaigns** | `campaigns`, `campaign_members`, `email_templates`, `sequences` | Marketing automation |
| **5 — Analytics** | `reports`, `dashboards`, `sales_metrics` | KPIs & forecasting |
| **6 — Commerce** | `products`, `price_books`, `price_book_entries`, `quotes`, `quote_line_items`, `orders`, `invoices` | Full quote-to-order |
| **7 — Integration** | `webhooks`, `webhook_events`, `integrations`, `automation_rules`, `api_keys` | Extensibility |

All models include: `created_at`, `updated_at`, `deleted_at` (soft-delete), `is_active`, proper foreign keys, cascade-safe UUID PKs, and indexed query columns.

---

## MCP Tools — Build Phases

Each phase builds on the previous one. Tools are independently deployable.

| Phase | Doc | Tools |
|-------|-----|-------|
| **1** | [Core CRM](mcp/docs/PHASE-1-CORE-CRM.md) | Company & Contact CRUD, merge, search |
| **2** | [Leads & Pipeline](mcp/docs/PHASE-2-LEADS-PIPELINE.md) | Lead capture, qualify, deal pipeline, stage moves |
| **3** | [Activities & Meetings](mcp/docs/PHASE-3-ACTIVITIES-MEETINGS.md) | Schedule meetings, log calls/emails, tasks, calendar |
| **4** | [Campaigns & Marketing](mcp/docs/PHASE-4-CAMPAIGNS-MARKETING.md) | Campaign creation, email templates, sequences |
| **5** | [Analytics & Reporting](mcp/docs/PHASE-5-ANALYTICS-REPORTING.md) | KPIs, pipeline velocity, forecasts, exports |
| **6** | [Quotes, Orders & Products](mcp/docs/PHASE-6-QUOTES-ORDER-PRODUCTS.md) | Product catalog, quoting, order-to-invoice |
| **7** | [Integrations & Automation](mcp/docs/PHASE-7-INTEGRATIONS-AUTOMATION.md) | Webhooks, Slack/Google sync, automation rules, API keys |

---

## Setup

```bash
cd mcp
uv sync
```

Create `.env`:

```env
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
```

Run:

```bash
uv run python server.py
```

---

## MCP Client Configuration

### opencode (`~/.config/opencode/opencode.json`)

```json
{
  "mcpServers": {
    "agentic-crm": {
      "command": "uv",
      "args": ["run", "--directory", "D:/GENAIProjects/Agentic-CRM-System/mcp", "python", "server.py"]
    }
  }
}
```

### Claude Desktop

```json
{
  "mcpServers": {
    "agentic-crm": {
      "command": "uv",
      "args": ["run", "--directory", "D:/GENAIProjects/Agentic-CRM-System/mcp", "python", "server.py"]
    }
  }
}
```

### VS Code (Cline / Continue)

```json
{
  "mcpServers": {
    "agentic-crm": {
      "command": "uv",
      "args": ["run", "--directory", "D:/GENAIProjects/Agentic-CRM-System/mcp", "python", "server.py"]
    }
  }
}
```

---

## Diagrams

Visual representations of the system architecture, data model, and sales flows are available as Eraser diagram-as-code files in [`mcp/diagrams/`](mcp/diagrams/).

| Diagram | File | Description |
|---------|------|-------------|
| Architecture | [`ARCHITECTURE.md`](mcp/diagrams/ARCHITECTURE.md) | System layers: Client → Server → per-phase tool scripts → DB + Logfire |
| ER Diagram | [`ERD.md`](mcp/diagrams/ERD.md) | Full 21-table data model with relationships |
| Sequence | [`SEQUENCE.md`](mcp/diagrams/SEQUENCE.md) | Lead-to-Deal flow with Logfire observability spans |

To render, paste the ` ```eraser` code block into [Eraser](https://app.eraser.io).

## Production Features

- **Connection pooling** — 10 pool / 20 overflow with recycle
- **Retry logic** — 3 attempts with exponential backoff
- **Soft-delete** — all records via `deleted_at` + `is_active`
- **Timestamps** — automatic `created_at` / `updated_at` on every table
- **Indexes** — all filtered and join columns indexed
- **UUID PKs** — collision-free distributed IDs
- **Decimal precision** — financial fields use `Decimal(15,2)`
- **Expire-on-commit off** — safe read-after-write
- **Any async DB** — swap `DATABASE_URL` for PostgreSQL, MySQL, or SQLite
- **Pydantic Logfire** — structured logging, metrics, tracing across all tools
- **Per-phase tool files** — `src/tools/core.py`, `pipeline.py`, `activities.py`, `campaigns.py`, `reporting.py`, `commerce.py`, `integrations.py` — scale by adding files, not bloating one

---

## Project Structure

```
mcp/
├── docs/                          # Phase-based tool documentation
│   ├── PHASE-1-CORE-CRM.md
│   ├── PHASE-2-LEADS-PIPELINE.md
│   ├── PHASE-3-ACTIVITIES-MEETINGS.md
│   ├── PHASE-4-CAMPAIGNS-MARKETING.md
│   ├── PHASE-5-ANALYTICS-REPORTING.md
│   ├── PHASE-6-QUOTES-ORDER-PRODUCTS.md
│   └── PHASE-7-INTEGRATIONS-AUTOMATION.md
├── diagrams/                      # Eraser diagram-as-code files
│   ├── ARCHITECTURE.md
│   ├── ERD.md
│   └── SEQUENCE.md
├── server.py                      # MCP entry point
├── src/
│   ├── config/
│   │   └── db_config.py           # DB settings (reads .env)
│   ├── services/
│   │   ├── db.py                  # Async engine, retry, pooling
│   │   ├── models.py              # 21 SQLModel table definitions
│   │   └── logfire.py             # Pydantic Logfire observability
│   └── tools/                     # One file per phase — scalable
│       ├── __init__.py
│       ├── core.py                # Phase 1: Company & Contact CRUD
│       ├── pipeline.py            # Phase 2: Leads, Deals, Pipeline
│       ├── activities.py          # Phase 3: Meetings, Tasks, Activity log
│       ├── campaigns.py           # Phase 4: Campaigns, Templates, Sequences
│       ├── reporting.py           # Phase 5: KPIs, Forecasts, Reports
│       ├── commerce.py            # Phase 6: Products, Quotes, Orders
│       └── integrations.py        # Phase 7: Webhooks, API Keys, Automation
├── .env
├── pyproject.toml
└── uv.lock
```

---

## Tech Stack

| Layer | Choice |
|-------|--------|
| Framework | [fastmcp](https://pypi.org/project/fastmcp/) |
| ORM | SQLModel (Pydantic + SQLAlchemy async) |
| Database | PostgreSQL (Neon) / MySQL / SQLite |
| Observability | [Pydantic Logfire](https://pydantic.dev/logfire) |
| Schema | Pydantic-v2 validated settings |
| Runtime | Python 3.14+, uv package manager |
