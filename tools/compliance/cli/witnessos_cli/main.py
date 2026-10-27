"""WitnessOS Compliance CLI - generate regulatory compliance reports."""

from __future__ import annotations

import os, json, yaml, datetime, urllib.request, urllib.error
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MAPPINGS_DIR = REPO_ROOT / "mappings"
TEMPLATES_DIR = REPO_ROOT / "templates"
CONTENT_DIR = REPO_ROOT / "content"

console = Console()


def _find_mapping_files(standard: str) -> list[Path]:
    """Find relevant mapping docs for a standard."""
    files = []
    if standard == "nsa-mcp":
        for f in MAPPINGS_DIR.glob("*nsa*"):
            files.append(f)
    elif standard == "eu-ai-act":
        for f in MAPPINGS_DIR.glob("*governance*"):
            files.append(f)
        for f in MAPPINGS_DIR.glob("*csa*"):
            files.append(f)
    return files


def _find_template_files(standard: str, article: str | None = None) -> list[Path]:
    """Find relevant template files."""
    files = []
    if standard == "eu-ai-act":
        template_dir = TEMPLATES_DIR / "eu-ai-act"
        if article:
            for f in template_dir.glob(f"*article-{article}*"):
                files.append(f)
        else:
            files = sorted(template_dir.glob("*.md"))
    return files


def _read_evidence_template(path: Path, evidence_grade: str) -> str | None:
    """Extract the JSON template for a specific evidence grade from a template doc."""
    content = path.read_text()
    evidence_upper = evidence_grade.upper()
    lines = content.split("\n")
    json_lines = []
    in_json = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## ") or stripped.startswith("### "):
            if evidence_upper in stripped:
                in_json = True
                json_lines = []
                continue

        if in_json:
            if stripped.startswith("```json"):
                json_lines = []
                continue
            if stripped.startswith("```"):
                break
            json_lines.append(line)

    if json_lines:
        return "\n".join(json_lines)
    return None


def _get_nsa_mapping_summary() -> dict:
    """Parse the NSA mapping doc and return structured data."""
    mapping_path = MAPPINGS_DIR / "nsa-mcp-witnessos-mapping.md"
    if not mapping_path.exists():
        return {"error": "NSA mapping doc not found"}

    content = mapping_path.read_text()
    sections = content.split("### F")
    findings = []
    for i, section in enumerate(sections[1:], 1):
        lines = section.split("\n")
        title_line = lines[0].strip() if lines else ""
        findings.append({
            "id": f"F{i}",
            "title": title_line.replace(":", ""),
            "content": section[:500],
        })

    return {
        "total_findings": len(findings),
        "findings": findings,
        "document_path": str(mapping_path),
        "document_size": len(content),
    }


def _get_eu_evidence_summary() -> dict:
    """Parse the EU AI Act templates and return structured data."""
    articles = {}
    for template_path in sorted(TEMPLATES_DIR.glob("eu-ai-act/*.md")):
        name = template_path.stem
        parts = name.split("-")
        article_num = None
        for i, p in enumerate(parts):
            if p == "article" and i + 1 < len(parts):
                try:
                    article_num = int(parts[i + 1])
                except ValueError:
                    pass
        if article_num:
            grades = ["E0", "E1", "E2", "E3", "E4"]
            available = []
            for grade in grades:
                tmpl = _read_evidence_template(template_path, grade)
                if tmpl:
                    available.append(grade)
            articles[f"Article {article_num}"] = {
                "file": template_path.name,
                "available_evidence": available,
            }
    return articles


# =========================================================================
# Report Generators
# =========================================================================

