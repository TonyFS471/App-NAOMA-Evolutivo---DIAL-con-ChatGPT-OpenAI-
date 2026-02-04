from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .architectures.math_engine import MathEngine
from .architectures.sstap_security import SSTAPSecurity
from .architectures.prompt_engineer import PromptEngineer
from .architectures.embeddings_4d import Embeddings4D
from .architectures.aquery_rag import AQueryRAG
from .architectures.multibinary import MultibinaryComputing
from .architectures.sa_attention import SAAttention
from .architectures.agentcodex import AgentCodexPro
from .architectures.ipa_introspection import IPAIntrospection
from .architectures.neuroembedx import NeuroEmbedX
from .architectures.moe_orchestrator import MoEOrchestrator
from .architectures.multimodal_processor import MultimodalProcessor
from .architectures.super_streaming import SuperStreaming
from .architectures.translator import Translator


@dataclass
class NAOMARegistry:
    math: MathEngine
    security: SSTAPSecurity
    prompt: PromptEngineer
    embed4d: Embeddings4D
    rag: AQueryRAG
    multibinary: MultibinaryComputing
    attention: SAAttention
    codex: AgentCodexPro
    ipa: IPAIntrospection
    neuro: NeuroEmbedX
    moe: MoEOrchestrator
    multimodal: MultimodalProcessor
    streaming: SuperStreaming
    translator: Translator

    @classmethod
    def create(cls) -> "NAOMARegistry":
        return cls(
            math=MathEngine(),
            security=SSTAPSecurity(),
            prompt=PromptEngineer(),
            embed4d=Embeddings4D(),
            rag=AQueryRAG(),
            multibinary=MultibinaryComputing(),
            attention=SAAttention(),
            codex=AgentCodexPro(),
            ipa=IPAIntrospection(),
            neuro=NeuroEmbedX(),
            moe=MoEOrchestrator(),
            multimodal=MultimodalProcessor(),
            streaming=SuperStreaming(),
            translator=Translator(),
        )

    def architectures(self) -> Dict[str, str]:
        # public names used in the UI + tools
        return {
            "NAOMA_Evolutivo": "Multi-architecture orchestrator (multi-agent routing + safety).",
            "IPA": "Deep introspection + bias and structure analysis.",
            "Embeddings4D": "Vector embeddings with temporal dimension τ.",
            "Multibinary": "Pascal-weighted fuzzy truth evaluation.",
            "S-A_Attention": "Statistical-adaptive attention distribution over tokens.",
            "A-Query_RAG": "Local retrieval over provided documents (TF-IDF/BM25).",
            "NeuroEmbedX": "Scientific language (molecules + unit conversions).",
            "AgentCodex": "Static code analysis + sandboxed execution.",
            "SSTAP_Security": "SQLi/XSS/prompt-injection/PII scanning and redaction.",
            "MoE_Orchestrator": "Router that recommends which expert tools to use.",
            "Multimodal_Processor": "Local image inspection + optional OpenAI vision description.",
            "PromptEngineer": "Prompt scoring, optimization, compression.",
            "MathEngine": "Symbolic calculus & algebra (SymPy).",
            "Super_Streaming": "Chunking + progressive disclosure helpers.",
        }
