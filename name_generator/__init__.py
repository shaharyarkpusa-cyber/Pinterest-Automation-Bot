"""Utilities for generating random full names.

This package centralises loading large first- and last-name pools and
provides reusable helpers for both CLI and web entry points.
"""

from .generator import GeneratedName, generate_names

__all__ = ["GeneratedName", "generate_names"]
