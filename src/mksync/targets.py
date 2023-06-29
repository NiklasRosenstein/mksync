from dataclasses import dataclass
from pathlib import Path

from adjudicator import get, rule


@dataclass(frozen=True)
class PreprocessFileTarget:
    """
    Represents that a given file should be preprocessed.
    """

    path: Path


@dataclass(frozen=True)
class PreprocessFileResult:
    content: str
    num_directives: int


@rule()
def _preprocess_file(file: PreprocessFileTarget) -> PreprocessFileResult:
    from .directives.generic import PreprocessorDirectives, RenderedDirective
    from .readfile import ReadFile, ReadFileRequest

    content = get(ReadFile, ReadFileRequest(file.path)).content
    offset = 0
    directives = get(PreprocessorDirectives, file)
    for directive in sorted(directives, key=lambda d: d.begin):
        replacement = get(RenderedDirective, directive)
        content = content[: directive.begin + offset] + replacement.text + content[directive.end + offset :]
        offset += len(replacement.text) - (directive.end - directive.begin)
    return PreprocessFileResult(content=content, num_directives=len(directives))
