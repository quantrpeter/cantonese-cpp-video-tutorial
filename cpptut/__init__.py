"""cpptut: builds the HKPS Cantonese C++ videos from Python scripts (video0.1.py, video0.2.py, …).

A video script lists its scenes (narration + what is on screen) and calls `build`. Everything
else is shared here: narration (OmniVoice + Whisper check), the logo on every frame, subtitles,
cards, the editor/terminal stage, real C++ runs in Docker, and the MP4 assembly.
"""

from . import env

env.reexec()  # first: switches to the video venv before anything imports Pillow, numpy or torch

from . import course, cpp  # noqa: E402
from .build import Scene, build, options  # noqa: E402
from .cpp import Input, Write  # noqa: E402
from .stage import Expect, Mark, Note, Open, Pause, Replace, Run, Scroll, Stage, Type  # noqa: E402
from .style import AMBER, BLUE, GREEN, MUTED, NAVY, PURPLE, RED, TEAL  # noqa: E402
from .text import about, zh_int, zh_num, zh_seconds  # noqa: E402
from .visuals import (AnatomyCard, Bar, BarCard, Box, BoxesCard, BoxRow, BulletCard, Card, CodeCard, CodeCompareCard, EndCard, Event,  # noqa: E402
                      FlowCard, Node, Pane, Part, RoadmapCard, Row, Step, StepsCard, Tile, TileCard,
                      TableCard, TimelineCard, TitleCard)

__all__ = [
    "course", "cpp", "Scene", "build", "options", "Input", "Write",
    "Expect", "Mark", "Note", "Open", "Pause", "Replace", "Run", "Scroll", "Stage", "Type",
    "AMBER", "BLUE", "GREEN", "MUTED", "NAVY", "PURPLE", "RED", "TEAL",
    "about", "zh_int", "zh_num", "zh_seconds",
    "AnatomyCard", "Bar", "BarCard", "Box", "BoxesCard", "BoxRow", "BulletCard", "Card", "CodeCard", "CodeCompareCard", "EndCard", "Event",
    "FlowCard", "Node", "Pane", "Part", "RoadmapCard", "Row", "Step", "StepsCard", "Tile", "TileCard",
    "TableCard", "TimelineCard", "TitleCard",
]
