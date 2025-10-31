"""High-level helpers for generating random full names."""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

from .pools import NamePoolError, load_name_pools


@dataclass(frozen=True)
class GeneratedName:
    """Simple data holder for a generated full name."""

    first_name: str
    last_name: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


def _get_first_name_pool(gender: str, *, male: Sequence[str], female: Sequence[str]) -> Sequence[str]:
    gender_lower = gender.lower()
    if gender_lower == "male":
        return male
    if gender_lower == "female":
        return female
    if gender_lower == "any":
        return male + female
    raise ValueError("Gender must be one of 'male', 'female', or 'any'")


def generate_names(
    count: int,
    *,
    gender: str = "any",
    seed: int | None = None,
    dataset_path=None,
) -> List[GeneratedName]:
    """Generate ``count`` random full names using the cached dataset."""

    if count <= 0:
        raise ValueError("Count must be a positive integer")

    dataset = Path(dataset_path) if dataset_path else None

    try:
        pools = load_name_pools(dataset)
    except NamePoolError as exc:  # pragma: no cover - simple pass-through
        raise ValueError(str(exc)) from exc

    first_name_pool = list(
        _get_first_name_pool(
            gender,
            male=pools["male_first_names"],
            female=pools["female_first_names"],
        )
    )
    last_name_pool = list(pools["last_names"])

    if not first_name_pool or not last_name_pool:
        raise ValueError("Name pools are empty; regenerate the dataset")

    rng = random.Random(seed)

    names: List[GeneratedName] = []
    for _ in range(count):
        first = rng.choice(first_name_pool)
        last = rng.choice(last_name_pool)
        names.append(GeneratedName(first, last))
    return names


def to_plain_text(names: Iterable[GeneratedName]) -> str:
    return "\n".join(name.full_name for name in names)


def to_json(names: Iterable[GeneratedName]) -> str:
    import json

    payload = [
        {
            "first_name": name.first_name,
            "last_name": name.last_name,
            "full_name": name.full_name,
        }
        for name in names
    ]
    return json.dumps(payload, ensure_ascii=False, indent=2)
