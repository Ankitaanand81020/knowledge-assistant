import re

# ----------------------------
# Patterns
# ----------------------------

EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')

PHONE_PATTERN = re.compile(r'(\+?\d{1,3}[- ]?)?\d{10}')

AADHAAR_PATTERN = re.compile(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}\b')

PAN_PATTERN = re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]\b')

SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')

CREDIT_CARD_PATTERN = re.compile(r'\b(?:\d[ -]*?){13,16}\b')


# ----------------------------
# Redactor
# ----------------------------

def redact(text: str):
    found = []

    def repl(pattern_name):
        def inner(match):
            found.append(pattern_name)
            return f"[{pattern_name.upper()} REDACTED]"
        return inner

    text = EMAIL_PATTERN.sub(repl("email"), text)
    text = PHONE_PATTERN.sub(repl("phone"), text)
    text = AADHAAR_PATTERN.sub(repl("aadhaar"), text)
    text = PAN_PATTERN.sub(repl("pan"), text)
    text = SSN_PATTERN.sub(repl("ssn"), text)
    text = CREDIT_CARD_PATTERN.sub(repl("credit_card"), text)

    return text, found


# ----------------------------
# Pretty test runner
# ----------------------------

def run_tests():
    print("PII Redaction Tests")
    print("=" * 50)

    tests = [
        {
            "text": "My email is john.doe@example.com and phone is 5551234567",
            "expected": "email + phone"
        },
        {
            "text": "Contact HR at hr@techcorp.internal or call +1-8005550199",
            "expected": "email + phone"
        },
        {
            "text": "My SSN is 123-45-6789 and card is 4111 1111 1111 1111",
            "expected": "ssn + credit_card"
        },
        {
            "text": "What is the leave policy?",
            "expected": "none"
        }
    ]

    for t in tests:
        redacted, found = redact(t["text"])

        print("\nOriginal :", t["text"])
        print("Redacted :", redacted)

        if found:
            summary = {}
            for f in found:
                summary[f] = summary.get(f, 0) + 1

            found_list = [{"type": k, "count": v} for k, v in summary.items()]
        else:
            found_list = "none"

        print("Found    :", found_list)


if __name__ == "__main__":
    run_tests()