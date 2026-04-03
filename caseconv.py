#!/usr/bin/env python3
"""caseconv - String case converter.

Convert between camelCase, snake_case, kebab-case, PascalCase, SCREAMING_SNAKE,
Title Case, sentence case, dot.case, path/case, and more.

Usage:
    caseconv "myVariableName" --all
    caseconv "my-kebab-string" --to snake
    caseconv "MY_CONSTANT" --to camel
    echo "some text here" | caseconv - --to pascal
"""
import argparse
import re
import sys


def tokenize(s: str) -> list[str]:
    """Split any-case string into lowercase word tokens."""
    # Handle camelCase/PascalCase boundaries
    s = re.sub(r'([a-z])([A-Z])', r'\1_\2', s)
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', s)
    # Split on non-alphanumeric
    tokens = re.split(r'[^a-zA-Z0-9]+', s)
    return [t.lower() for t in tokens if t]


def to_camel(tokens: list[str]) -> str:
    if not tokens: return ""
    return tokens[0] + ''.join(t.capitalize() for t in tokens[1:])

def to_pascal(tokens: list[str]) -> str:
    return ''.join(t.capitalize() for t in tokens)

def to_snake(tokens: list[str]) -> str:
    return '_'.join(tokens)

def to_screaming(tokens: list[str]) -> str:
    return '_'.join(t.upper() for t in tokens)

def to_kebab(tokens: list[str]) -> str:
    return '-'.join(tokens)

def to_train(tokens: list[str]) -> str:
    return '-'.join(t.capitalize() for t in tokens)

def to_dot(tokens: list[str]) -> str:
    return '.'.join(tokens)

def to_path(tokens: list[str]) -> str:
    return '/'.join(tokens)

def to_title(tokens: list[str]) -> str:
    return ' '.join(t.capitalize() for t in tokens)

def to_sentence(tokens: list[str]) -> str:
    if not tokens: return ""
    return tokens[0].capitalize() + ' ' + ' '.join(tokens[1:]) if len(tokens) > 1 else tokens[0].capitalize()

def to_flat(tokens: list[str]) -> str:
    return ''.join(tokens)

def to_upper_flat(tokens: list[str]) -> str:
    return ''.join(t.upper() for t in tokens)

def to_cobol(tokens: list[str]) -> str:
    return '-'.join(t.upper() for t in tokens)


CONVERTERS = {
    "camel": ("camelCase", to_camel),
    "pascal": ("PascalCase", to_pascal),
    "snake": ("snake_case", to_snake),
    "screaming": ("SCREAMING_SNAKE", to_screaming),
    "kebab": ("kebab-case", to_kebab),
    "train": ("Train-Case", to_train),
    "dot": ("dot.case", to_dot),
    "path": ("path/case", to_path),
    "title": ("Title Case", to_title),
    "sentence": ("Sentence case", to_sentence),
    "flat": ("flatcase", to_flat),
    "upperflat": ("UPPERFLATCASE", to_upper_flat),
    "cobol": ("COBOL-CASE", to_cobol),
}


def detect_case(s: str) -> str:
    """Best-effort detection of current case."""
    if '_' in s and s == s.upper(): return "screaming"
    if '_' in s and s == s.lower(): return "snake"
    if '-' in s and s == s.lower(): return "kebab"
    if '-' in s and s == s.upper(): return "cobol"
    if '-' in s and all(w[0].isupper() for w in s.split('-') if w): return "train"
    if '.' in s: return "dot"
    if '/' in s: return "path"
    if s[0].islower() and any(c.isupper() for c in s): return "camel"
    if s[0].isupper() and any(c.isupper() for c in s[1:]): return "pascal"
    if ' ' in s: return "title" if all(w[0].isupper() for w in s.split() if w) else "sentence"
    return "unknown"


def main():
    parser = argparse.ArgumentParser(description="String case converter")
    parser.add_argument("text", help="Text to convert (or - for stdin)")
    parser.add_argument("--to", dest="target", choices=list(CONVERTERS.keys()),
                        help="Target case")
    parser.add_argument("--all", action="store_true", help="Show all conversions")
    parser.add_argument("--detect", action="store_true", help="Detect current case")
    args = parser.parse_args()

    text = sys.stdin.read().strip() if args.text == "-" else args.text
    tokens = tokenize(text)

    if args.detect:
        case = detect_case(text)
        print(f"  Input:    {text}")
        print(f"  Detected: {case} ({CONVERTERS[case][0] if case in CONVERTERS else '?'})")
        print(f"  Tokens:   {tokens}")
        return

    if args.all:
        detected = detect_case(text)
        print(f"  Input:    {text}")
        print(f"  Detected: {detected}")
        print(f"  Tokens:   {tokens}")
        print()
        max_label = max(len(v[0]) for v in CONVERTERS.values())
        for key, (label, fn) in CONVERTERS.items():
            marker = " ←" if key == detected else ""
            print(f"  {label:>{max_label}}: {fn(tokens)}{marker}")
        return

    if args.target:
        label, fn = CONVERTERS[args.target]
        print(fn(tokens))
    else:
        # Default: show all
        for key, (label, fn) in CONVERTERS.items():
            print(f"  {label}: {fn(tokens)}")


if __name__ == "__main__":
    main()