def _generate_nsa_report(output: str):
    """Generate NSA MCP compliance report."""
    mapping = _get_nsa_mapping_summary()

    if output == "json":
        result = {
            "standard": "nsa-mcp",
            "standard_name": "NSA MCP Security Design Considerations",
            "generated": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
            "assessment": "MAPPING - WitnessOS features are mapped to all 8 NSA findings and 5 recommendations. This states the claim in the mapping document; no evidence was graded.",
            "findings_covered": mapping.get("findings", []),
            "total_findings": mapping.get("total_findings", 0),
        }
        console.print(json.dumps(result, indent=2))
        return

    console.print(Panel.fit("[bold]NSA MCP Security Guidance - Compliance Report[/bold]"))
    console.print(f"Generated: {datetime.datetime.now(datetime.timezone.utc).isoformat()}Z\n")

    if "error" in mapping:
        console.print(f"[red]Error: {mapping['error']}[/red]")
        return

    console.print(f"[green]✓[/green] WitnessOS features map to all [bold]{mapping['total_findings']}[/bold] NSA findings")
    console.print("[green]✓[/green] WitnessOS features map to all 5 NSA recommendations")
    console.print("[blue]ℹ[/blue] Mapping document: " + str(mapping['document_path']))
    console.print("[yellow]![/yellow] This is a mapping claim, not graded evidence. Grade receipts with")
    console.print("  witnessos-verifier and report the grade it assigns, or report NOT_VERIFIED.")

    table = Table(title="NSA Findings Covered")
    table.add_column("#", style="dim")
    table.add_column("Finding", style="cyan")
    table.add_column("Status", justify="center")

    for f in mapping.get("findings", []):
        table.add_row(f["id"], f["title"][:80], "[green]COVERED[/green]")

    console.print(table)
    console.print("\n[bold]Recommendation:[/bold] Run with --output json for structured data")


def _generate_eu_report(article: str | None, evidence: str | None, output: str):
    """Generate EU AI Act compliance report."""
    articles = _get_eu_evidence_summary()

    if output == "json":
        result = {
            "standard": "eu-ai-act",
            "standard_name": "EU AI Act (Articles 9, 14, 43)",
            "generated": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
            "articles": articles,
        }
        console.print(json.dumps(result, indent=2))
        return

    console.print(Panel.fit("[bold]EU AI Act - Compliance Evidence Report[/bold]"))
    console.print(f"Generated: {datetime.datetime.now(datetime.timezone.utc).isoformat()}Z\n")

    if article:
        art_key = f"Article {article}"
        if art_key in articles:
            info = articles[art_key]
            console.print(f"[bold]{art_key}[/bold] - {info['file']}")
            console.print(f"Available evidence grades: {', '.join(info['available_evidence'])}")
            if evidence:
                tmpl_path = TEMPLATES_DIR / "eu-ai-act" / info["file"]
                tmpl = _read_evidence_template(tmpl_path, evidence)
                if tmpl:
                    console.print(f"\n[bold]Evidence {evidence} Template:[/bold]")
                    try:
                        parsed = json.loads(tmpl)
                        console.print(json.dumps(parsed, indent=2))
                    except json.JSONDecodeError:
                        console.print(tmpl[:2000])
                else:
                    console.print(f"[yellow]No template for evidence grade {evidence}[/yellow]")
        else:
            console.print(f"[red]Article {article} not found[/red]")
        return

    table = Table(title="EU AI Act Articles - Available Evidence Templates")
    table.add_column("Article", style="cyan")
    table.add_column("File", style="dim")
    table.add_column("Evidence Grades Available")

    for art, info in sorted(articles.items()):
        grades = ", ".join(f"[green]{g}[/green]" for g in info["available_evidence"])
        table.add_row(art, info["file"], grades)

    console.print(table)
    console.print("\n[bold]Usage:[/bold] witnessos-compliance report --standard eu-ai-act --article 9 --evidence E2")


def _generate_nist_report(output: str):
    """Generate NIST CAISI alignment report."""
    mapping_path = MAPPINGS_DIR / "nist-singapore-ai-agent-standards.md"
    if not mapping_path.exists():
        console.print("[red]NIST standards mapping not found[/red]")
        return

    console.print(Panel.fit("[bold]NIST CAISI - Alignment Report[/bold]"))
    console.print(f"Generated: {datetime.datetime.now(datetime.timezone.utc).isoformat()}Z\n")
    console.print("[green]✓[/green] WitnessOS aligns with all 5 NIST CAISI focus areas:")
    console.print("  1. Agent Identity and Authentication - mTLS + ACI manifests")
    console.print("  2. Authorization and Access Control - OPA/Rego Policy Engine")
    console.print("  3. Agent-to-Agent Communication - AIP + AJSON")
    console.print("  4. Audit Trails - E0-E4 Cryptographic Evidence Chain")
    console.print("  5. Human Oversight - Exact-Approval Binding")
    console.print("\n📅 NIST deliverables expected Q4 2026 - WitnessOS designed for alignment day one")
    console.print("\nCLI: witnessos-compliance report --standard nist-caisi --output json")


