#!/usr/bin/env python3
"""
validate_review_report.py

Deterministic validator for PR readiness review reports.
Ensures that the generated report conforms to the required structure,
contains all mandatory sections, and explicitly enforces human decision gates.

Usage:
    python validate_review_report.py <path_to_report.md>
"""

import sys
import os
import re

REQUIRED_SECTIONS = [
    "## Review Context",
    "## Requirements / Acceptance Criteria Reviewed",
    "## Test Evidence",
    "## MUST FIX",
    "## SHOULD FIX",
    "## OPTIONAL",
    "## Final Review Summary",
]

REQUIRED_MARKERS = [
    "# PR Readiness Review",
    "Human decision required:",
]

def validate_report(file_path: str) -> bool:
    if not os.path.exists(file_path):
        print(f"ERROR: Report file does not exist: {file_path}", file=sys.stderr)
        return False

    if not os.path.isfile(file_path):
        print(f"ERROR: Path is not a file: {file_path}", file=sys.stderr)
        return False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Could not read report file: {e}", file=sys.stderr)
        return False

    missing_markers = []
    for marker in REQUIRED_MARKERS:
        if marker not in content:
            missing_markers.append(marker)

    missing_sections = []
    for section in REQUIRED_SECTIONS:
        if section not in content:
            missing_sections.append(section)

    errors = []
    if missing_markers:
        errors.append(f"Missing required markers: {missing_markers}")
    if missing_sections:
        errors.append(f"Missing required sections: {missing_sections}")

    # Verify Human decision required is set to YES or similar affirmative
    human_decision_pattern = re.search(r"Human decision required:\s*([A-Za-z]+)", content)
    if not human_decision_pattern:
        errors.append("Missing value for 'Human decision required'")
    elif human_decision_pattern.group(1).upper() not in ["YES", "TRUE"]:
        errors.append(f"Unexpected value for 'Human decision required': {human_decision_pattern.group(1)}")

    if errors:
        print("INVALID: Report validation failed with the following errors:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return False

    print("VALID: PR readiness review structure is complete.")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_review_report.py <path_to_report.md>", file=sys.stderr)
        sys.exit(2)

    report_path = sys.argv[1]
    is_valid = validate_report(report_path)
    if is_valid:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
