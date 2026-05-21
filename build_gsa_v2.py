"""
Golden Stars Academy - World-Class School Portal Ecosystem v2.0
Complete rebuild for goldenstarsacademy.com.ng on Truehost
"""

import os
from pathlib import Path

ROOT = Path(".")
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"

def write(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"  OK  {path}")

# ── 1. MAIN.PY ADDITIONS ──────────────────────────────────────────────────
MAIN_ADDITIONS = '''

# ── PROFILE UPDATE ROUTES ─────────────────────────────────────────────────

@app.get("/admin/profile", response_class=HTMLResponse)
def admin_profile(request: Request, db: Session = Depends(get_db),
                  user: User = Depends(require_login)):
    return templates.TemplateResponse("admin/profile.html", ctx(request, db, user=user))

@app.post("/admin/profile")
async def admin_profile_post(request: Request, db: Session = Depends(get_db),
                              user: User = Depends(require_login),
                              name: str = Form(...),
                              current_password: str = Form(""),
                              new_password: str = Form(""),
                              avatar: UploadFile = File(None)):
    u = db.get(User, user.id)
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
    flash(request, "Profile updated.")
    return RedirectResponse("/admin/profile", 302)

# ── STUDENT SEARCH API ────────────────────────────────────────────────────

@app.get("/api/students/search")
def search_students(q: str = "", db: Session = Depends(get_db)):
    students = db.exec(select(Student)).all()
    if q:
        q = q.lower()
        students = [s for s in students if q in s.full_name.lower()
                    or q in s.admission_no.lower()
                    or q in s.class_name.lower()]
    return [{"id": s.id, "name": s.full_name, "class": s.class_name,
             "adm": s.admission_no, "level": s.level} for s in students[:20]]

# ── BULK RESULT UPLOAD API ────────────────────────────────────────────────

@app.post("/staff/results/bulk")
async def staff_bulk_results(request: Request, db: Session = Depends(get_db),
                              file: UploadFile = File(...)):
    s = get_staff(request, db)
    import csv, io
    content = (await file.read()).decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    count = 0
    for row in reader:
        try:
            student_id = int(row.get("student_id", 0))
            st = db.get(Student, student_id)
            if not st: continue
            ca1 = float(row.get("ca1", 0))
            ca2 = float(row.get("ca2", 0))
            exam = float(row.get("exam", 0))
            total = ca1 + ca2 + exam
            grade = "A" if total >= 75 else "B" if total >= 65 else "C" if total >= 55 else "D" if total >= 45 else "F"
            remark = "Excellent" if total >= 75 else "Very Good" if total >= 65 else "Good" if total >= 55 else "Fair" if total >= 45 else "Fail"
            existing = db.exec(select(ExamResult).where(
                ExamResult.student_id == student_id,
                ExamResult.subject == row.get("subject", ""),
                ExamResult.term == row.get("term", "Third Term"),
                ExamResult.session == row.get("session", "2025/2026")
            )).first()
            if existing:
                existing.ca1=ca1; existing.ca2=ca2; existing.exam=exam
                existing.total=total; existing.grade=grade; existing.remark=remark
                existing.approved=False; existing.uploaded_by=s.name
                db.add(existing)
            else:
                db.add(ExamResult(student_id=student_id, student_name=st.full_name,
                                  admission_no=st.admission_no, class_name=st.class_name,
                                  subject=row.get("subject",""), ca1=ca1, ca2=ca2,
                                  exam=exam, total=total, grade=grade, remark=remark,
                                  term=row.get("term","Third Term"),
                                  session=row.get("session","2025/2026"),
                                  uploaded_by=s.name, approved=False))
            count += 1
        except Exception:
            continue
    db.commit()
    flash(request, f"{count} results uploaded successfully. Awaiting approval.")
    return RedirectResponse("/staff/results", 302)

# ── PARENT EDIT ROUTE ─────────────────────────────────────────────────────

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

# ── STAFF TOGGLE STATUS ───────────────────────────────────────────────────

@app.post("/admin/staff/{sid}/toggle")
def admin_toggle_staff(sid: int, request: Request, db: Session = Depends(get_db),
                       user: User = Depends(require_role("superadmin","ict"))):
    s = db.get(StaffUser, sid)
    if s:
        s.status = "inactive" if s.status == "active" else "active"
        db.add(s); db.commit()
        flash(request, f"Staff status updated to {s.status}.")
    return RedirectResponse("/admin/staff", 302)

# ── PRINT RESULT SHEET ────────────────────────────────────────────────────

@app.get("/parent/results/{student_id}/print", response_class=HTMLResponse)
def print_results(student_id: int, request: Request, db: Session = Depends(get_db),
                  term: str = "Third Term", session: str = "2025/2026"):
    p = get_parent(request, db)
    ids = [int(i) for i in p.student_ids.split(",") if i.strip().isdigit()]
    if student_id not in ids:
        raise HTTPException(403)
    student = db.get(Student, student_id)
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

# ── STUDENT CHANGE PASSWORD ───────────────────────────────────────────────

@app.post("/student/change-password")
def student_change_password(request: Request, db: Session = Depends(get_db),
                             new_password: str = Form(...)):
    st = get_student_portal(request, db)
    # Store as attribute in session — for full implementation use a StudentAuth table
    flash(request, "Password change feature coming soon. Contact admin.")
    return RedirectResponse("/student/dashboard", 302)

'''

print("Golden Stars Academy v2.0 - Build Script")
print("=" * 50)

