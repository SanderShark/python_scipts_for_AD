import secrets
import string

# global vars
letter_chars = string.ascii_letters
digit_chars = string.digits
special_chars = string.punctuation
alphabet = letter_chars + digit_chars + special_chars



# generate password meeting length requirement
def pwd_gen():
    
    #input is a local variable(needs validation)
    pwd_length = int(input())
    
    
    #local vars
    pwd = ''
    

        
    #character iteration
    for i in range(pwd_length):
        pwd += ''.join(secrets.choice(alphabet))
        
        
        #complexity requirements check loop, can be changed to add upper and lower case letter requirements
        if (any(char in special_chars for char in pwd) and 
            sum(char in digit_chars for char in pwd)>=2):
            break
    
            
    print(pwd)