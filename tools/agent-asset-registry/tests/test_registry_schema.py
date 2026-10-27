"""Tests for the Agent Asset Registry: registry entries must validate against the schema."""
import json
import pathlib

import jsonschema
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "agent-type-schema.json"
REGISTRY_DIR = REPO_ROOT / "registry"


def _load_schema():
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def _agent_type_entries():
    """Yield agent type entries (agent_types/**/*.yaml)."""
    for p in sorted((REGISTRY_DIR / "agent_types").rglob("*.yaml")):
        with open(p, encoding="utf-8") as f:
            yield p, yaml.safe_load(f)


def _vendor_entries():
    """Yield vendor entries (vendors/*.yaml)."""
    for p in sorted((REGISTRY_DIR / "vendors").rglob("*.yaml")):
        with open(p, encoding="utf-8") as f:
            yield p, yaml.safe_load(f)


def test_schema_is_valid_json():
    schema = _load_schema()
    assert schema.get("$schema"), "schema must declare its meta-schema"
    assert "properties" in schema


def test_all_agent_type_entries_validate_against_schema():
    schema = _load_schema()
    # Validate the schema itself first (raises if malformed).
    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(schema)
    entries = list(_agent_type_entries())
    assert entries, "registry must contain at least one agent type entry"
    for path, entry in entries:
        errors = sorted(validator.iter_errors(entry), key=lambda e: list(e.path))
        assert not errors, f"{path} fails schema: {[e.message for e in errors]}"


def test_vendor_entries_wellformed():
    entries = list(_vendor_entries())
    assert entries, "registry must contain at least one vendor entry"
    for path, entry in entries:
        assert isinstance(entry, dict), f"{path} must be a mapping"
        for key in ("id", "name", "description", "type"):
            assert entry.get(key), f"{path} missing required key {key!r}"


def test_registry_entries_have_unique_ids():
    seen = {}
    for path, entry in list(_agent_type_entries()) + list(_vendor_entries()):
        if isinstance(entry, dict) and "id" in entry:
            seen.setdefault(entry["id"], []).append(str(path))
    dupes = {k: v for k, v in seen.items() if len(v) > 1}
    assert not dupes, f"duplicate ids: {dupes}"
