from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List
import re


_BIAS_MARKERS = {
    "confirmation_bias": [r"(?i)\b(obviously|clearly|everyone knows)\b", r"(?i)\bmust be true\b"],
    "overconfidence": [r"(?i)\b(guaranteed|certain|100%)\b"],
    "hedging": [r"(?i)\b(maybe|perhaps|it seems|likely)\b"],
}


@dataclass
class IPAIntrospection:
    """
    Introspección Profunda Avanzada:
    analyze reasoning style signals (uncertainty, bias markers) on a given text.
    """

    def analyze_reasoning(self, text: str) -> Dict[str, Any]:
        signals = {}
        for k, pats in _BIAS_MARKERS.items():
            hits = []
            for p in pats:
                if re.search(p, (text or "")):
                    hits.append(p)
            signals[k] = {"hits": len(hits), "patterns": hits}
        style = "Balanced"
        if signals["overconfidence"]["hits"] and not signals["hedging"]["hits"]:
            style = "Overconfident"
        if signals["hedging"]["hits"] and not signals["overconfidence"]["hits"]:
            style = "Cautious"
        if signals["confirmation_bias"]["hits"]:
            style = "Potential bias"
        return {"style": style, "signals": signals}

    def trace_logic(self, text: str) -> Dict[str, Any]:
        # Simple structure extraction: premises -> conclusion markers
        premises = re.findall(r"(?i)\b(because|since|given that)\b[^.?!]*", text)
        conclusions = re.findall(r"(?i)\b(therefore|so|thus|as a result)\b[^.?!]*", text)
        return {"premises": [p.strip() for p in premises], "conclusions": [c.strip() for c in conclusions]}
