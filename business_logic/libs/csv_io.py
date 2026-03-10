from __future__ import annotations

import csv
from pathlib import Path


def read_csv_rows(input_path: Path) -> list[dict[str, str]]:
    with input_path.open(newline="", encoding="utf-8") as src:
        return list(csv.DictReader(src))


def write_csv_rows(
    output_path: Path, fieldnames: list[str], rows: list[dict[str, str]]
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

