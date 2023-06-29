from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from adjudicator import get, rule, union_rule

from ..readfile import ReadFile, ReadFileRequest
from ..targets import PreprocessFileTarget
from .generic import GenericPreprocessorDirectives, PreprocessorDirective, PreprocessorDirectives, RenderedDirective
from .parser import parse_directives


@dataclass(frozen=True)
@union_rule()
class IncludeFileDirective(PreprocessorDirective):
    """
    Represents a request to include the contents of a file in a Markdown file, declared with an
    `<!-- include:<filename> -->` directive. The directive may be terminated with a `<!-- end include -->` directive.
    If no such termination is found, the opening tag of the directive suffices to include the file.

    An optional `code:<lang>` attribute may be specified to indicate that the file should be included as a code block
    with the specified language.
    """

    filename: str
    code: str | None

    @classmethod
    def parse(cls, text: str) -> Iterator[IncludeFileDirective]:
        regex = re.compile(r"(?:\s+code:([^ ]+))?(.*?)$")
        for directive in parse_directives(text, "include"):
            m = regex.match(directive.opts)
            if m is None:
                raise ValueError(f"Invalid include directive: {directive.opts} (@{directive.begin})")
            code, filename = m.groups()
            yield cls(directive.begin, directive.end, filename, code)


@union_rule(PreprocessorDirectives)
class IncludeFileDirectives(GenericPreprocessorDirectives["IncludeFileDirective"]):
    ...


@rule()
def _get_include_file_directives(request: PreprocessFileTarget) -> IncludeFileDirectives:
    content = get(ReadFile, ReadFileRequest(request.path)).content
    return IncludeFileDirectives(IncludeFileDirective.parse(content))


@rule()
def _include_file_request(request: IncludeFileDirective) -> RenderedDirective:
    code = f" code:{request.code}" if request.code else ""
    begin_marker = f"```{request.code}\n" if request.code else ""
    end_marker = "```\n" if request.code else ""
    return RenderedDirective(
        f"<!-- include {request.filename}{code} -->\n{begin_marker}"
        + Path(request.filename).read_text().strip()
        + f"\n{end_marker}<!-- end include -->"
    )
