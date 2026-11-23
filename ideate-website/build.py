"""Build a standalone, host-anywhere copy of the Ideate Hub site.

index.html is written for the Claude artifact viewer, which adds the <!doctype>, <head>
and <body> wrapper itself. This script adds that wrapper plus favicon and link-preview
tags, copies only the images the page uses, and zips the result.

Usage:
    python3 build.py                          # relative share links
    python3 build.py https://www.example.com  # once you know the domain (better link previews)
"""
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "site"
ZIP = ROOT / "ideate-hub-site.zip"

TITLE = "Ideate Hub Ghana"
DESCRIPTION = ("Strategy-led marketing and communications agency in Tamale, Northern Ghana, "
               "working with NGOs, businesses and startups.")

site_url = (sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "")

src = (ROOT / "index.html").read_text(encoding="utf-8")

# Artifact-only tag; meaningless on a normal site
src = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\n?', "", src)

# Everything up to the end of the stylesheet belongs in <head>, the rest in <body>
split_at = src.index("</style>") + len("</style>")
head_part, body_part = src[:split_at], src[split_at:]

share_image = f"{site_url}/assets/share.jpg" if site_url else "assets/share.jpg"
url_tags = f'<link rel="canonical" href="{site_url}/">\n<meta property="og:url" content="{site_url}/">\n' if site_url else ""

page = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0F0F0F">
<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:image" content="{share_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{url_tags}{head_part.strip()}
<style>[hidden] {{ display: none !important; }} img {{ max-width: 100%; }}</style>
</head>
<body>
{body_part.strip()}
</body>
</html>
"""

if OUT.exists():
    shutil.rmtree(OUT)
(OUT / "images").mkdir(parents=True)
(OUT / "index.html").write_text(page, encoding="utf-8")

used = sorted(set(re.findall(r'src="(images/[^"]+)"', page)))
for rel in used:
    (OUT / rel).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / rel, OUT / rel)
shutil.copytree(ROOT / "assets", OUT / "assets")
(OUT / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")

if ZIP.exists():
    ZIP.unlink()
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(OUT.rglob("*")):
        if f.is_file():
            z.write(f, f.relative_to(OUT))

size_kb = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file()) // 1024
print(f"Built {OUT} ({len(used)} images, {size_kb} KB) and {ZIP.name}")
if not site_url:
    print("Tip: rerun with your domain, e.g. python3 build.py https://www.yourdomain.com, for better link previews.")
