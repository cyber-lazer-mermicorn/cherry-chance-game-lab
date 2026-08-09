"""Cherry Chance Game Lab — Slot & Game Research Engine."""

from __future__ import annotations
import json, time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class Game:
    name: str
    rtp: float
    volatility: str
    provider: str = ""
    features: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "rtp": self.rtp, "volatility": self.volatility,
                "provider": self.provider, "features": self.features}


class ChanceGameEngine:
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.games: list[Game] = []

    def add_game(self, name: str, rtp: float, volatility: str, **kw) -> Game:
        g = Game(name=name, rtp=rtp, volatility=volatility, **kw)
        self.games.append(g)
        return g

    def by_volatility(self, vol: str) -> list[Game]:
        return [g for g in self.games if g.volatility.lower() == vol.lower()]

    def export(self) -> str:
        path = self.output_dir / "games.json"
        path.write_text(json.dumps([g.to_dict() for g in self.games], indent=2))
        return str(path)

    def get_stats(self) -> dict[str, Any]:
        return {"total": len(self.games), "avg_rtp": sum(g.rtp for g in self.games) / max(len(self.games), 1)}
