# Exercice J1 - Nettoyage de données

# Variables d'entrée (raw)
header_raw = input("Enter a header name: ")
email_raw = input("Enter an email: ")
amount_raw = input("Enter an amount: ")


# Données nettoyées
header_cleaned = header_raw.strip().lower().replace(" ", "_")
email_cleaned = email_raw.strip().lower().replace(" ", "_")
amount_cleaned = amount_raw.replace(",", ".").replace(" ", "").replace("€", "")


# Données agrégées
email_valid = "@" in email_cleaned
amount_float = float(amount_cleaned)


# Affichage des résultats
# Side effect : print
print(
    f"Header: '{header_cleaned}', Email: '{email_cleaned}' (valid: {email_valid}), Amount: {amount_float}€"
)
