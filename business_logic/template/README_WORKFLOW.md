# Workflow Gemini Assist - Enterprise Safe

## Objective
Use Gemini Code Assist in VS Code on business code **without exposing enterprise confidential documents**.

## Folder contract
- `input/`: fake data with the same structure as enterprise data.
- `output/`: generated outputs.
- `secret/`: enterprise documents and references. Never shared with Gemini context.
- `../libs/`: shared generic utility modules (io, parsing, reusable cleaners).

## Non-negotiable rules
1. `secret/` is excluded with `.aiexclude`.
2. Prompts must reference only `input/`, `main.py`, `../libs/`, and non-sensitive docs.
3. Generic utility changes go in `../libs/*.py`.
4. Business-specific transforms can stay in `main.py` for this script.
5. Do not add `secret/` in Gemini Context Drawer.
6. If a prompt needs confidential business logic, describe it abstractly or use sanitized samples.

## VS Code setup checklist
1. Install/enable Gemini Code Assist extension.
2. Open folder `business_logic/script1` as workspace root.
3. Confirm `.aiexclude` exists at workspace root.
4. In Gemini Code Assist settings:
   - Context Exclusion File -> `.aiexclude`
   - Keep `.gitignore` exclusion enabled
5. In chat, attach only `main.py`, `../libs/*.py`, and `input/commandes_input_exemple.csv`.

## Runtime flow
1. Run script on sample input.
2. Validate output format.
3. Swap only runtime files when executed in enterprise environment.