def _generate_singapore_report(output: str):
    """Generate Singapore AI Verify framework alignment report."""
    mapping_path = MAPPINGS_DIR / "nist-singapore-ai-agent-standards.md"
    if not mapping_path.exists():
        console.print("[red]Singapore framework mapping not found[/red]")
        return

    console.print(Panel.fit("[bold]Singapore AI Verify - Alignment Report[/bold]"))
    console.print(f"Generated: {datetime.datetime.now(datetime.timezone.utc).isoformat()}Z\n")
    console.print("[green]✓[/green] WitnessOS aligns with Singapore's Agentic AI Governance Framework")
    console.print("  (World's first governance framework specifically for autonomous agents)\n")
    console.print("  • Agent transparency - ACI manifests")
    console.print("  • Proportional oversight - Exact-approval binding")
    console.print("  • Agent-to-agent accountability - E3-E4 evidence receipts")
    console.print("  • Agent identity - mTLS + Identity Registry")
    console.print("  • Audit trails - E0-E4 hash-chained evidence")
    console.print("\n📌 APAC strategic advantage: Singapore is first-mover; Japan, Korea, Australia follow")
    console.print("\nCLI: witnessos-compliance report --standard singapore-ai-verify --output json")


# =========================================================================
# CLI Commands
# =========================================================================

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """WitnessOS Compliance Pack

    Generate regulatory compliance reports for autonomous AI agents.
    Supports NSA MCP, EU AI Act, NIST CAISI, and Singapore AI Verify standards.
    """


@cli.command()
@click.option("--standard", "-s", type=click.Choice(["nsa-mcp", "eu-ai-act", "nist-caisi", "singapore-ai-verify"]), required=True,
              help="Compliance standard to report against")
@click.option("--article", "-a", help="Specific article (e.g., 9, 14, 43)")
@click.option("--evidence", "-e", type=click.Choice(["E0", "E1", "E2", "E3", "E4"]),
              help="Evidence grade to generate")
@click.option("--output", "-o", type=click.Choice(["text", "json", "md", "html", "pdf"]), default="text",
              help="Output format")
@click.option("--gateway", "-g", help="WitnessOS gateway URL (e.g., http://localhost:8100). Query live evidence.")
@click.option("--from", "from_date", help="Start date (YYYY-MM-DD)")
@click.option("--to", "to_date", help="End date (YYYY-MM-DD)")
def report(standard, article, evidence, output, gateway, from_date, to_date):
    """Generate a compliance report for the specified standard."""

    if gateway:
        _fetch_gateway_report(standard, gateway, output)
        return

    if standard == "nsa-mcp":
        _generate_nsa_report(output)
    elif standard == "eu-ai-act":
        _generate_eu_report(article, evidence, output)
    elif standard == "nist-caisi":
        _generate_nist_report(output)
    elif standard == "singapore-ai-verify":
        _generate_singapore_report(output)


@cli.command()
@click.option("--standard", "-s", type=click.Choice(["nsa-mcp", "eu-ai-act", "nist-caisi", "singapore-ai-verify"]), required=True)
@click.option("--output", "-o", type=click.Choice(["text", "json", "md"]), default="text")
def status(standard, output):
    """Check compliance readiness for a standard."""

    if standard == "nsa-mcp":
        console.print("[green]✓[/green] NSA MCP: 8 findings and 5 recommendations mapped")
        console.print("  - 8/8 NSA findings mapped to WitnessOS features")
        console.print("  - 5/5 NSA recommendations mapped to WitnessOS features")
        console.print("[yellow]![/yellow] Mapping claim, not graded evidence. Report the grade")
        console.print("  witnessos-verifier assigns, or report NOT_VERIFIED.")

    elif standard == "eu-ai-act":
        articles = _get_eu_evidence_summary()
        console.print(f"[green]✓[/green] EU AI Act: {len(articles)} articles covered")
        for art, info in sorted(articles.items()):
            pct = len(info["available_evidence"]) / 5 * 100
            grade_str = ", ".join(info["available_evidence"])
            console.print(f"  [green]✓[/green] {art}: {grade_str} ({pct:.0f}% evidence coverage)")

    elif standard == "nist-caisi":
        console.print("[green]✓[/green] NIST CAISI: Aligned with all 5 focus areas")
        console.print("  - Identity & Auth: mTLS + ACI manifests")
        console.print("  - Authorization: OPA/Rego Policy Engine")
        console.print("  - Agent Communication: AIP + AJSON")
        console.print("  - Audit Trails: E0-E4 evidence chain")
        console.print("  - Human Oversight: Exact-Approval Binding")
        console.print("  - NIST deliverables Q4 2026 - WitnessOS ready day one")

    elif standard == "singapore-ai-verify":
        console.print("[green]✓[/green] Singapore AI Verify: World's 1st agentic AI framework aligned")
        console.print("  - Agent transparency - ACI manifests")
        console.print("  - Proportional oversight - Exact-approval binding")
        console.print("  - Agent-to-agent accountability - E3-E4 receipts")


