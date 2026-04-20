import csv

with open(
    "./cours/exercices/J2_Exo_C_kpi/kpi_input.csv", newline="", encoding="utf-8"
) as f:
    rows = list(csv.DictReader(f))


print(rows)
