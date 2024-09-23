import re

# function for validating email
def email_validation(email):        
    if not email:
        return False
    
    # Regular expression for validating an email
    pattern = re.compile(
    r'^(?P<local_part>[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+)@(?P<domain>(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})$'
    )
    is_valid_email =  bool(pattern.match(email))
    if is_valid_email == True:
        return True
    else:
        return False
    
    