"""
Enrich BPC catalog with Microsoft Learn metadata.

Fetches stakeholder roles and process flow steps from the official
Dynamics 365 guidance hub for each L2 business process area.

Usage:
    py -3 scripts/enrich-bpc.py              # Fetch and save enrichment data
    py -3 scripts/enrich-bpc.py --refresh     # Re-fetch all (ignore cache)

Output: bpc/enrichment.json
"""
import json, re, sys, os, time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://learn.microsoft.com/en-us/dynamics365/guidance"
TOC_URL = f"{BASE_URL}/toc.json"
ENRICHMENT_FILE = ROOT / "bpc" / "enrichment.json"
CATALOG_FILE = ROOT / "bpc" / "catalog.json"

HEADERS = {"User-Agent": "Mozilla/5.0 (psi-solution-architecture enrichment)"}

refresh = "--refresh" in sys.argv


def fetch_url(url):
    """Fetch URL content as text."""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=20)
        return resp.read().decode("utf-8")
    except Exception as e:
        print(f"  WARN: Failed to fetch {url}: {e}")
        return None


def fetch_page_html(slug):
    """Fetch a Learn page and return raw HTML with decoded entities."""
    url = f"{BASE_URL}/{slug}"
    html = fetch_url(url)
    if not html:
        return None
    return html.replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", '"').replace("&nbsp;", " ")


def extract_stakeholders(html):
    """Extract stakeholder roles from page HTML."""
    stakeholders = []
    # Find Stakeholders section in HTML
    match = re.search(
        r"<h2[^>]*>\s*Stakeholders?\s*</h2>(.*?)(?:<h2|$)", html, re.DOTALL | re.IGNORECASE
    )
    if not match:
        return stakeholders

    section = match.group(1)
    # Extract <strong>Role name</strong> patterns
    roles = re.findall(r"<strong>([^<]+)</strong>", section)
    for role in roles:
        role = role.strip().rstrip(",.")
        if role and len(role) < 80 and "note" not in role.lower():
            stakeholders.append(role)

    # Also extract "such as X, Y, and Z" for specific role names
    such_as = re.findall(r"such as ([^.<]+)", section)
    for sa in such_as:
        names = [n.strip() for n in re.split(r",\s*(?:and\s+)?", sa)]
        for n in names:
            if n and len(n) > 3 and len(n) < 60:
                stakeholders.append(n)

    return stakeholders


def extract_flow_steps(html):
    """Extract process flow steps from page HTML."""
    steps = []
    # Find the flow section — look for "process flow" heading
    match = re.search(
        r"<h2[^>]*>[^<]*process flow[^<]*</h2>(.*?)(?:<h2|$)", html, re.DOTALL | re.IGNORECASE
    )
    if not match:
        return steps

    section = match.group(1)
    # Extract <em> or <li> items that represent process steps
    # Pattern: list items containing italic text like <em>Step name</em>
    em_items = re.findall(r"<em>([^<]+)</em>", section)
    for item in em_items:
        item = item.strip().rstrip(".")
        if item.lower() in ("start", "end", "") or "end-to-end" in item.lower():
            continue
        if len(item) > 5 and len(item) < 100:
            steps.append(item)

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for s in steps:
        if s.lower() not in seen:
            seen.add(s.lower())
            unique.append(s)
    return unique


def extract_description(html, title):
    """Extract first meaningful paragraph as description."""
    # Find first <p> after the <h1> that isn't "Applies to"
    paragraphs = re.findall(r"<p>([^<]{50,})</p>", html)
    for p in paragraphs:
        p = re.sub(r"<[^>]+>", "", p).strip()
        if "applies to" not in p.lower() and len(p) > 50:
            return p[:300]
    return ""


def discover_l2_pages():
    """Fetch TOC and extract all L2 overview page slugs."""
    print("Fetching TOC from Microsoft Learn...")
    raw = fetch_url(TOC_URL)
    if not raw:
        print("ERROR: Could not fetch TOC")
        return []

    toc = json.loads(raw)
    pages = []

    def walk(node):
        href = node.get("href", "")
        title = node.get("toc_title", "")
        if (
            href
            and href.startswith("business-processes/")
            and "overview" in href
            and href != "business-processes/overview"
            and "areas" not in href
        ):
            pages.append({"slug": href, "title": title})
        for c in node.get("children", node.get("items", [])):
            walk(c)

    walk(toc)
    print(f"  Found {len(pages)} overview pages in TOC")
    return pages


