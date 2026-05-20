import re
import os

print("Starting site update...")

# ── 1. UPDATE TOPBAR + FOOTER LINKS IN index.html ─────────────
path = os.path.join("templates", "index.html")
if not os.path.exists(path):
    print("ERROR: templates/index.html not found. Run create_index.py first.")
else:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Topbar links
    html = html.replace(
        '<a href="#"><i class="ti ti-user-circle"></i> Parent Login</a>',
        '<a href="/parent/login"><i class="ti ti-user-circle"></i> Parent Login</a>'
    )
    html = html.replace(
        '<a href="#"><i class="ti ti-users"></i> Staff</a>',
        '<a href="/staff/login"><i class="ti ti-users"></i> Staff</a>'
    )
    html = html.replace(
        '<a href="#"><i class="ti ti-school"></i> Student</a>',
        '<a href="/student/login"><i class="ti ti-school"></i> Student</a>'
    )
    # Footer portal links
    html = html.replace(
        '<a href="#">Parent Login</a>',
        '<a href="/parent/login">Parent Login</a>'
    )
    html = html.replace(
        '<a href="#">Student Login</a>',
        '<a href="/student/login">Student Login</a>'
    )

    # ── 2. REPLACE CAROUSEL ────────────────────────────────────
    new_carousel = """  <div class="carousel-wrap">
    <button class="carousel-nav prev" onclick="moveCarousel(-1)">&#8249;</button>
    <button class="carousel-nav next" onclick="moveCarousel(1)">&#8250;</button>

    <div class="carousel-slide active" style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);">
      <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:.06;font-size:320px;user-select:none;">📚</div>
      <div class="carousel-content">
        <div style="font-size:60px;margin-bottom:16px;">📚</div>
        <div class="carousel-quote">"Education is the <em>most powerful weapon</em> you can use to change the world."</div>
        <div class="carousel-author">— Nelson Mandela &nbsp;·&nbsp; Inspiring Excellence at Golden Stars Academy</div>
      </div>
    </div>

    <div class="carousel-slide" style="background:linear-gradient(135deg,#0d3b2e 0%,#1a5c3a 50%,#2d8a5e 100%);">
      <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:.06;font-size:320px;user-select:none;">💡</div>
      <div class="carousel-content">
        <div style="font-size:60px;margin-bottom:16px;">💡</div>
        <div class="carousel-quote">"The <em>function of education</em> is to teach one to think intensively and to think critically."</div>
        <div class="carousel-author">— Martin Luther King Jr. &nbsp;·&nbsp; Our Guiding Philosophy</div>
      </div>
    </div>

    <div class="carousel-slide" style="background:linear-gradient(135deg,#7c2d12 0%,#c2410c 50%,#ea580c 100%);">
      <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:.06;font-size:320px;user-select:none;">🤝</div>
      <div class="carousel-content">
        <div style="font-size:60px;margin-bottom:16px;">🤝</div>
        <div class="carousel-quote">"Tell me and I forget. Teach me and I remember. <em>Involve me and I learn.</em>"</div>
        <div class="carousel-author">— Benjamin Franklin &nbsp;·&nbsp; Active Learning at Golden Stars</div>
      </div>
    </div>

    <div class="carousel-slide" style="background:linear-gradient(135deg,#2e1065 0%,#4c1d95 50%,#6d28d9 100%);">
      <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:.06;font-size:320px;user-select:none;">🎓</div>
      <div class="carousel-content">
        <div style="font-size:60px;margin-bottom:16px;">🎓</div>
        <div class="carousel-quote">"Children must be taught <em>how to think,</em> not what to think."</div>
        <div class="carousel-author">— Margaret Mead &nbsp;·&nbsp; Critical Thinking at the Core</div>
      </div>
    </div>

    <div class="carousel-slide" style="background:linear-gradient(135deg,#1a3a6b 0%,#1e4d8c 50%,#1a5c7a 100%);">
      <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:.06;font-size:320px;user-select:none;">🙏</div>
      <div class="carousel-content">
        <div style="font-size:60px;margin-bottom:16px;">🙏</div>
        <div class="carousel-quote">"<em>God is Able</em> — our faith anchors our pursuit of excellence, character, and service."</div>
        <div class="carousel-author">— The Golden Stars Academy Motto &nbsp;·&nbsp; Est. 2011, GRA Gbessa, Abuja</div>
      </div>
    </div>

    <div class="carousel-dots" id="carouselDots"></div>
  </div>"""

    # Find and replace the carousel block
    start = html.find('<div class="carousel-wrap">')
    end   = html.find('<!-- STATS BAR -->')
    if start != -1 and end != -1:
        html = html[:start] + new_carousel + "\n\n  " + html[end:]
        print("  Carousel replaced successfully.")
    else:
        print("  WARNING: Could not find carousel block — skipping carousel update.")

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ templates/index.html updated.")


