from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


SQLI_PATTERNS = [
    r"(?i)\bunion\b.+\bselect\b",
    r"(?i)\bor\b\s+1\s*=\s*1\b",
    r"(?i)\bdrop\b\s+\btable\b",
    r"(?i)\b--\b",
    r"(?i)\b;\s*shutdown\b",
]
XSS_PATTERNS = [
    r"(?i)<\s*script\b",
    r"(?i)on\w+\s*=",
    r"(?i)javascript:",
]
PROMPT_INJECTION_PATTERNS = [
    r"(?i)\b(ignore|disregard)\b.+\b(instructions|previous)\b",
    r"(?i)\b(system prompt|developer message)\b",
    r"(?i)\bdo anything now\b",
]
PII_PATTERNS = {
    "email": r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    "phone": r"(?:(?:\+?\d{1,3})?[\s\-\.]?)?(?:\(?\d{2,3}\)?[\s\-\.]?)?\d{3}[\s\-\.]?\d{4}\b",
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
}


def _match_any(text: str, patterns: List[str]) -> List[str]:
    hits = []
    for p in patterns:
        if re.search(p, text):
            hits.append(p)
    return hits


@dataclass
class SSTAPSecurity:
    """
    Real multi-layer input security scanning.
    """

    def scan(self, text: str) -> Dict[str, Any]:
        sqli = _match_any(text, SQLI_PATTERNS)
        xss = _match_any(text, XSS_PATTERNS)
        inj = _match_any(text, PROMPT_INJECTION_PATTERNS)
        pii_found = self.detect_pii(text)["pii_found"]

        threats = []
        if sqli:
            threats.append("SQL_INJECTION")
        if xss:
            threats.append("XSS")
        if inj:
            threats.append("PROMPT_INJECTION")
        if pii_found:
            threats.append("PII")

        risk = "LOW"
        if "SQL_INJECTION" in threats or "XSS" in threats:
            risk = "HIGH"
        elif threats:
            risk = "MEDIUM"

        return {
            "risk_level": risk,
            "threats": threats,
            "evidence": {
                "sqli_patterns_hit": len(sqli),
                "xss_patterns_hit": len(xss),
                "prompt_injection_patterns_hit": len(inj),
            },
        }

    def sanitize(self, text: str) -> Dict[str, Any]:
        # Very conservative sanitizer: strip HTML/script-like patterns
        cleaned = re.sub(r"(?is)<\s*script.*?>.*?<\s*/\s*script\s*>", "", text)
        cleaned = re.sub(r"(?i)javascript:", "", cleaned)
        cleaned = re.sub(r"(?i)on\w+\s*=", "", cleaned)
        return {"original": text, "sanitized": cleaned}

    def detect_pii(self, text: str) -> Dict[str, Any]:
        found = []
        for k, p in PII_PATTERNS.items():
            for m in re.finditer(p, text):
                found.append({"type": k, "match": m.group(0), "start": m.start(), "end": m.end()})
        return {"pii_found": bool(found), "pii": found}

    def redact_pii(self, text: str) -> Dict[str, Any]:
        redacted = text
        details = []
        for k, p in PII_PATTERNS.items():
            def repl(m):
                details.append({"type": k, "match": m.group(0)})
                return f"[REDACTED_{k.upper()}]"
            redacted = re.sub(p, repl, redacted)
        return {"redacted": redacted, "redactions": details}
