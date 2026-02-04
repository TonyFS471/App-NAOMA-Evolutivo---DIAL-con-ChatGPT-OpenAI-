# NAOMA Evolutivo — DIAL (OpenAI Apps / MCP)

This project is an **MCP server** (Streamable HTTP) that exposes **14 unified AI architectures as real tools** (not “prompt wrappers”) and includes an **interactive ChatGPT App UI widget** (Skybridge).

## What you get (real compute)
- **MathEngine**: SymPy algebra + calculus (solve / derivative / integral / limits)
- **SSTAP Security**: SQLi/XSS/prompt-injection + PII detection & redaction
- **A‑Query RAG**: TF‑IDF retrieval (or BM25 fallback) over documents you add
- **Embeddings 4D**: vectors with temporal τ; OpenAI embeddings if API key is set, else deterministic hash embeddings
- **AgentCodex Pro**: AST static analysis + sandboxed Python execution (timeout enforced)
- **NeuroEmbedX**: molecule parsing (molar mass) + unit conversion
- **S‑A Attention**: token attention distribution
- **MoE Orchestrator**: routes a query to recommended expert tools
- **Super Streaming**: chunking + progressive disclosure helpers
- **Multimodal Processor**: local image inspection; optional OpenAI vision description

## Quick local run
```bash
# 1) create venv
python -m venv .venv
source .venv/bin/activate  # (Windows PowerShell: .venv\Scripts\Activate.ps1)

# 2) install deps
pip install -r requirements.txt

# 3) (optional) enable OpenAI features
export OPENAI_API_KEY="YOUR_KEY"     # Windows CMD: set OPENAI_API_KEY=...
export OPENAI_MODEL="gpt-4o-mini"
export OPENAI_EMBED_MODEL="text-embedding-3-small"

# 4) run server
python app/server.py
```

Server will listen on `http://localhost:8000`.

- Health: `GET http://localhost:8000/health`
- MCP endpoint: `POST http://localhost:8000/mcp`

### MCP smoke test
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

## Deploy to Railway (recommended)
1. Push this repo to GitHub.
2. Railway → **New Project** → **Deploy from GitHub repo**
3. Add environment variables (optional but recommended):
   - `OPENAI_API_KEY`
   - `OPENAI_MODEL` (e.g. `gpt-4o-mini`)
   - `OPENAI_EMBED_MODEL` (e.g. `text-embedding-3-small`)
   - `OPENAI_VISION_MODEL` (e.g. `gpt-4o-mini`)
4. Deploy.

## Connect to ChatGPT (Connector / Apps Dev Mode)
In ChatGPT:
- Settings → Apps / Connectors → Add connector
- URL: `https://YOUR-RAILWAY-URL/mcp`

Then in chat:
- “Open NAOMA dashboard”
- “Use NAOMA to analyze …”
- “Run `math.solve_equation` …”

## Submitting to OpenAI Apps directory (when verified)
Once your OpenAI account is verified for submission:
1. Deploy publicly over HTTPS (Railway URL is fine).
2. Ensure:
   - `/health` returns 200
   - `/mcp` works with `tools/list`
3. In the OpenAI developer portal, submit your app with:
   - Name: NAOMA Evolutivo — DIAL
   - MCP URL: `https://YOUR-RAILWAY-URL/mcp`
   - Privacy Policy & Terms: include links (you can host `PRIVACY_POLICY.md` / `TERMS.md` in a public site or your repo pages)

## Using RAG
1) Add docs:
```json
[
  {"id":"paper-1","source":"internal","text":"..."},
  {"id":"notes-2","source":"drive","text":"..."}
]
```
Call tool: `rag.add_documents`.

2) Search with: `rag.search`.

## Notes
- The dashboard UI is delivered via **Skybridge** (`text/html+skybridge`) inside ChatGPT.
- If `OPENAI_API_KEY` is not set, only the tools that require OpenAI (vision description, OpenAI embeddings) will be limited.
