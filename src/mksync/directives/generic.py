from dataclasses import dataclass
from typing import TypeVar

from adjudicator import RuleGraph, get, rule, union

from ..targets import PreprocessFileTarget

T = TypeVar("T")


@dataclass
class RenderedDirective:
    text: str


@union()
@dataclass(frozen=True)
class PreprocessorDirective:
    begin: int
    end: int


class GenericPreprocessorDirectives(tuple[T, ...]):
    pass


@union()
class PreprocessorDirectives(GenericPreprocessorDirectives[PreprocessorDirective]):
    """
    Represents a list of preprocessor directives in a Markdown file.
    """


@rule()
def _get_preprocessor_directives(request: PreprocessFileTarget) -> PreprocessorDirectives:
    """
    Fetches all preprocessor directives that can be found in the *request*.
    """

    members = get(RuleGraph).get_union_members(PreprocessorDirectives)
    results: list[PreprocessorDirective] = []
    for member in members:
        results += get(member, request)
    return PreprocessorDirectives(results)
