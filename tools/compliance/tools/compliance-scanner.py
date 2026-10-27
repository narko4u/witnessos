#!/usr/bin/env python3
"""
WitnessOS Compliance Scanner for EAB's 9-Agent Fleet.

Pipeline:
  1. SCAN — Use rogue-agent-audit detectors to find every agent process,
     endpoint, API key, and configuration in the environment.
  2. IDENTIFY — Cross-reference findings against the agent-asset-registry.
     Answer: "Is this agent known? What's its risk profile?"
  3. GRADE — For any WitnessOS-governed agents with evidence bundles,
     invoke witnessos-verifier to get E1-E4 grade.
  4. REPORT — Produce a single compliance scorecard.

Single file, no pip install, stdlib whenever possible.
"""

import asyncio
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

EAB_FLEET = [
    {"name": "Sovereign",         "type": "general-purpose", "role": "orchestrator", "risk": "high"},
    {"name": "Porgie",            "type": "general-purpose", "role": "prodigy/research", "risk": "medium"},
    {"name": "Hermes",            "type": "general-purpose", "role": "agent runtime", "risk": "high"},
    {"name": "Charlie",            "type": "workflow",      "role": "infrastructure",  "risk": "medium"},
    {"name": "Senti",             "type": "general-purpose", "role": "COO / ops",       "risk": "medium"},
    {"name": "Oscar",             "type": "general-purpose", "role": "sales / demo",    "risk": "medium"},
    {"name": "Socio",             "type": "general-purpose", "role": "social media",    "risk": "low"},
    {"name": "WitnessOS-Gateway", "type": "workflow",      "role": "gateway",          "risk":    "high"},
    {"name": "EAB-API",           "type": "workflow",      "role": "backend bridge",   "risk": "medium"},
]

KNOWN_COMPLIANCE_RISKS = {
    "Hermes": [
        "Runs as agent runtime with full tool access",
        "Has credential-bearing environment variables",
        "Process visibility: always running",
    ],
    "Sovereign": [
        "Orchestrator with delegate_task capability",
        "Has Slack + Telegram + Discord tokens",
        "Approval-gated but autonomous delegation",
    ],
    "Porgie": [
        "Has own Slack bot token (separate from Sovereign)",
        "NVIDIA NIM API access",
        "No Telegram token (after crash isolation)",
    ],
       "WitnessOS-Gateway": [
        "Brokers credentials — is itself a credential-bearing service",
        "Attack surface: credential theft, policy bypass, receipt spoofing",
        "Logged actions are the compliance trail itself",
    ],
}

# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass
class AgentFinding:
    agent_name: str
    category: str
    status: str  # "governed" | "ungoverned" | "unknown"
    endpoints_found: list[str] = field(default_factory=list)
    credentials_exposed: list[str] = field(default_factory=list)
    risk_profile: str = ""
    registry_match: bool = False
    evidence_grade: str = ""  # "E1" | "E2" | "E3" | "E4" | ""
    witnessos_integrated: bool = False
    recommendations: list[str] = field(default_factory=list)


@dataclass
class ComplianceReport:
    timestamp: str
    target: str
    fleet: list[AgentFinding] = field(default_factory=list)
    summary: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Scanner: Find agents via /proc
# ---------------------------------------------------------------------------


