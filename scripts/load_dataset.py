#!/usr/bin/env python3
"""Load and explore the LLM-VulnGen dataset.

Usage:
    python scripts/load_dataset.py [path/to/dataset.jsonl]

Prints a short summary and demonstrates common filtering operations.
"""
import json
import sys
from collections import Counter
from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "data" / "dataset.jsonl"


def load(path=DEFAULT_PATH):
    """Return the dataset as a list of dicts (one per sample)."""
    path = Path(path)
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def filter_samples(samples, *, model=None, language=None, task=None,
                   strategy=None, vulnerable=None, vuln_type=None):
    """Filter samples by any combination of attributes.

    Example:
        sqli = filter_samples(samples, language="php", vuln_type="sqli")
    """
    out = samples
    if model is not None:
        out = [s for s in out if s["model"] == model]
    if language is not None:
        out = [s for s in out if s["language"] == language]
    if task is not None:
        out = [s for s in out if s["task"] == task]
    if strategy is not None:
        out = [s for s in out if s["strategy"] == strategy]
    if vulnerable is not None:
        out = [s for s in out if s["is_vulnerable"] == vulnerable]
    if vuln_type is not None:
        out = [s for s in out if vuln_type in s["vulnerabilities"]]
    return out


def summarize(samples):
    n = len(samples)
    vuln = sum(1 for s in samples if s["is_vulnerable"])
    print(f"Samples: {n}")
    print(f"Vulnerable: {vuln} ({100 * vuln / n:.1f}%)")

    print("\nBy model:")
    by_model = Counter(s["model"] for s in samples)
    for m, total in sorted(by_model.items()):
        v = sum(1 for s in samples if s["model"] == m and s["is_vulnerable"])
        print(f"  {m:14s} {v:4d}/{total:<4d} ({100 * v / total:.1f}%)")

    print("\nBy vulnerability type:")
    types = Counter(t for s in samples for t in s["vulnerabilities"])
    for t, c in types.most_common():
        print(f"  {t:26s} {c:4d} ({100 * c / n:.1f}%)")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    data = load(path)
    summarize(data)
