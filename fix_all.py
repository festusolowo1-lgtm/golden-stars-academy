from pathlib import Path
import re

ROOT = Path(".")
INDEX = ROOT / "templates" / "index.html"

SLIDES = [
    {
        "bg": "linear-gradient(135deg,#1a3a6b 0%,#2d6a9f 100%)",
        "svg": '<svg viewBox="0 0 900 420" xmlns="http://www.w3.org/2000/svg" style="position:absolute;inset:0;width:100%;height:100%;opacity:.18"><rect x="60" y="60" width="120" height="160" rx="8" fill="#fff"/><rect x="70" y="70" width="100" height="12" rx="3" fill="#c9a84c"/><rect x="70" y="92" width="80" height="8" rx="2" fill="#fff" opacity=".6"/><rect x="70" y="108" width="90" height="8" rx="2" fill="#fff" opacity=".5"/><circle cx="600" cy="180" r="120" fill="none" stroke="#fff" stroke-width="3" opacity=".15"/><polygon points="600,100 620,160 680,160 632,198 650,260 600,222 550,260 568,198 520,160 580,160" fill="#c9a84c" opacity=".25"/></svg>',
        "badge": "Welcome",
        "title": "Golden Stars Academy",
        "sub": "Nurturing Excellence &mdash; GRA Gbessa, Abuja",
    },
    {
        "bg": "linear-gradient(135deg,#0f4c35 0%,#1a7a52 100%)",
        "svg": '<svg viewBox="0 0 900 420" xmlns="http://www.w3.org/2000/svg" style="position:absolute;inset:0;width:100%;height:100%;opacity:.18"><rect x="100" y="80" width="200" height="260" rx="10" fill="none" stroke="#fff" stroke-width="2"/><rect x="120" y="100" width="160" height="20" rx="4" fill="#c9a84c" opacity=".6"/><rect x="120" y="132" width="60" height="60" rx="4" fill="#fff" opacity=".2"/><rect x="192" y="132" width="88" height="10" rx="3" fill="#fff" opacity=".4"/><text x="580" y="230" font-size="120" fill="#fff" opacity=".1" font-family="serif">A+</text></svg>',
        "badge": "Academic Excellence",
        "title": "World-Class Education",
        "sub": "From Nursery to Senior Secondary &mdash; Holistic development for every child",
    },
    {
        "bg": "linear-gradient(135deg,#6b1a1a 0%,#9f2d2d 100%)",
        "svg": '<svg viewBox="0 0 900 420" xmlns="http://www.w3.org/2000/svg" style="position:absolute;inset:0;width:100%;height:100%;opacity:.18"><circle cx="200" cy="200" r="70" fill="none" stroke="#fff" stroke-width="2"/><circle cx="200" cy="200" r="45" fill="#c9a84c" opacity=".2"/><line x1="200" y1="130" x2="200" y2="200" stroke="#fff" stroke-width="3"/><line x1="200" y1="200" x2="240" y2="230" stroke="#c9a84c" stroke-width="2"/><rect x="400" y="80" width="350" height="260" rx="12" fill="none" stroke="#fff" stroke-width="1.5" opacity=".3"/></svg>',
        "badge": "School Calendar",
        "title": "Stay Up to Date",
        "sub": "Term dates, events, exams and activities &mdash; all in one place",
    },
    {
        "bg": "linear-gradient(135deg,#1a1a6b 0%,#2d2d9f 100%)",
        "svg": '<svg viewBox="0 0 900 420" xmlns="http://www.w3.org/2000/svg" style="position:absolute;inset:0;width:100%;height:100%;opacity:.18"><rect x="80" y="100" width="180" height="220" rx="10" fill="none" stroke="#fff" stroke-width="1.5"/><rect x="100" y="120" width="50" height="50" rx="25" fill="#c9a84c" opacity=".3"/><rect x="300" y="80" width="180" height="220" rx="10" fill="none" stroke="#c9a84c" stroke-width="2" opacity=".4"/><rect x="520" y="100" width="180" height="220" rx="10" fill="none" stroke="#fff" stroke-width="1.5"/></svg>',
        "badge": "Our Team",
        "title": "Dedicated Educators",
        "sub": "Qualified, passionate teachers committed to your child&rsquo;s success",
    },
    {
        "bg": "linear-gradient(135deg,#2d1a6b 0%,#6b2d9f 100%)",
        "svg": '<svg viewBox="0 0 900 420" xmlns="http://www.w3.org/2000/svg" style="position:absolute;inset:0;width:100%;height:100%;opacity:.18"><rect x="80" y="120" width="260" height="180" rx="8" fill="none" stroke="#fff" stroke-width="1.5"/><polygon points="210,155 220,185 252,185 226,203 236,233 210,215 184,233 194,203 168,185 200,185" fill="#fff" opacity=".25"/><rect x="380" y="80" width="200" height="14" rx="4" fill="#c9a84c" opacity=".5"/><rect x="380" y="106" width="340" height="10" rx="3" fill="#fff" opacity=".25"/><rect x="380" y="172" width="100" height="35" rx="17" fill="#c9a84c" opacity=".4"/></svg>',
        "badge": "Enrol Today",
        "title": "Begin Your Journey",
        "sub": "Admissions open &mdash; Give your child the Golden Stars advantage",
    },
]

