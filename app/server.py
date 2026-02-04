from __future__ import annotations

import os
import json
from typing import Any, Dict, List, Optional

from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, Response

try:
    # FastMCP package variant
    from fastmcp import FastMCP  # type: ignore
except Exception:  # pragma: no cover
    # Official MCP SDK path variant
    from mcp.server.fastmcp import FastMCP  # type: ignore

types = None  # (intentionally unused)

from naoma.registry import NAOMARegistry
from naoma.architectures.naoma_evolutivo import NAOMAEvolutivo


BASE_NAME = "NAOMA Evolutivo - DIAL"
MIME_WIDGET = "text/html+skybridge"

# Load widget HTML from file for easy editing
_UI_PATH = os.path.join(os.path.dirname(__file__), "naoma", "ui", "dashboard.html")
with open(_UI_PATH, "r", encoding="utf-8") as f:
    DASHBOARD_HTML = f.read()


registry = NAOMARegistry.create()
naoma = NAOMAEvolutivo(registry=registry)

mcp = FastMCP(
    name=BASE_NAME,
    instructions=(
        "NAOMA Evolutivo - DIAL: 14 unified architectures implemented as real tools "
        "(math, security, retrieval, embeddings, code sandbox, scientific parsing, multimodal inspection). "
        "Use tools to compute results; do not fabricate tool outputs."
    ),
)


def _calltool_result(text: str, structured: Dict[str, Any] | None = None, *, widget: bool = False) -> Dict[str, Any]:
    """
    Build a JSON-serializable tool result including a Skybridge widget.
    This stays compatible across MCP frameworks (FastMCP from Prefect or the official SDK).
    """
    structured = structured or {}
    payload: Dict[str, Any] = {
        "content": [{"type": "text", "text": text}],
        "structuredContent": structured,
    }
    if widget:
        payload["_meta"] = {
            "openai.com/widget": {
                "type": "simple",
                "template": {
                    "type": "resource",
                    "resource": {
                        "uri": "file://naoma_dashboard.html",
                        "mimeType": MIME_WIDGET,
                        "text": DASHBOARD_HTML,
                    },
                },
            }
        }
    return payload

# -----------------------------
# Custom routes (health + OAuth)
# -----------------------------
@mcp.custom_route("/", methods=["GET"])
async def index(request: Request) -> Response:
    return PlainTextResponse("NAOMA Evolutivo - DIAL MCP Server is running. Connect via /mcp")

@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> Response:
    return JSONResponse({"ok": True, "service": BASE_NAME})

# OpenAI Apps may probe OAuth discovery endpoints. If you don't use OAuth, returning 404 is acceptable.
@mcp.custom_route("/.well-known/oauth-authorization-server", methods=["GET"])
async def oauth_root(request: Request) -> Response:
    return JSONResponse({"error": "not_found"}, status_code=404)

@mcp.custom_route("/mcp/.well-known/oauth-authorization-server", methods=["GET"])
async def oauth_under_mcp(request: Request) -> Response:
    return JSONResponse({"error": "not_found"}, status_code=404)


# -----------------------------
# NAOMA core tools
# -----------------------------
@mcp.tool(name="naoma.dashboard")
def naoma_dashboard(language: str = "en") -> Any:
    """
    Open the NAOMA DIAL dashboard UI (Skybridge widget) inside ChatGPT.
    """
    arch = list(registry.architectures().keys())
    return _calltool_result(
        text="NAOMA Dashboard opened.",
        structured={"language": language, "architectures": arch},
        widget=True,
    )

@mcp.tool(name="naoma.architectures")
def naoma_architectures() -> Any:
    arch = list(registry.architectures().keys())
    return _calltool_result("Architectures listed.", {"architectures": arch, "descriptions": registry.architectures()})

@mcp.tool(name="naoma.status")
def naoma_status() -> Any:
    status = naoma.system_status()
    enabled = bool(os.getenv("OPENAI_API_KEY"))
    return _calltool_result("Status OK.", {"status": status, "openai": {"enabled": enabled}})

