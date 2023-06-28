import subprocess
import secrets
import string
import active_directory
import tkinter as tk

# Replace 'Get-Process' with the command that you want to run in PowerShell.
# subprocess.call('C:\Windows\System32\powershell.exe Get-Process', shell=False)

username = ""

# Password generator
def pwd_gen():
    letter_chars = string.ascii_letters
    digit_chars = string.digits
    special_chars = string.punctuation
    alphabet = letter_chars + digit_chars + special_chars
    pwd_length = 15

    pwd = ""
    complexity_met = False

    while not complexity_met:
        pwd = "".join(secrets.choice(alphabet) for _ in range(pwd_length))
        if any(char in special_chars for char in pwd) and sum(char in digit_chars for char in pwd) >= 2:
            complexity_met = True

ps = subprocess.Popen(['powershell'], stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

output_filename = "output.txt"

def enqueueOutput(out, filename):
    with open(filename, "w") as file:
        for line in iter(out.readline, b""):
            line_str = line.decode("utf-8")
            file.write(line_str)
    out.close()

ps_thread = Thread(target=enqueueOutput, args=(ps.stdout, output_filename))
ps_thread.daemon = True
ps_thread.start()

def runOutputUntilDone(process, cmd, timeout=20, done_message="done"):
    res = []
    process.stdin.write((cmd + ';Write-Host ' + done_message + '\n').encode('utf-8'))
    process.stdin.flush()
    try:
        current_line = ps.stdout.readline().decode("utf-8")
        while current_line:
            if current_line.strip() == done_message:
                return res
            print("Output from PowerShell process: " + current_line.strip())
            res.append(current_line)
            current_line = ps.stdout.readline().decode("utf-8")
    except Empty:
        return res

runOutputUntilDone(process=ps, cmd="Write-Host Booting up...", timeout=5, done_message="done")

group_list = runOutputUntilDone(process=ps, cmd="Get-ADGroup", timeout=5, done_message="done")

class Powershell:
    def sub_process(self, cmd):
        subprocess.call(['C:\Windows\System32\powershell.exe'] + cmd, shell=False)

    def login_to_adm(self):
        self.sub_process(['import ActiveDirectory'])
        self.sub_process(['Get-Credential'])

    def add_to_group(self):
        group_name = str(entry2.get())
        user_name = str(entry1.get())
        self.sub_process(['Add-ADGroupMember', '-Identity', group_name, '-Members', user_name], shell=False)

    def create_password(self):
        pwd = pwd_gen()
        self.sub_process(['$NewPwd = ConvertTo-SecureString', pwd, '-AsPlainText -Force'], shell=False)

    def set_password(self):
        user_name = str(entry1.get())
        self.sub_process(['Set-ADAccountPassword', '-Identity', user_name, '-NewPassword', '$NewPwd', '-Reset'])

    def unlock_account(self):
        user_name = str(entry1.get())
        self.sub_process(['Unlock-ADAccount', '-Identity', user_name])

pwrshl = Powershell()

class AD:
    def find_user(self):
        user = active_directory.find_user(str(entry1.get()))

    def find_computer(self):
        computer = active_directory.find_computer(str(entry1.get()))

actvdir = AD()

def clear_output():
    output.delete("1.0", tk.END)

def execute_function():
    selected_function = function_dropdown.get()
    if selected_function == "Add User to Group":
        pwrshl.add_to_group()
    elif selected_function == "Unlock Account":
        pwrshl.unlock_account()
    elif selected_function == "Generate Random Password":
        pwrshl.pwd_gen()
    elif selected_function == "Set Generated Password to User":
        pwrshl.set_password()
    elif selected_function == "Find User":
        actvdir.find_user()
    elif selected_function == "Find Computer":
        actvdir.find_computer()

window = tk.Tk()
window.title("PowerShell Functions")

label1 = tk.Label(window, text="Input 1:")
label1.pack()
entry1 = tk.Entry(window)
entry1.pack()

label2 = tk.Label(window, text="Input 2:")
label2.pack()
entry2 = tk.Entry(window)
entry2.pack()

function_options = [
    "Add User to Group",
    "Unlock Account",
    "Generate Random Password",
    "Set Generated Password to User",
    "Find User",
    "Find Computer"
]

function_dropdown = tk.StringVar(window)
function_dropdown.set(function_options[0])
dropdown_menu = tk.OptionMenu(window, function_dropdown, *function_options)
dropdown_menu.pack()

execute_button = tk.Button(window, text="Execute", command=execute_function)
execute_button.pack()

clear_button = tk.Button(window, text="Clear Output", command=clear_output)
clear_button.pack()

output = tk.Text(window, height=10, width=30)
output.pack()

window.mainloop()