def build_carousel():
    items = ""
    indicators = ""
    for i, s in enumerate(SLIDES):
        active = "active" if i == 0 else ""
        items += f"""
    <div class="carousel-item {active}">
      <div style="position:relative;height:460px;background:{s['bg']};overflow:hidden;display:flex;align-items:center;justify-content:center;">
        {s['svg']}
        <div style="position:relative;z-index:2;text-align:center;color:#fff;padding:0 20px;max-width:700px">
          <span style="background:rgba(201,168,76,.25);border:1px solid #c9a84c;color:#c9a84c;padding:4px 18px;border-radius:20px;font-size:.8rem;font-weight:700;letter-spacing:1px;text-transform:uppercase">{s['badge']}</span>
          <h1 style="font-size:2.6rem;font-weight:800;margin:.6rem 0 .4rem;text-shadow:0 2px 12px rgba(0,0,0,.4)">{s['title']}</h1>
          <p style="font-size:1.05rem;opacity:.88;margin-bottom:1.8rem">{s['sub']}</p>
          <a href="#about" style="background:#c9a84c;color:#fff;padding:.7rem 2rem;border-radius:30px;text-decoration:none;font-weight:700;margin-right:.5rem">Learn More</a>
          <a href="/admin/login" style="border:2px solid rgba(255,255,255,.5);color:#fff;padding:.65rem 1.8rem;border-radius:30px;text-decoration:none;font-weight:600">Admin Login</a>
        </div>
      </div>
    </div>"""
        checked = 'class="active"' if i == 0 else ""
        indicators += f'<button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="{i}" {checked} style="width:10px;height:10px;border-radius:50%;background:#c9a84c;opacity:.6;border:none"></button>\n'

    return f"""<div id="heroCarousel" class="carousel slide" data-bs-ride="carousel" data-bs-interval="5000">
  <div class="carousel-indicators" style="margin-bottom:.8rem">
    {indicators}
  </div>
  <div class="carousel-inner">
    {items}
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#heroCarousel" data-bs-slide="prev">
    <span class="carousel-control-prev-icon"></span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#heroCarousel" data-bs-slide="next">
    <span class="carousel-control-next-icon"></span>
  </button>
</div>"""


def fix_carousel(html):
    # Replace existing carousel if found
    pattern = re.compile(
        r'<div[^>]+id=["\']heroCarousel["\'].*?</div>\s*</div>\s*</div>',
        re.DOTALL
    )
    new_carousel = build_carousel()
    if pattern.search(html):
        html = pattern.sub(new_carousel, html, count=1)
        print("Carousel replaced.")
    else:
        # If no carousel found, insert after <body> or after first <div>
        html = html.replace("<body>", "<body>\n" + new_carousel, 1)
        print("Carousel inserted at top of body.")
    return html


