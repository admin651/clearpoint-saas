import re
import phonenumbers

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

def normalize_email(s: str) -> str:
    return (s or "").strip().lower()

def is_valid_email(s: str) -> bool:
    return bool(EMAIL_REGEX.match((s or "").strip()))

def normalize_phone(s: str, default_region: str = "US") -> tuple[str, bool]:
    s = (s or "").strip()
    try:
        num = phonenumbers.parse(s, default_region)
        valid = phonenumbers.is_possible_number(num) and phonenumbers.is_valid_number(num)
        e164 = phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164) if valid else s
        return e164, valid
    except Exception:
        return s, False

# Stub for external email verification
def external_email_status(email: str) -> str:
    # Replace with real API (ZeroBounce/Hunter). For now, infer via regex.
    return "valid" if is_valid_email(email) else "invalid"