def match_l2_to_pages(catalog, pages):
    """Match BPC L2 areas to their Microsoft Learn page slugs."""
    # Build a lookup from page title keywords to slug
    page_lookup = {}
    for p in pages:
        # Normalize title for matching
        key = p["title"].lower().replace(" overview", "").strip()
        page_lookup[key] = p["slug"]

    mappings = {}
    for l1_name, l1_data in catalog.items():
        l1_id = l1_data["id"]
        l1_slug = l1_name.lower().replace(" ", "-")

        for l2_name in l1_data["areas"]:
            seq = l1_data["areas"][l2_name]["seq"]
            l2_id = seq.split(".")[0] + "." + seq.split(".")[1]
            l2_lower = l2_name.lower()

            # Try exact match first
            matched_slug = page_lookup.get(l2_lower)

            # Try partial match
            if not matched_slug:
                for key, slug in page_lookup.items():
                    if l1_slug in slug and (
                        l2_lower in key
                        or key in l2_lower
                        or any(w in key for w in l2_lower.split()[:3] if len(w) > 4)
                    ):
                        matched_slug = slug
                        break

            mappings[l2_id] = {
                "l1_id": l1_id,
                "l1_name": l1_name,
                "l2_name": l2_name,
                "page_slug": matched_slug,
            }

    return mappings


def main():
    # Load existing enrichment if not refreshing
    existing = {}
    if ENRICHMENT_FILE.exists() and not refresh:
        with open(ENRICHMENT_FILE) as f:
            existing = json.load(f)
        print(f"Loaded existing enrichment: {len(existing)} entries")

    # Load BPC catalog
    with open(CATALOG_FILE) as f:
        catalog = json.load(f)

    # Discover all L2 pages from TOC
    pages = discover_l2_pages()

    # Match L2 areas to pages
    mappings = match_l2_to_pages(catalog, pages)

    matched = sum(1 for m in mappings.values() if m["page_slug"])
    print(f"  Matched {matched}/{len(mappings)} L2 areas to Learn pages")

    # Fetch each matched page
    enrichment = {}
    fetched = 0
    skipped = 0
    failed = 0

    for l2_id, meta in sorted(mappings.items()):
        slug = meta["page_slug"]

        # Skip if already enriched and not refreshing
        if l2_id in existing and not refresh:
            enrichment[l2_id] = existing[l2_id]
            skipped += 1
            continue

        entry = {
            "l1_id": meta["l1_id"],
            "l1_name": meta["l1_name"],
            "l2_id": l2_id,
            "l2_name": meta["l2_name"],
            "learn_url": f"https://learn.microsoft.com/en-us/dynamics365/guidance/{slug}" if slug else None,
            "stakeholders": [],
            "flow_steps": [],
            "description": "",
        }

        if not slug:
            enrichment[l2_id] = entry
            continue

        print(f"  Fetching {l2_id} {meta['l2_name'][:40]}... ", end="", flush=True)
        text = fetch_page_html(slug)
        if not text:
            print("FAILED")
            enrichment[l2_id] = entry
            failed += 1
            continue

        entry["stakeholders"] = extract_stakeholders(text)
        entry["flow_steps"] = extract_flow_steps(text)
        entry["description"] = extract_description(text, meta["l2_name"])

        enrichment[l2_id] = entry
        fetched += 1

        sh = len(entry["stakeholders"])
        fs = len(entry["flow_steps"])
        print(f"OK  stakeholders={sh}  flow_steps={fs}")

        # Rate limit: be polite to Microsoft
        time.sleep(0.5)

    # Save
    with open(ENRICHMENT_FILE, "w", encoding="utf-8") as f:
        json.dump(enrichment, f, indent=2, ensure_ascii=False)

    print(f"\nDone! Saved {len(enrichment)} entries to {ENRICHMENT_FILE}")
    print(f"  Fetched: {fetched}  Skipped (cached): {skipped}  Failed: {failed}  No page: {len(mappings) - matched}")


if __name__ == "__main__":
    main()
