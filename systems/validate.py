#!/usr/bin/env python3
import json
from pathlib import Path
import sys
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
SCHEMA_PATH = ROOT / "schema.json"
INDEX_PATH = ROOT / "index.json"
COMPARISON_PATH = REPO_ROOT / "comparisons" / "data" / "systems.json"
VALIDATION_CASES = sorted((REPO_ROOT / "tests" / "systems").glob("*.json"))

def load(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)

def unique_ids(items, label, path):
    ids = [item["id"] for item in items]
    duplicates = sorted({item_id for item_id in ids if ids.count(item_id) > 1})
    if duplicates:
        raise ValueError(f"{path}: duplicate {label} ids: {', '.join(duplicates)}")

def semantic_validate(data, path, check_paths):
    unique_ids(data["subjects"], "subject", path)
    unique_ids(data["relationships"], "relationship", path)
    subjects = {item["id"]: item for item in data["subjects"]}

    comparison_scopes = set()
    if check_paths:
        comparison_data = load(COMPARISON_PATH)
        for observation in comparison_data["observations"]:
            scope = observation["scope"]
            comparison_scopes.add((
                observation["system_id"],
                scope["interface"],
                scope["version"],
                scope["deployment_mode"],
            ))

    for subject in data["subjects"]:
        if "other" in subject["kinds"] and not subject.get("notes"):
            raise ValueError(f"{path}: subject {subject['id']} uses kind other without explanatory notes")
        if check_paths:
            target = REPO_ROOT / subject["document_path"]
            if not target.is_file():
                raise ValueError(f"{path}: missing document_path for {subject['id']}: {subject['document_path']}")
            comparison_scope = subject.get("comparison_scope")
            if comparison_scope:
                key = (
                    comparison_scope["system_id"],
                    comparison_scope["interface"],
                    comparison_scope["version"],
                    comparison_scope["deployment_mode"],
                )
                if key not in comparison_scopes:
                    raise ValueError(
                        f"{path}: subject {subject['id']} comparison_scope does not match "
                        f"a published comparison row: {comparison_scope}"
                    )

    for relationship in data["relationships"]:
        for field in ("source_id", "target_id"):
            if relationship[field] not in subjects:
                raise ValueError(
                    f"{path}: relationship {relationship['id']} references unknown "
                    f"{field}: {relationship[field]}"
                )
        if relationship["source_id"] == relationship["target_id"]:
            raise ValueError(f"{path}: relationship {relationship['id']} cannot be self-referential")

def validate_file(validator, path, expected_valid, check_paths=False):
    data = load(path)
    errors = sorted(validator.iter_errors(data), key=lambda error: list(error.path))
    messages = [
        f"{'.'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in errors
    ]
    if not messages:
        try:
            semantic_validate(data, path, check_paths)
        except ValueError as error:
            messages.append(str(error))
    is_valid = not messages
    if is_valid != expected_valid:
        expected = "valid" if expected_valid else "invalid"
        print(
            f"{path}: expected {expected}; "
            + (" | ".join(messages) if messages else "validation passed"),
            file=sys.stderr,
        )
        return False
    print(f"{'valid' if is_valid else 'expected-invalid'}: {path.relative_to(REPO_ROOT)}")
    return True

def main():
    validator = Draft202012Validator(load(SCHEMA_PATH), format_checker=FormatChecker())
    ok = validate_file(validator, INDEX_PATH, True, check_paths=True)
    for path in VALIDATION_CASES:
        ok = validate_file(validator, path, not path.name.startswith("invalid-")) and ok
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
