from __future__ import annotations

from datetime import datetime


def clean_email(raw: str) -> tuple[str, bool]:
    """
    Nettoie et valide une adresse e-mail.

    Args:
        raw: La chaîne de caractères de l'e-mail brut à nettoyer.

    Returns:
        Un tuple contenant l'adresse e-mail nettoyée (en minuscules, sans espaces)
        et un booléen indiquant si le format est valide.
    """
    value = (raw or "").strip().lower()
    return value, ("@" in value and "." in value)


def normalize_amount(raw: str) -> float | None:
    """
    Normalise un montant en chaîne de caractères vers un flottant.

    Gère les symboles monétaires, les séparateurs de milliers (espace ou virgule),
    et les séparateurs décimaux (virgule ou point).

    Args:
        raw: La chaîne de caractères du montant brut à normaliser.

    Returns:
        Le montant normalisé en tant que flottant, ou None si l'analyse échoue.
    """
    value = (raw or "").strip().replace("$", "").replace("€", "").replace(" ", "")
    if value == "":
        return None
    if "," in value and "." in value:
        value = value.replace(",", "")
    elif "," in value:
        value = value.replace(",", ".")
    try:
        return float(value)
    except ValueError:
        return None


def normalize_date(raw: str) -> str | None:
    """
    Normalise une date en chaîne de caractères au format 'YYYY-MM-DD'.

    Accepte les formats 'YYYY-MM-DD' et 'DD/MM/YYYY'.

    Args:
        raw: La chaîne de caractères de la date brute à normaliser.

    Returns:
        La date normalisée en chaîne de caractères, ou None si l'analyse échoue.
    """
    value = (raw or "").strip()
    if not value:
        return None

    try:
        dt = datetime.strptime(value, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        pass

    try:
        dt = datetime.strptime(value, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return None


def test():
    """Exécute des tests pour les fonctions de normalisation."""
    print(normalize_amount(" 1 200,50 €") == 1200.50)
    print(normalize_amount("1,200,50 $") == 1200.50)
    print(normalize_amount(" 999€") == 999.0)


print("🎉", __name__)


if __name__ == "__main__":
    test()
