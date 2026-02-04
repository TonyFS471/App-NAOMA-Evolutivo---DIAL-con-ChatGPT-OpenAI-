from __future__ import annotations

import hashlib
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


def _hash_vec(text: str, dim: int = 256) -> np.ndarray:
    # Deterministic pseudo-embedding (fallback)
    h = hashlib.sha256(text.encode("utf-8")).digest()
    seed = int.from_bytes(h[:8], "big", signed=False)
    rng = np.random.default_rng(seed)
    v = rng.normal(size=dim).astype(np.float32)
    v /= (np.linalg.norm(v) + 1e-9)
    return v


def _openai_embedding(text: str) -> Optional[np.ndarray]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI  # type: ignore
        client = OpenAI(api_key=api_key)
        model = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
        resp = client.embeddings.create(model=model, input=text)
        vec = np.array(resp.data[0].embedding, dtype=np.float32)
        vec /= (np.linalg.norm(vec) + 1e-9)
        return vec
    except Exception:
        return None


@dataclass
class Embeddings4D:
    """
    Real vector embeddings with a temporal dimension τ (4D = embedding + time component).
    If OPENAI_API_KEY is set, uses OpenAI embeddings; otherwise uses deterministic hash embeddings.
    """

    dim: int = 256

    def embed_4d(self, text: str, timestamp: Optional[float] = None) -> Dict[str, Any]:
        ts = float(timestamp) if timestamp is not None else time.time()
        vec = _openai_embedding(text)
        used = "openai" if vec is not None else "hash"
        if vec is None:
            vec = _hash_vec(text, dim=self.dim)
        # Temporal feature: normalized log-time bucket
        tau = np.tanh(np.log1p(max(ts, 1.0)) / 20.0).astype(np.float32)
        v4 = np.concatenate([vec, np.array([tau], dtype=np.float32)], axis=0)
        return {
            "provider": used,
            "timestamp": ts,
            "tau": float(tau),
            "dimensions": int(v4.shape[0]),
            "embedding_4d": v4.tolist(),
        }

    def similarity_4d(self, text_a: str, text_b: str, timestamp_a: Optional[float] = None, timestamp_b: Optional[float] = None) -> Dict[str, Any]:
        ea = self.embed_4d(text_a, timestamp_a)
        eb = self.embed_4d(text_b, timestamp_b)
        va = np.array(ea["embedding_4d"], dtype=np.float32)
        vb = np.array(eb["embedding_4d"], dtype=np.float32)
        sim = float(np.dot(va, vb) / ((np.linalg.norm(va) * np.linalg.norm(vb)) + 1e-9))
        return {
            "similarity": sim,
            "provider_a": ea["provider"],
            "provider_b": eb["provider"],
            "tau_a": ea["tau"],
            "tau_b": eb["tau"],
        }
