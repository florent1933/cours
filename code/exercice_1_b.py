email = input("Enter your email: ")

clean_email = email.strip().lower().replace(" ", "_")

is_valid_email = "@" in clean_email and "." in clean_email
print(f"Clean email: {clean_email} (valide: {is_valid_email})")
