# Data Schema

This document describes every field in the LLM-VulnGen dataset.

## `data/dataset.jsonl`

JSON Lines: one JSON object per line, one object per generated code sample.

| Field | Type | Example | Description |
|---|---|---|---|
| `id` | string | `vuln_p0000_search_python_quick_dirty__Gemma3_27b__T2__S0` | Globally unique identifier. Encodes prompt, model, temperature index (`T2`) and sample index (`S0`). |
| `prompt_id` | string | `vuln_p0000_search_python_quick_dirty` | Identifier of the prompt that produced the sample. Shared across models, temperatures, and repeated samples. |
| `model` | string | `Gemma3_27b` | Generating model. One of `Gemma3_27b`, `DeepSeek_7b`, `Mistral_7b`, `phi4_14b`. |
| `task` | string | `search` | Web application task the prompt asked for (e.g. `search`, `login`). |
| `language` | string | `python` | Target web stack. One of `python` (Flask), `nodejs` (Express), `php`. |
| `strategy` | string | `quick_dirty` | Vulnerability-inducing prompt strategy. One of `quick_dirty`, `copy_existing`, `deadline_pressure`, `legacy_style`, `minimal_code`. |
| `temperature` | float | `0.2` | Decoding temperature. One of `0.2`, `0.7`, `1.0`. |
| `code` | string | `from flask import ...` | The raw generated source code. |
| `code_length` | int | `469` | Length of `code` in characters. |
| `code_lines` | int | `18` | Number of lines in `code`. |
| `vulnerabilities` | list[string] | `["sqli"]` | Vulnerability types detected. Possible values: `sqli`, `xss`, `cmdi`, `path_traversal`, `ssrf`, `insecure_deserialization`. |
| `confidence_scores` | object | `{"sqli": 0.9}` | Detector confidence per detected type, in `[0, 1]`. |
| `vuln_count` | int | `1` | Number of distinct vulnerability types detected. |
| `is_vulnerable` | bool | `true` | `true` if `vuln_count > 0`. |
| `total_confidence` | float | `0.9` | Sum of `confidence_scores` values. |
| `timestamp` | string (ISO 8601) | `2025-11-16T19:49:39.831056` | Generation time. |

## `data/summary.csv`

A flattened, one-row-per-sample view for quick tabular analysis. Columns:
`id, model, task, language, strategy, temperature, is_vulnerable, vuln_count, vulnerabilities`.
The `vulnerabilities` column is a comma-separated string. For the full
per-sample detail (including `code` and `confidence_scores`), use
`dataset.jsonl`.

## `data/statistics.json`

Aggregate counts computed over the full dataset:

| Key | Description |
|---|---|
| `total_samples` | Number of samples (1080). |
| `vulnerable_samples` | Number of samples with ≥1 vulnerability. |
| `vulnerability_rate` | Percentage of vulnerable samples. |
| `models` | List of model names. |
| `vulnerability_types` | Count of samples containing each vulnerability type. |
| `model_statistics` | Per-model `total`, `vulnerable`, and `rate`. |
| `generation_date` | When statistics were produced. |

`statistics.json` can be regenerated from `dataset.jsonl` with
`python scripts/compute_statistics.py`.
