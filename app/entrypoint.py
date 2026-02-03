"""Railway-friendly entrypoint.

Why this exists:
- Railway expects the server to bind to 0.0.0.0 on the provided PORT.
- Railway healthchecks often hit GET /health.

FastMCP's built-in runner may bind to 127.0.0.1 depending on version/config.
This entrypoint forces a public bind (0.0.0.0) and provides /health.
"""

import os

from fastapi import FastAPI

# Import your MCP server definition (tools/architectures)
from .server import mcp  # noqa: E402


def _resolve_mcp_asgi_app():
    """Try multiple FastMCP APIs across versions to get an ASGI app."""

    # Preferred: a helper that returns a FastAPI/ASGI app
    if hasattr(mcp, "http_app"):
        http_app = getattr(mcp, "http_app")
        try:
            return http_app(path="/mcp")
        except TypeError:
            # Older signatures
            try:
                return http_app()
            except TypeError:
                return http_app

    # Common attribute names
    for attr in ("app", "asgi_app", "fastapi_app"):
        if hasattr(mcp, attr):
            return getattr(mcp, attr)

    raise RuntimeError(
        "Could not resolve an ASGI app from FastMCP. "
        "Check your fastmcp version and expose an app/http_app." 
    )


# Wrap MCP app with a stable health endpoint
mcp_asgi = _resolve_mcp_asgi_app()
app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


# Mount the MCP server (keeps /mcp and any other routes)
app.mount("/", mcp_asgi)


def main():
    import uvicorn

    port = int(os.getenv("PORT", os.getenv("NAOMA_PORT", "8787")))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
