from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
import re


@dataclass
class PromptEngineer:
    """
    Real prompt quality heuristics and transformations (no LLM required).
    """

    def analyze(self, prompt: str) -> Dict[str, Any]:
        length = len(prompt.strip())
        has_goal = bool(re.search(r"(?i)\b(goal|objective|task|you are|act as)\b", prompt))
        has_constraints = bool(re.search(r"(?i)\b(must|should|constraints|requirements|do not|avoid)\b", prompt))
        has_format = bool(re.search(r"(?i)\b(format|json|table|bullet|steps)\b", prompt))
        clarity = 0
        clarity += 25 if has_goal else 0
        clarity += 25 if has_constraints else 0
        clarity += 25 if has_format else 0
        clarity += 25 if length >= 80 else 10 if length >= 30 else 0

        grade = "F"
        if clarity >= 85:
            grade = "A"
        elif clarity >= 70:
            grade = "B"
        elif clarity >= 55:
            grade = "C"
        elif clarity >= 40:
            grade = "D"

        return {
            "length": length,
            "signals": {
                "goal": has_goal,
                "constraints": has_constraints,
                "format": has_format,
            },
            "score": clarity,
            "grade": grade,
        }

    def optimize(self, prompt: str) -> Dict[str, Any]:
        # Convert to a clearer template without changing meaning
        p = prompt.strip()
        bullets = []
        if p:
            bullets.append(p)

        optimized = (
            "You are an expert assistant.\n"
            "Task:\n"
            f"- {p}\n\n"
            "Constraints:\n"
            "- Be accurate and explicit about assumptions.\n"
            "- If something is missing, ask concise clarifying questions.\n\n"
            "Output format:\n"
            "- Provide a clear, structured answer with headings and bullet points.\n"
        )
        return {"optimized": optimized}

    def compress(self, prompt: str, max_chars: int = 600) -> Dict[str, Any]:
        p = re.sub(r"\s+", " ", prompt.strip())
        if len(p) <= max_chars:
            return {"compressed": p, "truncated": False}
        return {"compressed": p[:max_chars-1] + "…", "truncated": True}