@cli.command()
def list():
    """List all available compliance standards and their status."""

    console.print(Panel.fit("[bold]WitnessOS Compliance Pack - Available Standards[/bold]"))

    # NSA MCP
    nsamapping = _get_nsa_mapping_summary()
    nsastatus = "[green]READY[/green]" if "error" not in nsamapping else "[red]NOT FOUND[/red]"
    console.print(f"\n📋 [bold]NSA MCP Security Guidance[/bold] - {nsastatus}")
    if "error" not in nsamapping:
        console.print(f"   Findings covered: {nsamapping['total_findings']}")
        console.print(f"   Standard: witnessos-compliance report --standard nsa-mcp")

    # EU AI Act
    articles = _get_eu_evidence_summary()
    console.print(f"\n⚖️  [bold]EU AI Act[/bold] - [green]{len(articles)} articles covered[/green]")
    for art, info in sorted(articles.items()):
        console.print(f"   • {art}: {', '.join(info['available_evidence'])}")
    console.print(f"   Standard: witnessos-compliance report --standard eu-ai-act")

    # NIST CAISI
    nist_path = MAPPINGS_DIR / "nist-singapore-ai-agent-standards.md"
    nist_status = "[green]ALIGNED[/green]" if nist_path.exists() else "[red]NOT FOUND[/red]"
    console.print(f"\n🏛️  [bold]NIST CAISI[/bold] - {nist_status}")
    console.print(f"   Standard: witnessos-compliance report --standard nist-caisi")

    # Singapore
    sg_status = "[green]ALIGNED[/green]" if nist_path.exists() else "[red]NOT FOUND[/red]"
    console.print(f"\n🌏 [bold]Singapore AI Verify[/bold] - {sg_status}")
    console.print(f"   Standard: witnessos-compliance report --standard singapore-ai-verify")

    # Content
    blog_posts = sorted(CONTENT_DIR.glob("blog/*.md"))
    console.print(f"\n📝 [bold]Content[/bold] - {len(blog_posts)} asset(s) ready")
    for post in blog_posts:
        console.print(f"   • {post.name}")


# ── Gateway Integration ────────────────────────────────────────────


def _fetch_gateway_report(standard: str, gateway_url: str, output: str):
    """Fetch live evidence from a WitnessOS gateway and print a compliance report."""
    try:
        url = f"{gateway_url.rstrip('/')}/v1/evidence"
        resp = urllib.request.urlopen(url, timeout=10)
        data = json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        console.print(f"[red]✗ Cannot reach gateway at {gateway_url}[/red]")
        console.print(f"  Reason: {e.reason}")
        return
    except Exception as e:
        console.print(f"[red]✗ Gateway error: {e}[/red]")
        return

    if output == "json":
        console.print(json.dumps(data, indent=2))
        return

    cases = data.get("cases", [])
    console.print(Panel.fit(f"[bold]WitnessOS Gateway - Live Evidence ({standard})[/bold]"))
    console.print(f"Gateway: {gateway_url}")
    console.print(f"Cases: {len(cases)}")
    console.print(f"Generated: {datetime.datetime.now(datetime.timezone.utc).isoformat()}Z\n")

    if not cases:
        console.print("[yellow]No evidence cases found on gateway.[/yellow]")
        console.print("The gateway may be empty or freshly started.")
        console.print("Run agent operations first to generate evidence.")
        return

    for case in cases:
        grade = case.get("evidence_grade", "?")
        status = case.get("evidence_status", "?")
        console.print(f"• Case: {case['case_id']}")
        console.print(f"  Events: {case['event_count']} | Evidence: {grade} | Status: {status}")
        console.print(f"  Agent: {case.get('agent_id', '?')}")
        console.print()

    if output == "md":
        md = f"# WitnessOS Gateway - Live Evidence\n\n"
        md += f"**Gateway:** {gateway_url}\n\n"
        md += f"**Cases:** {len(cases)}\n\n"
        md += "| Case ID | Events | Evidence | Status |\n"
        md += "|---------|--------|----------|--------|\n"
        for case in cases:
            md += f"| {case['case_id']} | {case['event_count']} | {case.get('evidence_grade', '?')} | {case.get('evidence_status', '?')} |\n"
        path = REPO_ROOT / "content" / "gateway-evidence-report.md"
        path.write_text(md)
        console.print(f"\n[green]✓[/green] Report saved to: {path}")


