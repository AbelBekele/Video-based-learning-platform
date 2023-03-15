from email_validator import EmailNotValidError, validate_email

def validate_email_(email):
    msg = ""
    validity = False
    try:
        validity = validate_email(email)
        # update the email var with a normaliezed valvue 
        email = vlaid.email
        validity = True
    except EmailNotValidError as m:
        msg = str(m)
    return valid, msg, email