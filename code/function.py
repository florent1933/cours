def clean_email(email: str) -> str:
    return email.strip().lower().replace(" ", "_")


def is_valid_email(email: str) -> bool:
    return "@" in email and "." in email and " " not in email


def is_colt_email(email: str) -> bool:
    email_domain = get_email_domain(email)
    if email_domain is not None:
        return email_domain in ["colt.net", "colt.com"]
    return False


def get_email_domain(email: str) -> str | None:
    if "@" in email:
        return email.split("@")[1]
    return None


def main() -> None:
    email = "   yo.x@gmail.com"
    cleaned_email = clean_email(email)
    validity = is_valid_email(cleaned_email)
    is_colt = is_colt_email(cleaned_email)

    print(f"Cleaned email: {cleaned_email} (valid: {validity}, Colt email: {is_colt})")


main()
main()
