"""Packaging guards.

The 0.1.0 and 0.1.1 wheels installed cleanly and shipped no modules, so
``import witnessos_sdk`` failed for anyone using an installed package rather than
the source tree. Installation succeeding is not evidence that the package is
inside the artefact.

These tests cover configuration and version consistency without needing a build
toolchain. The artefact itself is proved by ``scripts/verify_package.sh``, which
builds a wheel, requires the module files inside it, installs it into a clean
environment and reproduces the normative digest.
"""

import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "witnessos_sdk"

EXPECTED_MODULES = {
    "__init__.py",
    "auth.py",
    "client.py",
    "contract.py",
    "digest.py",
    "models.py",
}


def _pyproject() -> dict:
    return tomllib.loads((ROOT / "pyproject.toml").read_text())


def test_source_package_is_complete():
    assert SRC.is_dir(), "src/witnessos_sdk is missing"
    present = {p.name for p in SRC.glob("*.py")}
    missing = EXPECTED_MODULES - present
    assert not missing, f"modules missing from the source package: {sorted(missing)}"


def test_pyproject_declares_src_package_dir():
    config = _pyproject()
    package_dir = config["tool"]["setuptools"]["package-dir"]
    assert package_dir.get("") == "src", package_dir
    find = config["tool"]["setuptools"]["packages"]["find"]
    assert find["where"] == ["src"], find


def test_declared_version_matches_the_package():
    declared = _pyproject()["project"]["version"]
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0, 'src');"
            "import witnessos_sdk; print(witnessos_sdk.__version__)",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == declared, (
        f"package __version__ {result.stdout.strip()} != pyproject {declared}"
    )


def test_verify_script_is_present_and_executable():
    script = ROOT / "scripts" / "verify_package.sh"
    assert script.is_file(), "scripts/verify_package.sh is missing"
    assert script.stat().st_mode & 0o111, "scripts/verify_package.sh is not executable"
