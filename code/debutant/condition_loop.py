emails_groups = [
    ["yo.lo@x.com"],
    ["clapie.florent@gmail.com", "clapieflorent+alias@gmail.com"],
    ["test@colt.net", "test@colt.com"],
]
emails_with_issues = []
range(3)  # 0, 1, 2


for emails in emails_groups:
    print(f"Processing group of emails: {emails}")
    for email in emails:
        print(f"Processing email: {email}")
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
            break

        print("-" * 20)
    else:
        print("Finished processing all emails.")

    print("=" * 40)
