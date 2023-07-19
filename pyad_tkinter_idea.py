import tkinter as tk
from pyad import aduser, ADContainer, ADGroup, ADComputer, pyad

def connect_to_ad():
    user = aduser.ADUser.from_cn("myuser")
    # Perform further operations with the user object
    # ...

def create_user():
    new_user = aduser.ADUser.create("newuser", "password", container="ou=users, dc=domain, dc=com")
    # Perform further operations with the new user object
    # ...

def create_group():
    new_group = ADGroup.create("newgroup", security_enabled=True, scope="UNIVERSAL",
                              optional_attributes={"description": "New group description"})
    # Perform further operations with the new group object
    # ...

def create_computer():
    ou = ADContainer.from_dn("ou=workstations, dc=domain, dc=com")
    new_computer = ADComputer.create("WS-489", ou)
    # Perform further operations with the new computer object
    # ...

# Set default connection parameters for pyad
pyad.set_defaults(ldap_server="dc1.domain.com", username="service_account", password="mypassword")

# Create the Tkinter window
window = tk.Tk()
window.title("Active Directory Interface")

# Connect to Active Directory button
connect_button = tk.Button(window, text="Connect to Active Directory", command=connect_to_ad)
connect_button.pack()

# Create User button
create_user_button = tk.Button(window, text="Create User", command=create_user)
create_user_button.pack()

# Create Group button
create_group_button = tk.Button(window, text="Create Group", command=create_group)
create_group_button.pack()

# Create Computer button
create_computer_button = tk.Button(window, text="Create Computer", command=create_computer)
create_computer_button.pack()

# Run the Tkinter event loop
window.mainloop()
