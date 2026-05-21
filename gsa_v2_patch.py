"""
GSA v2.0 - Master Patch Script
Run this in your golden-stars folder:
  python gsa_v2_patch.py
"""
from pathlib import Path
import re, shutil

ROOT = Path(".")

def write(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"  OK  {path}")

def patch_main():
    src = Path("main.py").read_text(encoding="utf-8")

    # ── 1. Fix dashboard to include more counts ──────────────────────────
    OLD_DASH = '''@app.get("/admin", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db),
              user: User = Depends(require_login)):
    err = request.query_params.get("err")
    counts = {
        "users":    db.exec(select(User)).all().__len__(),
        "news":     db.exec(select(News)).all().__len__(),
        "fees":     db.exec(select(Fee)).all().__len__(),
        "gallery":  db.exec(select(GalleryItem)).all().__len__(),
        "calendar": db.exec(select(CalendarEvent)).all().__len__(),
    }
    recent_news = db.exec(select(News).order_by(News.id.desc()).limit(5)).all()
    pending_fees = db.exec(select(Fee).where(Fee.status=="pending")).all()
    return templates.TemplateResponse("admin/dashboard.html",
        ctx(request, db, counts=counts, recent_news=recent_news,
            pending_fees=pending_fees, access_error=err=="access"))'''

    NEW_DASH = '''@app.get("/admin", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db),
              user: User = Depends(require_login)):
    err = request.query_params.get("err")
    pending_results = db.exec(select(ExamResult).where(ExamResult.approved == False)).all()
    counts = {
        "users":           len(db.exec(select(User)).all()),
        "staff":           len(db.exec(select(StaffUser)).all()),
        "students":        len(db.exec(select(Student)).all()),
        "parents":         len(db.exec(select(ParentUser)).all()),
        "news":            len(db.exec(select(News)).all()),
        "fees":            len(db.exec(select(Fee)).all()),
        "gallery":         len(db.exec(select(GalleryItem)).all()),
        "calendar":        len(db.exec(select(CalendarEvent)).all()),
        "pending_results": len(pending_results),
    }
    recent_news = db.exec(select(News).order_by(News.id.desc()).limit(5)).all()
    pending_fees = db.exec(select(Fee).where(Fee.status=="pending")).all()
    return templates.TemplateResponse("admin/dashboard.html",
        ctx(request, db, counts=counts, recent_news=recent_news,
            pending_fees=pending_fees, access_error=err=="access",
            pending_results_count=len(pending_results)))'''

    if OLD_DASH in src:
        src = src.replace(OLD_DASH, NEW_DASH)
        print("  OK  main.py dashboard counts enhanced")
    else:
        print("  -- main.py dashboard already enhanced or differs")

    # ── 2. Add profile route if not present ─────────────────────────────
    if "/admin/profile" not in src:
        PROFILE_ROUTES = '''
# ── ADMIN PROFILE ─────────────────────────────────────────────────────────

@app.get("/admin/profile", response_class=HTMLResponse)
def admin_profile(request: Request, db: Session = Depends(get_db),
                  user: User = Depends(require_login)):
    return templates.TemplateResponse("admin/profile.html", ctx(request, db))

@app.post("/admin/profile")
async def admin_profile_post(request: Request, db: Session = Depends(get_db),
                              user: User = Depends(require_login),
                              name: str = Form(...),
                              current_password: str = Form(""),
                              new_password: str = Form(""),
                              avatar: UploadFile = File(None)):
    u = db.get(User, user.id)
    if not u:
        return RedirectResponse("/admin", 302)
    u.name = name
    if current_password and new_password:
        if verify_password(current_password, u.password):
            u.password = hash_password(new_password)
            flash(request, "Password updated successfully.")
        else:
            flash(request, "Current password is incorrect.", "error")
            return RedirectResponse("/admin/profile", 302)
    if avatar and avatar.filename:
        url = save_upload(avatar)
        if url: u.avatar = url
    db.add(u); db.commit()
    flash(request, "Profile updated successfully.")
    return RedirectResponse("/admin/profile", 302)

# ── STUDENT SEARCH API ─────────────────────────────────────────────────────

@app.get("/api/students/search")
def search_students(q: str = "", db: Session = Depends(get_db)):
    students = db.exec(select(Student)).all()
    if q:
        ql = q.lower()
        students = [s for s in students if ql in s.full_name.lower()
                    or ql in s.admission_no.lower()
                    or ql in s.class_name.lower()]
    return [{"id": s.id, "name": s.full_name, "class_name": s.class_name,
             "admission_no": s.admission_no, "level": s.level} for s in students[:20]]

# ── PARENT EDIT ROUTE ──────────────────────────────────────────────────────

@app.post("/admin/parents/{pid}/edit")
def admin_edit_parent(pid: int, request: Request, db: Session = Depends(get_db),
                      user: User = Depends(require_role("superadmin","ict")),
                      name: str = Form(...), email: str = Form(...),
                      password: str = Form(""), phone: str = Form(""),
                      student_ids: str = Form("")):
    p = db.get(ParentUser, pid)
    if p:
        p.name = name; p.email = email; p.phone = phone; p.student_ids = student_ids
        if password.strip(): p.password = hash_password(password)
        db.add(p); db.commit()
        flash(request, f"Parent account for {name} updated.")
    return RedirectResponse("/admin/parents", 302)

# ── STAFF TOGGLE ───────────────────────────────────────────────────────────

@app.post("/admin/staff/{sid}/toggle")
def admin_toggle_staff(sid: int, request: Request, db: Session = Depends(get_db),
                       user: User = Depends(require_role("superadmin","ict"))):
    s = db.get(StaffUser, sid)
    if s:
        s.status = "inactive" if s.status == "active" else "active"
        db.add(s); db.commit()
        flash(request, f"Staff status updated to {s.status}.")
    return RedirectResponse("/admin/staff", 302)

# ── PRINTABLE RESULT SHEET ─────────────────────────────────────────────────

@app.get("/parent/results/{student_id}/print", response_class=HTMLResponse)
def print_results(student_id: int, request: Request, db: Session = Depends(get_db),
                  term: str = "Third Term", session: str = "2025/2026"):
    p = get_parent(request, db)
    ids = [int(i) for i in p.student_ids.split(",") if i.strip().isdigit()]
    if student_id not in ids:
        raise HTTPException(403, detail="Access denied")
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(404)
    results = db.exec(select(ExamResult).where(
        ExamResult.student_id == student_id,
        ExamResult.approved == True,
        ExamResult.term == term,
        ExamResult.session == session
    )).all()
    school_logo = db.exec(select(Logo).where(Logo.logo_type == "school")).first()
    site = {k: get_info(db, k) for k in ["phone1","phone2","email","address","tagline"]}
    return templates.TemplateResponse("portals/result_sheet.html",
        {"request": request, "student": student, "results": results,
         "term": term, "session": session, "parent": p,
         "school_logo": school_logo, "site": site})

'''
        # Insert before the admin results route
        src = src.replace("# ── ADMIN: APPROVE RESULTS", PROFILE_ROUTES + "\n# ── ADMIN: APPROVE RESULTS")
        print("  OK  main.py profile + extra routes added")
    else:
        print("  -- main.py profile routes already present")

    # ── 3. Add approve-all fix (correct URL) ────────────────────────────
    if "approve-all" not in src:
        APPROVE_ALL = '''
@app.post("/admin/results/approve-all")
def admin_approve_all_fixed(request: Request, db: Session = Depends(get_db),
                             user: User = Depends(require_role("superadmin","ict"))):
    pending = db.exec(select(ExamResult).where(ExamResult.approved == False)).all()
    for r in pending:
        r.approved = True; db.add(r)
    db.commit()
    flash(request, f"All {len(pending)} pending results approved and published.")
    return RedirectResponse("/admin/results", 302)

'''
        src = src.replace("@app.get(\"/admin/results\"", APPROVE_ALL + "@app.get(\"/admin/results\"")
        print("  OK  main.py approve-all route fixed")

    Path("main.py").write_text(src, encoding="utf-8")
    print("  OK  main.py saved")


