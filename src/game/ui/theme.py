from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    background = "#36393f"
    foreground = "#ffffff"
    secondary_background = "#2f3136"
    accent = "#7289da"
    border = "#202225"
    card_background = "#40444b"
    muted_text = "#b9bbbe"
