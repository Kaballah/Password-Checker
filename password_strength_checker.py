import re

# Function to load common passwords from a file
def load_common_passwords(filename):
    with open(filename, 'r') as file:
        return {line.strip().lower() for line in file}

# Function to check if a password is common
def check_common_passwords(password, common_passwords):
    # Check if the password is in the list of common passwords
    if password.lower() in common_passwords:
        return True

    # Check for specific patterns like "Qwerty"
    patterns = [
        r'qwerty', r'12345', r'password', r'abc123', r'letmein', r'welcome'
    ]

    for pattern in patterns:
        if re.search(pattern, password, re.IGNORECASE):
            return True

    return False

def check_password_strength(password, common_passwords):
    # Check for common passwords and patterns first
    if check_common_passwords(password, common_passwords):
        return "Weak", {"Common password or pattern": False}

    # Criteria for a strong password
    length_criteria = len(password) >= 8
    upper_criteria = re.search(r'[A-Z]', password) is not None
    lower_criteria = re.search(r'[a-z]', password) is not None
    digit_criteria = re.search(r'\d', password) is not None
    special_criteria = re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None

    # Evaluate the criteria
    strength_criteria = {
        "Length (>= 8 characters)": length_criteria,
        "Uppercase letter": upper_criteria,
        "Lowercase letter": lower_criteria,
        "Digit": digit_criteria,
        "Special character": special_criteria,
    }

    # Calculate the strength score
    score = sum(strength_criteria.values())
    max_score = len(strength_criteria)

    # Determine strength level
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

def main():
    print("Welcome to the Password Strength Checker!")
    password = input("Enter a password to check its strength: ")

    # Load common passwords from file
    common_passwords = load_common_passwords('common_used_passwords.txt')

    strength, criteria = check_password_strength(password, common_passwords)
    print(f"\nPassword Strength: {strength}")

    if strength != "Very Strong":
        print("Suggestions to improve your password:")
        suggestions = suggest_improvements(criteria)
        for suggestion in suggestions:
            print(f"- {suggestion}")

if __name__ == "__main__":
    main()
