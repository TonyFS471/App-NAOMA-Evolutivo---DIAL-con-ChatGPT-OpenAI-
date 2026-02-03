"""Railway ASGI entrypoint.

This service exposes a FastMCP HTTP server under `/mcp`.

Why earlier versions returned **500 Internal Server Error** on `/mcp`:
- We wrapped/mounted the FastMCP ASGI app inside another FastAPI app without
  running FastMCP's lifespan. FastMCP initializes internal async task groups
  during lifespan startup; without it, requests to `/mcp` crash.

Fix:
- Use the FastMCP HTTP ASGI app as the *root* ASGI app for uvicorn.
- Add our `/health` endpoint directly on that app (so we keep a stable health
  check for Railway).

Note:
- Opening `/mcp` in a browser may show 406/415 (normal). MCP clients send
  specific headers/content-types.
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.server import mcp


def _resolve_mcp_http_app():
    """Build the FastMCP HTTP ASGI app.

    Some FastMCP versions expose `http_app`, others may expose `asgi_app`.
    We try the common forms.
    """

    # FastMCP >=2.x
    if hasattr(mcp, "http_app"):
        return mcp.http_app(path="/mcp")

    # Fallback (older/alternate)
    if hasattr(mcp, "asgi_app"):
        return mcp.asgi_app(path="/mcp")

    raise RuntimeError(
        "FastMCP instance does not expose an HTTP ASGI app constructor. "
        "Expected `http_app` or `asgi_app`."
    )


# IMPORTANT: make the FastMCP app the root uvicorn target so its lifespan runs.
app = _resolve_mcp_http_app()


# Add a stable health endpoint for Railway.
# Works if `app` is FastAPI/Starlette.
try:
    # FastAPI style
    if hasattr(app, "get"):

        @app.get("/health")
        async def health():
            return {
                "status": "ok",
                "time": datetime.now(timezone.utc).isoformat(),
            }

    else:
        # Starlette style
        from starlette.responses import JSONResponse

        async def _health(_request):
            return JSONResponse(
                {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}
            )

        app.add_route("/health", _health, methods=["GET"])

except Exception:
    # If anything goes wrong, we still want the MCP app to run.
    pass


if __name__ == "__main__":
    # Allow running via `python -m app.entrypoint` (Railway/Docker).
    import uvicorn

    uvicorn.run(
        "app.entrypoint:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        log_level=os.getenv("LOG_LEVEL", "info"),
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
