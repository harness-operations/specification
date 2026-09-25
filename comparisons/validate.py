#!/usr/bin/env python3
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "schema.json"
CANONICAL_PATH = ROOT / "data" / "landscape.json"
FIXTURES = sorted((ROOT / "fixtures").glob("*.json"))


def load(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def unique_ids(items, label, path):
    ids = [item["id"] for item in items]
    duplicates = sorted({item_id for item_id in ids if ids.count(item_id) > 1})
    if duplicates:
        raise ValueError(f"{path}: duplicate {label} ids: {', '.join(duplicates)}")


def validate_references(data, path):
    capability_ids = {item["id"] for item in data["capabilities"]}
    system_ids = {item["id"] for item in data["systems"]}

    unique_ids(data["capabilities"], "capability", path)
    unique_ids(data["systems"], "system", path)
    unique_ids(data["observations"], "observation", path)
    unique_ids(data["integrations"], "integration", path)

    for observation in data["observations"]:
        if observation["capability_id"] not in capability_ids:
            raise ValueError(
                f"{path}: observation {observation['id']} references unknown capability "
                f"{observation['capability_id']}"
            )
        if observation["system_id"] not in system_ids:
            raise ValueError(
                f"{path}: observation {observation['id']} references unknown system "
                f"{observation['system_id']}"
            )

    for integration in data["integrations"]:
        for side in ("source", "target"):
            system_id = integration[side]["system_id"]
            if system_id not in system_ids:
                raise ValueError(
                    f"{path}: integration {integration['id']} {side} references unknown system "
                    f"{system_id}"
                )


def main():
    schema = load(SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    targets = [CANONICAL_PATH, *FIXTURES]
    failed = False

    for path in targets:
        data = load(path)
        errors = sorted(validator.iter_errors(data), key=lambda error: list(error.path))
        if errors:
            failed = True
            for error in errors:
                location = ".".join(str(part) for part in error.path) or "<root>"
                print(f"{path}: {location}: {error.message}", file=sys.stderr)
            continue

        try:
            validate_references(data, path)
        except ValueError as error:
            failed = True
            print(error, file=sys.stderr)
            continue

        print(f"valid: {path.relative_to(ROOT.parent)}")

    if failed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
