#!/usr/bin/env python3
"""Search the registry for agent types by keyword, category, or risk level."""

import argparse
import sys
import yaml
from pathlib import Path

REGISTRY_DIR = Path(__file__).resolve().parent.parent / "registry"


def load_all_agents() -> list[dict]:
    agents = []
    for fpath in REGISTRY_DIR.rglob("*.yaml"):
        if "vendors" in fpath.parts:
            continue
        try:
            with open(fpath) as f:
                data = yaml.safe_load(f)
            if data and isinstance(data, dict) and "id" in data:
                agents.append(data)
        except yaml.YAMLError:
            pass
    return agents


def search(agents: list[dict], keyword: str = "", category: str = "", risk: str = "") -> list[dict]:
    results = []
    kw = keyword.lower() if keyword else ""
    for a in agents:
        if kw and not any(kw in str(v).lower() for v in a.values()):
            continue
        if category and a.get("category", "").lower() != category.lower():
            continue
        if risk and a.get("risk_profile", "").lower() != risk.lower():
            continue
        results.append(a)
    return results


def main():
    parser = argparse.ArgumentParser(description="Search the Agent Asset Registry")
    parser.add_argument("-k", "--keyword", help="Search keyword")
    parser.add_argument("-c", "--category", choices=["general-purpose", "workflow", "industry"], help="Filter by category")
    parser.add_argument("-r", "--risk", choices=["low", "medium", "high", "critical"], help="Filter by risk profile")
    parser.add_argument("--list-categories", action="store_true", help="List all available categories")
    args = parser.parse_args()

    agents = load_all_agents()

    if args.list_categories:
        cats = sorted(set(a.get("category", "unknown") for a in agents))
        print("\nAvailable categories:")
        for c in cats:
            count = sum(1 for a in agents if a.get("category") == c)
            print(f"  • {c} ({count} agents)")
        return

    if not args.keyword and not args.category and not args.risk:
        parser.print_help()
        print("\nExample: python search-registry.py -k email -r high")
        return

    results = search(agents, keyword=args.keyword or "", category=args.category or "", risk=args.risk or "")

    if not results:
        print("\nNo matching agents found.")
        return

    print(f"\nFound {len(results)} matching agent(s):\n")
    for a in sorted(results, key=lambda x: x["id"]):
        print(f"  {a['id']}")
        print(f"  Name:     {a.get('name', 'N/A')}")
        print(f"  Category: {a.get('category', 'N/A')}")
        print(f"  Risk:     {a.get('risk_profile', 'N/A')}")
        print(f"  Vendor:   {a.get('vendor', 'N/A')}")
        desc = a.get("description", "")
        if desc:
            print(f"  Desc:     {desc[:120]}...")
        print()


if __name__ == "__main__":
    main()
