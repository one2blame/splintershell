"""Main entrypoint for the splinter-shell package"""
import logging
import sys

from .train import Train

programs = {
    "train": Train,
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

    if program() is not None:
        return 0


if __name__ == "__main__":
    exit(main())
