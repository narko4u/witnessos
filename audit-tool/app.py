"""
WitnessOS Rogue Agent Audit - Free One-Page Risk Assessment (A-002)

Flask app: company intake form → PDF audit report generation.
Regulatory timing: EU AI Act enforcement Aug 2, ByteDance/Alibaba Jul 15.
"""
import io
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from weasyprint import HTML


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.environ.get(
        "FLASK_SECRET_KEY",
        "witnessos-audit-dev-key-change-in-production"
    )

    # ── Routes ──────────────────────────────────────────────────────────

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html", form_data={},
                               china_deadline=_days_until("2026-07-15"),
                               eu_deadline=_days_until("2026-08-02"))

    @app.route("/generate", methods=["POST"])
    def generate():
        # ── Sanitise inputs ────────────────────────────────────────────
        company = _sanitise(request.form.get("company", ""))
        industry = _sanitise(request.form.get("industry", ""))
        email = request.form.get("email", "").strip().lower()
        employee_count = _sanitise(request.form.get("employee_count", ""))
        agent_count_raw = request.form.get("agent_count", "").strip()
        governance_raw = request.form.get("governance", "").strip()
        compliance_needs = _sanitise(request.form.get("compliance_needs", ""))
        concerns = _sanitise(request.form.get("concerns", ""))

        # ── Validation ─────────────────────────────────────────────────
        errors = []

        if len(company) < 2:
            errors.append("Company name is required.")

        if not _validate_email(email):
            errors.append("A valid email address is required.")

        # Parse agent count
        agent_count: int | None = None
        risk_level = "unknown"
        if agent_count_raw:
            try:
                agent_count = int(agent_count_raw)
                if agent_count < 0:
                    errors.append("Agent count cannot be negative.")
                elif agent_count > 100000:
                    errors.append("Agent count seems unreasonably high (max 100,000).")
                else:
                    risk_level = _assess_risk(agent_count, governance_raw)
            except ValueError:
                errors.append("Agent count must be a whole number.")

        if errors:
            for err in errors:
                flash(err, "error")
            return render_template("index.html", form_data=request.form)

        # ── Generate report ─────────────────────────────────────────────
        report_data = {
            "company": company or "Not specified",
            "industry": industry or "Not specified",
            "email": email,
            "employee_count": employee_count or "Not specified",
            "agent_count": str(agent_count) if agent_count is not None else "Not specified",
            "governance": _governance_level_label(governance_raw),
            "compliance_needs": compliance_needs or "Not specified",
            "concerns": concerns or "Not specified",
            "risk_level": risk_level,
            "generated_at": datetime.now(timezone.utc).strftime("%d %B %Y"),
            "eu_ai_act_countdown": _days_until("2026-08-02"),
            "china_deadline_countdown": _days_until("2026-07-15"),
        }

        # Render HTML report
        html_str = render_template("report.html", **report_data)

        # Convert to PDF
        try:
            pdf_bytes = HTML(string=html_str).write_pdf()
        except Exception as e:
            flash(f"Report generation failed: {str(e)}", "error")
            return render_template("index.html", form_data=request.form)

        # Save to file
        output_dir = Path(__file__).parent / "reports"
        output_dir.mkdir(parents=True, exist_ok=True)
        safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", company)[:40]
        filename = f"witnessos-audit_{safe_name}_{datetime.now(timezone.utc).strftime('%Y%m%d')}.pdf"
        pdf_path = output_dir / filename
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)

        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename,
        )

    return app


# ── Helpers ──────────────────────────────────────────────────────────────────

def _sanitise(text: str) -> str:
    """Strip dangerous characters."""
    if not text:
        return ""
    return re.sub(r"[<>&\"']", "", text.strip())


def _validate_email(email: str) -> bool:
    if not email or "@" not in email:
        return False
    pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email.strip()))


def _assess_risk(agent_count: int, governance_raw: str) -> str:
    """Assess risk based on agent count and governance maturity."""
    has_governance = bool(governance_raw.strip()) if governance_raw else False

    if agent_count == 0:
        return "none"
    elif agent_count < 5:
        return "low" if has_governance else "moderate"
    elif agent_count < 50:
        return "moderate" if has_governance else "high"
    elif agent_count < 500:
        return "high" if has_governance else "critical"
    else:
        return "critical"


def _governance_level_label(raw: str) -> str:
    """Map raw governance text to a label."""
    if not raw or not raw.strip():
        return "None / Not specified"
    raw_lower = raw.strip().lower()
    if "formal" in raw_lower or "dedicated" in raw_lower or "policy" in raw_lower:
        return "Formal governance program"
    elif "basic" in raw_lower or "manual" in raw_lower or "spreadsheet" in raw_lower:
        return "Basic / Manual tracking"
    elif "planning" in raw_lower or "considering" in raw_lower:
        return "Planning stage"
    else:
        return raw.strip()[:100]


def _days_until(target: str) -> int:
    """Days until a target date (ISO format)."""
    target_dt = datetime.strptime(target, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    delta = (target_dt - now).days
    return max(0, delta)


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5001))
    print(f"🚀 WitnessOS Audit Tool running on http://0.0.0.0:{port}", flush=True)
    app.run(host="0.0.0.0", port=port, debug=True)
