#!/usr/bin/env bash
# Build the SDK and prove the package is inside the artefact.
#
# Run before publishing. A wheel that installs and ships no modules is worse than
# a failed build, because the failure only shows up in a consumer's import.
set -euo pipefail

cd "$(dirname "$0")/.."

OUT="$(mktemp -d /tmp/sdk-build-XXXXXX)"
trap 'rm -rf "$OUT"' EXIT INT TERM

echo "== build"
if command -v uv >/dev/null 2>&1; then
  uv build -o "$OUT"
else
  python -m build --outdir "$OUT"
fi

WHEEL="$(ls "$OUT"/*.whl)"
SDIST="$(ls "$OUT"/*.tar.gz)"
echo "wheel: $WHEEL"
echo "sdist: $SDIST"

echo "== wheel must contain the package modules"
WHEEL_MODULES="$(unzip -Z1 "$WHEEL" | grep -c '^witnessos_sdk/.*\.py$' || true)"
echo "wheel modules: $WHEEL_MODULES"
if [ "$WHEEL_MODULES" -lt 6 ]; then
  echo "FAIL: wheel carries $WHEEL_MODULES package modules, expected at least 6" >&2
  unzip -Z1 "$WHEEL" >&2
  exit 1
fi

echo "== sdist must contain the sources and the tests"
SDIST_MODULES="$(tar tzf "$SDIST" | grep -c 'witnessos_sdk/.*\.py$' || true)"
echo "sdist modules: $SDIST_MODULES"
if [ "$SDIST_MODULES" -lt 6 ]; then
  echo "FAIL: sdist carries $SDIST_MODULES package modules" >&2
  exit 1
fi

echo "== install into a clean environment and import"
VENV="$OUT/venv"
uv venv -q "$VENV"
uv pip install --python "$VENV/bin/python" -q "$WHEEL"
(cd /tmp && "$VENV/bin/python" - <<'PY'
import witnessos_sdk as sdk
from witnessos_sdk.digest import canonical_mission_digest

digest = canonical_mission_digest(
    intent="Survey grid A and hold on completion",
    steps=[{"action": "survey", "parameters": {"zone": "A", "altitude_m": 25}}],
    capability_profile={"has_camera": True},
    robot_class="field_marker",
)
expected = "sha256:d5166d48c699a12df1736d3885665d5dcec492e189dc25c20450aa73ce563a1c"
if digest != expected:
    raise SystemExit(f"FAIL: published digest {digest} != normative {expected}")
print(f"import ok: {sdk.__file__}")
print(f"version: {sdk.__version__}")
print(f"digest: {digest}")
PY
)

echo "PACKAGE VERIFY: PASS"
