"""The syllabus, read from the tables in README.md (the single source of truth).

videoN.py is the Nth row of the syllabus: video1 = 0.1, video7 = 1.1, and so on.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache

from .style import ROOT

SERIES = "C++ 全攻略"  # on-screen series name (working title, see README "Open decisions")

_PART = re.compile(r"^### Part (\d+) (.+?): (.+?) \((\d+)\)\s*$", re.M)
_ROW = re.compile(r"^\| (\d+)\.(\d+) \| ([^|]+?) \|", re.M)


@dataclass(frozen=True)
class Part:
    num: int
    zh: str
    en: str


@dataclass(frozen=True)
class Episode:
    n: int        # video number: videoN.py
    id: str       # syllabus id, e.g. "0.1"
    title: str
    part: Part


@lru_cache(None)
def _load() -> tuple[list[Part], list[Episode]]:
    md = (ROOT / "README.md").read_text()
    parts = {int(m.group(1)): Part(int(m.group(1)), m.group(2).strip(), m.group(3).strip()) for m in _PART.finditer(md)}
    eps = []
    for m in _ROW.finditer(md):
        p = int(m.group(1))
        if p in parts:
            eps.append(Episode(len(eps) + 1, f"{p}.{m.group(2)}", m.group(3).strip(), parts[p]))
    return [parts[k] for k in sorted(parts)], eps


def parts() -> list[Part]:
    return _load()[0]


def episodes() -> list[Episode]:
    return _load()[1]


def episode(n: int) -> Episode:
    eps = episodes()
    if not 1 <= n <= len(eps):
        raise SystemExit(f"cpptut: there is no video {n} in the README syllabus (1–{len(eps)})")
    return eps[n - 1]
