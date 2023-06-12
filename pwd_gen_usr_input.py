import secrets
import string

# global vars
letter_chars = string.ascii_letters
digit_chars = string.digits
special_chars = string.punctuation
alphabet = letter_chars + digit_chars + special_chars

def pwd_gen():
    # input is a local variable (needs validation)
    pwd_length = int(input())

    # local vars
    pwd = ''
    complexity_met = False
    
    while not complexity_met:
        # character iteration
        pwd = ''.join(secrets.choice(alphabet) for _ in range(pwd_length))

        # complexity requirements check
        if any(char in special_chars for char in pwd) and sum(char in digit_chars for char in pwd) >= 2:
            complexity_met = True
    print(pwd)