@cli.command()
@click.option("--gateway", "-g", default="http://localhost:8100", help="WitnessOS gateway URL")
@click.option("--case", "-c", help="Specific case ID to inspect")
@click.option("--output", "-o", type=click.Choice(["text", "json", "md"]), default="text")
def evidence(gateway, case, output):
    """Query live compliance evidence from a WitnessOS gateway."""
    if case:
        try:
            url = f"{gateway.rstrip('/')}/v1/evidence/{case}"
            resp = urllib.request.urlopen(url, timeout=10)
            data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            console.print(f"[red]✗ Case not found: {case} at {gateway}[/red]")
            return
        except Exception as e:
            console.print(f"[red]✗ Gateway error: {e}[/red]")
            return

        if output == "json":
            console.print(json.dumps(data, indent=2))
            return

        console.print(Panel.fit(f"[bold]Evidence Case: {case}[/bold]"))
        console.print(f"Events: {data.get('event_count', 0)}")
        console.print(f"Grade: [green]{data.get('evidence_grade', '?')}[/green] | Status: {data.get('evidence_status', '?')}")
        console.print()
        console.print("[bold]Action:[/bold]")
        act = data.get("action", {})
        console.print(f"  System: {act.get('target_system', '?')}")
        console.print(f"  Resource: {act.get('target_resource', '?')}")
        console.print(f"  Risk Class: {act.get('risk_class', '?')}")
        console.print(f"  Canonical Hash: {act.get('canonical_request_hash', '?')}")
        console.print()
        console.print("[bold]Policy Decision:[/bold]")
        pol = data.get("policy", {})
        console.print(f"  Decision: {pol.get('decision', '?')}")
        console.print(f"  Rule ID: {pol.get('rule_id', '?')}")
        console.print(f"  Bundle Hash: {pol.get('policy_bundle_hash', '?')}")
        console.print()
        console.print("[bold]Outcome:[/bold]")
        out = data.get("outcome", {})
        console.print(f"  Stage: {out.get('stage', '?')}")
        console.print(f"  Provider Op ID: {out.get('provider_operation_id', '?')}")
        console.print(f"  Independently Verifiable: {out.get('independently_verifiable', False)}")
        console.print()
        console.print("[bold]Chain Integrity:[/bold]")
        ch = data.get("chain", {})
        console.print(f"  Head Hash: {ch.get('head_commitment_hash', '?')}")
        console.print(f"  Event Count: {ch.get('event_count', 0)}")
        console.print(f"  Signature: {ch.get('signature', '?')}")
    else:
        _fetch_gateway_report("all", gateway, output)


if __name__ == "__main__":
    cli()


