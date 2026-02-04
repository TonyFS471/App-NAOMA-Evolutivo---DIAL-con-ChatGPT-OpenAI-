from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..registry import NAOMARegistry


@dataclass
class NAOMAEvolutivo:
    """
    Unified orchestrator that coordinates multiple architecture engines.
    """

    registry: NAOMARegistry

    def system_status(self) -> Dict[str, Any]:
        return {
            "system": "NAOMA Evolutivo - DIAL",
            "architectures": list(self.registry.architectures().keys()),
            "rag_documents": len(self.registry.rag.docs),
        }

    def analyze(self, query: str, selected: Optional[List[str]] = None) -> Dict[str, Any]:
        selected = selected or ["MoE_Orchestrator", "SSTAP_Security", "S-A_Attention", "IPA"]
        # Always include security scan
        security = self.registry.security.scan(query)

        # Route and propose tools
        route = self.registry.moe.recommend(query)

        attention = self.registry.attention.compute_attention(query)
        ipa = self.registry.ipa.analyze_reasoning(query)

        # Optionally do a quick RAG pass if user has docs
        rag = None
        if "A-Query_RAG" in selected and self.registry.rag.docs:
            rag = self.registry.rag.search(query, top_k=5)

        return {
            "query": query,
            "selected_architectures": selected,
            "security": security,
            "moe": route,
            "attention": attention["top_tokens"],
            "introspection": ipa,
            "rag": rag,
        }
