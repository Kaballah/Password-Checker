import re
import tkinter as tk
from tkinter import messagebox

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

# Create the main window
root = tk.Tk()
root.title("Password Strength Checker")

# Create and place the widgets
tk.Label(root, text="Enter a password:").grid(row=0, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, show="*", width=30)
password_entry.grid(row=0, column=1, padx=10, pady=10)

check_button = tk.Button(root, text="Check Strength", command=evaluate_password)
check_button.grid(row=1, columnspan=2, pady=10)

strength_label = tk.Label(root, text="Password Strength: ", font=("Helvetica", 12))
strength_label.grid(row=2, columnspan=2, pady=10)

tk.Label(root, text="Suggestions:").grid(row=3, column=0, padx=10, pady=10)
suggestions_text = tk.Text(root, height=10, width=50)
suggestions_text.grid(row=4, columnspan=2, padx=10, pady=10)

# Run the main loop
root.mainloop()
