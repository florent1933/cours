def clean_email(email: str) -> str:
    """
    Cleans the given email by stripping leading and trailing spaces,
    converting to lowercase, and replacing spaces with underscores.
    """
    return email.strip().lower().replace(" ", "_")


def is_valid_email(email: str) -> bool:
    """
    A valid email must contain exactly one "@", at least one ".", and no spaces.
    """
    return email.count("@") == 1 and "." in email and " " not in email


def is_colt_email(email: str) -> bool:
    email_domain = get_email_domain(email)
    if email_domain is not None:
        return email_domain in ["colt.net", "colt.com"]
    return False


def get_email_domain(email: str) -> str | None:
    if "@" in email:
        return email.split("@")[1]
    return None


def get_email_username(email: str) -> str | None:
    if "@" in email:
        return email.split("@")[0]
    return None


def main() -> None:
    email = "   yo.x@gmail.com"
    cleaned_email = clean_email(email)
    validity = is_valid_email(cleaned_email)
    is_colt = is_colt_email(cleaned_email)

    username = get_email_username(cleaned_email)
    domain = get_email_domain(cleaned_email)

    print(
        f"Cleaned email: {cleaned_email} (valid: {validity}, Colt email: {is_colt}, Username: {username}, Domain: {domain})"
    )


if __name__ == "__main__":
    main()
