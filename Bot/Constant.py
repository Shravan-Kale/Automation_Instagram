import string

first_names_m = ["Rahul", "Soham", "Piyush", "Vaibhav", "Vedant", "Sanket"]
first_names_f = ["Priya", "Rashmi", "Roshni", "Ankita"]
last_names = ["Gupta", "Sharma", "Raghuwanshi", "Kapor"]

instagram_signup_url = "https://www.instagram.com/accounts/emailsignup/"
temp_mail_url = "https://temp-mail.org/en/"

letters = string.ascii_letters
digits = string.digits
special_chars = string.punctuation
password_alphabets = letters + digits + special_chars
username_alphabets = letters + digits

# Scrape temp mail from sites and save them. Find mails that can be revisited afterward.
# Ex temp-mail.org provides qr that can be used to revisit the mail.
mail_list = ["example.com"]
