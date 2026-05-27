import string
import secrets

SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{};:,.?/<>"

def generate_password(length, use_upper=True, use_lower=True, use_digits=True, use_special=True):
    if length < 1:
        return "Password length must be greater than 0."

    pools = []
    mandatory_chars = []

    if use_upper:
        pools.append(string.ascii_uppercase)
        mandatory_chars.append(secrets.choice(string.ascii_uppercase))

    if use_lower:
        pools.append(string.ascii_lowercase)
        mandatory_chars.append(secrets.choice(string.ascii_lowercase))

    if use_digits:
        pools.append(string.digits)
        mandatory_chars.append(secrets.choice(string.digits))

    if use_special:
        pools.append(SPECIAL_CHARACTERS)
        mandatory_chars.append(secrets.choice(SPECIAL_CHARACTERS))

    if not pools:
        return "Select at least one character type."

    if length < len(mandatory_chars):
        return f"Length must be at least {len(mandatory_chars)}."

    all_chars = "".join(pools)
    remaining_length = length - len(mandatory_chars)

    password_chars = mandatory_chars[:]
    for _ in range(remaining_length):
        password_chars.append(secrets.choice(all_chars))

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)

def check_password_strength(password):
    score = 0

    has_length = len(password) >= 8
    has_upper = any(ch.isupper() for ch in password)
    has_lower = any(ch.islower() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    has_special = any(ch in SPECIAL_CHARACTERS for ch in password)

    if has_length:
        score += 1
    if has_upper:
        score += 1
    if has_lower:
        score += 1
    if has_digit:
        score += 1
    if has_special:
        score += 1

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, {
        "Length >= 8": has_length,
        "Uppercase": has_upper,
        "Lowercase": has_lower,
        "Digit": has_digit,
        "Special Character": has_special
    }

def main():
    print("Password Generator & Strength Checker")
    length = int(input("Enter password length: "))

    password = generate_password(length)
    if password.startswith("Password length") or password.startswith("Select") or password.startswith("Length must"):
        print(password)
        return

    print("\nGenerated Password:", password)

    strength, checks = check_password_strength(password)
    print("Password Strength:", strength)

    print("\nChecks:")
    for rule, result in checks.items():
        print(f"{rule}: {'Passed' if result else 'Failed'}")

if __name__ == "__main__":
    main()