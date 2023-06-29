"""
MkSync is a utility to update Markdown files in-place to automate some common upkeep tasks, such as inling
example code and updating table of contents.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from mksync import mksync_file

logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("file", type=Path, help="the file to process")
parser.add_argument("--inplace", "-i", action="store_true", help="update the file in-place")
parser.add_argument("--verbose", "-v", default=0, action="count", help="enable verbose logging")


def main() -> None:
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose > 1 else logging.INFO if args.verbose > 0 else logging.WARNING,
        format="[%(asctime)s %(levelname)s] %(message)s",
    )

    result = mksync_file(args.file)
    if args.inplace:
        args.file.write_text(result.content)
    else:
        print(result.content)


if __name__ == "__main__":
    main()
