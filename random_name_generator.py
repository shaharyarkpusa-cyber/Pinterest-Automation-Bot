"""Command-line utility for generating random full names."""

from __future__ import annotations

import argparse
from typing import Sequence

from name_generator.generator import generate_names, to_json, to_plain_text


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate random full names from predefined name pools."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of names to generate (default: 10)",
    )
    parser.add_argument(
        "--gender",
        choices=["male", "female", "any"],
        default="any",
        help="Restrict first names to a specific gender pool (default: any)",
    )
    parser.add_argument(
        "--format",
        choices=["plain", "json"],
        default="plain",
        help="Output format (plain newline-separated text or JSON)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed for reproducible output",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default=None,
        help="Optional path to a custom name dataset (JSON)",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        generated = generate_names(
            args.count,
            gender=args.gender,
            seed=args.seed,
            dataset_path=args.dataset,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.format == "plain":
        output = to_plain_text(generated)
    else:
        output = to_json(generated)

    if output:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
