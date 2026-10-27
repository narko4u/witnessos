#!/usr/bin/env python3
"""Generate a comprehensive human-readable report of all registered agents."""

import yaml
from pathlib import Path
from datetime import datetime

REGISTRY_DIR = Path(__file__).resolve().parent.parent / "registry"


def load_all_entries() -> tuple[list[dict], list[dict]]:
    agents = []
    vendors = []
    for fpath in sorted(REGISTRY_DIR.rglob("*.yaml")):
        try:
            with open(fpath) as f:
                data = yaml.safe_load(f)
            if data and isinstance(data, dict):
                if "type" in data and data.get("type") == "vendor-platform":
                    vendors.append(data)
                elif "api_endpoints" in data:
                    vendors.append(data)
                elif "id" in data:
                    agents.append(data)
        except yaml.YAMLError:
            pass
    return agents, vendors


def risk_emoji(level: str) -> str:
    return {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(level, "⚪")


def main():
    agents, vendors = load_all_entries()
    date_str = datetime.now().strftime("%Y-%m-%d")

    print("╔══════════════════════════════════════════════════════════╗")
    print("║         AGENT ASSET REGISTRY — REGISTERED AGENTS        ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"  Generated: {date_str}")
    print(f"  Total agent types:  {len(agents)}")
    print(f"  Vendor platforms:   {len(vendors)}")
    print()

    # By category
    by_category: dict[str, list[dict]] = {}
    for a in agents:
        cat = a.get("category", "uncategorised")
        by_category.setdefault(cat, []).append(a)

    print("── Agent Types by Category ──")
    for cat in sorted(by_category.keys()):
        cat_agents = by_category[cat]
        by_risk: dict[str, int] = {}
        for a in cat_agents:
            r = a.get("risk_profile", "unknown")
            by_risk[r] = by_risk.get(r, 0) + 1
        risk_summary = ", ".join(f"{risk_emoji(k)} {k}: {v}" for k, v in sorted(by_risk.items()))
        print(f"\n  {cat.upper()} ({len(cat_agents)} agents)")
        print(f"  Risk distribution: {risk_summary}")
        for a in sorted(cat_agents, key=lambda x: x["id"]):
            caps = a.get("capabilities", [])
            behaviors = a.get("known_behaviors", [])
            print(f"\n    {risk_emoji(a.get('risk_profile', ''))} {a['name']} ({a['id']})")
            print(f"        Vendor: {a.get('vendor', 'N/A')}")
            print(f"        Risk:   {a.get('risk_profile', 'N/A')}")
            print(f"        Capabilities ({len(caps)}): {', '.join(caps[:5])}")
            print(f"        Known behaviors ({len(behaviors)}):")
            for b in behaviors[:3]:
                sev_emoji = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(b.get("severity", ""), "⚪")
                print(f"          {sev_emoji} {b.get('pattern', 'N/A')} — {b.get('description', '')[:80]}")
    print()

    # Vendors
    print("── Vendor Platforms ──")
    for v in sorted(vendors, key=lambda x: x.get("name", "")):
        print(f"\n  {v.get('name', 'N/A')} ({v.get('id', 'N/A')})")
        print(f"      Type: {v.get('type', 'N/A')}")
        endpoints = v.get("api_endpoints", [])
        if endpoints:
            print(f"      Endpoints:")
            for ep in endpoints[:3]:
                print(f"        • {ep}")

    print()
    print("── Registry Summary ──")
    print(f"  Total agent types:      {len(agents)}")
    critical_count = sum(1 for a in agents if a.get("risk_profile") == "critical")
    high_count = sum(1 for a in agents if a.get("risk_profile") == "high")
    print(f"  Critical risk agents:   {critical_count}")
    print(f"  High risk agents:       {high_count}")
    print(f"  Vendor platforms:       {len(vendors)}")
    print(f"  Repository:             github.com/narko4u/witnessos-agent-asset-registry")
    print()


if __name__ == "__main__":
    main()
