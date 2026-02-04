from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List
import re


@dataclass
class MoEOrchestrator:
    """
    Mixture-of-Experts router: classify query and recommend expert engines/tools.
    """

    def route(self, query: str) -> Dict[str, Any]:
        q = (query or "").lower()

        if re.search(r"\b(integral|derivative|solve|equation|matrix|limit)\b", q):
            return {"expert": "math", "confidence": 0.85}
        if re.search(r"\b(sql|xss|injection|password|token|auth|pii)\b", q):
            return {"expert": "security", "confidence": 0.85}
        if re.search(r"\b(code|python|javascript|bug|stacktrace|error)\b", q):
            return {"expert": "code", "confidence": 0.8}
        if re.search(r"\b(search|retrieve|rag|document|source|citation)\b", q):
            return {"expert": "rag", "confidence": 0.75}
        if re.search(r"\b(image|photo|picture|ocr|vision)\b", q):
            return {"expert": "multimodal", "confidence": 0.7}

        return {"expert": "general", "confidence": 0.55}

    def recommend(self, query: str) -> Dict[str, Any]:
        route = self.route(query)
        expert = route["expert"]
        mapping = {
            "math": ["math.solve_equation", "math.differentiate", "math.integrate", "math.limit"],
            "security": ["security.scan", "security.redact_pii", "security.sanitize"],
            "code": ["code.analyze", "code.safe_execute"],
            "rag": ["rag.add_documents", "rag.search"],
            "multimodal": ["multimodal.image_inspect", "multimodal.image_describe"],
            "general": ["naoma.analyze"],
        }
        return {"route": route, "suggested_tools": mapping.get(expert, mapping["general"])}
