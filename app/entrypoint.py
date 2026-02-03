"""Railway ASGI entrypoint.

This service exposes an MCP server at `/mcp` (FastMCP, streamable HTTP).

Important: FastMCP requires its lifespan to run at startup. If you see 500 errors
on `/mcp` with a message like "Task group is not initialized", it usually means
the FastMCP ASGI app's lifespan is not being executed.
We fix that in app.server by wrapping the FastMCP ASGI app in a parent FastAPI
app and passing `lifespan=mcp_app.lifespan`.
"""

from __future__ import annotations

import os

import uvicorn

from app.server import app


if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.getenv("PORT", "8787"))

    # Railway sits behind a reverse proxy; enable forwarded headers so URLs show https.
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        proxy_headers=True,
        forwarded_allow_ips="*",
        lifespan="on",
    )
