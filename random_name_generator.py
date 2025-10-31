"""Command-line utility for generating random full names.

This script produces random combinations of first and last names using
predefined pools. It supports basic customization via command-line flags
such as the number of names to return, gender bias for the first names,
output formatting, and deterministic output through a random seed.

Examples
--------
Generate five names and print them line by line::

    python random_name_generator.py --count 5

Return JSON-formatted output with deterministic results::

    python random_name_generator.py --count 3 --format json --seed 42

Select only traditionally female first names::

    python random_name_generator.py --gender female
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from typing import Iterable, List, Sequence


_MALE_FIRST_NAMES: Sequence[str] = (
    "Liam",
    "Noah",
    "Oliver",
    "James",
    "Elijah",
    "William",
    "Henry",
    "Lucas",
    "Benjamin",
    "Theodore",
    "Jack",
    "Levi",
    "Alexander",
    "Jackson",
    "Mateo",
    "Daniel",
    "Michael",
    "Ethan",
    "Sebastian",
    "Logan",
    "Owen",
    "Samuel",
    "Jacob",
    "Asher",
    "Aiden",
)

_FEMALE_FIRST_NAMES: Sequence[str] = (
    "Olivia",
    "Emma",
    "Charlotte",
    "Amelia",
    "Sophia",
    "Isabella",
    "Ava",
    "Mia",
    "Evelyn",
    "Luna",
    "Harper",
    "Camila",
    "Gianna",
    "Elizabeth",
    "Eleanor",
    "Ella",
    "Abigail",
    "Sofia",
    "Emily",
    "Avery",
    "Mila",
    "Scarlett",
    "Nova",
    "Aurora",
    "Chloe",
)

_LAST_NAMES: Sequence[str] = (
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Gonzalez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Taylor",
    "Moore",
    "Jackson",
    "Martin",
    "Lee",
    "Perez",
    "Thompson",
    "White",
    "Harris",
    "Sanchez",
    "Clark",
    "Ramirez",
    "Lewis",
    "Robinson",
)


@dataclass(frozen=True)
class GeneratedName:
    """Simple data holder for a generated full name."""

    first_name: str
    last_name: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


def _get_first_name_pool(gender: str) -> Sequence[str]:
    gender_lower = gender.lower()
    if gender_lower == "male":
        return _MALE_FIRST_NAMES
    if gender_lower == "female":
        return _FEMALE_FIRST_NAMES
    if gender_lower == "any":
        return _MALE_FIRST_NAMES + _FEMALE_FIRST_NAMES
    raise ValueError(
        "Gender must be one of 'male', 'female', or 'any'"
    )


def generate_names(
    count: int,
    *,
    gender: str = "any",
    seed: int | None = None,
) -> List[GeneratedName]:
    """Generate ``count`` random full names.

    Parameters
    ----------
    count:
        Number of names to generate. Must be positive.
    gender:
        Which first-name pool to draw from (``"male"``, ``"female"``, or
        ``"any"``). Defaults to ``"any"``.
    seed:
        Optional integer seed to make the output deterministic.
    """

    if count <= 0:
        raise ValueError("Count must be a positive integer")

    rng = random.Random(seed)
    first_name_pool = list(_get_first_name_pool(gender))
    last_name_pool = list(_LAST_NAMES)

    names = []
    for _ in range(count):
        first = rng.choice(first_name_pool)
        last = rng.choice(last_name_pool)
        names.append(GeneratedName(first, last))
    return names


def _format_plain(names: Iterable[GeneratedName]) -> str:
    return "\n".join(name.full_name for name in names)


def _format_json(names: Iterable[GeneratedName]) -> str:
    payload = [
        {"first_name": name.first_name, "last_name": name.last_name, "full_name": name.full_name}
        for name in names
    ]
    return json.dumps(payload, indent=2)


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
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        generated = generate_names(args.count, gender=args.gender, seed=args.seed)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.format == "plain":
        output = _format_plain(generated)
    else:
        output = _format_json(generated)

    if output:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