@mcp.tool(name="naoma.analyze")
def naoma_analyze(query: str, architectures: Optional[List[str]] = None, language: str = "en") -> Any:
    result = naoma.analyze(query, selected=architectures)
    # Short, computed summary (no prompt injection / no hidden reasoning)
    risk = result["security"]["risk_level"]
    top_tokens = [t["token"] for t in result["attention"][:5]]
    summary_en = f"Security risk: {risk}. Top attention tokens: {', '.join(top_tokens)}. Routed expert: {result['moe']['route']['expert']}."
    summary_es = f"Riesgo de seguridad: {risk}. Tokens principales: {', '.join(top_tokens)}. Experto: {result['moe']['route']['expert']}."
    summary = summary_en if language.lower().startswith("en") else summary_es
    return _calltool_result(summary, {"language": language, "analysis": result}, widget=True)



@mcp.tool(name="naoma.translate")
def naoma_translate(text: str, target_language: str = "en", source_language: Optional[str] = None) -> Any:
    """
    Professional translation (EN/ES) via OpenAI if OPENAI_API_KEY is configured.
    """
    tgt = "en" if target_language.lower().startswith("en") else "es"
    src = None
    if source_language:
        src = "en" if source_language.lower().startswith("en") else "es"
    return _calltool_result("Translation complete.", registry.translator.translate(text, tgt, src))


# -----------------------------
# Individual architecture tools
# -----------------------------
@mcp.tool(name="security.scan")
def security_scan(text: str) -> Any:
    return _calltool_result("Security scan complete.", registry.security.scan(text))

@mcp.tool(name="security.redact_pii")
def security_redact_pii(text: str) -> Any:
    return _calltool_result("PII redaction complete.", registry.security.redact_pii(text))

@mcp.tool(name="security.sanitize")
def security_sanitize(text: str) -> Any:
    return _calltool_result("Sanitization complete.", registry.security.sanitize(text))

@mcp.tool(name="math.solve_equation")
def math_solve_equation(equation: str, variable: str = "x") -> Any:
    return _calltool_result("Solved.", registry.math.solve_equation(equation, variable))

@mcp.tool(name="math.differentiate")
def math_differentiate(expression: str, variable: str = "x") -> Any:
    return _calltool_result("Differentiated.", registry.math.differentiate(expression, variable))

@mcp.tool(name="math.integrate")
def math_integrate(expression: str, variable: str = "x") -> Any:
    return _calltool_result("Integrated.", registry.math.integrate(expression, variable))

@mcp.tool(name="math.limit")
def math_limit(expression: str, variable: str = "x", to: str = "0", direction: str = "+") -> Any:
    return _calltool_result("Limit computed.", registry.math.limit(expression, variable, to, direction))

@mcp.tool(name="prompt.analyze")
def prompt_analyze(prompt: str) -> Any:
    return _calltool_result("Prompt analyzed.", registry.prompt.analyze(prompt))

@mcp.tool(name="prompt.optimize")
def prompt_optimize(prompt: str) -> Any:
    return _calltool_result("Prompt optimized.", registry.prompt.optimize(prompt))

@mcp.tool(name="prompt.compress")
def prompt_compress(prompt: str, max_chars: int = 600) -> Any:
    return _calltool_result("Prompt compressed.", registry.prompt.compress(prompt, max_chars))

@mcp.tool(name="embed4d.embed")
def embed4d_embed(text: str, timestamp: Optional[float] = None) -> Any:
    return _calltool_result("Embedded.", registry.embed4d.embed_4d(text, timestamp))

@mcp.tool(name="embed4d.similarity")
def embed4d_similarity(text_a: str, text_b: str, timestamp_a: Optional[float] = None, timestamp_b: Optional[float] = None) -> Any:
    return _calltool_result("Similarity computed.", registry.embed4d.similarity_4d(text_a, text_b, timestamp_a, timestamp_b))

@mcp.tool(name="rag.add_documents")
def rag_add_documents(documents: List[Dict[str, str]]) -> Any:
    return _calltool_result("Documents added.", registry.rag.add_documents(documents))

