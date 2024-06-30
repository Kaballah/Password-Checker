import re
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, Menu, Scrollbar, Frame

# Function to load common passwords from a file
def load_common_passwords(filename):
    with open(filename, 'r') as file:
        return {line.strip().lower() for line in file}

# Function to check if a password is common
def check_common_passwords(password, common_passwords):
    if password.lower() in common_passwords:
        return True

    patterns = [
        r'qwerty', r'12345', r'password', r'abc123', r'letmein', r'welcome'
    ]

    for pattern in patterns:
        if re.search(pattern, password, re.IGNORECASE):
            return True

    return False

def check_password_strength(password, common_passwords):
    if check_common_passwords(password, common_passwords):
        return "Weak", {"Common password or pattern": False}

    length_criteria = len(password) >= 8
    upper_criteria = re.search(r'[A-Z]', password) is not None
    lower_criteria = re.search(r'[a-z]', password) is not None
    digit_criteria = re.search(r'\d', password) is not None
    special_criteria = re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None

    strength_criteria = {
        "Length (>= 8 characters)": length_criteria,
        "Uppercase letter": upper_criteria,
        "Lowercase letter": lower_criteria,
        "Digit": digit_criteria,
        "Special character": special_criteria,
    }

    score = sum(strength_criteria.values())
    max_score = len(strength_criteria)

    if score == max_score:
        strength = "Very Strong"
    elif score == max_score - 1:
        strength = "Strong"
    elif score >= max_score - 2:
        strength = "Moderate"
    else:
        strength = "Weak"

    return strength, strength_criteria

def suggest_improvements(criteria):
    suggestions = []
    if "Common password or pattern" in criteria and not criteria["Common password or pattern"]:
        suggestions.append("Avoid using common passwords or patterns.")
    else:
        if not criteria["Length (>= 8 characters)"]:
            suggestions.append("Increase the length to at least 8 characters.")
        if not criteria["Uppercase letter"]:
            suggestions.append("Add at least one uppercase letter.")
        if not criteria["Lowercase letter"]:
            suggestions.append("Add at least one lowercase letter.")
        if not criteria["Digit"]:
            suggestions.append("Add at least one digit.")
        if not criteria["Special character"]:
            suggestions.append("Add at least one special character (e.g., !, @, #, etc.).")
    return suggestions

# GUI Functionality
def evaluate_password():
    password = password_entry.get()
    common_passwords = load_common_passwords('common_used_passwords.txt')

    strength, criteria = check_password_strength(password, common_passwords)
    strength_label.config(text=f"Password Strength: {strength}")

    suggestions = suggest_improvements(criteria)
    suggestions_text.delete(1.0, tk.END)
    for suggestion in suggestions:
        suggestions_text.insert(tk.END, f"- {suggestion}\n")

def clear_entries():
    password_entry.delete(0, tk.END)
    strength_label.config(text="Password Strength: ")
    suggestions_text.delete(1.0, tk.END)
    update_buttons_state()

def update_buttons_state(*args):
    if password_entry.get():
        check_button.config(state=NORMAL)
        clear_button.config(state=NORMAL)
    else:
        check_button.config(state=DISABLED)
        clear_button.config(state=DISABLED)

def change_theme(theme):
    try:
        root.style.theme_use(theme)
    except Exception as e:
        messagebox.showerror("Theme Error", f"{theme} is not a valid theme.")

def create_theme_menu(menu, themes):
    for theme in themes:
        menu.add_command(label=theme, command=lambda t=theme: change_theme(t))

# Create the main window
root = ttk.Window(themename="cosmo")
root.title("Password Strength Checker")
root.resizable(False, False)

# Create a menu for themes
menubar = Menu(root)

# Adding themes menu with scrollbar
frame = Frame(menubar)
scrollbar = Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

theme_menu = Menu(frame, tearoff=0)
frame.pack(side="left")

# Major themes at the top
major_themes = ["flatly", "darkly"]

# All available themes
all_themes = [
    "flatly", "darkly", "sandstone", "cosmo", "journal", "litera", "lumen", 
    "materia", "minty", "pulse", "united", "solar", "cyborg", "superhero", 
    "morph", "quartz", "vapor", "zephyr", "yeti"
]

# Filter out invalid themes
valid_themes = []
for theme in all_themes:
    try:
        root.style.theme_use(theme)
        valid_themes.append(theme)
    except:
        pass

# Sort the themes alphabetically, with 'flatly' and 'darkly' at the top
sorted_themes = sorted(set(valid_themes) - set(major_themes))
sorted_themes = major_themes + sorted_themes

# Add major themes
create_theme_menu(theme_menu, major_themes)
theme_menu.add_separator()

# Add other themes
create_theme_menu(theme_menu, sorted_themes[2:])

# theme_menu.config(yscrollcommand=scrollbar.set)
# scrollbar.config(command=theme_menu.yview)

menubar.add_cascade(label="Themes", menu=theme_menu)
root.config(menu=menubar)

# Create and place the widgets
ttk.Label(root, text="Enter a password:").grid(row=0, column=0, padx=10, pady=10)
password_entry = ttk.Entry(root, show="*", width=30)
password_entry.grid(row=0, column=1, padx=10, pady=10)
password_entry.bind("<KeyRelease>", update_buttons_state)

# Create a frame for buttons to align them horizontally
button_frame = ttk.Frame(root)
button_frame.grid(row=1, columnspan=2, pady=10)

check_button = ttk.Button(button_frame, text="Check Strength", command=evaluate_password, bootstyle=SUCCESS)
check_button.pack(side=tk.LEFT, pady=5)

clear_button = ttk.Button(button_frame, text="Clear", command=clear_entries, bootstyle=DANGER)
clear_button.pack(side=tk.LEFT, padx=5)

strength_label = ttk.Label(root, text="Password Strength: ", font=("Helvetica", 12))
strength_label.grid(row=2, columnspan=2, pady=10)

ttk.Label(root, text="Suggestions:").grid(row=3, column=0, padx=10, pady=10)
suggestions_text = ttk.Text(root, height=10, width=50)
suggestions_text.grid(row=4, columnspan=2, padx=10, pady=10)

# Run the main loop
root.mainloop()
