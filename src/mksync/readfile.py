from dataclasses import dataclass
from pathlib import Path

from adjudicator import rule


@dataclass(frozen=True)
class ReadFileRequest:
    path: Path


@dataclass(frozen=True)
class ReadFile:
    content: str


@rule()
def _read_file(request: ReadFileRequest) -> ReadFile:
    return ReadFile(content=request.path.read_text())