@mcp.tool(name="rag.search")
def rag_search(query: str, top_k: int = 5) -> Any:
    return _calltool_result("Search complete.", registry.rag.search(query, top_k))

@mcp.tool(name="rag.semantic_compress")
def rag_semantic_compress(text: str, query: str, max_sentences: int = 5) -> Any:
    return _calltool_result("Compressed.", registry.rag.semantic_compress(text, query, max_sentences))

@mcp.tool(name="multibinary.weighted_decision")
def multibinary_weighted_decision(scores: List[float], labels: List[str]) -> Any:
    return _calltool_result("Decision computed.", registry.multibinary.weighted_decision(scores, labels))

@mcp.tool(name="multibinary.fuzzy_evaluate")
def multibinary_fuzzy_evaluate(proposition_scores: Dict[str, float]) -> Any:
    return _calltool_result("Fuzzy evaluated.", registry.multibinary.fuzzy_evaluate(proposition_scores))

@mcp.tool(name="attention.compute")
def attention_compute(text: str) -> Any:
    return _calltool_result("Attention computed.", registry.attention.compute_attention(text))

@mcp.tool(name="attention.focus")
def attention_focus(text: str, focus_terms: List[str]) -> Any:
    return _calltool_result("Focus computed.", registry.attention.adaptive_focus(text, focus_terms))

@mcp.tool(name="code.analyze")
def code_analyze(code: str) -> Any:
    return _calltool_result("Code analyzed.", registry.codex.analyze_code(code))

@mcp.tool(name="code.safe_execute")
def code_safe_execute(code: str, timeout_seconds: float = 2.0) -> Any:
    return _calltool_result("Code executed.", registry.codex.safe_execute(code, timeout_seconds))

@mcp.tool(name="ipa.analyze_reasoning")
def ipa_analyze_reasoning(text: str) -> Any:
    return _calltool_result("Reasoning analyzed.", registry.ipa.analyze_reasoning(text))

@mcp.tool(name="ipa.trace_logic")
def ipa_trace_logic(text: str) -> Any:
    return _calltool_result("Logic traced.", registry.ipa.trace_logic(text))

@mcp.tool(name="neuro.parse_molecule")
def neuro_parse_molecule(formula: str) -> Any:
    return _calltool_result("Molecule parsed.", registry.neuro.parse_molecule(formula))

@mcp.tool(name="neuro.unit_convert")
def neuro_unit_convert(value: float, from_unit: str, to_unit: str) -> Any:
    return _calltool_result("Converted.", registry.neuro.unit_convert(value, from_unit, to_unit))

@mcp.tool(name="moe.recommend")
def moe_recommend(query: str) -> Any:
    return _calltool_result("MoE recommendation.", registry.moe.recommend(query))

@mcp.tool(name="multimodal.image_inspect")
def multimodal_image_inspect(image_base64: str) -> Any:
    return _calltool_result("Image inspected.", registry.multimodal.image_inspect(image_base64))

@mcp.tool(name="multimodal.image_describe")
def multimodal_image_describe(image_base64: str, prompt: str = "Describe the image briefly.") -> Any:
    return _calltool_result("Image described.", registry.multimodal.image_describe(image_base64, prompt))

@mcp.tool(name="stream.chunk")
def stream_chunk(text: str, chunk_size: int = 400) -> Any:
    return _calltool_result("Chunked.", registry.streaming.chunk(text, chunk_size))

@mcp.tool(name="stream.progressive")
def stream_progressive(text: str) -> Any:
    return _calltool_result("Progressive response prepared.", registry.streaming.progressive_response(text))


def main() -> None:
    """
    Railway / Docker entrypoint.
    """
    port = int(os.getenv("PORT", "8000"))
    # For OpenAI Apps / Connectors, the Streamable HTTP endpoint is /mcp
    mcp.run(transport="http", host="0.0.0.0", port=port, path="/mcp")


if __name__ == "__main__":
    main()
