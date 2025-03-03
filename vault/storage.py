from __future__ import annotations

from pathlib import Path
import json


class JsonStorage:
    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self) -> dict:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def write(self, doc: dict) -> None:
        self.path.write_text(json.dumps(doc, indent=2), encoding="utf-8")

