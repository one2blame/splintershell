"""CLI for the splintershell package"""
import sys

from .encode import main as encode_main
from .test import main as test_main
from .train import main as train_main

programs = {
    "train": train_main,
    "test": test_main,
    "encode": encode_main,
}


def splash() -> None:
    print(
        """███████ ██████  ██      ██ ███    ██ ████████ ███████ ██████  ███████ ██   ██ ███████ ██      ██      
██      ██   ██ ██      ██ ████   ██    ██    ██      ██   ██ ██      ██   ██ ██      ██      ██      
███████ ██████  ██      ██ ██ ██  ██    ██    █████   ██████  ███████ ███████ █████   ██      ██      
     ██ ██      ██      ██ ██  ██ ██    ██    ██      ██   ██      ██ ██   ██ ██      ██      ██      
███████ ██      ███████ ██ ██   ████    ██    ███████ ██   ██ ███████ ██   ██ ███████ ███████ ███████\n"""
    )


def main() -> int:
    splash()
    program = None

    if 1 < len(sys.argv):
        selection = sys.argv.pop(1)
        program = programs.get(selection, None)

    if not program:
        print("Must choose from one of the following programs:")
        print("\t" + ", ".join(programs.keys()))
        return 1

    return program()
