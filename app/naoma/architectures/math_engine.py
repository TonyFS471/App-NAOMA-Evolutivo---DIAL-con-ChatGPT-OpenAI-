from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import sympy as sp


@dataclass
class MathEngine:
    """
    Real symbolic/numeric math using SymPy.
    """

    def _sympify(self, expr: str) -> sp.Expr:
        # Basic hardening: disallow double underscore / dunder access patterns
        if "__" in expr:
            raise ValueError("Unsafe expression.")
        return sp.sympify(expr)

    def solve_equation(self, equation: str, variable: str = "x") -> Dict[str, Any]:
        """
        Solve equation like 'x**2 - 4 = 0' or 'x**2 - 4'.
        Returns solutions plus simplified forms.
        """
        x = sp.Symbol(variable)
        if "=" in equation:
            left, right = equation.split("=", 1)
            expr = self._sympify(left) - self._sympify(right)
        else:
            expr = self._sympify(equation)
        sols = sp.solve(expr, x)
        return {
            "variable": variable,
            "equation": str(expr),
            "solutions": [str(s) for s in sols],
            "solutions_latex": [sp.latex(s) for s in sols],
        }

    def differentiate(self, expr: str, variable: str = "x") -> Dict[str, Any]:
        x = sp.Symbol(variable)
        f = self._sympify(expr)
        d = sp.diff(f, x)
        return {"variable": variable, "expression": str(f), "derivative": str(d), "latex": sp.latex(d)}

    def integrate(self, expr: str, variable: str = "x") -> Dict[str, Any]:
        x = sp.Symbol(variable)
        f = self._sympify(expr)
        i = sp.integrate(f, x)
        return {"variable": variable, "expression": str(f), "integral": str(i), "latex": sp.latex(i)}

    def limit(self, expr: str, variable: str = "x", to: str = "0", dir: str = "+") -> Dict[str, Any]:
        x = sp.Symbol(variable)
        f = self._sympify(expr)
        lim = sp.limit(f, x, self._sympify(to), dir)
        return {"variable": variable, "expression": str(f), "to": to, "direction": dir, "limit": str(lim), "latex": sp.latex(lim)}
