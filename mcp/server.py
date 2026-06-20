from src.services.db import init_db, close_db
from src.tools.crm_tools import mcp


@mcp.on_startup
async def startup():
    await init_db()


@mcp.on_shutdown
async def shutdown():
    await close_db()


if __name__ == "__main__":
    mcp.run()
