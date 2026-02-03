"""
NAOMA Evolutivo - DIAL: OpenAI Apps SDK MCP Server
===================================================
14 Unified AI Architectures for AGI Foundations

Author: Ing. Santos Antonio Fraustro Solís
Patent: IMPI Mexico MX/a/2025/009736
License: All Rights Reserved

VERSION 3.1 - Using FastMCP.streamable_http_app() correctly
This version properly initializes the MCP session manager.
"""

import os
import json
from datetime import datetime, timezone

from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response

from mcp.server import FastMCP

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PORT = int(os.getenv("PORT", "8080"))

# ============================================================================
# THE 14 DIAL ARCHITECTURES
# ============================================================================

DIAL_ARCHITECTURES = {
    "naoma_evolutivo": {
        "name": "NAOMA Evolutivo",
        "icon": "🧠",
        "description": "Multi-agent Neural Auto-Optimization System with hierarchical dynamic architecture",
        "category": "Core Systems",
        "prompt": "Apply multi-agent neural optimization: analyze from multiple specialized perspectives, orchestrate collaborative solutions, and provide structured, actionable insights."
    },
    "ipa_introspection": {
        "name": "Advanced Deep Introspection (IPA)",
        "icon": "🔍",
        "description": "Algorithmic consciousness modules analyzing reasoning processes",
        "category": "Core Systems",
        "prompt": "Apply deep introspection: analyze your reasoning step-by-step, explain WHY you reach each conclusion, what alternatives you considered, and be transparent about uncertainty."
    },
    "embeddings_4d": {
        "name": "Dynamic 4D Embeddings",
        "icon": "🌐",
        "description": "Spatio-temporal representations evolving as trajectories in ℝ³ × τ",
        "category": "Advanced Processing",
        "prompt": "Apply 4D embedding principles: consider how concepts evolve over time, their spatial relationships to related ideas, and track semantic drift across temporal contexts."
    },
    "multibinary": {
        "name": "Integrated Multibinary Computing",
        "icon": "🔢",
        "description": "Pascal's Triangle weighted computation for exponential representational capacity",
        "category": "Advanced Processing",
        "prompt": "Apply multibinary computation: consider multiple simultaneous truth values, weighted evidence combinations, and analyze through exponentially richer state spaces."
    },
    "sa_attention": {
        "name": "S-A Attention (Statistical-Adaptive)",
        "icon": "🎯",
        "description": "Probabilistic modification of substantive keys by adjective queries",
        "category": "Advanced Processing",
        "prompt": "Apply Statistical-Adaptive attention: dynamically weight information relevance, use probabilistic key modification, and focus on the most pertinent aspects."
    },
    "aquery_rag": {
        "name": "A-Query System (RAG)",
        "icon": "📚",
        "description": "Semantic compression with complete traceability and evidence-based responses",
        "category": "Information Retrieval",
        "prompt": "Apply A-Query RAG: prioritize evidence-based responses with source traceability, compress semantic information efficiently, and state limitations clearly."
    },
    "neuroembedx": {
        "name": "NeuroEmbedX",
        "icon": "🧬",
        "description": "Scientific programming treating molecules, equations, tensors as first-class objects",
        "category": "Scientific Computing",
        "prompt": "Apply NeuroEmbedX: treat scientific entities as first-class objects, provide precise mathematical notation, chemical formulas, and bridge scientific domains computationally."
    },
    "agentcodex_pro": {
        "name": "AgentCodex Pro",
        "icon": "💻",
        "description": "Specialized agent for code generation, execution, and self-correction",
        "category": "Software Engineering",
        "prompt": "Apply AgentCodex Pro: generate clean, modular, well-documented code with error handling, tests, deployment instructions, and self-verify logic."
    },
    "sstap_security": {
        "name": "SSTAP Security",
        "icon": "🛡️",
        "description": "Multi-layer security with filtering, sanitization, and validation",
        "category": "Security & Safety",
        "prompt": "Apply SSTAP Security: validate inputs, sanitize outputs, prevent information leakage, prioritize user safety, data privacy, and flag security concerns proactively."
    },
    "moe_orchestrator": {
        "name": "MoE Orchestrator",
        "icon": "🎭",
        "description": "Mixture of Experts with dynamic routing and task-based specialization",
        "category": "Orchestration",
        "prompt": "Apply MoE orchestration: identify required expertise domains, coordinate from virtual expert perspectives, and synthesize into coherent, comprehensive solutions."
    },
    "multimodal_processor": {
        "name": "Multimodal Processor",
        "icon": "🖼️",
        "description": "Coherent fusion of text, images, audio, and video in unified embeddings",
        "category": "Multimodal",
        "prompt": "Apply multimodal processing: analyze images thoroughly, integrate visual with textual context, describe what you see, and synthesize insights across modalities."
    },
    "prompt_engineer": {
        "name": "PromptEngineer",
        "icon": "✨",
        "description": "Prompt auto-optimization through semantic rate-distortion analysis",
        "category": "Optimization",
        "prompt": "Apply PromptEngineer: analyze semantic structure, identify redundancies, clarify ambiguities, and optimize for both human readability and model comprehension."
    },
    "math_engine": {
        "name": "MathEngine",
        "icon": "📐",
        "description": "Symbolic mathematical computation with step-by-step problem solving",
        "category": "Scientific Computing",
        "prompt": "Apply MathEngine: solve problems step-by-step showing all work, use proper mathematical notation, handle algebra, calculus, statistics, and verify solutions."
    },
    "super_streaming": {
        "name": "Super Streaming Multimodal",
        "icon": "⚡",
        "description": "Real-time stream processing with selective attention and adaptive compression",
        "category": "Real-time Streaming",
        "prompt": "Apply Super Streaming: deliver responses incrementally - quick summary first, then details, then actionable items. Optimize for progressive disclosure."
    }
}

