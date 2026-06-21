#!/usr/bin/env python3
"""Generate index.html for decred.zip from resources.txt.

Usage:  python3 build.py

Reads the human-editable resources.txt, parses sections + resources,
and writes a static index.html. See resources.txt for the file format.
"""

import html
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "resources.txt"
OUT = ROOT / "index.html"

SITE_NAME = "decred.zip"
TAGLINE = "An archive of Decred resources"
SITE_URL = "https://decred.zip"
OG_IMAGE = SITE_URL + "/og.png"


def parse(text):
    """Return a list of (section_title, [ (name, url, desc), ... ])."""
    sections = []
    current = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("## "):
            current = (line[3:].strip(), [])
            sections.append(current)
            continue
        if line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) == 2:
            name, desc = parts
            url = name
        elif len(parts) >= 3:
            name, url, desc = parts[0], parts[1], "|".join(parts[2:]).strip()
        else:
            sys.stderr.write(f"skipping malformed line: {raw!r}\n")
            continue
        if "://" not in url:
            url = "https://" + url
        if current is None:
            current = ("Resources", [])
            sections.append(current)
        current[1].append((name, url, desc))
    return sections


def esc(s):
    return html.escape(s, quote=True)


ARROW = (
    '<svg class="card__arrow" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round" aria-hidden="true">'
    '<path d="M7 17 17 7M8 7h9v9"/></svg>'
)

SEARCH_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    'aria-hidden="true"><circle cx="11" cy="11" r="7"/>'
    '<path d="m21 21-4.3-4.3"/></svg>'
)


def render(sections):
    total = sum(len(items) for _, items in sections)
    blocks = []
    for title, items in sections:
        cards = []
        for name, url, desc in items:
            cards.append(
                '          <a class="card" href="{url}" '
                'data-search="{search}">\n'
                '            <span class="card__head">'
                '<span class="card__name">{name}</span>{arrow}</span>\n'
                '            <p class="card__desc">{desc}</p>\n'
                "          </a>".format(
                    url=esc(url),
                    name=esc(name),
                    desc=esc(desc),
                    arrow=ARROW,
                    search=esc((name + " " + desc).lower()),
                )
            )
        blocks.append(
            '      <section class="section">\n'
            '        <h2 class="section__title">{title}</h2>\n'
            '        <div class="grid">\n{cards}\n        </div>\n'
            "      </section>".format(title=esc(title), cards="\n".join(cards))
        )

    sections_html = "\n".join(blocks)
    updated = date.today().isoformat()

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#0a0e1a" />
    <title>{SITE_NAME} · {TAGLINE}</title>
    <meta name="description" content="{esc(TAGLINE)}. A curated index of Decred ecosystem websites, explorers, tools, and governance." />
    <link rel="canonical" href="{SITE_URL}/" />
    <meta property="og:site_name" content="{SITE_NAME}" />
    <meta property="og:title" content="{SITE_NAME}" />
    <meta property="og:description" content="{esc(TAGLINE)}. A curated index of Decred ecosystem websites, explorers, tools, and governance." />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{SITE_URL}/" />
    <meta property="og:image" content="{OG_IMAGE}" />
    <meta property="og:image:secure_url" content="{OG_IMAGE}" />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="{SITE_NAME} — {esc(TAGLINE)}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{SITE_NAME}" />
    <meta name="twitter:description" content="{esc(TAGLINE)}" />
    <meta name="twitter:image" content="{OG_IMAGE}" />
    <meta name="twitter:image:alt" content="{SITE_NAME} — {esc(TAGLINE)}" />
    <link rel="icon" type="image/svg+xml" href="dcr.svg" />
    <link rel="alternate icon" href="favicon.ico" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <header class="site-header">
      <div class="wrap">
        <a class="brand" href="/">
          <img class="brand__logo" src="dcr.svg" alt="Decred logo" width="56" height="56" />
          <span class="brand__name">decred<span class="tld">.zip</span></span>
        </a>
        <p class="tagline">{esc(TAGLINE)}</p>
        <div class="toolbar">
          <label class="search">
            {SEARCH_ICON}
            <input id="filter" type="search" placeholder="Filter {total} resources…" autocomplete="off" aria-label="Filter resources" />
          </label>
        </div>
      </div>
    </header>

    <main>
      <div class="wrap">
{sections_html}
        <p class="no-results" id="no-results">No resources match your search.</p>
      </div>
    </main>

    <footer class="site-footer">
      <div class="wrap site-footer__inner">
        <a class="brand brand--sm" href="/">
          <img class="brand__logo brand__logo--sm" src="dcr.svg" alt="" width="30" height="30" />
          <span class="brand__name brand__name--sm">decred<span class="tld">.zip</span></span>
        </a>
        <p class="site-footer__tagline">An archive of <span class="count">{total}</span> Decred resources, hand-picked and kept current.</p>
        <p class="site-footer__meta">Last updated {updated}</p>
      </div>
    </footer>

    <script>
      // Lightweight, progressive-enhancement filter. Works without it too.
      (function () {{
        var input = document.getElementById("filter");
        if (!input) return;
        var cards = Array.prototype.slice.call(document.querySelectorAll(".card"));
        var sections = Array.prototype.slice.call(document.querySelectorAll(".section"));
        var empty = document.getElementById("no-results");
        input.addEventListener("input", function () {{
          var q = input.value.trim().toLowerCase();
          var anyVisible = false;
          cards.forEach(function (c) {{
            var match = !q || c.getAttribute("data-search").indexOf(q) !== -1;
            c.style.display = match ? "" : "none";
            if (match) anyVisible = true;
          }});
          sections.forEach(function (s) {{
            var visible = s.querySelectorAll('.card:not([style*="display: none"])').length;
            s.style.display = visible ? "" : "none";
          }});
          if (empty) empty.style.display = anyVisible ? "none" : "block";
        }});
      }})();
    </script>
  </body>
</html>
"""


def main():
    if not SRC.exists():
        sys.exit(f"error: {SRC} not found")
    sections = parse(SRC.read_text(encoding="utf-8"))
    total = sum(len(items) for _, items in sections)
    OUT.write_text(render(sections), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} — {total} resources in {len(sections)} sections.")


if __name__ == "__main__":
    main()