def scan_process_tree() -> list[dict]:
    """Scan /proc for agent processes matching known frameworks."""
    found: list[dict] = []
    proc_dir = Path("/proc")
    if not proc_dir.exists():
        return found

    # Patterns from the rogue-agent-audit source
    agent_keywords = [
        "hermes", "sovereign", "porgie", "senti", "soci", "oscar",
        "witnessos", "gateway", "autogen", "crewai", "langchain",
        "langgraph", "ollama", "vllm", "nvidia-nim", "agent",
        "openai", "anthropic", "python", "node",
    ]

    framework_envs = [
        "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "HUGGINGFACE_TOKEN",
        "GITHUB_TOKEN", "SLACK_BOT_TOKEN", "TELEGRAM_BOT_TOKEN",
        "NVIDIA_API_KEY", "WITNESSOS_API_KEY", "AGENT_CONFIG",
        "HERMES_", "WITNESSOS_",
    ]

    for entry in proc_dir.iterdir():
        if not entry.name.isdigit():
            continue
        try:
            pid = int(entry.name)
            cmdline = (entry / "cmdline").read_text(errors="replace").replace("\0", " ").strip()
            if not cmdline:
                continue
            comm = (entry / "comm").read_text(errors="replace").strip()

            # Check if this process matches an agent
            cmd_lower = cmdline.lower()
            matched = []
            for kw in agent_keywords:
                if kw in cmd_lower or kw in comm.lower():
                    matched.append(kw)

            if not matched:
                continue

            # Read environment
            env_vars: dict[str, str] = {}
            try:
                environ_raw = (entry / "environ").read_bytes()
                for var in environ_raw.decode("utf-8", errors="replace").split("\0"):
                    if "=" in var:
                        k, _, v = var.partition("=")
                        env_vars[k] = v
            except (PermissionError, FileNotFoundError):
                pass

            exposed_creds = []
            for fw_key in framework_envs:
                for ev in env_vars:
                    if ev.upper().startswith(fw_key) or fw_key in ev.upper():
                        exposed_creds.append(f"{ev}={env_vars[ev][:8]}...")

            found.append({
                "pid": pid,
                "comm": comm,
                "cmdline": cmdline[:200],
                "matched_keywords": matched,
                "exposed_creds": exposed_creds[:5],  # max 5
            })
        except (PermissionError, FileNotFoundError):
            continue

    return found


def scan_http_endpoints() -> list[dict]:
    """Probe common agent API ports on localhost."""
    import urllib.request

    agent_paths = [
        "/v1/chat/completions", "/v1/models", "/api/agents",
        "/health", "/api/execute", "/api/tools",
    ]
    agent_ports = [8000, 8080, 8081, 11434, 11435, 3000, 5000, 7860, 9090, 1337]

    found = []
    for port in agent_ports:
        for path in agent_paths:
            url = f"http://localhost:{port}{path}"
            try:
                req = urllib.request.Request(url, method="GET")
                with urllib.request.urlopen(req, timeout=1) as resp:
                    found.append({
                        "url": url,
                        "port": port,
                        "path": path,
                        "status": resp.status,
                    })
            except Exception:
                pass
    return found


# ---------------------------------------------------------------------------
# Identify: Map to EAB fleet registry
# ---------------------------------------------------------------------------


def identify_agents(processes: list[dict], endpoints: list[dict]) -> list[AgentFinding]:
    """Match discovered agents against known EAB fleet."""
    findings: list[AgentFinding] = []

    for agent_spec in EAB_FLEET:
        name = agent_spec["name"].lower()
        agent_finding = AgentFinding(
            agent_name=agent_spec["name"],
            category=agent_spec["type"],
            status="unknown",
            risk_profile=agent_spec["risk"],
        )

        # Find matching processes
        matches = []
        for p in processes:
            cmd_lower = (p["cmdline"] + p["comm"]).lower()
            if name in cmd_lower:
                matches.append(p)

        if matches:
            agent_finding.status = "governed"
            for m in matches:
                agent_finding.credentials_exposed.extend(m["exposed_creds"])

        # Check for witnessos-related processes
        if "witnessos" in name or "gateway" in name:
            agent_finding.witnessos_integrated = True
            agent_finding.status = "governed"

        # Add known risks
        if agent_spec["name"] in KNOWN_COMPLIANCE_RISKS:
            agent_finding.recommendations.extend(KNOWN_COMPLIANCE_RISKS[agent_spec["name"]])

        # Attach endpoints found
        agent_finding.endpoints_found = [e["url"] for e in endpoints]

        findings.append(agent_finding)

    # Detected but not in fleet → "unknown"
    named_names = {a["name"].lower() for a in EAB_FLEET}
    for p in processes:
        for kw in p["matched_keywords"]:
            if kw not in [n.lower() for n in named_names] and kw != "agent":
                findings.append(
                    AgentFinding(
                        agent_name=kw,
                        category="general-purpose",
                        status="ungoverned",
                        risk_profile="critical",
                        recommendations=["UNKNOWN AGENT — register in asset registry immediately"],
                    )
                )

    return findings