def fix_stats_js(html):
    stats_js = """
<script>
(function(){
  fetch('/api/stats')
    .then(function(r){ return r.json(); })
    .then(function(d){
      document.querySelectorAll('[data-stat]').forEach(function(el){
        var key = el.getAttribute('data-stat');
        if(d[key] !== undefined) el.textContent = d[key];
      });
    })
    .catch(function(){});
})();
</script>"""
    if "fetch('/api/stats')" not in html:
        html = html.replace("</body>", stats_js + "\n</body>")
        print("Live stats JS injected.")
    else:
        print("Live stats JS already present.")
    return html


def fix_admin_sidebar(path):
    src = path.read_text(encoding="utf-8")
    old = """    {% if current_user.role == 'superadmin' %}
    <div class="sb-sec">Portals</div>
    <a href="/admin/staff"   class="sb-a {% if '/admin/staff'   in request.url.path %}on{% endif %}"><i class="ti ti-users"></i> Staff Accounts</a>
    <a href="/admin/parents" class="sb-a {% if '/admin/parents' in request.url.path %}on{% endif %}"><i class="ti ti-heart"></i> Parent Accounts</a>
    {% endif %}"""
    new = """    {% if current_user.role in ['superadmin','ict'] %}
    <a href="/admin/staff"   class="sb-a {% if '/admin/staff'   in request.url.path %}on{% endif %}"><i class="ti ti-users"></i> Staff Accounts</a>
    <a href="/admin/parents" class="sb-a {% if '/admin/parents' in request.url.path %}on{% endif %}"><i class="ti ti-heart"></i> Parent Accounts</a>
    {% endif %}"""
    if old in src:
        src = src.replace(old, new)
        path.write_text(src, encoding="utf-8")
        print("Admin sidebar patched for ICT role.")
    else:
        print("Sidebar already patched or structure differs - skipping.")


def fix_main_stats(path):
    src = path.read_text(encoding="utf-8")
    if "/api/stats" in src:
        print("/api/stats already exists in main.py - skipping.")
        return
    stats_route = '''
@app.get("/api/stats")
def api_stats(db: Session = Depends(get_db)):
    students   = db.exec(select(Student)).all()
    staff      = db.exec(select(StaffUser)).all()
    news_count = len(db.exec(select(News).where(News.published == True)).all())
    nursery  = get_info(db, "nursery_count",  str(len([s for s in students if "primary" in s.level.lower()])))
    jss      = get_info(db, "jss_count",      str(len([s for s in students if "jss" in s.level.lower()])))
    sss      = get_info(db, "sss_count",      str(len([s for s in students if "sss" in s.level.lower()])))
    teachers = get_info(db, "teacher_count",  str(len(staff)))
    return {
        "nursery_count":  nursery,
        "jss_count":      jss,
        "sss_count":      sss,
        "teacher_count":  teachers,
        "total_students": str(len(students)),
        "news_count":     str(news_count),
    }

'''
    src = src.replace("# ── STAFF AUTH ──", stats_route + "# ── STAFF AUTH ──")
    path.write_text(src, encoding="utf-8")
    print("/api/stats added to main.py.")


if __name__ == "__main__":
    # Fix index.html
    if INDEX.exists():
        html = INDEX.read_text(encoding="utf-8")
        html = fix_carousel(html)
        html = fix_stats_js(html)
        INDEX.write_text(html, encoding="utf-8")
        print("index.html updated.")
    else:
        print("WARNING: templates/index.html not found.")

    # Fix admin sidebar
    base = ROOT / "templates" / "admin" / "base.html"
    if base.exists():
        fix_admin_sidebar(base)

    # Fix main.py stats
    main_py = ROOT / "main.py"
    if main_py.exists():
        fix_main_stats(main_py)

    print("\nAll done! Now run:")
    print("  git add .")
    print('  git commit -m "fix carousel and stats"')
    print("  git push")