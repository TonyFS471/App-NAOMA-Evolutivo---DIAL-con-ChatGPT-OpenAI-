# 🧠 NAOMA Evolutivo - DIAL

## OpenAI Apps SDK - MCP Server

**14 Unified AI Architectures Laying the Foundations of AGI and Superintelligence**

[![Patent](https://img.shields.io/badge/Patent-IMPI%20MX%2Fa%2F2025%2F009736-blue.svg)](https://www.impi.gob.mx/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/Protocol-MCP-green.svg)](https://modelcontextprotocol.io/)

---

## 📋 Overview

NAOMA Evolutivo - DIAL is a ChatGPT App that provides 14 unified AI architectures
for enhanced analysis, code generation, mathematical computation, and more.

### The 14 DIAL Architectures

| # | Architecture | Icon | Category |
|---|-------------|------|----------|
| 1 | NAOMA Evolutivo | 🧠 | Core Systems |
| 2 | Advanced Deep Introspection (IPA) | 🔍 | Core Systems |
| 3 | Dynamic 4D Embeddings | 🌐 | Advanced Processing |
| 4 | Integrated Multibinary Computing | 🔢 | Advanced Processing |
| 5 | S-A Attention | 🎯 | Advanced Processing |
| 6 | A-Query System (RAG) | 📚 | Information Retrieval |
| 7 | NeuroEmbedX | 🧬 | Scientific Computing |
| 8 | AgentCodex Pro | 💻 | Software Engineering |
| 9 | SSTAP Security | 🛡️ | Security & Safety |
| 10 | MoE Orchestrator | 🎭 | Orchestration |
| 11 | Multimodal Processor | 🖼️ | Multimodal |
| 12 | PromptEngineer | ✨ | Optimization |
| 13 | MathEngine | 📐 | Scientific Computing |
| 14 | Super Streaming Multimodal | ⚡ | Real-time Streaming |

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Locally

```bash
python -m app.server
```

The server will start on `http://localhost:8787/mcp`

### 3. Test with ngrok (for ChatGPT connection)

```bash
ngrok http 8787
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.app`)

---

## 🔌 Connect to ChatGPT

### Step 1: Enable Developer Mode

1. Go to ChatGPT Settings
2. Enable "Developer Mode" (beta features)

### Step 2: Add Connector

1. Go to Settings → Connectors
2. Click "Add Connector"
3. Enter your MCP server URL: `https://your-server.com/mcp`
4. Click "Connect"

### Step 3: Test

Try asking ChatGPT:
- "Use NAOMA DIAL to list all architectures"
- "Analyze this problem with DIAL: [your question]"
- "Use AgentCodex to write Python code for [task]"
- "Solve this math problem with MathEngine: [equation]"

---

## 📤 Submit to OpenAI Apps Directory

### Prerequisites

1. **Verified OpenAI Developer Account**
   - Go to: https://platform.openai.com/
   - Complete business or individual verification

2. **Deploy your MCP server** (see Deployment section)

### Submission Process

1. Go to: https://platform.openai.com/apps-manage
2. Click "Submit New App"
3. Fill in the form:

**App Name:** NAOMA Evolutivo - DIAL

**Short Description:**
14 unified AI architectures for enhanced analysis, code generation, and mathematical computation.

**Long Description:**
NAOMA Evolutivo - DIAL provides 14 specialized AI architectures that work together to deliver multi-perspective analysis, deep introspection, code generation, mathematical problem-solving, and more. Each architecture adds a unique analytical lens to responses.

**Category:** Productivity / Developer Tools

**MCP Server URL:** `https://your-deployed-server.com/mcp`

**Privacy Policy URL:** [Your privacy policy]

### Tool Annotations (Important!)

For each tool, set these annotations correctly:

| Tool | readOnlyHint | openWorldHint | destructiveHint |
|------|-------------|---------------|-----------------|
| analyze_with_dial | true | false | false |
| list_dial_architectures | true | false | false |
| code_with_agentcodex | true | false | false |
| solve_math | true | false | false |

---

## ☁️ Deployment Options

### Railway (Recommended)

1. Push to GitHub
2. Connect to Railway
3. Deploy (uses Dockerfile automatically)

```bash
# Railway will use PORT environment variable
```

### Fly.io

```bash
fly launch
fly deploy
```

### Render

1. Connect GitHub repo
2. Select "Docker" deployment
3. Set PORT=8787

---

## 🔧 MCP Tools Reference

### `analyze_with_dial`

Analyze any query using multiple DIAL architectures.

```
analyze_with_dial(
    query="Your question here",
    architectures="naoma_evolutivo,ipa_introspection,sstap_security"
)
```

### `list_dial_architectures`

List all 14 available architectures.

```
list_dial_architectures()
```

### `code_with_agentcodex`

Generate code with AgentCodex Pro.

```
code_with_agentcodex(
    task="Create a REST API",
    language="python"
)
```

### `solve_math`

Solve mathematical problems.

```
solve_math(problem="∫ x² dx from 0 to 1")
```

---

## 📄 License & Patent

**© 2026 All Rights Reserved**

- **Author:** Ing. Santos Antonio Fraustro Solís
- **Professional License:** 4359351 (SEP, Mexico)
- **Patent Application:** IMPI Mexico MX/a/2025/009736
- **Copyright Registrations:** SafeCreative, INDAUTOR

---

## 📞 Contact

**Ing. Santos Antonio Fraustro Solís**
- Email: ingtonyfraustro251@gmail.com
- Location: Saltillo, Coahuila, México

---

## ✅ Submission Checklist

- [ ] Verified OpenAI Developer Account
- [ ] MCP server deployed with HTTPS
- [ ] Server responds to `/mcp` endpoint
- [ ] All tools have correct annotations
- [ ] Privacy policy URL ready
- [ ] App tested in ChatGPT Developer Mode
- [ ] Screenshots prepared
- [ ] Description written


## Health Check (Deploy)

- `GET /health` should return **200 OK**.
- MCP endpoint is: `POST /mcp` (this may return 406 in a browser; that's normal).

## ngrok quick setup (Windows)

1) Install ngrok and add it to PATH (or run it from its folder)
2) Add your authtoken:

```powershell
ngrok config add-authtoken <PASTE_YOUR_TOKEN_HERE>
```

3) Start tunnel:

```powershell
ngrok http 8787
```

Use the generated HTTPS URL + `/mcp` in your OpenAI Apps MCP connector.
