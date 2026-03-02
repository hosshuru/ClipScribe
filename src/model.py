import flet as ft
from dataclasses import dataclass, field
from typing import List

@ft.observable
@dataclass
class VideoModel:
    def __init__(self):
        self.source_path = ""
        self.source_type = "UNKNOWN"
        self.rev = 0
        self.duration = 0.0

    def update_source(self, path: str, s_type: str, duration=0.0):
        self.source_path = path
        self.source_type = s_type
        self.duration = duration
        self.rev += 1

@ft.observable
@dataclass
class ClipModel:
    path_list: List[str] = field(default_factory=list)
    selected_path: str = None
    rev: int = 0

    def append_source(self, path: str):
        self.path_list.append(path)
        self.rev += 1

    def select_clip(self, path: str):
        self.selected_path = path
        self.rev += 1