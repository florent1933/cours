from emails_utils import clean_email, is_valid_email, get_email_domain

email = "   @yo.x@gmail.com"
print(clean_email(email))
print(is_valid_email(clean_email(email)))
print(get_email_domain(clean_email(email)))
