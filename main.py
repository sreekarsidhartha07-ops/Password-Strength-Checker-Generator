#!/usr/bin/env python3
"""
Password Strength Checker & Generator — CLI
Run: python main.py
"""

import sys
from password_tool import evaluate_strength, generate_password, generate_passphrase

# ── ANSI colour helpers ────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"

RED    = "\033[91m"
ORANGE = "\033[33m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"
GRAY   = "\033[90m"

def color_for(label: str) -> str:
    return {
        "Very Weak":   RED,
        "Weak":        ORANGE,
        "Fair":        YELLOW,
        "Strong":      GREEN,
        "Very Strong": GREEN,
    }.get(label, WHITE)

def bar(score: int, width: int = 30) -> str:
    filled = int(score / 100 * width)
    empty  = width - filled
    pct_color = color_for("Very Weak") if score < 20 else \
                color_for("Weak")      if score < 40 else \
                color_for("Fair")      if score < 60 else \
                GREEN
    return pct_color + "█" * filled + GRAY + "░" * empty + RESET

def header():
    print(f"\n{CYAN}{BOLD}╔══════════════════════════════════════════════╗")
    print(f"║   🔐  Password Strength Checker & Generator  ║")
    print(f"╚══════════════════════════════════════════════╝{RESET}\n")

def menu():
    print(f"{WHITE}{BOLD}Choose an option:{RESET}")
    print(f"  {CYAN}1{RESET}  Check password strength")
    print(f"  {CYAN}2{RESET}  Generate a secure password")
    print(f"  {CYAN}3{RESET}  Generate a passphrase")
    print(f"  {CYAN}q{RESET}  Quit\n")

# ── Strength Checker UI ────────────────────────────────────────────────────────

def run_checker():
    print(f"\n{BOLD}── Password Strength Checker ──{RESET}")
    try:
        password = input(f"{DIM}Enter password to check: {RESET}")
    except (EOFError, KeyboardInterrupt):
        return

    result = evaluate_strength(password)

    col   = color_for(result["label"])
    score = result["score"]

    print(f"\n  Strength  {bar(score)}  {col}{BOLD}{result['label']}{RESET}  ({score}/100)")
    print(f"  Entropy   {result['entropy']} bits\n")

    if result["warnings"]:
        for w in result["warnings"]:
            print(f"  {RED}⚠  {w}{RESET}")
        print()

    print(f"  {BOLD}Suggestions:{RESET}")
    for tip in result["feedback"]:
        print(f"  {GRAY}•  {tip}{RESET}")
    print()


# ── Password Generator UI ──────────────────────────────────────────────────────

def ask_bool(prompt: str, default: bool = True) -> bool:
    yn = "Y/n" if default else "y/N"
    try:
        ans = input(f"  {prompt} [{yn}]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return default
    if ans in ("y", "yes"):
        return True
    if ans in ("n", "no"):
        return False
    return default

def run_generator():
    print(f"\n{BOLD}── Secure Password Generator ──{RESET}")
    try:
        raw = input(f"  Length (default 16): ").strip()
        length = int(raw) if raw.isdigit() else 16
    except (EOFError, KeyboardInterrupt):
        return

    uppercase  = ask_bool("Include uppercase  (A–Z)?", True)
    lowercase  = ask_bool("Include lowercase  (a–z)?", True)
    digits     = ask_bool("Include numbers    (0–9)?", True)
    symbols    = ask_bool("Include symbols  (!@#…)?", True)
    no_ambig   = ask_bool("Exclude ambiguous chars (0/O/l/1/I)?", False)

    try:
        pwd = generate_password(
            length=length,
            use_uppercase=uppercase,
            use_lowercase=lowercase,
            use_digits=digits,
            use_symbols=symbols,
            exclude_ambiguous=no_ambig,
        )
    except ValueError as e:
        print(f"\n{RED}Error: {e}{RESET}\n")
        return

    result = evaluate_strength(pwd)
    col    = color_for(result["label"])

    print(f"\n  {BOLD}Generated password:{RESET}")
    print(f"  {GREEN}{BOLD}{pwd}{RESET}\n")
    print(f"  Strength  {bar(result['score'])}  {col}{BOLD}{result['label']}{RESET}  ({result['score']}/100)")
    print(f"  Entropy   {result['entropy']} bits\n")

    # Offer to generate another
    try:
        again = input(f"  {DIM}Generate another? [y/N]: {RESET}").strip().lower()
        if again in ("y", "yes"):
            run_generator()
    except (EOFError, KeyboardInterrupt):
        pass


# ── Passphrase Generator UI ────────────────────────────────────────────────────

def run_passphrase():
    print(f"\n{BOLD}── Passphrase Generator ──{RESET}")
    try:
        raw = input("  Number of words (default 4): ").strip()
        num_words = int(raw) if raw.isdigit() else 4
        sep = input("  Separator (default '-'): ").strip() or "-"
    except (EOFError, KeyboardInterrupt):
        return

    phrase = generate_passphrase(num_words=num_words, separator=sep)
    result = evaluate_strength(phrase)
    col    = color_for(result["label"])

    print(f"\n  {BOLD}Generated passphrase:{RESET}")
    print(f"  {CYAN}{BOLD}{phrase}{RESET}\n")
    print(f"  Strength  {bar(result['score'])}  {col}{BOLD}{result['label']}{RESET}  ({result['score']}/100)")
    print(f"  Entropy   {result['entropy']} bits\n")


# ── Main Loop ─────────────────────────────────────────────────────────────────

def main():
    header()
    while True:
        menu()
        try:
            choice = input(f"{CYAN}>{RESET} ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break

        if choice == "1":
            run_checker()
        elif choice == "2":
            run_generator()
        elif choice == "3":
            run_passphrase()
        elif choice in ("q", "quit", "exit"):
            print(f"\n{DIM}Stay secure. Goodbye!{RESET}\n")
            sys.exit(0)
        else:
            print(f"\n{ORANGE}Invalid option — please enter 1, 2, 3, or q.{RESET}\n")


if __name__ == "__main__":
    main()
