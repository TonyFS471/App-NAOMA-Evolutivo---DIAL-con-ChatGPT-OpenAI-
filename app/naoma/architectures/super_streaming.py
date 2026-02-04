from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class SuperStreaming:
    """
    Progressive disclosure and chunking utilities for long text.
    """

    def chunk(self, text: str, chunk_size: int = 400) -> Dict[str, Any]:
        t = text or ""
        chunks = [t[i:i+chunk_size] for i in range(0, len(t), chunk_size)]
        return {"chunks": chunks, "count": len(chunks), "chunk_size": chunk_size}

    def progressive_response(self, text: str) -> Dict[str, Any]:
        # 3-level progressive disclosure: headline, outline, full
        full = (text or "").strip()
        headline = full.splitlines()[0][:120] if full else ""
        outline = "\n".join(full.splitlines()[:8])
        return {"headline": headline, "outline": outline, "full": full, "levels": 3}
