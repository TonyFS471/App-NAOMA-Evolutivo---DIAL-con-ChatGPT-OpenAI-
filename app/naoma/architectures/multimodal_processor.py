from __future__ import annotations

import base64
import io
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


def _try_pil():
    try:
        from PIL import Image  # type: ignore
        return Image
    except Exception:
        return None


@dataclass
class MultimodalProcessor:
    """
    Lightweight multimodal processing:
    - image_inspect: local pixel stats (no API key required)
    - image_describe: optional OpenAI vision description (requires OPENAI_API_KEY)
    """

    def image_inspect(self, image_base64: str) -> Dict[str, Any]:
        Image = _try_pil()
        if Image is None:
            return {"ok": False, "error": "Pillow is not installed. Install pillow."}
        raw = base64.b64decode(image_base64)
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        arr = np.array(im)
        h, w = arr.shape[:2]
        mean = arr.mean(axis=(0, 1)).tolist()
        # Dominant colors via simple quantization
        small = im.resize((max(1, w // 8), max(1, h // 8)))
        colors = small.getcolors(maxcolors=256) or []
        colors.sort(key=lambda x: -x[0])
        top = [{"rgb": c[1], "count": c[0]} for c in colors[:5]]
        return {
            "ok": True,
            "width": w,
            "height": h,
            "mean_rgb": mean,
            "top_colors": top,
        }

    def image_describe(self, image_base64: str, prompt: str = "Describe the image briefly.") -> Dict[str, Any]:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {"ok": False, "error": "OPENAI_API_KEY not set. Vision description requires an API key."}
        try:
            from openai import OpenAI  # type: ignore
            client = OpenAI(api_key=api_key)
            model = os.getenv("OPENAI_VISION_MODEL", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
            data_url = "data:image/png;base64," + image_base64
            resp = client.responses.create(
                model=model,
                input=[{
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {"type": "input_image", "image_url": data_url},
                    ],
                }],
            )
            text = ""
            for o in resp.output:
                if o.type == "message":
                    for c in o.content:
                        if c.type == "output_text":
                            text += c.text
            return {"ok": True, "model": model, "description": text.strip()}
        except Exception as e:
            return {"ok": False, "error": f"{type(e).__name__}: {e}"}
