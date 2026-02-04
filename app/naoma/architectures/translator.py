from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Literal, Optional


@dataclass
class Translator:
    """
    Professional translation via OpenAI (if configured).
    """

    def translate(self, text: str, target_language: Literal["en", "es"], source_language: Optional[Literal["en", "es"]] = None) -> Dict[str, Any]:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {"ok": False, "error": "OPENAI_API_KEY not set; translation requires OpenAI.", "text": text}

        try:
            from openai import OpenAI  # type: ignore
            client = OpenAI(api_key=api_key)
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

            src = source_language.upper() if source_language else "AUTO"
            tgt = target_language.upper()

            resp = client.responses.create(
                model=model,
                input=[
                    {
                        "role": "system",
                        "content": [
                            {"type": "input_text", "text": "You are a professional translator. Translate faithfully and naturally. Output only the translation."}
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": f"Source language: {src}\nTarget language: {tgt}\n\n{text}"}
                        ],
                    },
                ],
            )
            out = ""
            for o in resp.output:
                if o.type == "message":
                    for c in o.content:
                        if c.type == "output_text":
                            out += c.text
            return {"ok": True, "model": model, "target_language": target_language, "translation": out.strip()}
        except Exception as e:
            return {"ok": False, "error": f"{type(e).__name__}: {e}"}
