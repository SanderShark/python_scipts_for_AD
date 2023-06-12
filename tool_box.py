import tkinter as tk
import tkinter.simpledialog as sd
import secrets
import string



#global vars
letter_chars = string.ascii_letters
digit_chars = string.digits
special_chars = string.punctuation
alphabet = letter_chars + digit_chars + special_chars
# Global variable to store password length
pwd_length = None

#tool functions

def password_length():
    global pwd_length
    pwd_length = sd.askinteger("Input", "Enter the password length:")

def pwd_gen():
    output_window.delete("1.0", tk.END)
    global pwd_length
    
    if pwd_length is None:
        password_length()  # Prompt for password length if not previously entered

    pwd = ''
    complexity_met = False
    
    while not complexity_met:
        pwd = ''.join(secrets.choice(alphabet) for _ in range(pwd_length))
        
        if any(char in special_chars for char in pwd) and sum(char in digit_chars for char in pwd) >= 2:
            complexity_met = True
    
    output_window.insert(tk.END, "Password: \n" + str(pwd))



def repeat_pwd_gen():
    output_window.delete("1.0", tk.END)
    pwd_gen()  # Call the pwd_gen function
#GUI button functions, could simplify




def clear_window():
    output_window.delete("1.0", tk.END)

# Create the main window
window = tk.Tk()
window.title("Tools for tools")

# define buttons
button1 = tk.Button(window, text="Password Generator", command=pwd_gen)
button1.pack()

button4 = tk.Button(window, text="clear", command=clear_window)
button4.pack()

button5 = tk.Button(window, text="Repeat", command=repeat_pwd_gen)
button5.pack()

# Create the output window
output_window = tk.Text(window, height=10, width=40)
output_window.pack()

# Run the main loop
window.mainloop()
