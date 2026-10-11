"""argparslib."""

import argparse
from collections.abc import Sequence

DEFAULT_NAME = "world"


def greet(name: str) -> str:
    """Return a greeting for the given name."""
    return f"Hello, {name}!"


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser without running the program."""
    parser = argparse.ArgumentParser(description="Print a greeting.")
    parser.add_argument("--name", default=DEFAULT_NAME, help=f"name to greet (default: {DEFAULT_NAME})")
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    """Parse command-line arguments and print the greeting."""
    args = build_parser().parse_args(argv)
    print(greet(args.name))


if __name__ == "__main__":
    main()
