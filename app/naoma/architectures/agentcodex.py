from __future__ import annotations

import ast
import io
import multiprocessing as mp
import sys
import textwrap
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


_DISALLOWED_NAMES = {
    "__import__",
    "open",
    "exec",
    "eval",
    "compile",
    "input",
    "globals",
    "locals",
    "vars",
    "dir",
    "help",
}
_DISALLOWED_ATTR_PREFIXES = ("__",)


class _SafetyVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.issues: List[str] = []

    def visit_Import(self, node):  # noqa
        self.issues.append("Imports are not allowed.")
    def visit_ImportFrom(self, node):  # noqa
        self.issues.append("Imports are not allowed.")
    def visit_Call(self, node):  # noqa
        # Disallow calling dangerous builtins by name
        if isinstance(node.func, ast.Name) and node.func.id in _DISALLOWED_NAMES:
            self.issues.append(f"Call to '{node.func.id}' is not allowed.")
        self.generic_visit(node)
    def visit_Attribute(self, node):  # noqa
        if isinstance(node.attr, str) and node.attr.startswith(_DISALLOWED_ATTR_PREFIXES):
            self.issues.append("Dunder attribute access is not allowed.")
        self.generic_visit(node)


def _run_code_worker(code: str, q: mp.Queue) -> None:
    # Capture stdout
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        safe_builtins = {k: __builtins__[k] for k in ("abs", "min", "max", "sum", "len", "range", "print", "sorted", "enumerate")}
        safe_globals = {"__builtins__": safe_builtins}
        safe_locals: Dict[str, Any] = {}
        exec(code, safe_globals, safe_locals)  # noqa: S102 (sandboxed)
        q.put({"ok": True, "stdout": buf.getvalue(), "locals": {k: str(v) for k, v in safe_locals.items() if not k.startswith("_")}})
    except Exception as e:
        q.put({"ok": False, "error": f"{type(e).__name__}: {e}", "stdout": buf.getvalue()})
    finally:
        sys.stdout = old


@dataclass
class AgentCodexPro:
    """
    Code agent utilities:
    - static analysis (AST)
    - sandboxed execution (no imports / file IO / dunder)
    """

    def analyze_code(self, code: str) -> Dict[str, Any]:
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {"ok": False, "error": f"SyntaxError: {e}"}

        v = _SafetyVisitor()
        v.visit(tree)

        functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]

        return {
            "ok": len(v.issues) == 0,
            "issues": v.issues,
            "summary": {"functions": functions, "classes": classes},
        }

    def safe_execute(self, code: str, timeout_seconds: float = 2.0) -> Dict[str, Any]:
        analysis = self.analyze_code(code)
        if not analysis["ok"]:
            return {"ok": False, "error": "Unsafe code.", "analysis": analysis}

        q: mp.Queue = mp.Queue()
        p = mp.Process(target=_run_code_worker, args=(code, q))
        p.start()
        p.join(timeout_seconds)
        if p.is_alive():
            p.terminate()
            p.join(0.2)
            return {"ok": False, "error": f"Timeout after {timeout_seconds}s"}

        try:
            return q.get_nowait()
        except Exception:
            return {"ok": False, "error": "No output captured."}