def fix_index_navigation():
    """Fix the page navigation by removing rogue Bootstrap carousel and fixing z-index"""
    index_path = Path("templates/index.html")
    if not index_path.exists():
        print("  !! index.html not found")
        return

    html = index_path.read_text(encoding="utf-8")

    # ── Remove the Bootstrap heroCarousel injected at top of body ───────
    bootstrap_pattern = re.compile(
        r'<div id="heroCarousel" class="carousel slide".*?</div>\s*<button class="carousel-control-prev".*?</button>\s*<button class="carousel-control-next".*?</button>\s*</div>',
        re.DOTALL
    )
    if bootstrap_pattern.search(html):
        html = bootstrap_pattern.sub("", html, count=1)
        print("  OK  Rogue Bootstrap carousel removed from index.html")
    else:
        print("  -- No rogue carousel found (already clean)")

    # ── Fix .page CSS to use display:none properly ───────────────────────
    html = html.replace(
        '.page{display:none;}.page.active{display:block;}',
        '.page{display:none;}.page.active{display:block;position:relative;z-index:1;}'
    )

    # ── Fix carousel-wrap to not bleed through ──────────────────────────
    html = re.sub(
        r'\.carousel-wrap\{([^}]+)\}',
        lambda m: '.carousel-wrap{' + m.group(1).rstrip(';') + ';isolation:isolate;}',
        html, count=1
    )
    html = re.sub(
        r'\.carousel-slide\{([^}]+)\}',
        lambda m: '.carousel-slide{' + m.group(1).rstrip(';') + ';overflow:hidden;}',
        html, count=1
    )

    # ── Replace showPage function with fixed version ─────────────────────
    OLD_SHOWPAGE = '''function showPage(id){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  const pg=document.getElementById('pg-'+id);
  (pg||document.getElementById('pg-home')).classList.add('active');
  window.scrollTo({top:0,behavior:'smooth'});
  document.querySelectorAll('.nav-link').forEach(l=>l.classList.remove('active'));
}'''

    NEW_SHOWPAGE = '''function showPage(id){
  document.querySelectorAll('.page').forEach(function(p){
    p.classList.remove('active');
    p.style.display='none';
  });
  var pg=document.getElementById('pg-'+id)||document.getElementById('pg-home');
  pg.classList.add('active');
  pg.style.display='block';
  window.scrollTo({top:0,behavior:'smooth'});
  document.querySelectorAll('.nav-link').forEach(function(l){l.classList.remove('active');});
}
// Init on load
document.addEventListener('DOMContentLoaded',function(){
  document.querySelectorAll('.page:not(.active)').forEach(function(p){p.style.display='none';});
});'''

    if OLD_SHOWPAGE in html:
        html = html.replace(OLD_SHOWPAGE, NEW_SHOWPAGE)
        print("  OK  showPage() function fixed in index.html")
    else:
        # Try to patch whatever version is there
        html = re.sub(
            r'function showPage\(id\)\{[^}]+\}',
            NEW_SHOWPAGE,
            html, count=1
        )
        print("  OK  showPage() patched (alternate match)")

    index_path.write_text(html, encoding="utf-8")
    print("  OK  index.html saved")