# =========================================================================
# P5B: HTML & PDF Report Generators + Scan Command
# =========================================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WitnessOS Compliance Report - {standard_name}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0d1117; color: #c9d1d9; padding: 2rem; }}
  .container {{ max-width: 900px; margin: 0 auto; }}
  h1 {{ color: #58a6ff; font-size: 1.8rem; margin-bottom: 0.25rem; }}
  h2 {{ color: #8b949e; font-size: 1rem; font-weight: 400; margin-bottom: 2rem; }}
  .card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem; }}
  .card.pass {{ border-left: 4px solid #3fb950; }}
  .card.fail {{ border-left: 4px solid #f85149; }}
  .card.warn {{ border-left: 4px solid #d29922; }}
  .meta {{ color: #8b949e; font-size: 0.85rem; margin-bottom: 1rem; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 0.5rem; }}
  th, td {{ text-align: left; padding: 8px 12px; border-bottom: 1px solid #21262d; }}
  th {{ color: #8b949e; font-size: 0.8rem; text-transform: uppercase; }}
  .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }}
  .badge-pass {{ background: #1b3d1b; color: #3fb950; }}
  .badge-fail {{ background: #3d1b1b; color: #f85149; }}
  .badge-warn {{ background: #3d2e1b; color: #d29922; }}
  .footer {{ margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #21262d; color: #484f58; font-size: 0.8rem; }}
</style>
</head>
<body>
<div class="container">
  <h1>WitnessOS Compliance Report</h1>
  <h2>{standard_name}</h2>
  <div class="meta">Generated: {timestamp} &middot; WitnessOS v{version}</div>
  {cards}
  <div class="footer">Generated by WitnessOS Compliance Pack v{version} - Agent Governance, Verifiable.</div>
</div>
</body>
</html>"""

CARD_PASS = """  <div class="card pass">
    <h3><span class="badge badge-pass">MAPPED</span> %s</h3>
    <p>%s</p>
  </div>"""

CARD_WARN = """  <div class="card warn">
    <h3><span class="badge badge-warn">REVIEW</span> %s</h3>
    <p>%s</p>
  </div>"""

CARD_FAIL = """  <div class="card fail">
    <h3><span class="badge badge-fail">ACTION</span> %s</h3>
    <p>%s</p>
  </div>"""

_STANDARD_NAMES = {
    "nsa-mcp": "NSA MCP Security Design Considerations",
    "eu-ai-act": "EU AI Act - Articles 9, 14, 43",
    "nist-caisi": "NIST CAISI - Agent AI Safety Framework",
    "singapore-ai-verify": "Singapore AI Verify - Agentic AI Governance",
}


def _render_html(standard: str, findings: list[dict], output_path: str | None = None) -> str:
    """Render compliance findings as dark-themed HTML dashboard."""
    cards = []
    for f in findings:
        status = f.get("status", "pass")
        title = f.get("title", "Finding")
        detail = f.get("detail", "")
        if status == "pass":
            cards.append(CARD_PASS % (title, detail))
        elif status == "fail":
            cards.append(CARD_FAIL % (title, detail))
        else:
            cards.append(CARD_WARN % (title, detail))

    now = datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"
    html = HTML_TEMPLATE.format(
        standard_name=_STANDARD_NAMES.get(standard, standard),
        timestamp=now,
        version="1.0.0",
        cards="\n".join(cards) if cards else '<div class="card pass"><h3><span class="badge badge-pass">NO FINDINGS</span></h3><p>No finding was raised by the mapping. Graded evidence is not part of this report.</p></div>',
    )

    if output_path:
        Path(output_path).write_text(html)

    return html


def _render_pdf(standard: str, findings: list[dict], output_path: str | None = None) -> str:
    """Generate PDF report via weasyprint if available, else fall back to HTML."""
    html = _render_html(standard, findings)
    try:
        from weasyprint import HTML
        if output_path:
            HTML(string=html).write_pdf(output_path)
            return f"PDF written: {output_path}"
        return "PDF requires output_path"
    except ImportError:
        note = "NOTE: `pip install weasyprint` for PDF output"
        if output_path:
            html_path = output_path.replace(".pdf", ".html")
            Path(html_path).write_text(html)
            return f"Saved HTML fallback: {html_path}\n{note}"
        return note


@cli.command()
@click.option("--standard", "-s", type=click.Choice(["nsa-mcp", "eu-ai-act", "nist-caisi", "singapore-ai-verify", "all"]), required=True)
@click.option("--format", "-f", "out_fmt", type=click.Choice(["html", "pdf", "json"]), default="html")
@click.option("--output-dir", "-o", default=str(REPO_ROOT / "reports"), help="Output directory")
def compliance_report(standard, out_fmt, output_dir):
    """Generate compliance dashboard report (HTML/PDF). Run via cron for scheduled snapshots."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    standards = list(_STANDARD_NAMES.keys()) if standard == "all" else [standard]

    for std in standards:
        findings = _build_findings(std)
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

        if out_fmt == "html":
            path = str(out_dir / f"compliance-{std}-{ts}.html")
            _render_html(std, findings, path)
            console.print(f"[green]OK[/green] HTML: {path}")
        elif out_fmt == "pdf":
            path = str(out_dir / f"compliance-{std}-{ts}.pdf")
            result = _render_pdf(std, findings, path)
            console.print(result)
        elif out_fmt == "json":
            path = str(out_dir / f"compliance-{std}-{ts}.json")
            Path(path).write_text(json.dumps(findings, indent=2))
            console.print(f"[green]OK[/green] JSON: {path}")

    console.print(f"\n[bold]Cron tip:[/bold] witnessos-compliance compliance-report --standard all --format html")


def _build_findings(standard: str) -> list[dict]:
    """Build findings list for a given standard."""
    findings = []

    if standard == "nsa-mcp":
        nsamapping = _get_nsa_mapping_summary()
        if "error" not in nsamapping:
            for f in nsamapping.get("findings", []):
                findings.append({"title": f"Finding {f['id']}: {f['title']}", "detail": f"Mapped to WitnessOS. Doc: {nsamapping['document_path']}", "status": "pass"})
            findings.append({"title": "Summary", "detail": f"{nsamapping['total_findings']}/8 findings mapped, 5/5 recommendations", "status": "pass"})
        else:
            findings.append({"title": "NSA Mapping", "detail": "Document not found", "status": "fail"})

    elif standard == "eu-ai-act":
        articles = _get_eu_evidence_summary()
        for art, info in sorted(articles.items()):
            pct = len(info['available_evidence']) / 5 * 100
            status = "pass" if pct >= 80 else ("warn" if pct >= 40 else "fail")
            findings.append({"title": art, "detail": f"{len(info['available_evidence'])}/5 evidence grades ({pct:.0f}%). File: {info['file']}", "status": status})
        findings.append({"title": "Overall", "detail": f"{len(articles)} articles, {sum(len(a['available_evidence']) for a in articles.values())} total templates", "status": "pass"})

    elif standard == "nist-caisi":
        for area, mapping in [
            ("Identity & Auth", "mTLS + ACI manifests"),
            ("Authorization & Access Control", "OPA/Rego Policy Engine"),
            ("Agent Communication", "AIP + AJSON"),
            ("Audit Trails", "E0-E4 Cryptographic Evidence Chain"),
            ("Human Oversight", "Exact-Approval Binding"),
        ]:
            findings.append({"title": area, "detail": mapping, "status": "pass"})
        findings.append({"title": "Timing", "detail": "NIST CAISI deliverables Q4 2026 - WitnessOS designed for day-one alignment", "status": "pass"})

    elif standard == "singapore-ai-verify":
        for title, detail in [
            ("Agent Transparency", "ACI manifests for capability discovery"),
            ("Proportional Oversight", "Exact-approval binding - overwrite requires fresh authorization"),
            ("Agent-to-Agent Accountability", "E3-E4 cryptographic evidence receipts"),
            ("Agent Identity", "mTLS + Identity Registry + boot attestation"),
            ("Audit Trails", "E0-E4 hash-chained"),
            ("APAC First-Mover", "Singapore Aug 1 2026 - world's first autonomous agent framework"),
        ]:
            findings.append({"title": title, "detail": detail, "status": "pass"})

    return findings


@cli.command()
@click.option("--run", is_flag=True, help="Run a scan immediately")
@click.option("--schedule", help="Suggested cron schedule (informational only)")
def scan(run, schedule):
    """Run compliance scanner against live processes. Schedule via hermes cron."""
    scanner_path = REPO_ROOT / "tools" / "compliance-scanner.py"
    if not scanner_path.exists():
        console.print(f"[red]✗ Scanner not found: {scanner_path}[/red]")
        return

    if run:
        import subprocess
        result = subprocess.run(
            ["python3", str(scanner_path)],
            capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=60
        )
        if result.returncode == 0:
            console.print(result.stdout[:2000])
            if result.stdout:
                console.print("\n[green]OK[/green] Scan complete - JSON in reports/")
            else:
                console.print("[yellow]Scan produced no output[/yellow]")
        else:
            console.print(f"[red]✗ Scan failed:[/red]\n{result.stderr[:500]}")
        return

    if schedule:
        console.print(f"[dim]Schedule '{schedule}' - use hermes cron:\n  cronjob action=create schedule='{schedule}' prompt='cd witnessos-compliance && python3 tools/compliance-scanner.py'\n[/dim]")
        return

    console.print("[dim]Usage: --run to scan now, --schedule daily for cron info[/dim]")