# ---------------------------------------------------------------------------
# Compliance grader
# ---------------------------------------------------------------------------


def grade_compliance(findings: list[AgentFinding]) -> dict:
    """Compute compliance grades per agent."""
    grades = {}

    for f in findings:
        score = 0
        max_score = 5

        if f.status == "governed":
            score += 1  # discovered + identified
        if not f.credentials_exposed:
            score += 1  # no exposed credentials
        if f.risk_profile != "high":
            score += 1  # moderate risk or below
        if "gateway" in f.agent_name.lower() or f.witnessos_integrated:
            score += 1  # witness-aware or integration-based
        if f.recommendations:
            score += 1  # has documented risk awareness

        # Derive grade
        if score == 5:
            grade = "A"
        elif score >= 4:
            grade = "B"
        elif score >= 3:
            grade = "C"
        elif score >= 2:
            grade = "D"
        else:
            grade = "F"

        grades[f.agent_name] = {
            "score": score,
            "max_score": max_score,
            "grade": grade,
            "status": f.status,
        }

    return grades


# ---------------------------------------------------------------------------
# Verifier integration
# ---------------------------------------------------------------------------


def verify_evidence_bundles(project_root: str) -> dict:
    """Look for witnessos-verifier bundles and E4-check them."""
    results = {}
    verifier_bin = os.path.join(project_root, "witnessos-verifier/.ny/bin/witness-verifier")
    if not os.path.isfile(verifier_bin):
        # try wild card in $PATH
        try:
            result = subprocess.run(["which", "witnessos-verifier"], capture_output=True, text=True)
            if result.returncode == 0:
                verifier_bin = result.stdout.strip()
            else:
                return {"error": "verifier binary not found"}
        except Exception:
            return {"error": "which command failed"}

    bundles_dir = Path(project_root) / "witnessos-audit/witnessos-verifier/fixtures"
    if bundles_dir.exists():
        for bundle_path in sorted(bundles_dir.iterdir()):
            if bundle_path.is_dir():
                try:
                    res = subprocess.run(
                        [verifier_bin, "verify", "--json", str(bundle_path)],
                        capture_output=True, text=True, timeout=30,
                    )
                    results[bundle_path.name] = json.loads(res.stdout)
                except Exception as e:
                    results[bundle_path.name] = {"error": str(e)}

    return results if results else {"info": "no fixture bundles found"}


# ---------------------------------------------------------------------------
# Report Generator
# ---------------------------------------------------------------------------


def generate_report(
    findings: list[AgentFinding],
    grades: dict,
    verifier_results: dict,
) -> ComplianceReport:
    report = ComplianceReport(
        timestamp=datetime.now(timezone.utc).isoformat(),
        target="EAB 9-Agent Fleet",
    )

    report.fleet = findings
    governed = sum(1 for f in findings if f.status == "governed")
    ungoverned = total_agents = len(EAB_FLEET) - governed
    e4_receipts = sum(
        1 for v in verifier_results.values()
        if isinstance(v, dict) and v.get("grade") == "E4"
    )

    report.summary = {
        "total_agents_scanned": total_agents,
        "governed": governed,
        "ungoverned": ungoverned,
        "e4_receipts": e4_receipts,
        "grade_distribution": {
            g: sum(1 for gr in grades.values() if gr["grade"] == g)
            for g in ["A", "B", "C", "D", "F"]
        },
        "verifier_bundles": list(verifier_results.keys()),
    }
    return report