# ============================================================================
# CREATE FASTMCP SERVER
# ============================================================================

# Initialize FastMCP with stateless HTTP mode for Railway scalability
mcp = FastMCP(
    name="NAOMA DIAL",
    instructions="14 Unified AI Architectures for AGI Foundations by Ing. Santos Antonio Fraustro Solís",
    stateless_http=True,  # Important for Railway multi-replica
    json_response=True,   # Better compatibility
)

# ============================================================================
# DEFINE TOOLS
# ============================================================================

@mcp.tool()
def analyze_with_dial(
    query: str,
    architectures: str = "naoma_evolutivo,ipa_introspection,sstap_security"
) -> dict:
    """
    Analyze a query using NAOMA DIAL's unified AI architectures.
    
    This tool activates specified DIAL architectures to provide enhanced,
    multi-perspective analysis. Each architecture adds a unique analytical
    lens to the response.
    
    Args:
        query: The question, problem, or topic to analyze
        architectures: Comma-separated architecture IDs (naoma_evolutivo, ipa_introspection, 
            embeddings_4d, multibinary, sa_attention, aquery_rag, neuroembedx, agentcodex_pro,
            sstap_security, moe_orchestrator, multimodal_processor, prompt_engineer, 
            math_engine, super_streaming)
    
    Returns:
        Analysis configuration with active architectures and combined prompts
    """
    arch_list = [a.strip() for a in architectures.split(",") if a.strip()]
    active_archs = [a for a in arch_list if a in DIAL_ARCHITECTURES]
    
    if not active_archs:
        active_archs = ["naoma_evolutivo"]
    
    if "sstap_security" not in active_archs:
        active_archs.append("sstap_security")
    
    arch_details = []
    combined_instructions = []
    
    for arch_id in active_archs:
        arch = DIAL_ARCHITECTURES[arch_id]
        arch_details.append({
            "id": arch_id,
            "name": arch["name"],
            "icon": arch["icon"],
            "category": arch["category"]
        })
        combined_instructions.append(f"[{arch['icon']} {arch['name']}]: {arch['prompt']}")
    
    return {
        "query": query,
        "architectures_active": arch_details,
        "total_architectures": len(active_archs),
        "combined_instructions": "\n\n".join(combined_instructions),
        "timestamp": datetime.now().isoformat(),
        "author": "Ing. Santos Antonio Fraustro Solís",
        "patent": "IMPI Mexico MX/a/2025/009736"
    }


