#!/usr/bin/env python3
"""Recompute aggregate statistics from dataset.jsonl.

Reproduces the contents of data/statistics.json from the raw samples, so that
reviewers and users can verify the published aggregates.

Usage:
    python scripts/compute_statistics.py            # print to stdout
    python scripts/compute_statistics.py --write     # overwrite data/statistics.json
"""
import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "dataset.jsonl"
OUT = ROOT / "data" / "statistics.json"


def compute(samples):
    total = len(samples)
    vulnerable = sum(1 for s in samples if s["is_vulnerable"])
    models = sorted({s["model"] for s in samples})

    vuln_types = Counter()
    for s in samples:
        for t in s["vulnerabilities"]:
            vuln_types[t] += 1

    model_stats = {}
    for m in models:
        ms = [s for s in samples if s["model"] == m]
        mv = sum(1 for s in ms if s["is_vulnerable"])
        model_stats[m] = {
            "total": len(ms),
            "vulnerable": mv,
            "rate": 100 * mv / len(ms) if ms else 0.0,
        }

    return {
        "total_samples": total,
        "vulnerable_samples": vulnerable,
        "vulnerability_rate": 100 * vulnerable / total if total else 0.0,
        "models": models,
        "vulnerability_types": dict(vuln_types),
        "generation_date": datetime.now().isoformat(),
        "model_statistics": model_stats,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true",
                    help="overwrite data/statistics.json")
    args = ap.parse_args()

    with DATA.open(encoding="utf-8") as f:
        samples = [json.loads(line) for line in f if line.strip()]

    stats = compute(samples)
    text = json.dumps(stats, indent=2)
    print(text)

    if args.write:
        OUT.write_text(text, encoding="utf-8")
        print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
