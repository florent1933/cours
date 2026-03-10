email = "   yo. lo@x.com"

cleaned_email = email.strip().lower()

is_valid_email = (
    "@" in cleaned_email and "." in cleaned_email and " " not in cleaned_email
)


if is_valid_email:
    is_colt_email = "@colt.net" in cleaned_email or "@colt.com" in cleaned_email
    print("Email is valid")
    if is_colt_email:
        print("Email is colt domain")
    else:
        print("Email is not colt domain")
else:
    print("Email is invalid")

# one liner
is_valid_email = (
    "@" in cleaned_email
    and "." in cleaned_email
    and ("@colt.net" in cleaned_email or "@colt.com" in cleaned_email)
)
