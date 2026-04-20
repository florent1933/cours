# Workflow Gemini Assist - Enterprise Safe

## Objective
Use Gemini Code Assist in VS Code on business code **without exposing enterprise confidential documents**.
Default stack for the intermediate course:
- `polars` for tabular transformations
- `Altair` for notebook charts
- notebook for exploration, `.py` script for production execution

## Folder contract
- `input/`: fake data with the same structure as enterprise data.
- `output/`: generated outputs.
- `secret/`: enterprise documents and references. Never shared with Gemini context.
- `../libs/`: shared generic utility modules (io, parsing, reusable cleaners).
- `analyse_metier.ipynb`: exploration and quality checks on sample data.

## Non-negotiable rules
1. `secret/` is excluded with `.aiexclude`.
2. Prompts must reference only `input/`, `analyse_metier.ipynb`, `main.py`, `../libs/`, and non-sensitive docs.
3. Generic utility changes go in `../libs/*.py`.
4. Business-specific transforms can stay in `main.py` for this script.
5. Do not add `secret/` in Gemini Context Drawer.
6. If a prompt needs confidential business logic, describe it abstractly or use sanitized samples.
7. Prefer adding derived columns instead of overwriting source columns.
8. Do not switch to `pandas` unless explicitly requested.

## VS Code setup checklist
1. Install/enable Gemini Code Assist extension.
2. Open folder `business_logic/template` as workspace root.
3. Confirm `.aiexclude` exists at workspace root.
4. In Gemini Code Assist settings:
   - Context Exclusion File -> `.aiexclude`
   - Keep `.gitignore` exclusion enabled
5. Install runtime packages:
   - `polars`
   - `fastexcel`
   - `xlsxwriter`
   - `altair`
6. In chat, attach only `analyse_metier.ipynb`, `main.py`, `../libs/*.py`, and `input/commandes_input_exemple.csv`.

## Runtime flow
1. Explore sample input in `analyse_metier.ipynb`.
2. Validate derived columns and charts.
3. Move stable logic to `main.py`.
4. Run script on sample input.
5. Validate output format.
6. Swap only runtime files when executed in enterprise environment.
