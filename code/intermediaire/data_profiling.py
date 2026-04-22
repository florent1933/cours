import polars as pl
import sys

# --- Configuration ---
# Define the path to the dataset.
# Using a variable makes it easy to change the file later.
FILE_PATH = "cours/jeux_de_donnees/ecommerce_pedagogique/input/commandes_brutes.csv"
CATEGORICAL_COLS = ["categorie", "sous_categorie", "statut", "region"]
NUMERICAL_COLS = ["profit", "montant"]
EMAIL_COL = "email"
CURRENCY_SYMBOLS = ["€", "$", "£", "¥"]

print(f"--- In-depth Analysis for: {FILE_PATH} ---\n")

# --- Data Loading ---
# Load the data from the specified CSV file.
try:
    df = pl.read_csv(FILE_PATH)
except Exception as e:
    print(f"Error loading the file: {e}")
    sys.exit(1)

# --- 1. Cardinality Analysis ---
# Calculate the number of unique values for each column to identify
# identifiers, categories, and free-text fields.
print("--- 1. Cardinality Analysis (Unique Values per Column) ---")
print(df.select(pl.all().n_unique()))


# --- 2. Categorical Distribution ---
# Understand the distribution of key categorical columns.
print("\n--- 2. Categorical Distribution ---")
for col in CATEGORICAL_COLS:
    if col in df.columns:
        print(f"\nValue counts for '{col}':")
        print(df[col].value_counts(sort=True))


# --- 3. Numerical Distribution (Profit) ---
# Examine the quantiles of the 'profit' column to understand its spread
# and identify potential skewness or extreme values.
print("\n--- 3. Numerical Distribution (Profit Quantiles) ---")
if "profit" in df.columns:
    print(
        df.select(
            pl.col("profit").quantile(q).alias(f"profit_quantile_{q}")
            for q in [0.0, 0.25, 0.5, 0.75, 1.0]
        )
    )


# --- 4. Specific Data Quality Checks ---
print("\n--- 4. Specific Data Quality Checks ---")

# Email validation
if EMAIL_COL in df.columns:
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    invalid_email_count = df.filter(~pl.col(EMAIL_COL).str.contains(email_regex)).height
    print(f"\nNumber of rows with invalid email format: {invalid_email_count}")

# Currency validation
if "montant" in df.columns:
    currencies_to_keep = "".join(CURRENCY_SYMBOLS)
    regex_pattern = f"[{currencies_to_keep}]"
    rows_without_valid_currency = df.filter(
        ~pl.col("montant").str.contains(regex_pattern)
    ).height
    print(
        f"Number of 'montant' rows without a valid currency symbol: {rows_without_valid_currency}"
    )


print("\n--- End of In-depth Analysis ---")
