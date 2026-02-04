from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
import re

# Minimal atomic weights (g/mol). Extend as needed.
ATOMIC_WEIGHTS = {
    "H": 1.008, "C": 12.011, "N": 14.007, "O": 15.999, "S": 32.06, "P": 30.974,
    "Na": 22.990, "Cl": 35.45, "K": 39.098, "Ca": 40.078, "Mg": 24.305,
}

_FORMULA_RE = re.compile(r"([A-Z][a-z]?)(\d*)")


def _parse_formula(formula: str) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for el, num in _FORMULA_RE.findall(formula.strip()):
        n = int(num) if num else 1
        counts[el] = counts.get(el, 0) + n
    if not counts:
        raise ValueError("Invalid formula")
    return counts


@dataclass
class NeuroEmbedX:
    """
    Scientific language utilities:
    - parse chemical formula and compute molar mass
    - unit conversions (temperature + common units)
    """

    def parse_molecule(self, formula: str) -> Dict[str, Any]:
        counts = _parse_formula(formula)
        missing = [el for el in counts if el not in ATOMIC_WEIGHTS]
        if missing:
            return {"ok": False, "error": f"Unknown elements: {missing}", "parsed": counts}
        mass = sum(ATOMIC_WEIGHTS[el] * n for el, n in counts.items())
        return {"ok": True, "formula": formula, "parsed": counts, "molar_mass_g_mol": mass}

    def unit_convert(self, value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
        fu = from_unit.strip().lower()
        tu = to_unit.strip().lower()

        # Temperature
        if fu in ("c", "celsius") and tu in ("f", "fahrenheit"):
            return {"value": value * 9/5 + 32, "unit": "F"}
        if fu in ("f", "fahrenheit") and tu in ("c", "celsius"):
            return {"value": (value - 32) * 5/9, "unit": "C"}
        if fu in ("k", "kelvin") and tu in ("c", "celsius"):
            return {"value": value - 273.15, "unit": "C"}
        if fu in ("c", "celsius") and tu in ("k", "kelvin"):
            return {"value": value + 273.15, "unit": "K"}

        # Length
        factors = {
            ("m", "cm"): 100.0, ("cm", "m"): 0.01,
            ("m", "mm"): 1000.0, ("mm", "m"): 0.001,
            ("km", "m"): 1000.0, ("m", "km"): 0.001,
        }
        if (fu, tu) in factors:
            return {"value": value * factors[(fu, tu)], "unit": tu}

        # Mass
        factors2 = {("kg", "g"): 1000.0, ("g", "kg"): 0.001}
        if (fu, tu) in factors2:
            return {"value": value * factors2[(fu, tu)], "unit": tu}

        return {"ok": False, "error": f"Unsupported conversion: {from_unit} -> {to_unit}"}
