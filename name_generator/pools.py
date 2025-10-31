"""Load cached datasets of first and last names."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Sequence

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "name_pools.json"


class NamePoolError(RuntimeError):
    """Raised when the name pool data cannot be loaded."""


@lru_cache(maxsize=1)
def load_name_pools(path: Path | None = None) -> Dict[str, Sequence[str]]:
    """Load name pools from disk.

    Parameters
    ----------
    path:
        Optional override for the dataset path. Defaults to
        ``data/name_pools.json`` located at the project root.
    """

    dataset_path = path or DATA_FILE
    if not dataset_path.exists():
        raise NamePoolError(
            f"Name dataset not found at {dataset_path}. Generate it before use."
        )

    try:
        payload = json.loads(dataset_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive
        raise NamePoolError(
            f"Failed to parse name dataset {dataset_path}: {exc}"
        ) from exc

    required_keys = {"male_first_names", "female_first_names", "last_names"}
    if not required_keys.issubset(payload):
        missing = required_keys - set(payload)
        raise NamePoolError(
            f"Name dataset {dataset_path} missing keys: {', '.join(sorted(missing))}"
        )

    # Ensure all pools are sequences of strings.
    cleaned: Dict[str, List[str]] = {}
    for key, values in payload.items():
        if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
            raise NamePoolError(
                f"Unexpected format for key '{key}' in dataset {dataset_path}"
            )
        cleaned[key] = [v.strip() for v in values if v.strip()]

    return cleaned
