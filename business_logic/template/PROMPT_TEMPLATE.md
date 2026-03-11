# Prompt template - Gemini (enterprise safe)

## Context you can use
- File: `main.py`
- Utility modules: `../libs/*.py`
- Sample input: `input/commandes_input_exemple.csv`
- Expected output format: `output/resultat_exemple.csv`

## Strict constraints
- Never request content from `secret/`.
- Never infer enterprise confidential rules from unknown data.
- If a rule is missing, ask for a sanitized rule example.

## Prompt skeleton
"""
You are helping on a Python ETL script.
Task: <describe change>
Files you can use: main.py, ../libs/*.py and input/commandes_input_exemple.csv.
Do not use or request any file in secret/.
If utility logic is generic/reusable, implement in ../libs/*.py.
If logic is business-specific to this script, keep it in main.py.
Expected output schema: commande_id, client, email_clean, email_valide, montant_net, date_commande, statut, anomalie.
Return:
1) code changes
2) quick test command
3) expected output rows for 2 sample records
"""

## Validation before accept
- Script runs locally.
- Output schema unchanged unless explicitly requested.
- No dependency on `secret/`.
