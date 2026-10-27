"""Tests for the WitnessOS Compliance CLI entry point."""
import subprocess
import sys
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
CLI_DIR = REPO_ROOT / "cli"


def test_cli_imports():
    """The CLI package must import cleanly."""
    sys.path.insert(0, str(CLI_DIR))
    import witnessos_cli.main  # noqa: F401


def test_cli_help_runs():
    """`witnessos-compliance --help` must exit 0 and list commands."""
    result = subprocess.run(
        [sys.executable, "-m", "witnessos_cli.main", "--help"],
        cwd=str(CLI_DIR),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert "Usage" in result.stdout or "Usage" in result.stderr


def test_cli_reports_mapping_dir_exists():
    """The mappings directory the CLI reads must exist at repo root."""
    assert (REPO_ROOT / "mappings").is_dir(), "mappings/ directory missing"
