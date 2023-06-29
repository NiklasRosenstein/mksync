import itertools
import logging
import re
from dataclasses import dataclass
from typing import Iterator, Sequence

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ParsedDirective:
    begin: int
    end: int
    opts: str
    keyword: str


def parse_directives(text: str, *keywords: str) -> Iterator[ParsedDirective]:
    codeblocks = get_codeblock_positions(text)
    begin_regex = re.compile(r"<!--\s*(" + "|".join(map(re.escape, keywords)) + r")(.*)?\s*-->")
    end_regex = re.compile(r"<!--\s*end\s*(" + "|".join(map(re.escape, keywords)) + r")\s*-->")
    offset = 0

    def search(pattern: re.Pattern[str]) -> re.Match[str] | None:
        """
        Search for the given patern, but make sure it does not sit inside a code block.
        """

        match = pattern.search(text, offset)
        while match is not None:
            # Check if the match is between two code blocks.
            if is_position_inside_codeblock(match.start(), codeblocks):
                logger.debug(
                    "Skipping directive %r in [%d, %d] because it is inside a code block",
                    match.group(1),
                    match.start(),
                    match.end(),
                )
                match = pattern.search(text, match.end())
            else:
                break

        return match

    begin_match = search(begin_regex)
    while offset < len(text) and begin_match is not None:
        opts = begin_match.group(2).strip()
        begin = begin_match.start()
        offset = begin_match.end()
        end_match = search(end_regex)
        next_begin_match = search(begin_regex)

        if end_match is None or (next_begin_match and next_begin_match.start() < end_match.start()):
            end = begin_match.end()
            offset = begin_match.end()
        else:
            end = end_match.end()
            offset = end_match.end()

        logger.debug("Found directive %r in [%d, %d]", begin_match.group(1), begin, end)
        yield ParsedDirective(begin, end, opts, begin_match.group(1))

        begin_match = next_begin_match


def get_codeblock_positions(text: str) -> list[tuple[int, int]]:
    """
    Returns a list of pairs of indices marking the beginning and end of Markdown code blocks in *text*.
    """

    code_block_marker = re.compile(r"^```+\w*", re.M)
    return [
        pair
        for idx, pair in enumerate(itertools.pairwise(m.start() for m in re.finditer(code_block_marker, text)))
        if idx % 2 == 0
    ]


def is_position_inside_codeblock(pos: int, markers: Sequence[tuple[int, int]]) -> bool:
    """
    Returns true if the given position is inside a code block.
    """

    return any(pos in range(*pair) for pair in markers)
