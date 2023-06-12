import tkinter as tk
from datetime import datetime, timedelta
import pytz
import random

def generate_random_timezone():
    # Get a list of all available timezones
    timezones = pytz.all_timezones
    # Choose a random timezone
    random_timezone = random.choice(timezones)
    
    # Get the current time in the chosen timezone
    current_time = datetime.now(pytz.timezone(random_timezone))
    
    # Format the output string
    output_string = f"Random Timezone: {random_timezone}\nCurrent Time: {current_time}"
    
    # Insert the output string into the output window
    output_window.insert(tk.END, output_string + "\n")

# Create the main window
window = tk.Tk()
window.title("Random Timezone Generator")

# Create the button
generate_button = tk.Button(window, text="Generate Random Timezone", command=generate_random_timezone)
generate_button.pack()

# Create the output window
output_window = tk.Text(window, height=10, width=40)
output_window.pack()

# Run the main loop
window.mainloop()

