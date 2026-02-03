"""
NAOMA Evolutivo - DIAL: OpenAI Apps SDK MCP Server
===================================================
14 Unified AI Architectures for AGI Foundations

Author: Ing. Santos Antonio Fraustro Solís
Patent: IMPI Mexico MX/a/2025/009736
License: All Rights Reserved

This MCP server exposes the 14 DIAL architectures as tools
that ChatGPT can call to provide enhanced AI responses.
"""

import os
from datetime import datetime
from typing import Dict, List, Any

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastmcp import FastMCP

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
# WIDGET HTML COMPONENT
# ============================================================================

WIDGET_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NAOMA DIAL</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 50%, #1e1b4b 100%);
            color: white;
            min-height: 100vh;
            padding: 16px;
        }
        .container { max-width: 100%; }
        .header {
            text-align: center;
            margin-bottom: 16px;
            padding: 16px;
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .logo { font-size: 40px; margin-bottom: 8px; }
        h1 {
            font-size: 22px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 4px;
        }
        .subtitle { color: #94a3b8; font-size: 13px; }
        .stats {
            display: flex;
            justify-content: center;
            gap: 24px;
            margin-top: 12px;
        }
        .stat { text-align: center; }
        .stat-value { font-size: 20px; font-weight: bold; color: #6366f1; }
        .stat-label { font-size: 11px; color: #64748b; }
        .architectures {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 8px;
            margin-top: 16px;
        }
        .arch-card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 12px;
            transition: all 0.2s;
            cursor: pointer;
        }
        .arch-card:hover {
            background: rgba(99, 102, 241, 0.1);
            border-color: rgba(99, 102, 241, 0.3);
        }
        .arch-card.active {
            background: rgba(99, 102, 241, 0.2);
            border-color: #6366f1;
        }
        .arch-icon { font-size: 20px; margin-bottom: 6px; }
        .arch-name { font-size: 11px; font-weight: 600; margin-bottom: 2px; }
        .arch-category { font-size: 10px; color: #64748b; }
        .result {
            margin-top: 16px;
            padding: 12px;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            border: 1px solid rgba(99, 102, 241, 0.3);
        }
        .result-title { font-size: 12px; font-weight: 600; color: #6366f1; margin-bottom: 8px; }
        .result-query { font-size: 13px; color: #e2e8f0; margin-bottom: 8px; }
        .result-archs { font-size: 11px; color: #94a3b8; }
        .footer {
            text-align: center;
            margin-top: 16px;
            padding-top: 12px;
            border-top: 1px solid rgba(255,255,255,0.1);
            font-size: 10px;
            color: #64748b;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🧠</div>
            <h1>NAOMA Evolutivo - DIAL</h1>
            <p class="subtitle">14 Unified AI Architectures for AGI</p>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value" id="activeCount">0</div>
                    <div class="stat-label">Active</div>
                </div>
                <div class="stat">
                    <div class="stat-value">14</div>
                    <div class="stat-label">Total</div>
                </div>
            </div>
        </div>
        
        <div class="architectures" id="archGrid"></div>
        
        <div class="result" id="resultSection" style="display: none;">
            <div class="result-title">📊 Analysis Result</div>
            <div class="result-query" id="resultQuery"></div>
            <div class="result-archs" id="resultArchs"></div>
        </div>
        
        <div class="footer">
            <p>Developed by Ing. Santos Antonio Fraustro Solís</p>
            <p>Patent IMPI Mexico MX/a/2025/009736</p>
        </div>
    </div>
    
    <script>
        const architectures = [
            { id: 'naoma_evolutivo', name: 'NAOMA Evolutivo', icon: '🧠', category: 'Core' },
            { id: 'ipa_introspection', name: 'Deep Introspection', icon: '🔍', category: 'Core' },
            { id: 'embeddings_4d', name: '4D Embeddings', icon: '🌐', category: 'Processing' },
            { id: 'multibinary', name: 'Multibinary', icon: '🔢', category: 'Processing' },
            { id: 'sa_attention', name: 'S-A Attention', icon: '🎯', category: 'Processing' },
            { id: 'aquery_rag', name: 'A-Query RAG', icon: '📚', category: 'Retrieval' },
            { id: 'neuroembedx', name: 'NeuroEmbedX', icon: '🧬', category: 'Scientific' },
            { id: 'agentcodex_pro', name: 'AgentCodex Pro', icon: '💻', category: 'Engineering' },
            { id: 'sstap_security', name: 'SSTAP Security', icon: '🛡️', category: 'Security' },
            { id: 'moe_orchestrator', name: 'MoE Orchestrator', icon: '🎭', category: 'Orchestration' },
            { id: 'multimodal_processor', name: 'Multimodal', icon: '🖼️', category: 'Multimodal' },
            { id: 'prompt_engineer', name: 'PromptEngineer', icon: '✨', category: 'Optimization' },
            { id: 'math_engine', name: 'MathEngine', icon: '📐', category: 'Scientific' },
            { id: 'super_streaming', name: 'Super Streaming', icon: '⚡', category: 'Streaming' }
        ];
        
        let activeArchs = new Set(['naoma_evolutivo', 'sstap_security']);
        
        function renderArchitectures() {
            const grid = document.getElementById('archGrid');
            grid.innerHTML = architectures.map(arch => `
                <div class="arch-card ${activeArchs.has(arch.id) ? 'active' : ''}" 
                     onclick="toggleArch('${arch.id}')">
                    <div class="arch-icon">${arch.icon}</div>
                    <div class="arch-name">${arch.name}</div>
                    <div class="arch-category">${arch.category}</div>
                </div>
            `).join('');
            
            document.getElementById('activeCount').textContent = activeArchs.size;
        }
        
        function toggleArch(id) {
            if (id === 'sstap_security') return;
            if (activeArchs.has(id)) {
                activeArchs.delete(id);
            } else {
                activeArchs.add(id);
            }
            renderArchitectures();
            
            if (window.openai && window.openai.setWidgetState) {
                window.openai.setWidgetState({ activeArchitectures: Array.from(activeArchs) });
            }
        }
        
        function showResult(data) {
            if (data && data.query) {
                document.getElementById('resultSection').style.display = 'block';
                document.getElementById('resultQuery').textContent = '📝 ' + data.query;
                document.getElementById('resultArchs').textContent = 
                    '🔧 ' + data.total_architectures + ' architectures active';
            }
        }
        
        // Initialize
        renderArchitectures();
        
        // Check for data from ChatGPT
        if (window.openai && window.openai.toolOutput) {
            const data = window.openai.toolOutput;
            
            if (data.structuredContent) {
                showResult(data.structuredContent);
                
                if (data.structuredContent.architectures_active) {
                    activeArchs = new Set(data.structuredContent.architectures_active.map(a => a.id));
                    activeArchs.add('sstap_security');
                    renderArchitectures();
                }
            }
        }
        
        // Report height to ChatGPT
        if (window.openai && window.openai.notifyIntrinsicHeight) {
            setTimeout(() => {
                window.openai.notifyIntrinsicHeight(document.body.scrollHeight);
            }, 100);
        }
    </script>
</body>
</html>"""

# ============================================================================
# MCP SERVER SETUP
# ============================================================================

# Initialize FastMCP server
mcp = FastMCP(
    name="NAOMA DIAL",
)

# ---------------------------------------------------------------------------
# Human-friendly landing page (Railway / browser)
# ---------------------------------------------------------------------------

@mcp.custom_route("/", methods=["GET"])
async def index(request: Request):
    """Simple landing page so the Railway base URL doesn't return 404."""
    base = str(request.base_url).rstrip("/")
    mcp_url = base + MCP_PATH
    health_url = base + "/health"
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>NAOMA DIAL MCP Server</title>
  <style>
    body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;background:#0b0f19;color:#e8eefc;margin:0;}}
    .wrap{{max-width:900px;margin:0 auto;padding:40px 20px;}}
    .card{{background:#111a2e;border:1px solid #223055;border-radius:16px;padding:20px;box-shadow:0 10px 30px rgba(0,0,0,.35);}}
    code{{background:#0b1224;border:1px solid #223055;border-radius:10px;padding:2px 8px;}}
    a{{color:#8bd3ff;}}
    .muted{{opacity:.85;}}
    .row{{display:flex;flex-wrap:wrap;gap:12px;margin-top:14px;}}
    .pill{{background:#0b1224;border:1px solid #223055;border-radius:999px;padding:10px 14px;}}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>NAOMA DIAL — MCP Server</h1>
    <p class="muted">Your deployment is running. If you open the base URL in a browser, this page is what you should see.</p>

    <div class="card">
      <h2>Endpoints</h2>
      <div class="row">
        <div class="pill">MCP endpoint: <a href="{mcp_url}"><code>{mcp_url}</code></a></div>
        <div class="pill">Health: <a href="{health_url}"><code>{health_url}</code></a></div>
      </div>

      <h3 style="margin-top:18px">Why <code>/mcp</code> may show 406 in the browser</h3>
      <p class="muted">That is normal. The MCP endpoint expects specific headers from an MCP client. Use ChatGPT/your MCP client, or test with curl.</p>
      <pre style="white-space:pre-wrap;background:#0b1224;border:1px solid #223055;border-radius:12px;padding:12px;overflow:auto">curl -i -H "Accept: application/json" "{mcp_url}"</pre>

      <h3>Connect from ChatGPT</h3>
      <p class="muted">In ChatGPT, add a new MCP server and paste the MCP endpoint URL above.</p>
    </div>

    <p class="muted" style="margin-top:18px">Built with FastMCP. 🚀</p>
  </div>
</body>
</html>"""
    return HTMLResponse(html)


@mcp.custom_route("/favicon.ico", methods=["GET"])
async def favicon():
    # Avoid noisy 404s from browsers.
    return Response(status_code=204)


# ============================================================================
# MCP TOOLS
# ============================================================================

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
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8787"))
    print(f"🧠 NAOMA Evolutivo - DIAL starting on port {port}")
    print(f"📋 14 DIAL Architectures loaded")
    print(f"🔗 MCP endpoint: http://localhost:{port}/mcp")
    mcp.run(transport="http", host="0.0.0.0", port=port)