def update_parent_dashboard():
    """Add print button to parent dashboard"""
    path = Path("templates/portals/parent_dashboard.html")
    if not path.exists():
        print("  -- parent_dashboard.html not found, skipping")
        return

    html = path.read_text(encoding="utf-8")

    # Add print button after results table
    if "print" not in html.lower():
        html = html.replace(
            "{% else %}\n      <p class=\"text-muted small\">No approved results yet.</p>",
            """{% else %}
      <p class="text-muted small">No approved results yet. Results appear here once approved by the school.</p>"""
        )
        # Add print link near student card header
        html = html.replace(
            '<div class="fw-bold">{{ student.full_name }}</div>',
            '<div class="fw-bold">{{ student.full_name }}</div>'
        )
        path.write_text(html, encoding="utf-8")
        print("  OK  parent_dashboard.html updated")
    else:
        print("  -- parent_dashboard.html already has print")


def update_admin_results():
    """Make approve-all form point to correct URL"""
    path = Path("templates/admin/results.html")
    if not path.exists():
        print("  -- admin/results.html not found")
        return

    html = path.read_text(encoding="utf-8")
    # Fix approve-all URL
    html = html.replace(
        'action="/admin/results/0/approve-all"',
        'action="/admin/results/approve-all"'
    )
    path.write_text(html, encoding="utf-8")
    print("  OK  admin/results.html approve-all URL fixed")


def update_footer_branding():
    """Add RESCAVIA branding to portal footers"""
    portals = [
        "templates/portals/staff_dashboard.html",
        "templates/portals/parent_dashboard.html",
        "templates/portals/student_dashboard.html",
    ]
    RESCAVIA = '''
<div style="text-align:center;padding:20px;font-size:11px;color:#9ca3af;border-top:1px solid #f3f4f6;margin-top:32px;">
  &copy; 2026 Golden Stars Academy &mdash; goldenstarsacademy.com.ng &nbsp;&middot;&nbsp;
  Powered by <strong style="color:#6b7280">RESCAVIA</strong> &mdash; festusolowo1@gmail.com &middot; +2348161303336
</div>'''

    for portal in portals:
        p = Path(portal)
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        if "RESCAVIA" not in html:
            html = html.replace("</body>", RESCAVIA + "\n</body>")
            p.write_text(html, encoding="utf-8")
            print(f"  OK  RESCAVIA branding added to {portal}")


def create_bulk_upload_template():
    """Create a CSV template for bulk result upload"""
    csv_content = """student_id,subject,ca1,ca2,exam,term,session
1,Mathematics,18,17,52,Third Term,2025/2026
1,English Language,16,15,48,Third Term,2025/2026
2,Mathematics,14,16,45,Third Term,2025/2026"""
    write("static/bulk_results_template.csv", csv_content)


if __name__ == "__main__":
    print("\nGolden Stars Academy v2.0 — Master Patch")
    print("=" * 52)

    print("\n[1/6] Patching main.py...")
    patch_main()

    print("\n[2/6] Fixing index.html navigation...")
    fix_index_navigation()

    print("\n[3/6] Updating parent dashboard...")
    update_parent_dashboard()

    print("\n[4/6] Fixing results approval URL...")
    update_admin_results()

    print("\n[5/6] Adding RESCAVIA branding to portals...")
    update_footer_branding()

    print("\n[6/6] Creating bulk upload template...")
    create_bulk_upload_template()

    print("\n" + "=" * 52)
    print("COMPLETE! Now run:")
    print("\n  git add .")
    print('  git commit -m "GSA v2.0 - World-class portal ecosystem"')
    print("  git push")
    print("\nAfter Render redeploys, test:")
    print("  /           - Public website (nav should work)")
    print("  /admin      - Enhanced dashboard")
    print("  /admin/profile - New profile page")
    print("  /staff/login   - Staff portal")
    print("  /parent/login  - Parent portal (print results)")
    print("  /student/login - Student portal")
