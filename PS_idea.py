import subprocess, secrets, string, active_directory
import tkinter as tk


# replace 'Get-Process' with the command that yoy want to run in powershell.
# Which means I have to program each command individually through variables.
###     subprocess.call('C:\Windows\System32\powershell.exe Get-Process', shell=False)


username=""

# password generator

def pwd_gen():
    
    letter_chars = string.ascii_letters
    digit_chars = string.digits
    special_chars = string.punctuation
    alphabet = letter_chars + digit_chars + special_chars
    # input is a local variable (needs validation)
    pwd_length = 15

    # local vars
    pwd = ''
    complexity_met = False
    
    while not complexity_met:
        # character iteration
        pwd = ''.join(secrets.choice(alphabet) for _ in range(pwd_length))

        # complexity requirements check
        if any(char in special_chars for char in pwd) and sum(char in digit_chars for char in pwd) >= 2:
            complexity_met = True




class Powershell:
    
    global adm_user_name = ''
    global auth_id = ''
    
    def sub_process():
        subprocess.call('C:\Windows\System32\powershell.exe ' + self + '-WindowStyle Hidden')
        
    
    def login_to_adm(sub_process):
        self.subprocess(self + 'import ActiveDirectory ')
        self.subprocess(self + 'Get-Credential ')
        
        
    def add_to_group(sub_process):
        group_name = str(entry2.get())
        user_name = str(entry1.get())
        self.subprocess(self + 'Add-ADGroupMember -Identity {group_name} -Members {user_name} ' , shell=False)
        
    
    
    def create_password(sub_process):
        pwd = pwd_gen()
        self.sub_process(self,' $NewPwd = ConvertTo-SecureString {pwd} -AsPlainText -Force ', shell=False)
        
        
        
    def set_password():
        subprocess.call(self,' Set-ADAccountPassword -Identity {user_name} -NewPassword $NewPwd -Reset ' , shell =False)
        
    def unlock_account():
        subprocess.call(self,' Unlock-ADAccount -Identity {user_name} ', shell=False)

pwrshl = Powershell() # gotta initiate those classes 

#example use pwrshl.create_password()


class AD():
    def find_user():
        user = active_directory.find_user (str(entry1.get()))
    def find_computer():
        computer = active_directory.find_computer (str(entry1.get()))
    
   # def export_users():
    #   for user in active_directory.search (objectCategory='Person', objectClass='User'):
     #       return user
        
   # def users_in_ou():
    #    users = active_directory.AD_object ("LDAP://ou=Users,dc=com,dc=example")
     #   for user in users.search (objectCategory='Person'):
      #      print user


# need to save these to file, going to be to large for output
    #def list_groups():
     ##      print group.cn
        
    #def user_in_group():
     #   me = active_directory.find_user (usern_input) # defaults to current user
      #  for group in me.memberOf:
       #     print "Members of group", group.cn
        #for group_member in group.member:
         #   print "  ", group_member

actvdir = AD()


#class None:
## this command turns a password into a secure string
 #$NewPwd = ConvertTo-SecureString "MyComplexPassword@123" -AsPlainText -Force
 
# Setting the users password

 #   Set-ADAccountPassword -Identity user03 -NewPassword $NewPwd -Reset












### tkinter window stuff

#
# need to figure out this entry1.get()

# both entrys need to end up in the funtions above



#

# use output.delete("1.0", tk.END) for output delete at beggining of function

#general clear button
def clear_output():
    output.delete("1.0", tk.END)

# Create input fields
label1 = tk.Label(window, text="Input 1:")
label1.pack()
entry1 = tk.Entry(window)
entry1.pack()

label2 = tk.Label(window, text="Input 2:")
label2.pack()
entry2 = tk.Entry(window)
entry2.pack()

# Create function buttons
group_add_button = tk.Button(window, text="Add User(input 1) to Group(input 2)", command=pwrshl.add_to_group)
group_add_button.pack()

unlk_act = tk.Button(window, text="Unlock Account(input 1)", command=pwrshl.unlock_account)
unlk_act.pack()

pwd_button = tk.Button(window, text="Generate Random Password", command=pwrshl.pwd_gen)
pwd_button.pack()

set_pwd = tk.Button(window, text="Set Generated Password to User(input 1)", command=pwrshl.set_password)
set_pwd.pack()

clear_button = tk.Button(window, text="Clear Output", command=clear_output)
clear_button.pack()

# Create output window
output = tk.Text(window, height=10, width=30)
output.pack()

# Start the main event loop
window.mainloop()
