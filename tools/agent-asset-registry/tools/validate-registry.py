#!/usr/bin/env python3
"""Validate all registry YAML files against the agent-type schema."""

import json
import sys
import yaml
from pathlib import Path

REGISTRY_DIR = Path(__file__).resolve().parent.parent / "registry"
SCHEMA_PATH = REGISTRY_DIR.parent / "schema" / "agent-type-schema.json"


def load_schema(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def validate_type(filepath: Path, schema: dict) -> tuple[bool, list[str]]:
    errors: list[str] = []
    try:
        with open(filepath) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return False, [f"YAML parse error: {e}"]

    if not isinstance(data, dict):
        return False, ["File is not a valid YAML object"]

    required = ["id", "name", "description", "category", "capabilities", "risk_profile", "known_behaviors"]
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if "risk_profile" in data and data["risk_profile"] not in ("low", "medium", "high", "critical"):
        errors.append(f"Invalid risk_profile: {data.get('risk_profile')}")

    if "known_behaviors" in data and isinstance(data["known_behaviors"], list):
        for i, b in enumerate(data["known_behaviors"]):
            if not isinstance(b, dict):
                errors.append(f"known_behaviors[{i}]: expected object, got {type(b).__name__}")
            else:
                for bf in ("pattern", "severity", "description"):
                    if bf not in b:
                        errors.append(f"known_behaviors[{i}]: missing field '{bf}'")

    return len(errors) == 0, errors


def main():
    schema = load_schema(str(SCHEMA_PATH))
    yaml_files = list(REGISTRY_DIR.rglob("*.yaml"))

    if not yaml_files:
        print(f"❌ No YAML files found in {REGISTRY_DIR}")
        sys.exit(1)

    total = len(yaml_files)
    valid = 0
    invalid = 0

    print(f"\n  Agent Asset Registry — Validator\n")
    print(f"  Schema: {SCHEMA_PATH.name}")
    print(f"  Files:  {total}\n")

    for fpath in sorted(yaml_files):
        rel = fpath.relative_to(REGISTRY_DIR)
        ok, errors = validate_type(fpath, schema)
        if ok:
            valid += 1
            print(f"  ✓  {rel}")
        else:
            invalid += 1
            print(f"  ✗  {rel}")
            for e in errors:
                print(f"       {e}")

    print(f"\n  Valid:   {valid}")
    print(f"  Invalid: {invalid}")
    print(f"  Total:   {total}\n")

    if invalid > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