# ── 2. GLOBAL CSS VARIABLES ──────────────────────────────────────────────
GLOBAL_CSS = """
/* ═══════════════════════════════════════════════════════
   GOLDEN STARS ACADEMY — Global Design System
   goldenstarsacademy.com.ng
   Powered by RESCAVIA — festusolowo1@gmail.com
   ═══════════════════════════════════════════════════════ */

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&display=swap');

:root {
  /* Brand Palette */
  --navy:        #0f2340;
  --navy-light:  #1a3a6b;
  --navy-mid:    #234888;
  --gold:        #c9a84c;
  --gold-light:  #e8c96a;
  --gold-pale:   #fdf6e3;
  --crimson:     #b32020;
  --crimson-soft:#f5e8e8;

  /* Semantic */
  --success:     #16a34a;
  --success-bg:  #dcfce7;
  --warning:     #d97706;
  --warning-bg:  #fef3c7;
  --danger:      #dc2626;
  --danger-bg:   #fee2e2;
  --info:        #0891b2;
  --info-bg:     #e0f2fe;

  /* Neutrals */
  --white:       #ffffff;
  --bg:          #f4f7fb;
  --bg-card:     #ffffff;
  --border:      rgba(15,35,64,0.10);
  --border-md:   rgba(15,35,64,0.18);
  --text:        #0f2340;
  --text-muted:  #5a6a82;
  --text-light:  #8fa3bc;

  /* Typography */
  --font-body:   'Plus Jakarta Sans', 'Segoe UI', sans-serif;
  --font-serif:  'Instrument Serif', Georgia, serif;

  /* Spacing */
  --r-sm:  6px;
  --r-md:  10px;
  --r-lg:  16px;
  --r-xl:  24px;

  /* Shadows */
  --shadow-xs: 0 1px 3px rgba(15,35,64,0.06);
  --shadow-sm: 0 2px 8px rgba(15,35,64,0.08);
  --shadow-md: 0 4px 20px rgba(15,35,64,0.10);
  --shadow-lg: 0 12px 40px rgba(15,35,64,0.14);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: var(--font-body);
  color: var(--text);
  background: var(--bg);
  font-size: 14px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
a { text-decoration: none; color: inherit; }
img { max-width: 100%; display: block; }
button { cursor: pointer; font-family: inherit; }
input, select, textarea { font-family: inherit; }

/* Utility */
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); border: 0; }
.truncate { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.badge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 10px; border-radius: 20px;
  font-size: 11px; font-weight: 600; letter-spacing: .3px;
}
.badge-navy    { background: var(--navy); color: #fff; }
.badge-gold    { background: var(--gold-pale); color: #7a5c0a; border: 1px solid var(--gold); }
.badge-success { background: var(--success-bg); color: #14532d; }
.badge-warning { background: var(--warning-bg); color: #78350f; }
.badge-danger  { background: var(--danger-bg);  color: #7f1d1d; }
.badge-info    { background: var(--info-bg);    color: #164e63; }
.badge-muted   { background: #f1f5f9; color: var(--text-muted); }

/* Buttons */
.btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 9px 18px; border-radius: var(--r-md);
  font-size: 13px; font-weight: 600; border: none;
  transition: all .18s; cursor: pointer; white-space: nowrap;
}
.btn-primary   { background: var(--navy); color: #fff; }
.btn-primary:hover { background: var(--navy-mid); transform: translateY(-1px); box-shadow: var(--shadow-sm); }
.btn-gold      { background: var(--gold); color: #fff; }
.btn-gold:hover { background: #b8902a; transform: translateY(-1px); }
.btn-outline   { background: transparent; border: 1.5px solid var(--border-md); color: var(--text); }
.btn-outline:hover { border-color: var(--navy); background: var(--bg); }
.btn-success   { background: var(--success); color: #fff; }
.btn-success:hover { background: #15803d; }
.btn-danger    { background: var(--danger); color: #fff; }
.btn-danger:hover  { background: #b91c1c; }
.btn-sm { padding: 6px 12px; font-size: 12px; }
.btn-lg { padding: 12px 26px; font-size: 15px; }
.btn-icon { padding: 8px; }
.btn-block { width: 100%; justify-content: center; }

/* Cards */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  box-shadow: var(--shadow-xs);
}
.card-body { padding: 20px; }
.card-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
}
.card-title { font-size: 15px; font-weight: 700; }
.card-sub   { font-size: 12px; color: var(--text-muted); margin-top: 2px; }

/* Tables */
.table-wrap { overflow-x: auto; border-radius: var(--r-lg); }
.table {
  width: 100%; border-collapse: collapse; font-size: 13px;
}
.table th {
  padding: 11px 14px; text-align: left;
  font-size: 11px; font-weight: 700; letter-spacing: .5px;
  text-transform: uppercase; color: var(--text-muted);
  background: #f8fafc; border-bottom: 1px solid var(--border);
}
.table td { padding: 12px 14px; border-bottom: 1px solid var(--border); vertical-align: middle; }
.table tbody tr:hover td { background: #f8fafc; }
.table tbody tr:last-child td { border-bottom: none; }

/* Forms */
.form-group { margin-bottom: 16px; }
.form-label { display: block; font-size: 12px; font-weight: 600; color: var(--text-muted); margin-bottom: 5px; letter-spacing: .2px; }
.form-control {
  width: 100%; padding: 10px 14px;
  border: 1.5px solid var(--border-md);
  border-radius: var(--r-md); font-size: 13px;
  background: var(--white); color: var(--text);
  transition: border-color .15s, box-shadow .15s; outline: none;
}
.form-control:focus { border-color: var(--navy); box-shadow: 0 0 0 3px rgba(15,35,64,0.08); }
.form-control::placeholder { color: var(--text-light); }
.form-hint { font-size: 11px; color: var(--text-muted); margin-top: 4px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
@media (max-width: 600px) { .form-row { grid-template-columns: 1fr; } }

/* Alert */
.alert {
  padding: 12px 16px; border-radius: var(--r-md);
  font-size: 13px; display: flex; align-items: flex-start; gap: 10px;
  border: 1px solid transparent; margin-bottom: 16px;
}
.alert-success { background: var(--success-bg); color: #14532d; border-color: #bbf7d0; }
.alert-error   { background: var(--danger-bg);  color: #7f1d1d; border-color: #fecaca; }
.alert-warning { background: var(--warning-bg); color: #78350f; border-color: #fde68a; }
.alert-info    { background: var(--info-bg);    color: #164e63; border-color: #bae6fd; }

/* Stat Cards */
.stat-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px,1fr)); gap: 14px; margin-bottom: 24px; }
.stat-card {
  background: var(--bg-card); border-radius: var(--r-lg);
  padding: 18px; border: 1px solid var(--border);
  position: relative; overflow: hidden;
}
.stat-card::before {
  content: ''; position: absolute; top: 0; left: 0;
  width: 4px; height: 100%;
}
.stat-navy::before  { background: var(--navy); }
.stat-gold::before  { background: var(--gold); }
.stat-green::before { background: var(--success); }
.stat-red::before   { background: var(--danger); }
.stat-icon { font-size: 22px; margin-bottom: 10px; }
.stat-val { font-size: 26px; font-weight: 800; color: var(--text); line-height: 1; }
.stat-label { font-size: 11px; color: var(--text-muted); margin-top: 4px; text-transform: uppercase; letter-spacing: .4px; font-weight: 600; }
.stat-delta { font-size: 11px; color: var(--success); margin-top: 4px; }

/* Empty State */
.empty-state { text-align: center; padding: 48px 20px; color: var(--text-muted); }
.empty-state i { font-size: 40px; margin-bottom: 12px; opacity: .4; display: block; }
.empty-state h4 { font-size: 15px; font-weight: 600; color: var(--text); margin-bottom: 6px; }
.empty-state p { font-size: 13px; }

/* Skeleton */
.sk { background: linear-gradient(90deg,#f0f0f0 25%,#e0e0e0 50%,#f0f0f0 75%); background-size: 200% 100%; animation: sk 1.4s infinite; border-radius: 6px; min-height: 14px; }
@keyframes sk { 0%{background-position:200% 0}100%{background-position:-200% 0} }

/* Responsive */
@media (max-width: 768px) {
  .stat-grid { grid-template-columns: 1fr 1fr; }
}
"""

write("static/css/global.css", GLOBAL_CSS)

# ── 3. ENHANCED INDEX.HTML ─────────────────────────────────────────────
# The key fix: remove the rogue Bootstrap carousel and fix the carousel-wrap
# Also add Bootstrap CDN properly for components that use it

INDEX_FIX_JS = """
<script>
// ── FIX: Ensure carousel-slide SVG doesn't bleed through pages ──
document.querySelectorAll('.carousel-wrap svg').forEach(function(svg){
  svg.style.pointerEvents = 'none';
});

// ── FIX: Page navigation z-index ──
function showPage(id){
  document.querySelectorAll('.page').forEach(function(p){
    p.style.display = 'none';
    p.classList.remove('active');
  });
  var pg = document.getElementById('pg-'+id) || document.getElementById('pg-home');
  pg.style.display = 'block';
  pg.classList.add('active');
  window.scrollTo({top:0,behavior:'smooth'});
  document.querySelectorAll('.nav-link').forEach(function(l){l.classList.remove('active');});
}

// ── FIX: Init page on load ──
document.addEventListener('DOMContentLoaded', function(){
  document.querySelectorAll('.page').forEach(function(p){
    if(!p.classList.contains('active')) p.style.display = 'none';
  });
});
</script>
"""

print("Index.html fix JS ready")

