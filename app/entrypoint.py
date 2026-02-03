"""Railway entrypoint.

Important:
ChatGPT MCP uses Streamable HTTP and FastMCP needs its internal runtime
initialized (async task group, session manager, etc.).

If you run the raw ASGI app returned by `mcp.http_app()` under uvicorn without
proper lifespan wiring, the `/mcp` endpoint can crash with:
  "Task group is not initialized. Make sure to use run()."

So for Railway we start via `mcp.run(...)` (through `run_server()`), which is
the most compatible way across FastMCP versions.
"""

from __future__ import annotations

from app.server import run_server


if __name__ == "__main__":
    run_server()
