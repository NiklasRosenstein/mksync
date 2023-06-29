import logging
from pathlib import Path

from adjudicator import Params, RuleEngine

from mksync.targets import PreprocessFileResult, PreprocessFileTarget

__version__ = "0.1.4"
__all__ = ["mksync_file"]
logger = logging.getLogger(__name__)
modules = [
    "mksync." + x
    for x in [
        "readfile",
        "targets",
        "directives.generic",
        "directives.include",
        "directives.runcmd",
        "directives.toc",
    ]
]


def mksync_file(path: Path) -> PreprocessFileResult:
    target = PreprocessFileTarget(path=path)
    engine = RuleEngine()
    engine.assert_(engine.graph)

    for module in modules:
        logger.debug("Loading module %s", module)
        engine.load_module(module)

    return engine.get(PreprocessFileResult, Params(target))
