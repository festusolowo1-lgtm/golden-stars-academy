from pathlib import Path
import re

f = Path("templates/index.html")
html = f.read_text(encoding="utf-8")

# ── FIX 1: carousel-wrap needs overflow:hidden and proper stacking ──
html = html.replace(
    '.carousel-wrap{position:relative;overflow:hidden;height:480px;background:var(--brand);}',
    '.carousel-wrap{position:relative;overflow:hidden;height:480px;background:var(--brand);isolation:isolate;}'
)
html = html.replace(
    '.carousel-wrap{position:relative;overflow:hidden;height:520px;background:var(--brand);}',
    '.carousel-wrap{position:relative;overflow:hidden;height:520px;background:var(--brand);isolation:isolate;}'
)

# ── FIX 2: pages need a proper z-index context ──
html = html.replace(
    '.page{display:none;}.page.active{display:block;}',
    '.page{display:none;position:relative;z-index:1;}.page.active{display:block;}'
)

# ── FIX 3: the illustrated carousel slides have inline style backgrounds
# but the carousel-wrap inline style override needs height too ──
html = html.replace(
    '<div class="carousel-wrap" style="height:520px;">',
    '<div class="carousel-wrap" style="height:520px;isolation:isolate;">'
)
html = html.replace(
    '<div class="carousel-wrap">',
    '<div class="carousel-wrap" style="isolation:isolate;">'
)

# ── FIX 4: Each illustrated slide's inner div needs z-index reset ──
# The SVGs inside slides are position:absolute which can bleed out
# Make sure carousel-slide has proper containment
html = html.replace(
    '.carousel-slide{position:absolute;inset:0;opacity:0;transition:opacity .8s ease;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#0f2d5a,var(--brand),#1a5c7a);}',
    '.carousel-slide{position:absolute;inset:0;opacity:0;transition:opacity .8s ease;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#0f2d5a,var(--brand),#1a5c7a);overflow:hidden;}'
)

f.write_text(html, encoding="utf-8")
print("Done! Check if .page and carousel styles were updated.")

# Show what was changed
for i, line in enumerate(html.split('\n'), 1):
    if 'isolation' in line or ('page' in line.lower() and 'z-index' in line):
        print(f"Line {i}: {line[:120]}")