# ── 4. ENHANCED ADMIN BASE ─────────────────────────────────────────────
ADMIN_BASE_V2 = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{% block title %}Admin{% endblock %} · Golden Stars Academy</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css"/>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
/* ── RESET & BASE ──────────────────────────────────────── */
*{box-sizing:border-box;margin:0;padding:0;}
:root{
  --navy:#0f2340;--navy-l:#1a3a6b;--navy-m:#234888;
  --gold:#c9a84c;--gold-l:#fdf6e3;
  --bg:#f0f4f9;--card:#fff;--border:rgba(15,35,64,.1);--border-m:rgba(15,35,64,.18);
  --txt:#0f2340;--muted:#5a6a82;--light:#8fa3bc;
  --green:#16a34a;--green-bg:#dcfce7;
  --amber:#d97706;--amber-bg:#fef3c7;
  --red:#dc2626;--red-bg:#fee2e2;
  --blue:#0891b2;--blue-bg:#e0f2fe;
  --sb-w:240px;--top-h:60px;
  --r:10px;--r-lg:16px;
  --sh-xs:0 1px 3px rgba(15,35,64,.06);
  --sh-sm:0 2px 8px rgba(15,35,64,.08);
  --sh-md:0 4px 20px rgba(15,35,64,.10);
}
body{font-family:'Plus Jakarta Sans','Segoe UI',sans-serif;background:var(--bg);color:var(--txt);font-size:13.5px;line-height:1.55;-webkit-font-smoothing:antialiased;}
a{text-decoration:none;color:inherit;}
button{cursor:pointer;font-family:inherit;}
input,select,textarea{font-family:inherit;}

