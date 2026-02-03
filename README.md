# 🧠 NAOMA Evolutivo - DIAL

## OpenAI Apps SDK MCP Server v3.1

**14 Unified AI Architectures for AGI Foundations**

---

### Author
**Ing. Santos Antonio Fraustro Solís**
- Professional License: 4359351 (SEP, Mexico)
- Patent: IMPI Mexico MX/a/2025/009736
- Email: ingtonyfraustro251@gmail.com
- Location: Saltillo, Coahuila, México

---

## 🚀 Quick Deploy to Railway

1. **Push this code to GitHub**

2. **Connect to Railway:**
   - Go to [railway.app](https://railway.app)
   - New Project → Deploy from GitHub repo
   - Select this repository

3. **Railway auto-deploys using Dockerfile**

4. **Get your URL:**
   - Format: `https://your-app.up.railway.app`
   - MCP Endpoint: `https://your-app.up.railway.app/mcp`

---

## 🔌 Connect to ChatGPT

1. Open ChatGPT
2. Go to **Settings** → Enable **Developer Mode**
3. Add new **MCP Connector**
4. Paste your MCP endpoint URL: `https://your-app.up.railway.app/mcp`
5. Test: *"Use NAOMA DIAL to analyze AI safety"*

---

## 📋 The 14 DIAL Architectures

| # | Architecture | Icon | Category |
|---|-------------|------|----------|
| 1 | NAOMA Evolutivo | 🧠 | Core Systems |
| 2 | Deep Introspection (IPA) | 🔍 | Core Systems |
| 3 | Dynamic 4D Embeddings | 🌐 | Advanced Processing |
| 4 | Multibinary Computing | 🔢 | Advanced Processing |
| 5 | S-A Attention | 🎯 | Advanced Processing |
| 6 | A-Query RAG | 📚 | Information Retrieval |
| 7 | NeuroEmbedX | 🧬 | Scientific Computing |
| 8 | AgentCodex Pro | 💻 | Software Engineering |
| 9 | SSTAP Security | 🛡️ | Security & Safety |
| 10 | MoE Orchestrator | 🎭 | Orchestration |
| 11 | Multimodal Processor | 🖼️ | Multimodal |
| 12 | PromptEngineer | ✨ | Optimization |
| 13 | MathEngine | 📐 | Scientific Computing |
| 14 | Super Streaming | ⚡ | Real-time Streaming |

---

## 🛠️ MCP Tools

- `analyze_with_dial` - Analyze queries with multiple architectures
- `list_dial_architectures` - List all 14 architectures
- `code_with_agentcodex` - Generate code with AgentCodex Pro
- `solve_math` - Solve math problems with MathEngine

---

## 🧪 Test Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python -m uvicorn app.server:app --host 0.0.0.0 --port 8080

# Test health
curl http://localhost:8080/health

# Test MCP tools/list
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

---

## ⚙️ Technical Details

- **Framework:** FastMCP (Official MCP Python SDK)
- **Transport:** Streamable HTTP (stateless mode)
- **Server:** Uvicorn + Starlette
- **Scalability:** Multi-replica ready (stateless_http=True)

---

## 📄 License

All Rights Reserved © 2026 Ing. Santos Antonio Fraustro Solís

Patent Protected: IMPI Mexico MX/a/2025/009736
