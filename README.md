# 🔐 Password Strength Checker & Generator

A Python CLI tool to **evaluate password strength** and **generate cryptographically random passwords**, with real-time feedback to help users create strong, secure credentials.

---

## Features

- **Strength Checker** — scores passwords 0–100 based on length, character complexity, entropy, and common-pattern detection
- **Secure Password Generator** — randomized passwords using any combination of uppercase, lowercase, digits, and symbols
- **Passphrase Generator** — memorable multi-word passphrases for human-friendly security
- **Real-time feedback** — actionable tips to improve weak passwords
- **Entropy calculation** — Shannon entropy displayed for each password
- **Pattern detection** — warns about common passwords, repeated characters, and keyboard sequences
- **Ambiguous-character exclusion** — optional removal of visually similar chars (0/O/l/1/I)

---

## Usage

```
╔══════════════════════════════════════════════╗
║   🔐  Password Strength Checker & Generator  ║
╚══════════════════════════════════════════════╝

Choose an option:
  1  Check password strength
  2  Generate a secure password
  3  Generate a passphrase
  q  Quit
```

### Check a Password
```
> 1
Enter password to check: hunter2

  Strength  ███████░░░░░░░░░░░░░░░░░░░░░░░  Weak  (28/100)
  Entropy   33.6 bits

  Suggestions:
  •  Short (7 chars) — aim for 12+
  •  Add uppercase letters (A–Z)
  •  Add symbols (!@#$%^&*...)
```

### Generate a Password
```
> 2
  Length (default 16): 20
  Include uppercase  (A–Z)? [Y/n]: y
  Include symbols  (!@#…)? [Y/n]: y
  Exclude ambiguous chars? [y/N]: n

  Generated password:
  kR8$mP!vZ2@nWqL9#eXd

  Strength  ██████████████████████████████  Very Strong  (95/100)
  Entropy   130.8 bits
```

### Generate a Passphrase
```
> 3
  Number of words (default 4): 4
  Separator (default '-'):

  Generated passphrase:
  tiger-bloom-orbit-frost-42

  Strength  ████████████████████░░░░░░░░░░  Strong  (72/100)
```

---

## Running Tests

```bash
pip install pytest
python -m pytest tests.py -v
```

---

## Project Structure

```
password-tool/
├── main.py          # CLI entry point
├── password_tool.py # Core logic (checker + generator)
├── tests.py         # Unit tests (pytest)
└── README.md
```

---

## How Scoring Works

| Component         | Max Points | Details                              |
|-------------------|-----------|--------------------------------------|
| Length            | 60        | Scales from <6 (0) to 16+ chars (60)|
| Character types   | 60        | +15 per type: lower/upper/digit/sym  |
| Entropy bonus     | 20        | Based on charset × length            |
| Pattern penalty   | −30       | Common passwords, repeats, sequences |

Final score is clamped to **0–100**.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