def print_report(report: ComplianceReport) -> None:
    """Pretty-print the compliance matrix."""
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║     WITNESSOS COMPLIANCE SCANNER — EAB FLEET SCAN               ║")
    print(f"║     Timestamp: {report.timestamp}                        ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()

    print(f"📊 SUMMARY")
    print(f"  Total agents in fleet:           {report.summary['total_agents_scanned']}")
    print(f"  Governed (known + registered):   {report.summary['governed']}")
    print(f"  Ungoverned (unknown):            {report.summary['ungoverned']}")
    print(f"  E4 receipts verified:            {report.summary['e4_receipts']}")
    print()

    print(f"📋 COMPLIANCE MATRIX")
    print(f"  {'Agent':<22} {'Status':<12} {'Risk':<10} {'Grade':<6} {'Credentials':<12}")
    print(f"  {'-'*22} {'-'*12} {'-'*10} {'-'*6} {'-'*12}")

    for f in report.fleet:
        grade = report.summary.get("grade", "—")
        creds = "clean" if not f.credentials_exposed else f"{len(f.credentials_exposed)} exposed"
        print(f"  {f.agent_name:<22} {f.status:<12} {f.risk_profile:<10} {grade:<6} {creds:<12}")

    print()

    # keys
    high_risk = [f for f in report.fleet if f.risk_profile == "high"]
    if high_risk:
        print("🔴 HIGH-RISK AGENTS")
        for f in high_risk:
            print(f"  • {f.agent_name}: {f.category} / {f.status}")
            for r in f.recommendations:
                print(f"    - {r}")
        print()

    exposed = [f for f in report.fleet if f.credentials_exposed]
    if exposed:
        print("🔑 AGENTS WITH EXPOSED CREDENTIALS")
        for f in exposed:
            print(f"  • {f.agent_name}:")
            for cred in f.credentials_exposed:
                print(f"    - {cred}")
        print()

    ungoverned = [f for f in report.fleet if f.status != "governed"]
    if ungoverned:
        print("⚠️  UNGOVERNED AGENTS — Requires registration")
        for f in ungoverned:
            print(f"  • {f.agent_name} — {f.risk_profile} risk")
            print(f"    Action: Register via Agent Asset Registry + Wire to WitnessOS")
        print()

    print("🔍 RECOMMENDATIONS")
    print("  1. Make all high-risk agents E4-capable (integrate with verifier)")
    print("  2. Zero-credential-exposure target for all 9 agents")
    print("  3. Run this scanner as cron job — hourly for production fleet")
    print("  4. Register unknown agents in asset registry before Aug 2 enforcement")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


async def main():
    print("🔍 WitnessOS Compliance Scanner — Starting EAB Fleet Scan...")
    print()

    # Step I: Scan
    print("📡 [1/5] Scanning process tree...")
    processes = scan_process_tree()
    print(f"   Found {len(processes)} agent-matching processes")

    print("🌐 [2/5] Scanning HTTP endpoints...")
    endpoints = scan_http_endpoints()
    print(f"   Found {len(endpoints)} live AI agent endpoints")

    # Step 2: Identify
    print("🆔 [3/5] Mapping to EAB fleet...")
    findings = identify_agents(processes, endpoints)

    # Step 3: Grade
    print("📊 [4/5] Computing compliance grades...")
    grades = grade_compliance(findings)

    # Step 4: Verifier
    print("📜 [5/5] Checking E4 evidence bundles...")
    here = Path.home() / ".hermes/profiles/porgie/workspace"
    verifier_results = verify_evidence_bundles(str(here))
    verified_count = sum(
        1 for v in verifier_results.values()
        if isinstance(v, dict) and v.get("grade") == "E4"
    )
    print(f"   {verified_count} E4-vertex receipts verified")

    # Generate report
    report = generate_report(findings, grades, verifier_results)
    print_report(report)

    # Save JSON
    output_path = Path.home() / ".hermes/profiles/porgie/workspace/reports"
    output_path.mkdir(parents=True, exist_ok=True)
    json_path = output_path / "eab-compliance-scan-2026-07-28.json"

    report_dict = {
        "timestamp": report.timestamp,
        "target": report.target,
        "summary": report.summary,
        "fleet": [
            {
                "name": f.agent_name,
                "status": f.status,
                "risk_profile": f.risk_profile,
                "credentials_exposed": len(f.credentials_exposed),
                "endpoints_found": len(f.endpoints_found),
                "recommendations": f.recommendations,
            }
            for f in report.fleet
        ],
    }

    with open(json_path, "w") as f:
        json.dump(report_dict, f, indent=2, default=str)

    print(f"📄 Report saved: {json_path}")
    print()
    print("✅ Scan complete. Compliance ready for Eddie review.")


if __name__ == "__main__":
    asyncio.run(main())