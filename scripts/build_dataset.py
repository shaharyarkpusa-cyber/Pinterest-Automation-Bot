"""Regenerate the name dataset using Faker locale providers."""

from __future__ import annotations

import importlib
import json
from pathlib import Path

DEFAULT_OUTPUT = Path(__file__).resolve().parent.parent / "data" / "name_pools.json"


LOCALE_CODES = [
    "en_US",
    "en_GB",
    "en",
    "es_ES",
    "es_MX",
    "es",
    "fr_FR",
    "fr",
    "de_DE",
    "de",
    "it_IT",
    "it",
    "pt_PT",
    "pt_BR",
    "pt",
    "nl_NL",
    "nl",
    "ru_RU",
    "ru",
    "pl_PL",
    "pl",
    "sv_SE",
    "sv",
]


def gather_names():
    male = set()
    female = set()
    last = set()

    for code in LOCALE_CODES:
        module_name = f"faker.providers.person.{code}"
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue
        provider = getattr(module, "Provider")
        male.update(getattr(provider, "first_names_male", []))
        female.update(getattr(provider, "first_names_female", []))
        last.update(getattr(provider, "last_names", []))

    if not male or not female or not last:
        raise RuntimeError("Failed to collect name pools; ensure Faker is installed")

    return {
        "male_first_names": sorted(male),
        "female_first_names": sorted(female),
        "last_names": sorted(last),
    }


def main(output_path: Path = DEFAULT_OUTPUT) -> int:
    data = gather_names()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        "Saved dataset to",
        output_path,
        f"({len(data['male_first_names'])} male, {len(data['female_first_names'])} female, {len(data['last_names'])} last names)",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
