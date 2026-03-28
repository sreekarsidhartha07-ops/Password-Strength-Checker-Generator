"""
Tests for password_tool.py
Run: python -m pytest tests.py -v
"""

import pytest
from password_tool import (
    evaluate_strength,
    generate_password,
    generate_passphrase,
    calculate_entropy,
)


# ── evaluate_strength ──────────────────────────────────────────────────────────

class TestEvaluateStrength:
    def test_empty_password(self):
        r = evaluate_strength("")
        assert r["score"] == 0
        assert r["label"] == "Empty"

    def test_very_weak(self):
        r = evaluate_strength("abc")
        assert r["label"] in ("Very Weak", "Weak")
        assert r["score"] < 40

    def test_common_password_penalised(self):
        r = evaluate_strength("password")
        assert r["score"] < 20
        assert any("commonly" in w.lower() for w in r["warnings"])

    def test_strong_password(self):
        r = evaluate_strength("T!g3r$Blu3_Moon42!")
        assert r["score"] >= 60
        assert r["label"] in ("Strong", "Very Strong")

    def test_long_random_password(self):
        pwd = "Xy9#mPqL!vR2@eWs8$nKdZ7^"
        r = evaluate_strength(pwd)
        assert r["score"] >= 80

    def test_entropy_positive(self):
        r = evaluate_strength("Hello123!")
        assert r["entropy"] > 0

    def test_repeated_chars_warned(self):
        r = evaluate_strength("aaabbb111")
        assert any("repeat" in w.lower() for w in r["warnings"])

    def test_sequential_pattern_warned(self):
        r = evaluate_strength("abcdef123")
        assert any("sequential" in w.lower() or "pattern" in w.lower() for w in r["warnings"])


# ── generate_password ──────────────────────────────────────────────────────────

class TestGeneratePassword:
    def test_default_length(self):
        pwd = generate_password()
        assert len(pwd) == 16

    def test_custom_length(self):
        for l in [8, 12, 24, 32]:
            assert len(generate_password(length=l)) == l

    def test_only_lowercase(self):
        pwd = generate_password(length=20, use_uppercase=False, use_digits=False, use_symbols=False)
        assert pwd.islower()

    def test_only_digits(self):
        pwd = generate_password(length=20, use_uppercase=False, use_lowercase=False, use_symbols=False)
        assert pwd.isdigit()

    def test_no_charset_raises(self):
        with pytest.raises(ValueError):
            generate_password(use_uppercase=False, use_lowercase=False, use_digits=False, use_symbols=False)

    def test_too_short_raises(self):
        with pytest.raises(ValueError):
            generate_password(length=2)

    def test_no_ambiguous(self):
        ambiguous = set("0Ol1I")
        for _ in range(20):
            pwd = generate_password(length=20, exclude_ambiguous=True)
            assert not ambiguous.intersection(set(pwd)), f"Ambiguous char found in: {pwd}"

    def test_all_charsets_present(self):
        """With all charsets and length 20, expect all types represented (probabilistic)."""
        import re
        for _ in range(10):
            pwd = generate_password(length=20)
            has_upper  = bool(re.search(r'[A-Z]', pwd))
            has_lower  = bool(re.search(r'[a-z]', pwd))
            has_digit  = bool(re.search(r'\d', pwd))
            has_symbol = bool(re.search(r'[^a-zA-Z\d]', pwd))
            if has_upper and has_lower and has_digit and has_symbol:
                return  # passed
        pytest.fail("All-charset password never included all types in 10 tries")

    def test_randomness(self):
        """Two calls should not return the same password."""
        assert generate_password() != generate_password()


# ── generate_passphrase ────────────────────────────────────────────────────────

class TestGeneratePassphrase:
    def test_default_word_count(self):
        phrase = generate_passphrase()
        # default 4 words + 1 number = 5 parts
        parts = phrase.split("-")
        assert len(parts) == 5

    def test_custom_separator(self):
        phrase = generate_passphrase(num_words=3, separator="_")
        assert "_" in phrase
        assert "-" not in phrase

    def test_ends_with_number(self):
        phrase = generate_passphrase(num_words=3)
        last_part = phrase.split("-")[-1]
        assert last_part.isdigit()

    def test_randomness(self):
        assert generate_passphrase() != generate_passphrase()


# ── calculate_entropy ──────────────────────────────────────────────────────────

class TestCalculateEntropy:
    def test_empty(self):
        assert calculate_entropy("") == 0.0

    def test_only_lowercase(self):
        e = calculate_entropy("abcdef")
        assert e > 0

    def test_entropy_increases_with_charset(self):
        e_lower  = calculate_entropy("abcdef")
        e_mixed  = calculate_entropy("abCdEf")
        e_full   = calculate_entropy("abCd1!")
        assert e_full > e_mixed > e_lower

    def test_entropy_increases_with_length(self):
        short = calculate_entropy("Ab1!")
        long  = calculate_entropy("Ab1!Ab1!Ab1!Ab1!")
        assert long > short
