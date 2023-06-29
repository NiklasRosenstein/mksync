from __future__ import annotations

import logging
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from adjudicator import get, rule, union_rule

from ..readfile import ReadFile, ReadFileRequest
from ..targets import PreprocessFileTarget
from .generic import GenericPreprocessorDirectives, PreprocessorDirective, PreprocessorDirectives, RenderedDirective
from .parser import parse_directives

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
@union_rule()
class RuncmdDirective(PreprocessorDirective):
    code: str | None
    command: str

    @classmethod
    def parse(cls, path: Path, text: str) -> Iterator[RuncmdDirective]:
        for directive in parse_directives(text, "runcmd"):
            match = re.match(r"(?:code:(\w*)\s+)?(.*)", directive.opts)
            assert match is not None
            code, command = match.groups()
            yield cls(directive.begin, directive.end, code, command)


@union_rule(PreprocessorDirectives)
class RuncmdDirectives(GenericPreprocessorDirectives["RuncmdDirective"]):
    ...


@rule()
def _get_toc_directives(request: PreprocessFileTarget) -> RuncmdDirectives:
    content = get(ReadFile, ReadFileRequest(request.path)).content
    return RuncmdDirectives(RuncmdDirective.parse(request.path, content))


@rule()
def _render_runcmd(request: RuncmdDirective) -> RenderedDirective:
    logger.info(f"Running command: {request.command}")
    output = subprocess.run(request.command, shell=True, capture_output=True, text=True).stdout.strip()

    code = f" code:{request.code}" if request.code is not None else ""
    begin_marker = f"```{request.code}\n" if request.code is not None else ""
    end_marker = "```\n" if request.code is not None else ""

    return RenderedDirective(
        f"<!-- runcmd{code} {request.command} -->\n{begin_marker}{output}\n{end_marker}<!-- end runcmd -->"
    )
