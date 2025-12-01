import re
import math

COMMON_PASSWORDS = {
    "123456", "password", "12345678", "qwerty", "abc123",
    "password1", "111111", "123123", "admin", "letmein"
}

def password_entropy(password):
    """Estimate password entropy in bits."""
    pool = 0
    if re.search(r"[a-z]", password): pool += 26
    if re.search(r"[A-Z]", password): pool += 26
    if re.search(r"\d", password): pool += 10
    if re.search(r"[^\w]", password): pool += 32  # symbols
    if pool == 0:
        return 0
    return round(len(password) * math.log2(pool), 2)

def check_password(password):
    """Evaluate password strength with detailed scoring and feedback."""
    score = 0
    feedback = []

    # Length
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Password is too short (minimum 8 characters)")
        
    types = {
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digit": bool(re.search(r"\d", password)),
        "symbol": bool(re.search(r"[^\w]", password))
    }

    score += sum(types.values())

    # Common password check
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("Password is a common password!")
        score = max(score - 2, 0)
        
    entropy = password_entropy(password)
    if entropy < 40:
        feedback.append(f"Low entropy: {entropy} bits")
    elif entropy < 60:
        feedback.append(f"Moderate entropy: {entropy} bits")
    else:
        feedback.append(f"High entropy: {entropy} bits")

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    else:
        strength = "Strong"

    return {
        "password": password,
        "score": score,
        "strength": strength,
        "entropy_bits": entropy,
        "feedback": feedback
    }

if __name__ == "__main__":
    pw = "StrongPass123!"
    result = check_password(pw)
    print(result)
