import subprocess
import string
import secrets
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


def execute_powershell_command(command):
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(
            ["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", command],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            startupinfo=startupinfo
        )
        output, error = process.communicate()
    except Exception as e:
        output = ""
        error = str(e)

    return output.strip(), error.strip()


def get_ad_groups():
    command = "Get-ADGroup -Filter * | Select-Object Name"
    try:
        output, error = execute_powershell_command(command)

        if error:
            print("Error retrieving AD groups:", error)
            return []

        # Split the output into lines and remove any leading/trailing whitespace
        lines = output.strip().split("\n")

        # Filter out the lines "Name" and "----"
        lines = [line.strip() for line in lines if line.strip() not in ["Name", "----"]]

        # Print the completed list
        print("AD Group List:")
        for group_name in lines:
            print(group_name)

        # Return the list of AD group names
        return lines

    except Exception as e:
        print("Error retrieving AD groups:", str(e))
        return []


def start_ad():
    try:
        process = subprocess.Popen(
            ["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", "Import-Module ActiveDirectory"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output, error = process.communicate()
    except Exception as e:
        output = ""
        error = str(e)

    return output.strip(), error.strip()



def lock_status():
    user_name = entry5.get()
    command = f"Get-ADUser {user_name} -Properties * | Select-Object LockedOut"
    output, error = execute_powershell_command(command)
     
    if error:
        print("Error messages:", error)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, output)



def execute_function():
    selected_page = notebook.nametowidget(notebook.select())
    selected_function = notebook.tab(notebook.select(), "text")

#functions in elif with page name as == 
#error handling and output handled by the parent function block
    if selected_function == "Add User to Group":
        group_name = entry4.get()
        user_name = entry3.get()
        command = f"Add-ADGroupMember -Identity '{group_name}' -Members '{user_name}'"
        output, error = execute_powershell_command(command)
    elif selected_function == "Unlock Account":
        user_name = entry5.get()
        command = f"Unlock-ADAccount -Identity '{user_name}'"
        output, error = execute_powershell_command(command)
    elif selected_function == "Generate Random Password":
        password = generate_random_password()
        output = password
        error = ""
    elif selected_function == "Set Generated Password to User":
        user_name = entry6.get()
        password = generate_random_password()
        output_text.insert(tk.END, f"Password set to: {password}\n")  # Insert message in tkinter output window
        command = f"Set-ADAccountPassword -Identity '{user_name}' -NewPassword (ConvertTo-SecureString -AsPlainText '{password}' -Force)"
        output, error = execute_powershell_command(command)

        # Display the output in the tkinter output window
        output_text.insert(tk.END, "Output from PowerShell process:\n")
        output_text.insert(tk.END, output)
    
        # Display error messages, if any
        if error:
            output_text.insert(tk.END, "Error messages:\n")
            output_text.insert(tk.END, error)
    
        output_text.see(tk.END)  # Scroll to the end of the output
    elif selected_function == "Search Groups":
        keywords = entry7.get()

        output = []  # Initialize an empty list

        for line in current_group_list:
            if keywords in line:
                output.append(line)

            if output:
            # Output the search results to the tkinter output window
                output_text.insert(tk.END, "\n".join(output) + "\n")
                error = ""
            else:
                 output_text.insert(tk.END, "No matches found.\n")
                 error = ""
    elif selected_function == "Get-Process":
        command = "Get-Process"
        output, error = execute_powershell_command(command)
    elif selected_function == "Set License Attribute":
        
        # these are domain spessific license attribute locations. Would need to set proper attribute for extended use.
        #check license
        ## adding this here: get-ADUser -Identity {user_name} -extensionAttribute10
        #set is already written
        
        user_name = entry1.get()
        license_id = entry2.get()
        command = f"Set-ADUser -Identity {user_name} -Replace @{{extensionAttribute10={license_id}}}"
        output, error = execute_powershell_command(command)
        print("Output from PowerShell process:", output)
        if error:
            print("Error messages:", error)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, output)

    elif selected_function == "Last Password Change":
        user_name = entry8.get()
        command = f"Get-ADUser -Identity "{user_name}" -Properties PasswordLastSet | Select-Object -ExpandProperty PasswordLastSet"
        output, error = execute_powershell_command(command)


    if error:
        print("Error messages:", error)
    output_text.delete("1.0", tk.END)  # Clear previous text
    output_text.insert(tk.END, output)