/* ── SIDEBAR ───────────────────────────────────────────── */
.sb{
  position:fixed;top:0;left:0;height:100vh;width:var(--sb-w);
  background:var(--navy);color:#fff;
  display:flex;flex-direction:column;
  z-index:200;overflow-y:auto;overflow-x:hidden;
  transition:transform .25s;
}
.sb-head{
  padding:0 18px;height:var(--top-h);
  display:flex;align-items:center;gap:10px;
  border-bottom:1px solid rgba(255,255,255,.08);flex-shrink:0;
}
.sb-logo{width:36px;height:36px;border-radius:50%;object-fit:contain;flex-shrink:0;}
.sb-brand{font-size:12px;font-weight:700;line-height:1.25;}
.sb-brand small{display:block;font-size:10px;opacity:.4;font-weight:400;margin-top:1px;}
.sb-body{flex:1;padding:10px 0;overflow-y:auto;}
.sb-sec{
  font-size:9.5px;font-weight:800;letter-spacing:.08em;
  text-transform:uppercase;color:rgba(255,255,255,.3);
  padding:16px 18px 5px;
}
.sb-a{
  display:flex;align-items:center;gap:9px;
  padding:9px 12px 9px 18px;
  font-size:12.5px;color:rgba(255,255,255,.68);
  border-left:3px solid transparent;
  transition:all .15s;border-radius:0 8px 8px 0;margin-right:8px;
}
.sb-a:hover{background:rgba(255,255,255,.07);color:#fff;}
.sb-a.on{background:rgba(201,168,76,.15);border-left-color:var(--gold);color:#fff;font-weight:600;}
.sb-a i{font-size:17px;flex-shrink:0;}
.sb-a .badge-count{
  margin-left:auto;background:var(--red);color:#fff;
  font-size:9px;font-weight:700;padding:1px 6px;border-radius:10px;
}
.sb-foot{
  padding:12px 14px;border-top:1px solid rgba(255,255,255,.08);flex-shrink:0;
}
.sb-user{display:flex;align-items:center;gap:9px;margin-bottom:9px;}
.sb-av{
  width:32px;height:32px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-weight:700;font-size:12px;color:#fff;flex-shrink:0;
  overflow:hidden;
}
.sb-av img{width:100%;height:100%;object-fit:cover;}
.sb-uname{font-size:12px;font-weight:700;line-height:1.2;}
.sb-urole{font-size:10px;opacity:.4;}
.sb-out{
  width:100%;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);
  color:#fff;padding:7px;border-radius:7px;font-size:11.5px;
  display:flex;align-items:center;justify-content:center;gap:6px;
}
.sb-out:hover{background:rgba(255,255,255,.14);}

/* ── TOPBAR ────────────────────────────────────────────── */
.topbar{
  position:fixed;top:0;left:var(--sb-w);right:0;height:var(--top-h);
  background:var(--card);border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
  padding:0 24px;z-index:100;box-shadow:var(--sh-xs);
}
.topbar-left{display:flex;align-items:center;gap:14px;}
.topbar-title{font-size:15px;font-weight:700;}
.topbar-sub{font-size:11px;color:var(--muted);}
.topbar-right{display:flex;align-items:center;gap:10px;}
.topbar-btn{
  width:36px;height:36px;border-radius:8px;border:1px solid var(--border-m);
  background:transparent;color:var(--muted);
  display:flex;align-items:center;justify-content:center;font-size:18px;
}
.topbar-btn:hover{background:var(--bg);color:var(--txt);}
.role-badge{
  padding:4px 12px;border-radius:20px;font-size:11px;font-weight:700;
  letter-spacing:.3px;
}

/* ── MAIN ──────────────────────────────────────────────── */
.main{margin-left:var(--sb-w);padding-top:var(--top-h);min-height:100vh;}
.content{padding:24px;}

/* ── FLASH ─────────────────────────────────────────────── */
.flash{
  padding:12px 16px;border-radius:var(--r);font-size:13px;
  display:flex;align-items:center;gap:10px;margin-bottom:16px;
  border:1px solid transparent;
}
.flash-ok {background:var(--green-bg);color:#14532d;border-color:#bbf7d0;}
.flash-err{background:var(--red-bg);color:#7f1d1d;border-color:#fecaca;}

/* ── CARDS ─────────────────────────────────────────────── */
.card{
  background:var(--card);border-radius:var(--r-lg);
  border:1px solid var(--border);box-shadow:var(--sh-xs);
  margin-bottom:18px;
}
.card-hd{
  padding:16px 20px;border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
  flex-wrap:wrap;gap:10px;
}
.card-title{font-size:15px;font-weight:700;}
.card-sub{font-size:11.5px;color:var(--muted);margin-top:2px;}
.card-body{padding:20px;}

/* ── STAT CARDS ────────────────────────────────────────── */
.sg{display:grid;grid-template-columns:repeat(auto-fill,minmax(155px,1fr));gap:14px;margin-bottom:22px;}
.sc{
  background:var(--card);border-radius:var(--r-lg);
  padding:18px 18px 16px;border:1px solid var(--border);
  box-shadow:var(--sh-xs);position:relative;overflow:hidden;
}
.sc::before{content:'';position:absolute;top:0;left:0;width:4px;height:100%;}
.sc-navy::before{background:var(--navy);}
.sc-gold::before{background:var(--gold);}
.sc-green::before{background:var(--green);}
.sc-red::before  {background:var(--red);}
.sc-blue::before {background:var(--blue);}
.sc-i{font-size:22px;margin-bottom:10px;color:var(--muted);}
.sc-v{font-size:28px;font-weight:800;line-height:1;}
.sc-l{font-size:10.5px;color:var(--muted);margin-top:4px;text-transform:uppercase;letter-spacing:.5px;font-weight:700;}

/* ── TABLE ─────────────────────────────────────────────── */
.tbl-wrap{overflow-x:auto;}
.tbl{width:100%;border-collapse:collapse;font-size:13px;}
.tbl th{
  padding:10px 14px;text-align:left;
  font-size:10.5px;font-weight:700;letter-spacing:.5px;
  text-transform:uppercase;color:var(--muted);
  background:#f8fafc;border-bottom:1px solid var(--border);
}
.tbl td{padding:12px 14px;border-bottom:1px solid var(--border);vertical-align:middle;}
.tbl tbody tr:hover td{background:#f8fafc;}
.tbl tbody tr:last-child td{border-bottom:none;}

/* ── FORMS ─────────────────────────────────────────────── */
.fg{margin-bottom:14px;}
.fg label{display:block;font-size:11.5px;font-weight:700;color:var(--muted);margin-bottom:5px;letter-spacing:.2px;}
.fg input,.fg select,.fg textarea{
  width:100%;padding:9px 13px;
  border:1.5px solid var(--border-m);border-radius:var(--r);
  font-size:13px;background:var(--card);color:var(--txt);
  transition:border-color .15s,box-shadow .15s;outline:none;
}
.fg input:focus,.fg select:focus,.fg textarea:focus{
  border-color:var(--navy);box-shadow:0 0 0 3px rgba(15,35,64,.08);
}
.fg textarea{resize:vertical;min-height:80px;}
.fg input[type=file]{padding:7px;}
.fg-row{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
@media(max-width:640px){.fg-row{grid-template-columns:1fr;}}

/* ── BUTTONS ───────────────────────────────────────────── */
.btn{
  display:inline-flex;align-items:center;gap:7px;
  padding:9px 18px;border-radius:var(--r);border:none;
  font-size:13px;font-weight:600;cursor:pointer;
  transition:all .18s;white-space:nowrap;
}
.btn:hover{transform:translateY(-1px);box-shadow:var(--sh-sm);}
.btn:active{transform:translateY(0);}
.btn-primary{background:var(--navy);color:#fff;}
.btn-primary:hover{background:var(--navy-m);}
.btn-gold{background:var(--gold);color:#fff;}
.btn-gold:hover{background:#b8902a;}
.btn-success{background:var(--green);color:#fff;}
.btn-success:hover{background:#15803d;}
.btn-danger{background:var(--red);color:#fff;}
.btn-danger:hover{background:#b91c1c;}
.btn-outline{background:transparent;border:1.5px solid var(--border-m);color:var(--txt);}
.btn-outline:hover{border-color:var(--navy);background:var(--bg);}
.btn-sm{padding:6px 12px;font-size:12px;border-radius:7px;}
.btn-xs{padding:4px 9px;font-size:11px;border-radius:6px;}

/* ── BADGES ────────────────────────────────────────────── */
.badge{
  display:inline-flex;align-items:center;gap:4px;
  padding:3px 10px;border-radius:20px;
  font-size:11px;font-weight:700;letter-spacing:.3px;
}
.b-navy  {background:var(--navy);color:#fff;}
.b-gold  {background:var(--gold-l);color:#7a5c0a;border:1px solid var(--gold);}
.b-green {background:var(--green-bg);color:#14532d;}
.b-amber {background:var(--amber-bg);color:#78350f;}
.b-red   {background:var(--red-bg);color:#7f1d1d;}
.b-blue  {background:var(--blue-bg);color:#164e63;}
.b-gray  {background:#f1f5f9;color:var(--muted);}
.b-active  {background:var(--green-bg);color:#14532d;}
.b-inactive{background:#f1f5f9;color:var(--muted);}
.b-pending {background:var(--amber-bg);color:#78350f;}
.b-approved{background:var(--green-bg);color:#14532d;}
.b-sa{background:#ede9fe;color:#5b21b6;}
.b-ic{background:#dcfce7;color:#14532d;}
.b-me{background:#e0f2fe;color:#164e63;}
.b-bu{background:#fef3c7;color:#78350f;}

/* ── MISC ──────────────────────────────────────────────── */
.prev{width:90px;height:90px;border-radius:8px;object-fit:contain;border:1px solid var(--border);background:var(--bg);}
.sk{background:linear-gradient(90deg,#f0f0f0 25%,#e0e0e0 50%,#f0f0f0 75%);background-size:200% 100%;animation:sk 1.4s infinite;border-radius:6px;min-height:14px;}
@keyframes sk{0%{background-position:200% 0}100%{background-position:-200% 0}}
.empty{text-align:center;padding:48px 20px;color:var(--muted);}
.empty i{font-size:36px;margin-bottom:12px;opacity:.35;display:block;}
.empty h4{font-size:15px;font-weight:700;color:var(--txt);margin-bottom:6px;}
.empty p{font-size:13px;}
.page-hd{display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:22px;}
.page-hd-left h2{font-size:21px;font-weight:800;}
.page-hd-left p{font-size:13px;color:var(--muted);margin-top:3px;}
.divider{height:1px;background:var(--border);margin:20px 0;}
.info-box{background:#eff6ff;border:1px solid #bfdbfe;border-radius:var(--r);padding:12px 15px;font-size:13px;color:#1e40af;display:flex;gap:9px;align-items:flex-start;}
.warn-box{background:var(--amber-bg);border:1px solid #fde68a;border-radius:var(--r);padding:12px 15px;font-size:13px;color:#78350f;display:flex;gap:9px;}
.avatar{
  width:36px;height:36px;border-radius:50%;
  display:inline-flex;align-items:center;justify-content:center;
  font-weight:700;font-size:13px;flex-shrink:0;overflow:hidden;
}
.avatar img{width:100%;height:100%;object-fit:cover;}

/* ── MOBILE SIDEBAR ────────────────────────────────────── */
@media(max-width:900px){
  .sb{transform:translateX(-100%);}
  .sb.open{transform:translateX(0);}
  .main{margin-left:0;}
  .topbar{left:0;}
  .mob-toggle{display:flex!important;}
}
.mob-toggle{display:none;background:none;border:none;color:var(--muted);font-size:22px;margin-right:8px;}
.sb-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:199;}
.sb-overlay.show{display:block;}

/* ── MODAL ─────────────────────────────────────────────── */
.modal-bg{
  display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);
  z-index:500;align-items:center;justify-content:center;padding:20px;
}
.modal-bg.open{display:flex;}
.modal{
  background:var(--card);border-radius:var(--r-lg);
  box-shadow:var(--sh-lg);width:100%;max-width:560px;
  max-height:90vh;overflow-y:auto;
}
.modal-head{
  padding:18px 22px;border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
}
.modal-head h3{font-size:16px;font-weight:700;}
.modal-body{padding:22px;}
.modal-foot{padding:16px 22px;border-top:1px solid var(--border);display:flex;justify-content:flex-end;gap:10px;}
.modal-close{background:none;border:none;font-size:22px;color:var(--muted);line-height:1;}
.modal-close:hover{color:var(--txt);}

/* ── SEARCH BAR ────────────────────────────────────────── */
.search-bar{
  position:relative;flex:1;min-width:200px;
}
.search-bar i{
  position:absolute;left:11px;top:50%;transform:translateY(-50%);
  color:var(--muted);font-size:16px;pointer-events:none;
}
.search-bar input{
  padding-left:36px!important;
}

/* ── ACCORDION ─────────────────────────────────────────── */
.acc-item{border:1px solid var(--border);border-radius:var(--r);margin-bottom:8px;}
.acc-head{
  width:100%;background:none;border:none;text-align:left;
  padding:13px 16px;display:flex;align-items:center;justify-content:space-between;
  font-size:13.5px;font-weight:600;color:var(--txt);
}
.acc-head i.chevron{transition:transform .2s;}
.acc-head.open i.chevron{transform:rotate(180deg);}
.acc-body{padding:0 16px;max-height:0;overflow:hidden;transition:max-height .25s,padding .25s;}
.acc-body.open{max-height:600px;padding:0 16px 16px;}

/* ── TIMELINE ──────────────────────────────────────────── */
.timeline{position:relative;padding-left:28px;}
.timeline::before{content:'';position:absolute;left:8px;top:0;bottom:0;width:2px;background:var(--border);}
.tl-item{position:relative;margin-bottom:18px;}
.tl-dot{
  position:absolute;left:-24px;top:3px;
  width:10px;height:10px;border-radius:50%;
  background:var(--card);border:2px solid var(--navy);
}
.tl-dot.done{background:var(--green);border-color:var(--green);}
.tl-title{font-size:13px;font-weight:600;}
.tl-sub{font-size:12px;color:var(--muted);margin-top:2px;}

/* ── PROGRESS ──────────────────────────────────────────── */
.progress{height:8px;background:#f1f5f9;border-radius:4px;overflow:hidden;}
.progress-bar{height:100%;border-radius:4px;background:var(--navy);transition:width .4s;}
.progress-bar.gold{background:var(--gold);}
.progress-bar.green{background:var(--green);}

/* ── DATA VIZ MINI ─────────────────────────────────────── */
.grade-pill{
  display:inline-block;width:30px;height:30px;border-radius:50%;
  font-size:12px;font-weight:800;text-align:center;line-height:30px;
}
.grade-A{background:#dcfce7;color:#14532d;}
.grade-B{background:#dbeafe;color:#1e3a8a;}
.grade-C{background:#fef9c3;color:#713f12;}
.grade-D{background:#ffedd5;color:#7c2d12;}
.grade-F{background:#fee2e2;color:#7f1d1d;}
</style>
</head>
<body>

<!-- Sidebar Overlay (mobile) -->
<div class="sb-overlay" id="sbOverlay" onclick="closeSidebar()"></div>

<!-- ── SIDEBAR ────────────────────────────────────────── -->
<div class="sb" id="sidebar">
  <div class="sb-head">
    {% if school_logo and school_logo.url %}
      <img class="sb-logo" src="{{ school_logo.url }}" alt="GSA"/>
    {% else %}
      <svg class="sb-logo" viewBox="0 0 300 340" xmlns="http://www.w3.org/2000/svg" style="background:rgba(255,255,255,.08);border-radius:50%">
        <path d="M150 8 L272 54 L272 182 Q272 284 150 332 Q28 284 28 182 L28 54 Z" fill="#E8B830"/>
        <path d="M150 22 L258 62 L258 182 Q258 272 150 316 Q42 272 42 182 L42 62 Z" fill="#CC2200"/>
        <path d="M65 110 L235 110 L235 215 Q235 255 150 285 Q65 255 65 215 Z" fill="#1a3575"/>
        <polygon points="150,95 155,110 171,110 158,120 163,135 150,126 137,135 142,120 129,110 145,110" fill="#F5C518"/>
      </svg>
    {% endif %}
    <div class="sb-brand">Golden Stars<small>Admin Portal · GSA</small></div>
  </div>

  <nav class="sb-body">
    <div class="sb-sec">Main</div>
    <a href="/admin" class="sb-a {% if request.url.path=='/admin' %}on{% endif %}">
      <i class="ti ti-layout-dashboard"></i> Dashboard
    </a>
    <a href="/" target="_blank" class="sb-a">
      <i class="ti ti-world"></i> View Website
    </a>

    {% if current_user.role in ['superadmin','ict'] %}
    <div class="sb-sec">Administration</div>
    {% if current_user.role=='superadmin' %}
    <a href="/admin/users" class="sb-a {% if '/admin/users' in request.url.path %}on{% endif %}">
      <i class="ti ti-users"></i> User Management
    </a>
    {% endif %}
    <a href="/admin/staff" class="sb-a {% if '/admin/staff' in request.url.path %}on{% endif %}">
      <i class="ti ti-id-badge"></i> Staff Accounts
    </a>
    <a href="/admin/parents" class="sb-a {% if '/admin/parents' in request.url.path %}on{% endif %}">
      <i class="ti ti-heart-handshake"></i> Parent Accounts
    </a>
    {% endif %}

    {% if current_user.role in ['superadmin','ict'] %}
    <div class="sb-sec">Content</div>
    <a href="/admin/news" class="sb-a {% if '/admin/news' in request.url.path %}on{% endif %}">
      <i class="ti ti-news"></i> News & Insights
    </a>
    <a href="/admin/gallery" class="sb-a {% if '/admin/gallery' in request.url.path %}on{% endif %}">
      <i class="ti ti-camera"></i> Gallery & Team
    </a>
    <a href="/admin/calendar" class="sb-a {% if '/admin/calendar' in request.url.path %}on{% endif %}">
      <i class="ti ti-calendar-event"></i> Calendar
    </a>
    <a href="/admin/siteinfo" class="sb-a {% if '/admin/siteinfo' in request.url.path %}on{% endif %}">
      <i class="ti ti-settings-2"></i> Site Information
    </a>
    <a href="/admin/logos" class="sb-a {% if '/admin/logos' in request.url.path %}on{% endif %}">
      <i class="ti ti-photo-star"></i> Logo Manager
    </a>
    {% endif %}

    {% if current_user.role in ['superadmin','bursar'] %}
    <div class="sb-sec">Finance</div>
    <a href="/admin/fees" class="sb-a {% if '/admin/fees' in request.url.path %}on{% endif %}">
      <i class="ti ti-currency-naira"></i> Fee Management
    </a>
    {% endif %}

    {% if current_user.role in ['superadmin','ict'] %}
    <div class="sb-sec">Academics</div>
    <a href="/admin/results" class="sb-a {% if '/admin/results' in request.url.path %}on{% endif %}">
      <i class="ti ti-chart-bar"></i> Results Approval
      {% set pending_count = pending_results_count | default(0) %}
      {% if pending_count > 0 %}
      <span class="badge-count">{{ pending_count }}</span>
      {% endif %}
    </a>
    {% endif %}

    <div class="sb-sec">Portals</div>
    <a href="/staff/login" target="_blank" class="sb-a">
      <i class="ti ti-door-enter"></i> Staff Portal
    </a>
    <a href="/parent/login" target="_blank" class="sb-a">
      <i class="ti ti-door-enter"></i> Parent Portal
    </a>
    <a href="/student/login" target="_blank" class="sb-a">
      <i class="ti ti-door-enter"></i> Student Portal
    </a>
  </nav>

  <div class="sb-foot">
    <div class="sb-user">
      {% set rc={'superadmin':'#7c3aed','ict':'#16a34a','media':'#0891b2','bursar':'#b45309'} %}
      <div class="sb-av" style="background:{{ rc.get(current_user.role,'#1a3a6b') }}">
        {% if current_user.avatar and current_user.avatar.startswith('/') %}
          <img src="{{ current_user.avatar }}" alt="{{ current_user.name }}"/>
        {% else %}
          {{ current_user.avatar or current_user.name[:2].upper() }}
        {% endif %}
      </div>
      <div>
        <div class="sb-uname">{{ current_user.name.split()[0] }}</div>
        <div class="sb-urole">{{ current_user.role }}</div>
      </div>
    </div>
    <a href="/admin/profile" class="sb-out" style="margin-bottom:6px;">
      <i class="ti ti-user-circle"></i> My Profile
    </a>
    <a href="/admin/logout"><button class="sb-out"><i class="ti ti-logout"></i> Sign Out</button></a>
  </div>
</div>

<!-- ── TOPBAR ─────────────────────────────────────────── -->
<div class="topbar">
  <div class="topbar-left">
    <button class="mob-toggle" onclick="openSidebar()">
      <i class="ti ti-menu-2"></i>
    </button>
    <div>
      <div class="topbar-title">{% block page_title %}Dashboard{% endblock %}</div>
      <div class="topbar-sub">goldenstarsacademy.com.ng · Admin Panel</div>
    </div>
  </div>
  <div class="topbar-right">
    <a href="/" target="_blank">
      <button class="topbar-btn" title="View Website"><i class="ti ti-world"></i></button>
    </a>
    <a href="/admin/profile">
      <button class="topbar-btn" title="Profile"><i class="ti ti-user-circle"></i></button>
    </a>
    {% set rc={'superadmin':'b-sa','ict':'b-ic','media':'b-me','bursar':'b-bu'} %}
    <span class="badge {{ rc.get(current_user.role,'b-gray') }}">
      {{ current_user.role|title }}
    </span>
  </div>
</div>

<!-- ── CONTENT ────────────────────────────────────────── -->
<main class="main">
  <div class="content">
    {% for f in flash_msgs %}
    <div class="flash {{ 'flash-ok' if f.cat=='success' else 'flash-err' }}">
      <i class="ti ti-{{ 'circle-check' if f.cat=='success' else 'alert-circle' }}"></i>
      {{ f.msg }}
    </div>
    {% endfor %}
    {% block content %}{% endblock %}
  </div>
</main>

<!-- ── FOOTER ─────────────────────────────────────────── -->
<footer style="margin-left:var(--sb-w);padding:14px 24px;border-top:1px solid var(--border);background:var(--card);display:flex;justify-content:space-between;align-items:center;font-size:11px;color:var(--light);">
  <span>&copy; 2026 Golden Stars Academy, GRA Gbessa, Abuja. All rights reserved.</span>
  <span>Powered by <strong style="color:var(--muted)">RESCAVIA</strong> &mdash; festusolowo1@gmail.com &middot; +2348161303336</span>
</footer>

<script>
function openSidebar(){
  document.getElementById('sidebar').classList.add('open');
  document.getElementById('sbOverlay').classList.add('show');
}
function closeSidebar(){
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('sbOverlay').classList.remove('show');
}
function openModal(id){document.getElementById(id).classList.add('open');}
function closeModal(id){document.getElementById(id).classList.remove('open');}
document.querySelectorAll('.modal-bg').forEach(m=>{
  m.addEventListener('click',function(e){if(e.target===this)this.classList.remove('open');});
});
document.querySelectorAll('.acc-head').forEach(btn=>{
  btn.addEventListener('click',function(){
    this.classList.toggle('open');
    const body=this.nextElementSibling;
    body.classList.toggle('open');
  });
});
function filterTable(input,tableId){
  const q=input.value.toLowerCase();
  document.querySelectorAll('#'+tableId+' tbody tr').forEach(row=>{
    row.style.display=row.textContent.toLowerCase().includes(q)?'':'none';
  });
}
</script>
</body>
</html>"""

write("templates/admin/base.html", ADMIN_BASE_V2)

# ── 5. ENHANCED ADMIN DASHBOARD ───────────────────────────────────────────
DASHBOARD = """{% extends "admin/base.html" %}
{% block title %}Dashboard{% endblock %}
{% block page_title %}Dashboard{% endblock %}
{% block content %}

<div class="sg">
  <div class="sc sc-navy">
    <div class="sc-i"><i class="ti ti-users"></i></div>
    <div class="sc-v">{{ counts.users }}</div>
    <div class="sc-l">Admin Users</div>
  </div>
  <div class="sc sc-gold">
    <div class="sc-i"><i class="ti ti-id-badge"></i></div>
    <div class="sc-v">{{ counts.staff }}</div>
    <div class="sc-l">Staff Members</div>
  </div>
  <div class="sc sc-green">
    <div class="sc-i"><i class="ti ti-school"></i></div>
    <div class="sc-v">{{ counts.students }}</div>
    <div class="sc-l">Students Enrolled</div>
  </div>
  <div class="sc sc-blue">
    <div class="sc-i"><i class="ti ti-heart-handshake"></i></div>
    <div class="sc-v">{{ counts.parents }}</div>
    <div class="sc-l">Parent Accounts</div>
  </div>
  <div class="sc sc-red">
    <div class="sc-i"><i class="ti ti-chart-bar"></i></div>
    <div class="sc-v">{{ counts.pending_results }}</div>
    <div class="sc-l">Pending Results</div>
  </div>
  <div class="sc sc-gold">
    <div class="sc-i"><i class="ti ti-news"></i></div>
    <div class="sc-v">{{ counts.news }}</div>
    <div class="sc-l">News Posts</div>
  </div>
</div>

{% if counts.pending_results > 0 %}
<div class="warn-box" style="margin-bottom:18px;">
  <i class="ti ti-alert-triangle" style="font-size:18px;flex-shrink:0;margin-top:1px;"></i>
  <div>
    <strong>{{ counts.pending_results }} result(s) awaiting approval.</strong>
    <a href="/admin/results" style="color:var(--amber);text-decoration:underline;margin-left:6px;">Review now &rarr;</a>
  </div>
</div>
{% endif %}

{% if access_error %}
<div class="flash flash-err" style="margin-bottom:18px;">
  <i class="ti ti-lock"></i> You don't have permission to access that section.
</div>
{% endif %}

<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;">

  <!-- Recent News -->
  <div class="card">
    <div class="card-hd">
      <div>
        <div class="card-title">Recent News</div>
        <div class="card-sub">Latest published posts</div>
      </div>
      <a href="/admin/news" class="btn btn-sm btn-outline">View All</a>
    </div>
    <div class="tbl-wrap">
      <table class="tbl">
        <thead><tr><th>Title</th><th>Date</th><th>Status</th></tr></thead>
        <tbody>
          {% for n in recent_news %}
          <tr>
            <td style="font-weight:600;max-width:200px;" class="truncate">{{ n.title }}</td>
            <td style="color:var(--muted);font-size:12px;">{{ n.date }}</td>
            <td>
              {% if n.published %}
              <span class="badge b-green">Live</span>
              {% else %}
              <span class="badge b-gray">Draft</span>
              {% endif %}
            </td>
          </tr>
          {% else %}
          <tr><td colspan="3" style="text-align:center;padding:24px;color:var(--muted);">No news posts yet.</td></tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>

  <!-- Pending Fees -->
  <div class="card">
    <div class="card-hd">
      <div>
        <div class="card-title">Pending Fees</div>
        <div class="card-sub">Awaiting approval</div>
      </div>
      <a href="/admin/fees" class="btn btn-sm btn-outline">Manage</a>
    </div>
    <div class="tbl-wrap">
      <table class="tbl">
        <thead><tr><th>Level</th><th>Term</th><th>Amount</th><th>Action</th></tr></thead>
        <tbody>
          {% for f in pending_fees %}
          <tr>
            <td style="font-weight:600;">{{ f.level }}</td>
            <td style="color:var(--muted);font-size:12px;">{{ f.term }}</td>
            <td style="font-weight:700;color:var(--navy);">&#8358;{{ "{:,.0f}".format(f.amount) }}</td>
            <td>
              <form method="post" action="/admin/fees/{{ f.id }}/approve" style="display:inline;">
                <button class="btn btn-xs btn-success">Approve</button>
              </form>
            </td>
          </tr>
          {% else %}
          <tr><td colspan="4" style="text-align:center;padding:24px;color:var(--muted);">All fees approved.</td></tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>

</div>

<!-- Quick Actions -->
<div class="card" style="margin-top:18px;">
  <div class="card-hd">
    <div class="card-title">Quick Actions</div>
    <div class="card-sub">Common tasks</div>
  </div>
  <div class="card-body" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;">
    <a href="/admin/staff" class="btn btn-outline" style="flex-direction:column;gap:6px;padding:16px;text-align:center;">
      <i class="ti ti-user-plus" style="font-size:22px;color:var(--navy);"></i>
      <span>Add Staff</span>
    </a>
    <a href="/admin/parents" class="btn btn-outline" style="flex-direction:column;gap:6px;padding:16px;text-align:center;">
      <i class="ti ti-heart-handshake" style="font-size:22px;color:var(--gold);"></i>
      <span>Add Parent</span>
    </a>
    <a href="/admin/results" class="btn btn-outline" style="flex-direction:column;gap:6px;padding:16px;text-align:center;">
      <i class="ti ti-chart-bar" style="font-size:22px;color:var(--green);"></i>
      <span>Approve Results</span>
    </a>
    <a href="/admin/news/create" class="btn btn-outline" style="flex-direction:column;gap:6px;padding:16px;text-align:center;">
      <i class="ti ti-news" style="font-size:22px;color:var(--blue);"></i>
      <span>Post News</span>
    </a>
    <a href="/admin/fees/create" class="btn btn-outline" style="flex-direction:column;gap:6px;padding:16px;text-align:center;">
      <i class="ti ti-currency-naira" style="font-size:22px;color:var(--amber);"></i>
      <span>Add Fee</span>
    </a>
    <a href="/admin/siteinfo" class="btn btn-outline" style="flex-direction:column;gap:6px;padding:16px;text-align:center;">
      <i class="ti ti-settings-2" style="font-size:22px;color:var(--muted);"></i>
      <span>Site Settings</span>
    </a>
  </div>
</div>

<p style="text-align:center;font-size:11px;color:var(--light);margin-top:24px;">
  Powered by <strong>RESCAVIA</strong> &mdash; festusolowo1@gmail.com &middot; +2348161303336
</p>

{% endblock %}"""

write("templates/admin/dashboard.html", DASHBOARD)

# ── 6. PRINTABLE RESULT SHEET ─────────────────────────────────────────────
RESULT_SHEET = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Result Sheet &mdash; {{ student.full_name }}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Plus Jakarta Sans',sans-serif;color:#0f2340;background:#fff;font-size:13px;}
.page{max-width:800px;margin:0 auto;padding:32px;}
.header{display:flex;align-items:center;gap:20px;border-bottom:3px solid #0f2340;padding-bottom:16px;margin-bottom:20px;}
.logo{width:80px;height:80px;object-fit:contain;}
.logo-fallback{width:80px;height:80px;border-radius:50%;background:#0f2340;display:flex;align-items:center;justify-content:center;}
.school-name{font-size:22px;font-weight:800;color:#0f2340;line-height:1.2;}
.school-sub{font-size:12px;color:#5a6a82;margin-top:3px;}
.school-motto{font-size:11px;color:#c9a84c;font-weight:700;letter-spacing:.5px;margin-top:4px;}
.report-title{
  background:#0f2340;color:#fff;text-align:center;
  padding:10px;font-size:14px;font-weight:700;letter-spacing:1px;
  border-radius:6px;margin-bottom:16px;
}
.student-info{
  display:grid;grid-template-columns:1fr 1fr;gap:10px;
  background:#f4f7fb;border-radius:8px;padding:14px;margin-bottom:20px;
}
.si-item label{font-size:10px;font-weight:700;color:#5a6a82;text-transform:uppercase;letter-spacing:.5px;display:block;margin-bottom:2px;}
.si-item span{font-size:13px;font-weight:600;color:#0f2340;}
table{width:100%;border-collapse:collapse;margin-bottom:20px;}
thead tr{background:#0f2340;color:#fff;}
th{padding:10px 12px;text-align:left;font-size:11px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;}
td{padding:9px 12px;border-bottom:1px solid #e5e9f0;}
tbody tr:hover td{background:#f8fafc;}
.grade{
  display:inline-block;width:28px;height:28px;border-radius:50%;
  font-size:11px;font-weight:800;text-align:center;line-height:28px;
}
.grade-A{background:#dcfce7;color:#14532d;}
.grade-B{background:#dbeafe;color:#1e3a8a;}
.grade-C{background:#fef9c3;color:#713f12;}
.grade-D{background:#ffedd5;color:#7c2d12;}
.grade-F{background:#fee2e2;color:#7f1d1d;}
.summary-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:20px;}
.summary-box{background:#f4f7fb;border-radius:8px;padding:12px;text-align:center;}
.summary-box .val{font-size:20px;font-weight:800;color:#0f2340;}
.summary-box .lbl{font-size:10px;color:#5a6a82;text-transform:uppercase;letter-spacing:.5px;font-weight:700;margin-top:3px;}
.footer-row{display:flex;justify-content:space-between;align-items:flex-end;margin-top:30px;border-top:1px solid #e5e9f0;padding-top:20px;}
.sig-line{border-top:1.5px solid #0f2340;width:160px;text-align:center;padding-top:5px;font-size:11px;color:#5a6a82;font-weight:600;}
.footer-note{text-align:center;font-size:10px;color:#8fa3bc;margin-top:12px;}
@media print{
  body{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  .no-print{display:none;}
}
</style>
</head>
<body>
<div class="page">
  <!-- Header -->
  <div class="header">
    {% if school_logo and school_logo.url %}
      <img class="logo" src="{{ school_logo.url }}" alt="GSA Logo">
    {% else %}
      <div class="logo-fallback">
        <svg width="50" height="58" viewBox="0 0 300 340" xmlns="http://www.w3.org/2000/svg">
          <path d="M150 8 L272 54 L272 182 Q272 284 150 332 Q28 284 28 182 L28 54 Z" fill="#E8B830"/>
          <path d="M65 110 L235 110 L235 215 Q235 255 150 285 Q65 255 65 215 Z" fill="#1a3575"/>
          <polygon points="150,95 155,110 171,110 158,120 163,135 150,126 137,135 142,120 129,110 145,110" fill="#F5C518"/>
        </svg>
      </div>
    {% endif %}
    <div>
      <div class="school-name">Golden Stars Academy</div>
      <div class="school-sub">{{ site.address or 'Q762, After Living Faith Church, Yetu Quarters, GRA Gbessa, Abuja' }}</div>
      <div class="school-sub">{{ site.phone1 or '+234 803 442 8823' }} &middot; {{ site.email or 'info@goldenstarsacademy.com' }}</div>
      <div class="school-motto">"GOD IS ABLE" &mdash; goldenstarsacademy.com.ng</div>
    </div>
  </div>

  <div class="report-title">STUDENT ACADEMIC REPORT &mdash; {{ term.upper() }} &middot; {{ session }}</div>

  <!-- Student Info -->
  <div class="student-info">
    <div class="si-item"><label>Student Name</label><span>{{ student.full_name }}</span></div>
    <div class="si-item"><label>Admission No.</label><span>{{ student.admission_no }}</span></div>
    <div class="si-item"><label>Class</label><span>{{ student.class_name }}</span></div>
    <div class="si-item"><label>Level</label><span>{{ student.level }}</span></div>
    <div class="si-item"><label>Session</label><span>{{ session }}</span></div>
    <div class="si-item"><label>Term</label><span>{{ term }}</span></div>
  </div>

  <!-- Summary -->
  {% if results %}
  {% set total_score = results | sum(attribute='total') %}
  {% set avg = (total_score / results|length) | round(1) %}
  {% set a_count = results | selectattr('grade','equalto','A') | list | length %}
  <div class="summary-grid">
    <div class="summary-box"><div class="val">{{ results|length }}</div><div class="lbl">Subjects</div></div>
    <div class="summary-box"><div class="val">{{ "{:.1f}".format(avg) }}</div><div class="lbl">Average Score</div></div>
    <div class="summary-box"><div class="val">{{ a_count }}</div><div class="lbl">A Grades</div></div>
    <div class="summary-box">
      <div class="val" style="color:{% if avg>=75 %}#16a34a{% elif avg>=55 %}#d97706{% else %}#dc2626{% endif %}">
        {% if avg>=75 %}Excellent{% elif avg>=65 %}Very Good{% elif avg>=55 %}Good{% elif avg>=45 %}Fair{% else %}Needs Work{% endif %}
      </div>
      <div class="lbl">Overall</div>
    </div>
  </div>
  {% endif %}

  <!-- Results Table -->
  <table>
    <thead>
      <tr>
        <th>Subject</th>
        <th style="text-align:center;">CA1<br><small style="font-weight:400;opacity:.7">/20</small></th>
        <th style="text-align:center;">CA2<br><small style="font-weight:400;opacity:.7">/20</small></th>
        <th style="text-align:center;">Exam<br><small style="font-weight:400;opacity:.7">/60</small></th>
        <th style="text-align:center;">Total<br><small style="font-weight:400;opacity:.7">/100</small></th>
        <th style="text-align:center;">Grade</th>
        <th>Remark</th>
      </tr>
    </thead>
    <tbody>
      {% for r in results %}
      <tr>
        <td style="font-weight:600;">{{ r.subject }}</td>
        <td style="text-align:center;">{{ r.ca1 }}</td>
        <td style="text-align:center;">{{ r.ca2 }}</td>
        <td style="text-align:center;">{{ r.exam }}</td>
        <td style="text-align:center;font-weight:800;font-size:15px;">{{ r.total }}</td>
        <td style="text-align:center;"><span class="grade grade-{{ r.grade }}">{{ r.grade }}</span></td>
        <td style="color:#5a6a82;">{{ r.remark }}</td>
      </tr>
      {% else %}
      <tr><td colspan="7" style="text-align:center;padding:24px;color:#8fa3bc;">No approved results available for this term.</td></tr>
      {% endfor %}
    </tbody>
  </table>

  <!-- Grading Key -->
  <div style="background:#f4f7fb;border-radius:8px;padding:12px 16px;margin-bottom:20px;">
    <div style="font-size:10px;font-weight:700;color:#5a6a82;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px;">Grading Scale</div>
    <div style="display:flex;gap:16px;font-size:12px;">
      <span><strong>A</strong> &mdash; 75–100 &middot; Excellent</span>
      <span><strong>B</strong> &mdash; 65–74 &middot; Very Good</span>
      <span><strong>C</strong> &mdash; 55–64 &middot; Good</span>
      <span><strong>D</strong> &mdash; 45–54 &middot; Fair</span>
      <span><strong>F</strong> &mdash; 0–44 &middot; Fail</span>
    </div>
  </div>

  <!-- Signatures -->
  <div class="footer-row">
    <div>
      <div class="sig-line">Class Teacher</div>
    </div>
    <div>
      <div class="sig-line">Head of Section</div>
    </div>
    <div>
      <div class="sig-line">Principal / Director</div>
    </div>
  </div>

  <div class="footer-note" style="margin-top:20px;">
    This result sheet is computer-generated and official when signed and stamped.<br>
    <strong>Golden Stars Academy</strong> &mdash; Raising World-Class Leaders &middot; goldenstarsacademy.com.ng<br>
    <em style="color:#c9a84c;">Powered by RESCAVIA &mdash; festusolowo1@gmail.com &middot; +2348161303336</em>
  </div>

  <!-- Print Button -->
  <div class="no-print" style="text-align:center;margin-top:28px;">
    <button onclick="window.print()" style="background:#0f2340;color:#fff;border:none;padding:12px 28px;border-radius:8px;font-size:14px;font-weight:700;cursor:pointer;font-family:inherit;">
      &#128438; Print Result Sheet
    </button>
    <a href="/parent/dashboard" style="display:inline-block;margin-left:10px;padding:12px 20px;border:1.5px solid #e5e9f0;border-radius:8px;font-size:13px;font-weight:600;color:#5a6a82;">
      &larr; Back
    </a>
  </div>
</div>
</body>
</html>"""

write("templates/portals/result_sheet.html", RESULT_SHEET)

# ── 7. ADMIN PROFILE PAGE ─────────────────────────────────────────────────
ADMIN_PROFILE = """{% extends "admin/base.html" %}
{% block title %}My Profile{% endblock %}
{% block page_title %}My Profile{% endblock %}
{% block content %}
<div class="page-hd">
  <div class="page-hd-left">
    <h2>My Profile</h2>
    <p>Update your personal information and password</p>
  </div>
</div>
<div style="display:grid;grid-template-columns:280px 1fr;gap:20px;align-items:start;">
  <!-- Avatar Card -->
  <div class="card">
    <div class="card-body" style="text-align:center;">
      <div style="width:90px;height:90px;border-radius:50%;margin:0 auto 14px;overflow:hidden;background:var(--navy);display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:800;color:var(--gold);">
        {% if current_user.avatar and current_user.avatar.startswith('/') %}
          <img src="{{ current_user.avatar }}" style="width:100%;height:100%;object-fit:cover;">
        {% else %}
          {{ current_user.avatar or current_user.name[:2].upper() }}
        {% endif %}
      </div>
      <div style="font-size:16px;font-weight:700;">{{ current_user.name }}</div>
      <div style="margin-top:6px;">
        {% set rc={'superadmin':'b-sa','ict':'b-ic','media':'b-me','bursar':'b-bu'} %}
        <span class="badge {{ rc.get(current_user.role,'b-gray') }}">{{ current_user.role|title }}</span>
      </div>
      <div style="font-size:12px;color:var(--muted);margin-top:10px;">{{ current_user.email }}</div>
      <div style="font-size:11px;color:var(--light);margin-top:4px;">Member since {{ current_user.created }}</div>
      <div class="divider"></div>
      <div style="text-align:left;">
        <div style="font-size:11px;color:var(--muted);font-weight:700;margin-bottom:8px;text-transform:uppercase;letter-spacing:.5px;">Quick Links</div>
        <a href="/admin" class="btn btn-outline btn-sm btn-block" style="margin-bottom:8px;"><i class="ti ti-layout-dashboard"></i> Dashboard</a>
        <a href="/" target="_blank" class="btn btn-outline btn-sm btn-block"><i class="ti ti-world"></i> View Website</a>
      </div>
    </div>
  </div>
  <!-- Edit Form -->
  <div class="card">
    <div class="card-hd"><div class="card-title">Edit Profile</div></div>
    <div class="card-body">
      <form method="post" action="/admin/profile" enctype="multipart/form-data">
        <div class="fg-row">
          <div class="fg">
            <label>Full Name *</label>
            <input type="text" name="name" value="{{ current_user.name }}" required class="form-control">
          </div>
          <div class="fg">
            <label>Email Address</label>
            <input type="email" value="{{ current_user.email }}" disabled class="form-control" style="background:#f4f7fb;cursor:not-allowed;">
            <div class="form-hint">Email cannot be changed</div>
          </div>
        </div>
        <div class="fg">
          <label>Profile Photo</label>
          <input type="file" name="avatar" accept="image/*" class="form-control">
          <div class="form-hint">Upload a square photo. Max 2MB.</div>
        </div>
        <div class="divider"></div>
        <div style="font-size:13px;font-weight:700;color:var(--muted);margin-bottom:14px;text-transform:uppercase;letter-spacing:.4px;font-size:11px;">Change Password</div>
        <div class="fg-row">
          <div class="fg">
            <label>Current Password</label>
            <input type="password" name="current_password" class="form-control" placeholder="Enter current password">
          </div>
          <div class="fg">
            <label>New Password</label>
            <input type="password" name="new_password" class="form-control" placeholder="Enter new password">
          </div>
        </div>
        <div class="info-box" style="margin-bottom:16px;">
          <i class="ti ti-info-circle" style="font-size:17px;flex-shrink:0;margin-top:1px;"></i>
          Leave password fields blank to keep your current password.
        </div>
        <button type="submit" class="btn btn-primary"><i class="ti ti-check"></i> Save Changes</button>
      </form>
    </div>
  </div>
</div>
{% endblock %}"""

write("templates/admin/profile.html", ADMIN_PROFILE)

# ── 8. ENHANCED MAIN.PY PATCH ─────────────────────────────────────────────
MAIN_PATCH = '''
# Patch dashboard to include more counts
'''

print("\n" + "=" * 50)
print("Build complete! Files created:")
print("  templates/admin/base.html     - World-class admin layout")
print("  templates/admin/dashboard.html - Enhanced dashboard")
print("  templates/admin/profile.html  - Admin profile page")
print("  templates/portals/result_sheet.html - Printable results")
print("  static/css/global.css         - Design system CSS")
print("\nNext: patch main.py dashboard route + push to GitHub")
