# Agentic CRM System — MCP Server

An MCP (Model Context Protocol) server for optimizing CRM operations through AI-powered agents. Built with Python, SQLModel, and async PostgreSQL.

## Tech Stack

- **Python 3.11+** — async runtime
- **SQLModel** — ORM with Pydantic + SQLAlchemy
- **PostgreSQL (Neon)** — via asyncpg
- **SQLAlchemy (async)** — engine and session management

## Project Structure

```
mcp/
├── server.py              # Entry point
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   └── db_config.py   # DB settings (reads .env)
│   ├── services/
│   │   ├── db.py          # Async engine & session factory
│   │   └── models.py      # SQLModel table definitions
│   └── tools/
│       └── __init__.py
├── .env                   # DATABASE_URL (not committed)
├── pyproject.toml
└── uv.lock
```

## Database Models

| Table | Key Fields |
|-------|-----------|
| `users` | id (UUID PK), name, email (unique), role |
| `companies` | id (UUID PK), company_name, industry, employee_count, location |
| `contacts` | id (int PK), company_id (FK → companies), first_name, last_name, email, phone, job_title |
| `meetings` | id (UUID PK), title, scheduled_at, status, organizer_id (FK → users), contact_id (FK → contacts), company_id (FK → companies) |
| `campaigns` | id (UUID PK), name, type, status, budget, company_id (FK → companies), created_by (FK → users) |

## Setup

```bash
cd mcp
uv sync
```

Create a `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
```

Run the server:

```bash
uv run python server.py
```

## MCP Client Configuration

To use this server with an MCP client (e.g., opencode, Claude Desktop), add it to your client's MCP config:

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

### Claude Desktop (`claude_desktop_config.json`)

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
