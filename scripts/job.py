
import os
import sys
from pathlib import Path

from pyats.easypy import run

# compute the script path from this location
SCRIPT_PATH = Path(__file__).absolute()
UTIL_PATH = SCRIPT_PATH.parents[1]
if str(UTIL_PATH) not in sys.path:
    sys.path.append(str(UTIL_PATH))


def main(runtime):
    """job file entrypoint"""
    # run script

    run(
        testscript="scripts/test_script.py",
        runtime=runtime,
    )
