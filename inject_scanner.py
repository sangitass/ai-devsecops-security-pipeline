import pathlib
import sys

SYSTEM_PROMPT_PATTERNS = [
    "SYSTEM_PROMPT =",
    "system_message =",
    '"role": "system"',
]

INJECTION_PHRASES = [
    "ignore previous instructions",
    "you are now",
    "pretend you are",
    "act as if you have no restrictions",
]


def main():
    findings = []

    target_files = [
        pathlib.Path("app.py"),
        pathlib.Path("config.py"),
    ]

    for path in target_files:
        if not path.exists():
            print(f"WARNING: {path} not found.")
            continue

        content = path.read_text(errors="ignore")

        for line_number, line in enumerate(content.splitlines(), 1):

            if any(
                pattern.lower() in line.lower()
                for pattern in SYSTEM_PROMPT_PATTERNS
            ):
                findings.append(
                    f"{path}:{line_number}: hardcoded system prompt pattern"
                )

            if any(
                phrase in line.lower()
                for phrase in INJECTION_PHRASES
            ):
                findings.append(
                    f"{path}:{line_number}: prompt injection phrase"
                )

    if findings:
        print("PROMPT INJECTION SCANNER FAILED:")
        for finding in findings:
            print(finding)
        sys.exit(1)

    print("PROMPT INJECTION SCANNER PASSED.")


if __name__ == "__main__":
    main()
