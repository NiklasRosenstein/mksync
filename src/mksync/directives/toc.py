from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from adjudicator import get, rule, union_rule

from ..readfile import ReadFile, ReadFileRequest
from ..targets import PreprocessFileTarget
from .generic import GenericPreprocessorDirectives, PreprocessorDirective, PreprocessorDirectives, RenderedDirective
from .parser import get_codeblock_positions, is_position_inside_codeblock, parse_directives


@dataclass(frozen=True)
@union_rule()
class TocDirective(PreprocessorDirective):
    path: Path

    @classmethod
    def parse(cls, path: Path, text: str) -> Iterator[TocDirective]:
        for directive in parse_directives(text, "table of contents", "toc"):
            yield cls(directive.begin, directive.end, path)


@union_rule(PreprocessorDirectives)
class TocDirectives(GenericPreprocessorDirectives["TocDirective"]):
    ...


@rule()
def _get_toc_directives(request: PreprocessFileTarget) -> TocDirectives:
    content = get(ReadFile, ReadFileRequest(request.path)).content
    return TocDirectives(TocDirective.parse(request.path, content))


@rule()
def _render_toc(request: TocDirective) -> RenderedDirective:
    content = get(ReadFile, ReadFileRequest(request.path)).content
    codeblocks = get_codeblock_positions(content)
    regex = re.compile(r"(#+)\s+(.*)")
    matches = [
        m for m in regex.finditer(content, request.end) if not is_position_inside_codeblock(m.start(), codeblocks)
    ]
    min_depth = min(len(match.group(1)) for match in matches)
    toc = []
    for match in matches:
        depth = len(match.group(1)) - min_depth
        anchor = re.sub(r"[^a-zA-Z0-9-]", "", match.group(2).lower().replace(" ", "-"))
        toc.append("  " * depth + f"* [{match.group(2)}](#{anchor})")

    toc_string = "\n".join(toc)
    return RenderedDirective(f"<!-- table of contents -->\n{toc_string}\n<!-- end table of contents -->")
