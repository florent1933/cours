# Prompt template - Gemini (enterprise safe)

## Context you can use
- Notebook: `analyse_metier.ipynb`
- File: `main.py`
- Utility modules: `../libs/*.py`
- Sample inputs: `input/restaurant_orders_anonymous.csv`, `input/daily.csv`
- Expected output format: `output/enriched_orders_with_eur.csv`

## Strict constraints
- Never request content from `secret/`.
- Never infer enterprise confidential rules from unknown data.
- If a rule is missing, ask for a sanitized rule example.
- Use `polars` for dataframe operations.
- Use `Altair` for notebook charts.
- Do not use `pandas` unless explicitly requested.
- Preserve source columns and create derived columns instead of overwriting by default.

## Prompt skeleton
"""
You are helping on a Python ETL script and notebook.
Task: <describe change>
Files you can use: analyse_metier.ipynb, main.py, ../libs/*.py, input/restaurant_orders_anonymous.csv and input/daily.csv.
Do not use or request any file in secret/.
Use Polars (`import polars as pl`) for tabular transformations.
Use Altair for notebook charts.
If utility logic is generic/reusable, implement in ../libs/*.py.
If logic is business-specific to this script, keep it in main.py.
Preserve source columns and create derived columns by default.
Expected output schema: original order columns + order_date_fr + price_eur + daily_revenue_eur.
Return:
1) code changes
2) quick test command
3) expected output rows for 2 sample records
"""

## Validation before accept
- Script runs locally.
- Output schema unchanged unless explicitly requested.
- No dependency on `secret/`.
