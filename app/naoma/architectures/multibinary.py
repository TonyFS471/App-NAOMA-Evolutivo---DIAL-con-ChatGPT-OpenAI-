from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
import math


def _pascal_row(n: int) -> List[int]:
    row = [1]
    for k in range(1, n + 1):
        row.append(row[-1] * (n - k + 1) // k)
    return row


@dataclass
class MultibinaryComputing:
    """
    Integrated multibinary computing using weighted fuzzy truth values derived from Pascal's triangle.
    """

    def weighted_decision(self, scores: List[float], labels: List[str]) -> Dict[str, Any]:
        if len(scores) != len(labels) or not scores:
            raise ValueError("scores and labels must be same non-zero length")
        n = len(scores) - 1
        weights = _pascal_row(n)
        weights = [w / sum(weights) for w in weights]
        # Normalize scores to [0,1]
        smin, smax = min(scores), max(scores)
        norm = [(s - smin) / (smax - smin + 1e-9) for s in scores]
        agg = sum(w * s for w, s in zip(weights, norm))
        best_i = max(range(len(scores)), key=lambda i: norm[i])
        return {
            "weights_pascal": weights,
            "normalized_scores": norm,
            "aggregate_truth": agg,
            "recommendation": labels[best_i],
        }

    def fuzzy_evaluate(self, proposition_scores: Dict[str, float]) -> Dict[str, Any]:
        # Turn multiple proposition scores into multi-valued truth distribution
        labels = list(proposition_scores.keys())
        scores = list(proposition_scores.values())
        smin, smax = min(scores), max(scores)
        probs = [(s - smin) / (smax - smin + 1e-9) for s in scores]
        total = sum(probs) + 1e-9
        dist = {l: p / total for l, p in zip(labels, probs)}
        entropy = -sum(p * math.log(p + 1e-12) for p in dist.values())
        return {"distribution": dist, "entropy": entropy}