# ── 3. UPDATE ADMIN SIDEBAR ────────────────────────────────────
base_path = os.path.join("templates", "admin", "base.html")
if not os.path.exists(base_path):
    print("ERROR: templates/admin/base.html not found.")
else:
    with open(base_path, "r", encoding="utf-8") as f:
        base = f.read()

    old_finance = """    {% if current_user.role in ['superadmin','bursar'] %}
    <div class="sb-sec">Finance</div>
    <a href="/admin/fees" class="sb-a {% if '/admin/fees' in request.url.path %}on{% endif %}"><i class="ti ti-cash"></i> Fee Management</a>
    {% endif %}"""

    new_finance = """    {% if current_user.role in ['superadmin','bursar'] %}
    <div class="sb-sec">Finance</div>
    <a href="/admin/fees" class="sb-a {% if '/admin/fees' in request.url.path %}on{% endif %}"><i class="ti ti-cash"></i> Fee Management</a>
    {% endif %}
    {% if current_user.role in ['superadmin','ict'] %}
    <div class="sb-sec">Academic</div>
    <a href="/admin/results" class="sb-a {% if '/admin/results' in request.url.path %}on{% endif %}"><i class="ti ti-chart-bar"></i> Results Approval</a>
    {% endif %}
    {% if current_user.role == 'superadmin' %}
    <div class="sb-sec">Portals</div>
    <a href="/admin/staff"   class="sb-a {% if '/admin/staff'   in request.url.path %}on{% endif %}"><i class="ti ti-users"></i> Staff Accounts</a>
    <a href="/admin/parents" class="sb-a {% if '/admin/parents' in request.url.path %}on{% endif %}"><i class="ti ti-heart"></i> Parent Accounts</a>
    {% endif %}"""

    if old_finance in base:
        base = base.replace(old_finance, new_finance)
        print("✅ Admin sidebar updated.")
    else:
        print("  WARNING: Could not find finance block in base.html.")
        print("  Add these links manually to templates/admin/base.html sidebar:")
        print("    /admin/results  → Results Approval")
        print("    /admin/staff    → Staff Accounts")
        print("    /admin/parents  → Parent Accounts")

    with open(base_path, "w", encoding="utf-8") as f:
        f.write(base)


# ── 4. CHECK main.py FOR NEW MODELS ───────────────────────────
print("\nChecking main.py for portal models...")
if os.path.exists("main.py"):
    with open("main.py", "r", encoding="utf-8") as f:
        main_content = f.read()
    models = ["class Student", "class StaffUser", "class Assignment",
              "class AssignmentSubmission", "class ExamResult", "class ParentUser"]
    missing = [m for m in models if m not in main_content]
    if missing:
        print("\n⚠️  MISSING models in main.py — copy from add_to_main.py artifact:")
        for m in missing:
            print(f"   {m}")
    else:
        print("✅ All portal models found in main.py")
else:
    print("ERROR: main.py not found.")

print("\n" + "="*50)
print("DONE! Next steps:")
print("="*50)
print("1. If models are missing: add them to main.py")
print("2. Run: python -m uvicorn main:app --reload")
print("3. Visit http://localhost:8000")
print("\nPortal URLs:")
print("  Staff   -> http://localhost:8000/staff/login")
print("  Parent  -> http://localhost:8000/parent/login")
print("  Student -> http://localhost:8000/student/login")
print("  Admin   -> http://localhost:8000/admin/login")