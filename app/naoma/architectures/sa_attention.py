from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
import math
import re


def _tokens(text: str) -> List[str]:
    return re.findall(r"[A-Za-zÀ-ÿ0-9']+", text)


def _softmax(xs: List[float]) -> List[float]:
    m = max(xs) if xs else 0.0
    exps = [math.exp(x - m) for x in xs]
    s = sum(exps) + 1e-12
    return [e / s for e in exps]


@dataclass
class SAAttention:
    """
    Statistical-Adaptive Attention: produces token-level attention weights using heuristics.
    """

    def compute_attention(self, text: str) -> Dict[str, Any]:
        toks = _tokens(text)
        weights = []
        for t in toks:
            w = 1.0
            if t.isupper() and len(t) > 2:
                w += 1.2
            if t[0].isupper():
                w += 0.4
            if t.endswith(("ing", "tion", "ment", "dad", "ción", "mente")):
                w += 0.6
            if re.match(r"\d+", t):
                w += 0.5
            weights.append(w)
        attn = _softmax(weights)
        ranked = sorted(zip(toks, attn), key=lambda x: -x[1])[:10]
        return {"tokens": toks, "attention": attn, "top_tokens": [{"token": k, "weight": float(v)} for k, v in ranked]}

    def adaptive_focus(self, text: str, focus_terms: List[str]) -> Dict[str, Any]:
        toks = _tokens(text)
        focus = set(ft.lower() for ft in focus_terms)
        weights = []
        for t in toks:
            w = 1.0
            if t.lower() in focus:
                w += 2.5
            weights.append(w)
        attn = _softmax(weights)
        ranked = sorted(zip(toks, attn), key=lambda x: -x[1])[:10]
        return {"focus_terms": focus_terms, "top_tokens": [{"token": k, "weight": float(v)} for k, v in ranked]}