def generate_random_password():
    letter_chars = string.ascii_letters
    digit_chars = string.digits
    special_chars = "!@#$%^&*()_-+=?/\\'\":;{}[]|"
    alphabet = letter_chars + digit_chars + special_chars
    pwd_length = 15

    pwd = ""
    complexity_met = False

    while not complexity_met:
        pwd = "".join(secrets.choice(alphabet) for _ in range(pwd_length))
        if any(char in special_chars for char in pwd) and sum(char in digit_chars for char in pwd) >= 2:
            complexity_met = True

    return pwd


# execute block below

start_ad()
current_group_list = get_ad_groups()



window = tk.Tk()
window.title("PowerShell Functions")

# Load and display the image
image_path = "C:\\Users\\SamSanderson\\Pictures\\resized_asrc.jpg"
image = Image.open(image_path)
image_tk = ImageTk.PhotoImage(image)
image_label = tk.Label(window, image=image_tk)
image_label.pack()

# Set the window dimensions to cover the cmd window
window.geometry("800x400")

# Create a notebook to hold the pages
notebook = ttk.Notebook(window)
notebook.pack(fill=tk.BOTH, expand=True)

# Create pages for each function
function_pages = []
function_options = [
    "Set License Attribute",
    "Add User to Group",
    "Unlock Account",
    "Generate Random Password",
    "Set Generated Password to User",
    "Search Groups",
    "Last Password Change"
]
for function_name in function_options:
    page = ttk.Frame(notebook)
    function_pages.append(page)
    notebook.add(page, text=function_name)


activate_button = tk.Button(text="Activate AD", command=start_ad)
activate_button.place(x=0, y=0)


# "Set License Attribute" page
label1 = tk.Label(function_pages[0], text="Username:")
label1.pack()
entry1 = tk.Entry(function_pages[0])
entry1.pack()
label2 = tk.Label(function_pages[0], text="License ID:")
label2.pack()
entry2 = tk.Entry(function_pages[0])
entry2.pack()

# "Add User to Group" page
label3 = tk.Label(function_pages[1], text="Username")
label3.pack()
entry3 = tk.Entry(function_pages[1])
entry3.pack()
label4 = tk.Label(function_pages[1], text="Group Name(exact):")
label4.pack()
entry4 = tk.Entry(function_pages[1])
entry4.pack()


# "Unlock Account" page
label5 = tk.Label(function_pages[2], text="Username:")
label5.pack()
entry5 = tk.Entry(function_pages[2])
entry5.pack()
check_unlock = tk.Button(function_pages[2], text="Check lock status", command=lock_status)
check_unlock.pack()

# "Password Generate" page
label6 = tk.Label(function_pages[3], text="Random 15 character password")
label6.pack()
label7 = tk.Label(function_pages[3], text="Meets company complexity requirement")
label7.pack()

# "Set user new password" page
label8 = tk.Label(function_pages[4], text="Username:")
label8.pack()
entry6 = tk.Entry(function_pages[4])
entry6.pack()

# "Search Groups" page
label9 = tk.Label(function_pages[5], text="Search for groups: Uses wildcard, search for contains=input")
label9.pack()
entry7 = tk.Entry(function_pages[5])
entry7.pack()

# "Last Password Change" page
label10 = tk.Label(function_pages[6], text="Check when username last changed password:"
label10.pack()
entry8 = tk.Entry(function_pages[6])
entry8.pack()


# Execute button
execute_button = tk.Button(window, text="Execute", command=execute_function)
execute_button.pack()

# Output text area
output_text = tk.Text(window, height=500, width=100)
output_text.pack()

# Scrollbar for output text
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=output_text.yview)

# Start the main loop
window.mainloop()

