# Prompt template - Gemini (enterprise safe)

## Context you can use
- Notebook: `analyse_metier.ipynb`
- File: `main.py`
- Utility modules: `../libs/*.py`
- Sample input: `input/commandes_input_exemple.csv`
- Expected output format: `output/resultat_exemple.csv`

## Strict constraints
- Never request content from `secret/`.
- Never infer enterprise confidential rules from unknown data.
- If a rule is missing, ask for a sanitized rule example.
- Use `polars` for dataframe operations.
- Use `Altair` for notebook charts.
- Do not use `pandas` unless explicitly requested.
- Preserve source columns and add derived columns instead of overwriting by default.

## Prompt skeleton
"""
You are helping on a Python ETL script and notebook.
Task: <describe change>
Files you can use: analyse_metier.ipynb, main.py, ../libs/*.py and input/commandes_input_exemple.csv.
Do not use or request any file in secret/.
Use Polars (`import polars as pl`) for tabular transformations.
Use Altair for notebook charts.
If utility logic is generic/reusable, implement in ../libs/*.py.
If logic is business-specific to this script, keep it in main.py.
Preserve source columns and create derived columns by default.
Expected output schema: commande_id, client, email, montant, date_commande, statut, email_clean, email_valide, montant_net, date_commande_clean, statut_normalise, anomalie.
Return:
1) code changes
2) quick test command
3) expected output rows for 2 sample records
"""

## Validation before accept
- Script runs locally.
- Output schema unchanged unless explicitly requested.
- No dependency on `secret/`.