@mcp.tool()
def list_dial_architectures() -> dict:
    """
    List all 14 DIAL architectures available in NAOMA Evolutivo.
    
    Use this to discover available architectures and their capabilities.
    """
    architectures = []
    categories = {}
    
    for arch_id, arch in DIAL_ARCHITECTURES.items():
        architectures.append({
            "id": arch_id,
            "name": arch["name"],
            "icon": arch["icon"],
            "description": arch["description"],
            "category": arch["category"]
        })
        
        cat = arch["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(f"{arch['icon']} {arch['name']}")
    
    return {
        "total": 14,
        "architectures": architectures,
        "categories": categories,
        "title": "NAOMA Evolutivo - DIAL",
        "author": "Ing. Santos Antonio Fraustro Solís"
    }


@mcp.tool()
def code_with_agentcodex(task: str, language: str = "python") -> dict:
    """
    Generate code using AgentCodex Pro architecture.
    
    Args:
        task: Description of what the code should do
        language: Programming language (python, javascript, typescript, etc.)
    """
    return {
        "task": task,
        "language": language,
        "architecture": "AgentCodex Pro",
        "instructions": f"Generate clean, modular {language} code for: {task}. Include error handling, comments, and usage examples."
    }


@mcp.tool()
def solve_math(problem: str) -> dict:
    """
    Solve mathematical problems using MathEngine architecture.
    
    Args:
        problem: The mathematical problem or equation to solve
    """
    return {
        "problem": problem,
        "architecture": "MathEngine",
        "instructions": f"Solve step-by-step with proper notation: {problem}"
    }


# ============================================================================
# CUSTOM ROUTES (Added to the Starlette app)
# ============================================================================

@mcp.custom_route("/", methods=["GET"])
async def index(request: Request) -> HTMLResponse:
    """Landing page."""
    base = str(request.base_url).rstrip("/")
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>NAOMA DIAL MCP Server</title>
  <style>
    body{{font-family:system-ui,-apple-system,sans-serif;background:#0b0f19;color:#e8eefc;margin:0;padding:20px;}}
    .container{{max-width:800px;margin:0 auto;}}
    h1{{background:linear-gradient(135deg,#6366f1,#8b5cf6,#06b6d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}}
    .card{{background:#111a2e;border:1px solid #223055;border-radius:12px;padding:20px;margin:16px 0;}}
    code{{background:#0b1224;padding:2px 8px;border-radius:4px;}}
    pre{{background:#0b1224;padding:16px;border-radius:8px;overflow-x:auto;white-space:pre-wrap;}}
    a{{color:#8bd3ff;}}
    .status{{display:inline-block;background:#10b981;padding:4px 12px;border-radius:20px;font-size:0.85em;}}
    .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px;margin-top:16px;}}
    .arch{{background:#0b1224;border:1px solid #223055;border-radius:8px;padding:10px;text-align:center;}}
    .arch-icon{{font-size:1.5em;}}
  </style>
</head>
<body>
  <div class="container">
    <h1>🧠 NAOMA Evolutivo - DIAL</h1>
    <span class="status">✓ Online</span>
    <p>14 Unified AI Architectures for AGI Foundations</p>
    
    <div class="card">
      <h2>🔗 Endpoints</h2>
      <p><strong>MCP:</strong> <code>{base}/mcp</code></p>
      <p><strong>Health:</strong> <code>{base}/health</code></p>
      <p style="color:#94a3b8;font-size:0.9em;">Note: MCP endpoint expects JSON-RPC from ChatGPT/MCP clients.</p>
    </div>
    
    <div class="card">
      <h2>🧪 Test MCP</h2>
      <pre>curl -X POST {base}/mcp \\
  -H "Content-Type: application/json" \\
  -d '{{"jsonrpc":"2.0","method":"tools/list","id":1}}'</pre>
    </div>
    
    <div class="card">
      <h2>🔌 Connect from ChatGPT</h2>
      <ol style="line-height:1.8;">
        <li>Open ChatGPT → Settings → Developer Mode</li>
        <li>Add new MCP connector</li>
        <li>Paste URL: <code>{base}/mcp</code></li>
        <li>Test: "Use NAOMA DIAL to analyze AI safety"</li>
      </ol>
    </div>
    
    <div class="card">
      <h2>📋 14 Architectures</h2>
      <div class="grid">
        {"".join(f'<div class="arch"><div class="arch-icon">{a["icon"]}</div><div style="font-size:0.85em;">{a["name"]}</div></div>' for a in DIAL_ARCHITECTURES.values())}
      </div>
    </div>
    
    <p style="text-align:center;color:#64748b;margin-top:24px;">
      Developed by <strong>Ing. Santos Antonio Fraustro Solís</strong><br/>
      Patent IMPI Mexico MX/a/2025/009736 • © 2026
    </p>
  </div>
</body>
</html>"""
    return HTMLResponse(content=html)


@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    """Health check endpoint for Railway."""
    return JSONResponse({
        "status": "ok",
        "time": datetime.now(timezone.utc).isoformat(),
        "name": "NAOMA DIAL",
        "version": "3.1.0",
        "architectures": 14
    })


@mcp.custom_route("/favicon.ico", methods=["GET"])
async def favicon_ico(request: Request) -> Response:
    """Favicon - return 204."""
    return Response(status_code=204)


@mcp.custom_route("/favicon.svg", methods=["GET"])
async def favicon_svg(request: Request) -> Response:
    """Favicon SVG - return 204."""
    return Response(status_code=204)


@mcp.custom_route("/favicon.png", methods=["GET"])
async def favicon_png(request: Request) -> Response:
    """Favicon PNG - return 204."""
    return Response(status_code=204)


# OAuth discovery endpoints - return 404 as required by OpenAI Apps SDK
# when not using authentication

@mcp.custom_route("/.well-known/oauth-authorization-server", methods=["GET"])
async def oauth_well_known(request: Request) -> JSONResponse:
    """Return 404 for OAuth discovery (not using auth)."""
    return JSONResponse(
        {"error": "not_found", "message": "OAuth not configured"},
        status_code=404
    )


@mcp.custom_route("/.well-known/oauth-authorization-server/mcp", methods=["GET"])
async def oauth_well_known_mcp(request: Request) -> JSONResponse:
    """Return 404 for OAuth discovery /mcp (not using auth)."""
    return JSONResponse(
        {"error": "not_found", "message": "OAuth not configured"},
        status_code=404
    )


@mcp.custom_route("/.well-known/oauth-protected-resource", methods=["GET"])
async def oauth_protected_resource(request: Request) -> JSONResponse:
    """Return 404 for OAuth protected resource (not using auth)."""
    return JSONResponse(
        {"error": "not_found", "message": "OAuth not configured"},
        status_code=404
    )


@mcp.custom_route("/mcp/.well-known/oauth-authorization-server", methods=["GET"])
async def oauth_mcp_well_known(request: Request) -> JSONResponse:
    """Return 404 for nested OAuth discovery (not using auth)."""
    return JSONResponse(
        {"error": "not_found", "message": "OAuth not configured"},
        status_code=404
    )


# ============================================================================
# GET THE STARLETTE APP
# ============================================================================

# This creates the Starlette app with proper lifespan and session manager
app = mcp.streamable_http_app()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def run_server():
    """Start the server."""
    import uvicorn
    
    print("=" * 60)
    print("🧠 NAOMA Evolutivo - DIAL MCP Server v3.1.0")
    print("=" * 60)
    print(f"📋 14 DIAL Architectures loaded")
    print(f"🔗 MCP endpoint: /mcp")
    print(f"🚀 Starting on port {PORT}...")
    print("=" * 60)
    
    uvicorn.run(
        "app.server:app",
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )


if __name__ == "__main__":
    run_server()
