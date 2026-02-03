"""
NAOMA Evolutivo - DIAL: OpenAI Apps SDK MCP Server
===================================================
14 Unified AI Architectures for AGI Foundations

Author: Ing. Santos Antonio Fraustro Solís
Patent: IMPI Mexico MX/a/2025/009736
License: All Rights Reserved

FIXED VERSION - Proper ASGI lifespan integration
"""

import os
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Runtime configuration
# ---------------------------------------------------------------------------
MCP_PATH = os.getenv("MCP_PATH", "/mcp")
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
# MCP SERVER SETUP (Tools only - no custom routes here!)
# ============================================================================

mcp = FastMCP(name="NAOMA DIAL")


@mcp.tool()
def analyze_with_dial(query: str, architectures: str = "naoma_evolutivo,ipa_introspection,sstap_security") -> dict:
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
# FASTAPI APPLICATION WITH PROPER LIFESPAN
# ============================================================================

# Get the MCP ASGI app
mcp_app = mcp.http_app(path=MCP_PATH)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    CRITICAL: This lifespan context manager initializes FastMCP's
    StreamableHTTPSessionManager task group. Without this, /mcp will 500.
    """
    async with mcp_app.lifespan(app):
        print("🧠 NAOMA Evolutivo - DIAL MCP Server Started")
        print(f"📋 14 DIAL Architectures loaded")
        print(f"🔗 MCP endpoint: {MCP_PATH}")
        yield
        print("🛑 NAOMA DIAL Server shutting down...")


# Create FastAPI app WITH the MCP lifespan
app = FastAPI(
    title="NAOMA Evolutivo - DIAL",
    description="14 Unified AI Architectures for AGI Foundations",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount MCP app at its path
app.mount(MCP_PATH, mcp_app)


# ============================================================================
# FASTAPI ROUTES (NOT mcp.custom_route!)
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Landing page for Railway / browser access."""
    base = str(request.base_url).rstrip("/")
    mcp_url = f"{base}{MCP_PATH}"
    health_url = f"{base}/health"
    
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>NAOMA DIAL MCP Server</title>
  <style>
    body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;background:#0b0f19;color:#e8eefc;margin:0;}}
    .wrap{{max-width:900px;margin:0 auto;padding:40px 20px;}}
    .card{{background:#111a2e;border:1px solid #223055;border-radius:16px;padding:24px;box-shadow:0 10px 30px rgba(0,0,0,.35);margin-bottom:20px;}}
    code{{background:#0b1224;border:1px solid #223055;border-radius:6px;padding:2px 8px;font-family:monospace;}}
    pre{{background:#0b1224;border:1px solid #223055;border-radius:12px;padding:16px;overflow-x:auto;white-space:pre-wrap;}}
    a{{color:#8bd3ff;}}
    h1{{background:linear-gradient(135deg,#6366f1,#8b5cf6,#06b6d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:2.5em;margin-bottom:10px;}}
    .status{{display:inline-block;background:#10b981;color:white;padding:4px 12px;border-radius:20px;font-size:0.85em;margin-left:10px;}}
    .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-top:16px;}}
    .arch{{background:#0b1224;border:1px solid #223055;border-radius:10px;padding:12px;}}
    .arch-icon{{font-size:1.5em;margin-bottom:4px;}}
    .arch-name{{font-weight:600;font-size:0.9em;}}
    .arch-cat{{font-size:0.75em;color:#64748b;}}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>🧠 NAOMA Evolutivo - DIAL</h1>
    <span class="status">✓ Online</span>
    
    <div class="card">
      <h2>🔗 Endpoints</h2>
      <p><strong>MCP Endpoint:</strong> <a href="{mcp_url}"><code>{mcp_url}</code></a></p>
      <p><strong>Health Check:</strong> <a href="{health_url}"><code>{health_url}</code></a></p>
      <p style="color:#64748b;font-size:0.9em;">Note: The MCP endpoint expects JSON-RPC requests from ChatGPT/MCP clients. Browser access may show 405/406.</p>
    </div>
    
    <div class="card">
      <h2>📋 14 DIAL Architectures</h2>
      <div class="grid">
        <div class="arch"><div class="arch-icon">🧠</div><div class="arch-name">NAOMA Evolutivo</div><div class="arch-cat">Core Systems</div></div>
        <div class="arch"><div class="arch-icon">🔍</div><div class="arch-name">Deep Introspection</div><div class="arch-cat">Core Systems</div></div>
        <div class="arch"><div class="arch-icon">🌐</div><div class="arch-name">4D Embeddings</div><div class="arch-cat">Advanced Processing</div></div>
        <div class="arch"><div class="arch-icon">🔢</div><div class="arch-name">Multibinary</div><div class="arch-cat">Advanced Processing</div></div>
        <div class="arch"><div class="arch-icon">🎯</div><div class="arch-name">S-A Attention</div><div class="arch-cat">Advanced Processing</div></div>
        <div class="arch"><div class="arch-icon">📚</div><div class="arch-name">A-Query RAG</div><div class="arch-cat">Information Retrieval</div></div>
        <div class="arch"><div class="arch-icon">🧬</div><div class="arch-name">NeuroEmbedX</div><div class="arch-cat">Scientific Computing</div></div>
        <div class="arch"><div class="arch-icon">💻</div><div class="arch-name">AgentCodex Pro</div><div class="arch-cat">Software Engineering</div></div>
        <div class="arch"><div class="arch-icon">🛡️</div><div class="arch-name">SSTAP Security</div><div class="arch-cat">Security & Safety</div></div>
        <div class="arch"><div class="arch-icon">🎭</div><div class="arch-name">MoE Orchestrator</div><div class="arch-cat">Orchestration</div></div>
        <div class="arch"><div class="arch-icon">🖼️</div><div class="arch-name">Multimodal</div><div class="arch-cat">Multimodal</div></div>
        <div class="arch"><div class="arch-icon">✨</div><div class="arch-name">PromptEngineer</div><div class="arch-cat">Optimization</div></div>
        <div class="arch"><div class="arch-icon">📐</div><div class="arch-name">MathEngine</div><div class="arch-cat">Scientific Computing</div></div>
        <div class="arch"><div class="arch-icon">⚡</div><div class="arch-name">Super Streaming</div><div class="arch-cat">Real-time</div></div>
      </div>
    </div>
    
    <div class="card">
      <h2>🧪 Test with curl</h2>
      <pre>curl -X POST {mcp_url} \\
  -H "Content-Type: application/json" \\
  -d '{{"jsonrpc":"2.0","method":"tools/list","id":1}}'</pre>
    </div>
    
    <div class="card">
      <h2>🔌 Connect from ChatGPT</h2>
      <ol>
        <li>Go to ChatGPT Settings → Developer Mode</li>
        <li>Add new MCP connector</li>
        <li>Paste URL: <code>{mcp_url}</code></li>
        <li>Test: "Use NAOMA DIAL to analyze AI safety"</li>
      </ol>
    </div>
    
    <p style="text-align:center;color:#64748b;margin-top:24px;">
      Developed by <strong>Ing. Santos Antonio Fraustro Solís</strong><br/>
      Patent IMPI Mexico MX/a/2025/009736 • © 2026
    </p>
  </div>
</body>
</html>"""
    return HTMLResponse(content=html)


@app.get("/health")
async def health():
    """Health check endpoint for Railway."""
    return {
        "status": "ok",
        "time": datetime.now(timezone.utc).isoformat(),
        "name": "NAOMA DIAL",
        "version": "2.0.0",
        "architectures": 14
    }


@app.get("/favicon.ico")
async def favicon():
    """Return empty favicon to prevent 404 noise."""
    return Response(status_code=204)


@app.get("/favicon.svg")
async def favicon_svg():
    """Return empty favicon SVG."""
    return Response(status_code=204)


@app.get("/favicon.png")
async def favicon_png():
    """Return empty favicon PNG."""
    return Response(status_code=204)


@app.get("/api/architectures")
async def get_architectures():
    """REST API endpoint to list all architectures."""
    return {
        "total": 14,
        "architectures": [
            {
                "id": arch_id,
                "name": arch["name"],
                "icon": arch["icon"],
                "description": arch["description"],
                "category": arch["category"]
            }
            for arch_id, arch in DIAL_ARCHITECTURES.items()
        ]
    }


# ============================================================================
# MAIN ENTRY
# ============================================================================

def run_server():
    """Start the server with uvicorn."""
    import uvicorn
    
    print("=" * 60)
    print("🧠 NAOMA Evolutivo - DIAL MCP Server v2.0.0")
    print("=" * 60)
    print(f"📋 14 DIAL Architectures loaded")
    print(f"🔗 MCP endpoint: {MCP_PATH}")
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
