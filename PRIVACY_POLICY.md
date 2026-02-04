# Privacy Policy — NAOMA Evolutivo — DIAL

**Effective date:** 2026-02-03

This MCP server (“NAOMA”) processes requests you send from ChatGPT to provide tool outputs (math, security scans, retrieval over documents you provide, etc.).

## Data we process
- **User input text**: the content you submit to tools.
- **Optional documents**: only the documents you explicitly send via `rag.add_documents`.
- **Optional images**: only images you explicitly send via the multimodal tools.

## Data storage
- By default, NAOMA keeps **documents in memory** for the running process to enable retrieval.
- No intentional long-term persistence is performed unless you modify the server to use storage.

## Third parties
If you set `OPENAI_API_KEY`, NAOMA may call **OpenAI APIs** for:
- embeddings (optional)
- vision description (optional)

## Security
- The server includes input security scanning (SSTAP) and PII detection/redaction tools.
- Code execution is sandboxed with restrictions and a time limit.

## Contact
Owner: Ing. Santos Antonio Fraustro Solís (Tony)

If you need changes for compliance (e.g., retention, deletion, logging), you can implement them in this codebase.
