"""
Password Strength Checker & Generator
A Python program to evaluate password strength and generate secure passwords.
"""

import re
import random
import string
import math


# ─────────────────────────────────────────────
#  PASSWORD STRENGTH CHECKER
# ─────────────────────────────────────────────

def check_length(password: str) -> tuple[int, str]:
    """Score password based on length."""
    length = len(password)
    if length < 6:
        return 0, f"Too short ({length} chars) — use at least 8"
    elif length < 8:
        return 1, f"Short ({length} chars) — aim for 12+"
    elif length < 12:
        return 2, f"Acceptable length ({length} chars)"
    elif length < 16:
        return 3, f"Good length ({length} chars)"
    else:
        return 4, f"Excellent length ({length} chars)"


def check_complexity(password: str) -> tuple[int, list[str]]:
    """Score password based on character complexity."""
    score = 0
    feedback = []

    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?`~]', password))

    if has_lower:
        score += 1
    else:
        feedback.append("Add lowercase letters (a–z)")

    if has_upper:
        score += 1
    else:
        feedback.append("Add uppercase letters (A–Z)")

    if has_digit:
        score += 1
    else:
        feedback.append("Add numbers (0–9)")

    if has_symbol:
        score += 1
    else:
        feedback.append("Add symbols (!@#$%^&*...)")

    return score, feedback


def check_patterns(password: str) -> tuple[int, list[str]]:
    """Detect weak patterns and penalize."""
    penalty = 0
    warnings = []

    common_passwords = {
        "password", "123456", "qwerty", "abc123", "letmein",
        "welcome", "monkey", "dragon", "master", "sunshine",
        "password1", "iloveyou", "admin", "login", "passw0rd"
    }
    if password.lower() in common_passwords:
        penalty += 3
        warnings.append("This is a commonly used password — change it!")

    if re.search(r'(.)\1{2,}', password):
        penalty += 1
        warnings.append("Avoid repeating characters (e.g. 'aaa', '111')")

    sequences = ["abcdefghijklmnopqrstuvwxyz", "0123456789", "qwertyuiop", "asdfghjkl"]
    pwd_lower = password.lower()
    for seq in sequences:
        for i in range(len(seq) - 2):
            if seq[i:i+3] in pwd_lower:
                penalty += 1
                warnings.append(f"Avoid keyboard/sequential patterns (e.g. '{seq[i:i+3]}')")
                break

    return penalty, warnings


def calculate_entropy(password: str) -> float:
    """Calculate Shannon entropy of the password."""
    charset_size = 0
    if re.search(r'[a-z]', password):
        charset_size += 26
    if re.search(r'[A-Z]', password):
        charset_size += 26
    if re.search(r'\d', password):
        charset_size += 10
    if re.search(r'[^a-zA-Z\d]', password):
        charset_size += 32
    if charset_size == 0:
        return 0.0
    return len(password) * math.log2(charset_size)


def evaluate_strength(password: str) -> dict:
    """
    Evaluate overall password strength.
    Returns a dict with score (0–100), label, color, and detailed feedback.
    """
    if not password:
        return {
            "score": 0,
            "label": "Empty",
            "color": "red",
            "entropy": 0.0,
            "feedback": ["Please enter a password."],
            "warnings": [],
        }

    length_score, length_feedback = check_length(password)
    complexity_score, complexity_feedback = check_complexity(password)
    penalty, pattern_warnings = check_patterns(password)
    entropy = calculate_entropy(password)

    raw = (length_score * 15) + (complexity_score * 15) - (penalty * 10)
    # Entropy bonus (max 20 pts)
    entropy_bonus = min(20, int(entropy / 4))
    raw += entropy_bonus
    score = max(0, min(100, raw))

    if score < 20:
        label, color = "Very Weak", "red"
    elif score < 40:
        label, color = "Weak", "orange"
    elif score < 60:
        label, color = "Fair", "yellow"
    elif score < 80:
        label, color = "Strong", "green"
    else:
        label, color = "Very Strong", "bright_green"

    feedback = [length_feedback] + complexity_feedback

    return {
        "score": score,
        "label": label,
        "color": color,
        "entropy": round(entropy, 1),
        "feedback": feedback,
        "warnings": pattern_warnings,
    }


# ─────────────────────────────────────────────
#  PASSWORD GENERATOR
# ─────────────────────────────────────────────

def generate_password(
    length: int = 16,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    exclude_ambiguous: bool = False,
) -> str:
    """
    Generate a cryptographically-random password.

    Args:
        length: Desired password length (min 4).
        use_uppercase: Include A–Z.
        use_lowercase: Include a–z.
        use_digits: Include 0–9.
        use_symbols: Include special characters.
        exclude_ambiguous: Remove 0/O/l/1/I to avoid visual confusion.

    Returns:
        A random password string.

    Raises:
        ValueError: If no character sets are selected or length < 4.
    """
    if length < 4:
        raise ValueError("Password length must be at least 4.")

    charset = ""
    required_chars = []

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    if exclude_ambiguous:
        ambiguous = "0Ol1I"
        lowercase = ''.join(c for c in lowercase if c not in ambiguous)
        uppercase = ''.join(c for c in uppercase if c not in ambiguous)
        digits = ''.join(c for c in digits if c not in ambiguous)

    if use_lowercase:
        charset += lowercase
        required_chars.append(random.choice(lowercase))
    if use_uppercase:
        charset += uppercase
        required_chars.append(random.choice(uppercase))
    if use_digits:
        charset += digits
        required_chars.append(random.choice(digits))
    if use_symbols:
        charset += symbols
        required_chars.append(random.choice(symbols))

    if not charset:
        raise ValueError("At least one character set must be selected.")

    # Fill remaining length with random choices
    remaining = [random.choice(charset) for _ in range(length - len(required_chars))]
    password_list = required_chars + remaining
    random.shuffle(password_list)

    return ''.join(password_list)


def generate_passphrase(num_words: int = 4, separator: str = "-") -> str:
    """
    Generate a memorable passphrase from random words.

    Args:
        num_words: Number of words in the passphrase.
        separator: Character to join words.

    Returns:
        A passphrase string.
    """
    # Compact word list for offline use
    words = [
        "apple", "brave", "cloud", "dance", "eagle", "flame", "grape",
        "hotel", "image", "juice", "knife", "lemon", "magic", "night",
        "ocean", "piano", "queen", "river", "stone", "tiger", "umbra",
        "vault", "water", "xenon", "yacht", "zebra", "alpha", "bloom",
        "chess", "delta", "epoch", "frost", "globe", "haste", "igloo",
        "jewel", "karma", "laser", "maple", "noble", "orbit", "pearl",
        "quest", "raven", "sigma", "torch", "ultra", "vibes", "witch",
        "exult", "yield", "zonal", "audio", "boxer", "crisp", "dwarf",
        "ember", "flair", "ghost", "helix", "intro", "joker", "knack",
    ]
    selected = random.choices(words, k=num_words)
    # Add a random number for extra entropy
    selected.append(str(random.randint(10, 99)))
    return separator.join(selected)
