from __future__ import annotations

import os
import re
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


def _sentences(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[A-Za-zÀ-ÿ0-9']{2,}", text.lower())


@dataclass
class AQueryRAG:
    """
    Real retrieval over a local corpus.
    - Uses TF-IDF (scikit-learn) if installed
    - Else falls back to BM25 implemented in pure Python
    """

    docs: List[Dict[str, Any]] = field(default_factory=list)
    _tfidf_vectorizer: Any = None
    _tfidf_matrix: Any = None
    _bm25: Any = None

    def add_documents(self, documents: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        documents: [{"id": "...", "text": "...", "source": "..."}]
        """
        added = 0
        for d in documents:
            if "text" not in d:
                continue
            self.docs.append(
                {
                    "id": d.get("id") or f"doc_{len(self.docs)+1}",
                    "text": d["text"],
                    "source": d.get("source", ""),
                }
            )
            added += 1
        self._rebuild_indexes()
        return {"added": added, "total": len(self.docs)}

    def _rebuild_indexes(self) -> None:
        # Try TF-IDF
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
            texts = [d["text"] for d in self.docs]
            if not texts:
                self._tfidf_vectorizer, self._tfidf_matrix = None, None
                return
            self._tfidf_vectorizer = TfidfVectorizer(stop_words="english")
            self._tfidf_matrix = self._tfidf_vectorizer.fit_transform(texts)
            self._bm25 = None
        except Exception:
            self._tfidf_vectorizer, self._tfidf_matrix = None, None
            self._bm25 = _BM25.from_docs([d["text"] for d in self.docs])

    def search(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        if not self.docs:
            return {"query": query, "results": []}

        if self._tfidf_vectorizer is not None and self._tfidf_matrix is not None:
            qv = self._tfidf_vectorizer.transform([query])
            scores = (self._tfidf_matrix @ qv.T).toarray().ravel()
            idx = np.argsort(-scores)[:top_k]
            results = []
            for i in idx:
                results.append(
                    {
                        "id": self.docs[int(i)]["id"],
                        "source": self.docs[int(i)]["source"],
                        "score": float(scores[int(i)]),
                        "excerpt": self._best_excerpt(self.docs[int(i)]["text"], query),
                    }
                )
            return {"query": query, "engine": "tfidf", "results": results}

        # BM25 fallback
        scores = self._bm25.score(query)
        idx = np.argsort(-np.array(scores))[:top_k]
        results = []
        for i in idx:
            results.append(
                {
                    "id": self.docs[int(i)]["id"],
                    "source": self.docs[int(i)]["source"],
                    "score": float(scores[int(i)]),
                    "excerpt": self._best_excerpt(self.docs[int(i)]["text"], query),
                }
            )
        return {"query": query, "engine": "bm25", "results": results}

    def semantic_compress(self, text: str, query: str, max_sentences: int = 5) -> Dict[str, Any]:
        # Select the sentences most relevant to query based on token overlap
        q = set(_tokenize(query))
        sent = _sentences(text)
        scored = []
        for s in sent:
            tok = set(_tokenize(s))
            overlap = len(q & tok)
            scored.append((overlap, s))
        scored.sort(key=lambda x: (-x[0], -len(x[1])))
        keep = [s for sc, s in scored[:max_sentences] if sc > 0]
        if not keep:
            keep = sent[:max_sentences]
        return {"compressed": " ".join(keep), "sentences": keep, "max_sentences": max_sentences}

    def _best_excerpt(self, text: str, query: str, max_chars: int = 320) -> str:
        # Pull sentence containing highest overlap with query tokens
        q = set(_tokenize(query))
        best = ""
        best_score = -1
        for s in _sentences(text):
            score = len(q & set(_tokenize(s)))
            if score > best_score:
                best_score = score
                best = s
        if not best:
            best = text.strip()
        best = re.sub(r"\s+", " ", best)
        if len(best) > max_chars:
            return best[: max_chars - 1] + "…"
        return best


@dataclass
class _BM25:
    docs: List[List[str]]
    idf: Dict[str, float]
    avgdl: float
    k1: float = 1.5
    b: float = 0.75

    @classmethod
    def from_docs(cls, texts: List[str]) -> "_BM25":
        tokenized = [_tokenize(t) for t in texts]
        N = len(tokenized) or 1
        df = {}
        for doc in tokenized:
            for term in set(doc):
                df[term] = df.get(term, 0) + 1
        idf = {t: math.log(1 + (N - f + 0.5) / (f + 0.5)) for t, f in df.items()}
        avgdl = sum(len(d) for d in tokenized) / max(len(tokenized), 1)
        return cls(docs=tokenized, idf=idf, avgdl=avgdl)

    def score(self, query: str) -> List[float]:
        q_terms = _tokenize(query)
        scores = []
        for doc in self.docs:
            score = 0.0
            dl = len(doc) or 1
            tf = {}
            for w in doc:
                tf[w] = tf.get(w, 0) + 1
            for t in q_terms:
                if t not in tf:
                    continue
                f = tf[t]
                idf = self.idf.get(t, 0.0)
                denom = f + self.k1 * (1 - self.b + self.b * (dl / (self.avgdl or 1.0)))
                score += idf * (f * (self.k1 + 1)) / (denom + 1e-9)
            scores.append(score)
        return scores
