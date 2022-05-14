"""Main entrypoint for the splinter-shell package"""

import logging
import sys

from .calibrate import main as calibrate_main

programs = {
    "calibrate": calibrate_main,
}


def main() -> int:
    program = None

    if 1 < len(sys.argv):
        selection = sys.argv.pop(1)
        program = programs.get(selection, None)

    if not program:
        logging.error("Must choose from one of the following programs:")
        print("\t" + ", ".join(programs.keys()))
        return 1

    return program()


if __name__ == "__main__":
    exit(main())
