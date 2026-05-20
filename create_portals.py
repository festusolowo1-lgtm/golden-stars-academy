"""
Run once from your golden-stars/ folder:
    python create_portals.py

Creates:
  templates/portals/teacher.html
  templates/portals/parent.html
  templates/portals/student.html
"""
import os

os.makedirs("templates/portals", exist_ok=True)

def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"✅ Created: {path}")

# ══════════════════════════════════════════════════════════════
# SHARED PORTAL CSS
# ══════════════════════════════════════════════════════════════
PORTAL_CSS = """
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Segoe UI',Arial,sans-serif;background:#f5f6f8;color:#1c1c2e;min-height:100vh;}
.hidden{display:none!important;}
.page{display:none;}.page.active{display:block;}
/* NAV */
.pnav{background:var(--pc);color:#fff;padding:12px 28px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 2px 8px rgba(0,0,0,.15);}
.pnav-logo{display:flex;align-items:center;gap:10px;}
.pnav-logo svg{border-radius:50%;}
.pnav-title{font-size:14px;font-weight:700;line-height:1.2;}
.pnav-title small{display:block;font-size:10px;opacity:.55;font-weight:400;}
.pnav-user{display:flex;align-items:center;gap:10px;}
.pnav-av{width:32px;height:32px;border-radius:50%;background:rgba(255,255,255,.2);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;color:#fff;}
.pnav-name{font-size:12px;font-weight:600;}
.pnav-role{font-size:10px;opacity:.55;}
.logout-btn{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);color:#fff;padding:5px 13px;border-radius:6px;font-size:12px;cursor:pointer;font-family:inherit;}
.logout-btn:hover{background:rgba(255,255,255,.22);}
/* SIDEBAR */
.shell{display:flex;min-height:calc(100vh - 56px);}
.sidebar{width:210px;background:#fff;border-right:1px solid #eee;padding:14px 0;flex-shrink:0;}
.sb-link{display:flex;align-items:center;gap:9px;padding:10px 18px;font-size:13px;color:#555;cursor:pointer;border-left:3px solid transparent;transition:all .15s;text-decoration:none;}
.sb-link:hover{background:#f5f6f8;color:var(--pc);}
.sb-link.on{background:var(--pc-light);color:var(--pc);border-left-color:var(--pc);font-weight:600;}
.sb-link i{font-size:17px;}
.sb-sec{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#aaa;padding:10px 18px 3px;}
/* MAIN */
.main{flex:1;padding:22px;overflow-y:auto;}
/* CARDS */
.card{background:#fff;border-radius:12px;padding:20px;box-shadow:0 1px 5px rgba(0,0,0,.05);margin-bottom:16px;}
.card-hd{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:10px;}
.card-title{font-size:15px;font-weight:700;}
.card-sub{font-size:12px;color:#888;margin-top:2px;}
/* STATS */
.sg{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:12px;margin-bottom:18px;}
.sc{background:#fff;border-radius:10px;padding:14px;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,.05);}
.sc-icon{font-size:22px;margin-bottom:5px;}
.sc-val{font-size:22px;font-weight:700;color:var(--pc);}
.sc-lbl{font-size:11px;color:#888;margin-top:2px;}
/* TABLE */
.tbl{width:100%;border-collapse:collapse;font-size:13px;}
.tbl th{padding:9px 12px;text-align:left;font-weight:600;font-size:11px;color:#666;border-bottom:1px solid #eee;background:#f8f9fc;text-transform:uppercase;letter-spacing:.03em;}
.tbl td{padding:10px 12px;border-bottom:1px solid #f2f2f5;vertical-align:middle;}
.tbl tr:hover td{background:#fafbff;}
.tbl-wrap{overflow-x:auto;}
/* FORM */
.fg{margin-bottom:13px;}
.fg label{display:block;font-size:12px;font-weight:600;color:#555;margin-bottom:4px;}
.fg input,.fg select,.fg textarea{width:100%;padding:9px 12px;border:1px solid #ddd;border-radius:7px;font-size:13px;outline:none;font-family:inherit;background:#fff;}
.fg input:focus,.fg select:focus,.fg textarea:focus{border-color:var(--pc);}
.fg textarea{resize:vertical;min-height:80px;}
.fg-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
/* BUTTONS */
.btn{display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:7px;border:none;font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;transition:opacity .15s;}
.btn:hover{opacity:.88;}
.btn-p{background:var(--pc);color:#fff;}
.btn-d{background:#dc2626;color:#fff;}
.btn-ok{background:#16a34a;color:#fff;}
.btn-o{background:transparent;border:1.5px solid var(--pc);color:var(--pc);}
.btn-sm{padding:4px 10px;font-size:12px;}
/* BADGE */
.bdg{display:inline-block;padding:2px 9px;border-radius:10px;font-size:11px;font-weight:600;}
.bdg-ok{background:#dcfce7;color:#16a34a;}
.bdg-warn{background:#fef3c7;color:#b45309;}
.bdg-info{background:#dbeafe;color:#1d4ed8;}
.bdg-err{background:#fee2e2;color:#dc2626;}
.bdg-grey{background:#f3f4f6;color:#555;}
/* MODAL */
.modal-ov{position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:500;display:flex;align-items:center;justify-content:center;padding:16px;}
.modal-box{background:#fff;border-radius:14px;padding:26px;width:100%;max-width:500px;max-height:90vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,.2);}
.modal-hd{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;}
.modal-hd h3{font-size:15px;font-weight:700;}
.modal-close{border:none;background:none;font-size:20px;cursor:pointer;color:#888;}
/* FLASH */
.flash{padding:10px 14px;border-radius:8px;font-size:13px;margin-bottom:14px;display:flex;align-items:center;gap:8px;}
.flash-ok{background:#dcfce7;color:#166534;border:1px solid #bbf7d0;}
.flash-err{background:#fee2e2;color:#991b1b;border:1px solid #fecaca;}
/* LOGIN */
.login-wrap{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;}
.login-box{background:#fff;border-radius:16px;padding:32px;width:100%;max-width:380px;box-shadow:0 20px 60px rgba(0,0,0,.15);}
.login-box h1{font-size:18px;font-weight:700;text-align:center;margin-bottom:4px;color:var(--pc);}
.login-box .sub{font-size:12px;color:#888;text-align:center;margin-bottom:22px;}
.btn-full{width:100%;padding:12px;background:var(--pc);color:#fff;border:none;border-radius:7px;font-size:14px;font-weight:600;cursor:pointer;font-family:inherit;}
/* RESULT CARD */
.result-card{background:#fff;border-radius:12px;border:1px solid #eee;overflow:hidden;margin-bottom:14px;}
.result-hd{padding:14px 18px;background:var(--pc);color:#fff;display:flex;justify-content:space-between;align-items:center;}
.result-hd h3{font-size:14px;font-weight:700;}
.result-body{padding:0;}
.score-row{display:flex;justify-content:space-between;align-items:center;padding:10px 18px;border-bottom:1px solid #f5f5f5;font-size:13px;}
.score-row:last-child{border-bottom:none;}
.score-bar-wrap{flex:1;margin:0 14px;height:6px;background:#f0f0f0;border-radius:3px;overflow:hidden;}
.score-bar{height:100%;border-radius:3px;background:var(--pc);}
/* ASSIGNMENT CARD */
.assign-card{background:#fff;border:1px solid #eee;border-radius:12px;padding:16px;margin-bottom:12px;transition:box-shadow .2s;}
.assign-card:hover{box-shadow:0 4px 16px rgba(0,0,0,.08);}
.assign-title{font-size:14px;font-weight:700;margin-bottom:5px;}
.assign-meta{font-size:12px;color:#888;margin-bottom:8px;}
.assign-desc{font-size:13px;color:#555;line-height:1.6;margin-bottom:10px;}
/* PROGRESS BAR */
.prog-bar{height:6px;background:#e5e7eb;border-radius:3px;overflow:hidden;margin-top:4px;}
.prog-fill{height:100%;background:var(--pc);border-radius:3px;transition:width .5s;}
"""

LOGO_SVG = """<svg width="36" height="36" viewBox="0 0 300 340" xmlns="http://www.w3.org/2000/svg" style="border-radius:50%;flex-shrink:0">
  <path d="M150 8 L272 54 L272 182 Q272 284 150 332 Q28 284 28 182 L28 54 Z" fill="#E8B830"/>
  <path d="M150 22 L258 62 L258 182 Q258 272 150 316 Q42 272 42 182 L42 62 Z" fill="#CC2200"/>
  <path d="M65 110 L235 110 L235 215 Q235 255 150 285 Q65 255 65 215 Z" fill="#1a3575"/>
  <polygon points="150,95 155,110 171,110 158,120 163,135 150,126 137,135 142,120 129,110 145,110" fill="#F5C518"/>
</svg>"""

# ══════════════════════════════════════════════════════════════
# TEACHER PORTAL
# ══════════════════════════════════════════════════════════════
write("templates/portals/teacher.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Teacher Portal · Golden Stars Academy</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css"/>
<style>
{PORTAL_CSS}
:root{{--pc:#1a3a6b;--pc-light:#e8eef8;}}
body{{background:var(--bg,#f5f6f8);}}
</style>
</head>
<body>

<!-- LOGIN -->
<div id="loginView">
  <div style="min-height:100vh;background:linear-gradient(135deg,#0f2d5a,#1a3a6b);display:flex;align-items:center;justify-content:center;padding:20px;">
    <div class="login-box">
      <div style="display:flex;justify-content:center;margin-bottom:14px;">{LOGO_SVG.replace('width="36" height="36"','width="64" height="64"')}</div>
      <h1>Teacher Portal</h1>
      <div class="sub">Golden Stars Academy — Staff Login</div>
      <div id="loginErr" class="flash flash-err hidden"></div>
      <div class="fg"><label>Email / Staff ID</label><input type="email" id="tEmail" placeholder="teacher@goldenstarsacademy.com"/></div>
      <div class="fg"><label>Password</label><input type="password" id="tPass" placeholder="••••••••"/></div>
      <button class="btn-full" onclick="teacherLogin()">Sign In</button>
      <div style="text-align:center;margin-top:14px;">
        <a href="/" style="font-size:12px;color:#888;">← Back to Website</a>
      </div>
      <div style="background:#f5f6f8;border-radius:8px;padding:10px;margin-top:14px;font-size:11px;color:#888;text-align:center;">
        Demo: teacher@gsa.com / teacher123
      </div>
    </div>
  </div>
</div>

<!-- APP -->
<div id="appView" class="hidden">
  <!-- TOPNAV -->
  <div class="pnav">
    <div class="pnav-logo">{LOGO_SVG}<div class="pnav-title">Golden Stars Academy<small>Teacher Portal</small></div></div>
    <div class="pnav-user">
      <div class="pnav-av" id="tAv">T</div>
      <div><div class="pnav-name" id="tName">Teacher</div><div class="pnav-role" id="tSubject">Mathematics</div></div>
      <button class="logout-btn" onclick="teacherLogout()">Sign Out</button>
    </div>
  </div>

  <div class="shell">
    <!-- SIDEBAR -->
    <div class="sidebar">
      <div class="sb-sec">Main</div>
      <div class="sb-link on" onclick="tShow('dashboard')"><i class="ti ti-dashboard"></i> Dashboard</div>
      <div class="sb-sec">Students</div>
      <div class="sb-link" onclick="tShow('students')"><i class="ti ti-users"></i> Class List</div>
      <div class="sb-link" onclick="tShow('addStudent')"><i class="ti ti-user-plus"></i> Add Student</div>
      <div class="sb-sec">Academics</div>
      <div class="sb-link" onclick="tShow('assignments')"><i class="ti ti-clipboard-list"></i> Assignments</div>
      <div class="sb-link" onclick="tShow('createAssign')"><i class="ti ti-plus"></i> Create Assignment</div>
      <div class="sb-link" onclick="tShow('submissions')"><i class="ti ti-send"></i> Submissions</div>
      <div class="sb-sec">Results</div>
      <div class="sb-link" onclick="tShow('scores')"><i class="ti ti-chart-bar"></i> Upload Scores</div>
      <div class="sb-link" onclick="tShow('results')"><i class="ti ti-award"></i> View Results</div>
    </div>

    <!-- MAIN CONTENT -->
    <div class="main">

      <!-- DASHBOARD -->
      <div class="page active" id="t-dashboard">
        <h2 style="font-size:18px;font-weight:700;margin-bottom:5px;">Good morning, <span id="tGreetName">Teacher</span>! 👋</h2>
        <p style="font-size:13px;color:#888;margin-bottom:18px;">Here's your classroom overview for today.</p>
        <div class="sg">
          <div class="sc"><div class="sc-icon">👥</div><div class="sc-val" id="dashStudents">0</div><div class="sc-lbl">My Students</div></div>
          <div class="sc"><div class="sc-icon">📋</div><div class="sc-val" id="dashAssign">0</div><div class="sc-lbl">Assignments</div></div>
          <div class="sc"><div class="sc-icon">📬</div><div class="sc-val" id="dashSubs">0</div><div class="sc-lbl">Submissions</div></div>
          <div class="sc"><div class="sc-icon">⏳</div><div class="sc-val" id="dashPending">0</div><div class="sc-lbl">Pending Grade</div></div>
        </div>
        <div class="card">
          <div class="card-hd"><div><div class="card-title">Recent Submissions</div><div class="card-sub">Assignments awaiting grading</div></div><button class="btn btn-p btn-sm" onclick="tShow('submissions')">View All</button></div>
          <div id="dashSubsList"><p style="color:#aaa;font-size:13px;">No pending submissions.</p></div>
        </div>
        <div class="card">
          <div class="card-hd"><div><div class="card-title">Active Assignments</div></div><button class="btn btn-p btn-sm" onclick="tShow('createAssign')"><i class="ti ti-plus"></i> New</button></div>
          <div id="dashAssignList"><p style="color:#aaa;font-size:13px;">No assignments yet.</p></div>
        </div>
      </div>

      <!-- CLASS LIST -->
      <div class="page" id="t-students">
        <div class="card">
          <div class="card-hd"><div><div class="card-title">Class List</div><div class="card-sub">All students under your care</div></div><button class="btn btn-p" onclick="tShow('addStudent')"><i class="ti ti-user-plus"></i> Add Student</button></div>
          <div class="tbl-wrap"><table class="tbl">
            <thead><tr><th>#</th><th>Name</th><th>Class</th><th>Gender</th><th>Parent Contact</th><th>Actions</th></tr></thead>
            <tbody id="studentsTbody"><tr><td colspan="6" style="text-align:center;color:#aaa;padding:20px;">No students yet. Add your first student.</td></tr></tbody>
          </table></div>
        </div>
      </div>

      <!-- ADD STUDENT -->
      <div class="page" id="t-addStudent">
        <div class="card" style="max-width:560px;">
          <div class="card-title" style="margin-bottom:4px;">Add New Student</div>
          <div class="card-sub" style="margin-bottom:18px;">Student will be visible to parents and linked to results</div>
          <div class="fg-row">
            <div class="fg"><label>First Name</label><input type="text" id="sFirstName" placeholder="e.g. Chioma"/></div>
            <div class="fg"><label>Last Name</label><input type="text" id="sLastName" placeholder="e.g. Okafor"/></div>
          </div>
          <div class="fg-row">
            <div class="fg"><label>Class / Grade</label><select id="sClass">
              <option>Nursery 1</option><option>Nursery 2</option><option>Primary 1</option><option>Primary 2</option>
              <option>Primary 3</option><option>Primary 4</option><option>Primary 5</option><option>Primary 6</option>
              <option>JSS 1</option><option>JSS 2</option><option>JSS 3</option>
              <option>SSS 1</option><option>SSS 2</option><option>SSS 3</option>
            </select></div>
            <div class="fg"><label>Gender</label><select id="sGender"><option>Female</option><option>Male</option></select></div>
          </div>
          <div class="fg-row">
            <div class="fg"><label>Parent/Guardian Name</label><input type="text" id="sParent" placeholder="e.g. Mrs. Okafor"/></div>
            <div class="fg"><label>Parent Phone</label><input type="text" id="sParentPhone" placeholder="+234 ..."/></div>
          </div>
          <div class="fg"><label>Parent/Guardian Email (for login)</label><input type="email" id="sParentEmail" placeholder="parent@email.com"/></div>
          <div class="fg"><label>Student ID / Admission Number</label><input type="text" id="sAdmNo" placeholder="e.g. GSA/2024/001"/></div>
          <div style="display:flex;gap:10px;">
            <button class="btn btn-p" onclick="addStudent()"><i class="ti ti-user-check"></i> Add Student</button>
            <button class="btn btn-o" onclick="tShow('students')">Cancel</button>
          </div>
        </div>
      </div>

      <!-- ASSIGNMENTS -->
      <div class="page" id="t-assignments">
        <div class="card">
          <div class="card-hd"><div><div class="card-title">All Assignments</div><div class="card-sub">Homework and classwork assigned to students</div></div><button class="btn btn-p" onclick="tShow('createAssign')"><i class="ti ti-plus"></i> Create</button></div>
          <div id="assignList"><p style="color:#aaa;font-size:13px;">No assignments yet.</p></div>
        </div>
      </div>

      <!-- CREATE ASSIGNMENT -->
      <div class="page" id="t-createAssign">
        <div class="card" style="max-width:580px;">
          <div class="card-title" style="margin-bottom:4px;">Create Assignment</div>
          <div class="card-sub" style="margin-bottom:18px;">Students will see this in their portal and can submit work</div>
          <div class="fg"><label>Assignment Title</label><input type="text" id="aTitle" placeholder="e.g. Chapter 5 Exercise — Fractions"/></div>
          <div class="fg-row">
            <div class="fg"><label>Subject</label><input type="text" id="aSubject" placeholder="e.g. Mathematics"/></div>
            <div class="fg"><label>Target Class</label><select id="aClass">
              <option>All Classes</option><option>Nursery 1</option><option>Nursery 2</option>
              <option>Primary 1</option><option>Primary 2</option><option>Primary 3</option>
              <option>Primary 4</option><option>Primary 5</option><option>Primary 6</option>
              <option>JSS 1</option><option>JSS 2</option><option>JSS 3</option>
              <option>SSS 1</option><option>SSS 2</option><option>SSS 3</option>
            </select></div>
          </div>
          <div class="fg"><label>Description / Instructions</label><textarea id="aDesc" placeholder="Write the assignment instructions clearly..."></textarea></div>
          <div class="fg-row">
            <div class="fg"><label>Due Date</label><input type="date" id="aDue"/></div>
            <div class="fg"><label>Max Score</label><input type="number" id="aMax" value="100" min="1"/></div>
          </div>
          <div style="display:flex;gap:10px;">
            <button class="btn btn-p" onclick="createAssignment()"><i class="ti ti-send"></i> Assign Now</button>
            <button class="btn btn-o" onclick="tShow('assignments')">Cancel</button>
          </div>
        </div>
      </div>

      <!-- SUBMISSIONS -->
      <div class="page" id="t-submissions">
        <div class="card">
          <div class="card-hd"><div><div class="card-title">Student Submissions</div><div class="card-sub">Review and grade submitted assignments</div></div></div>
          <div id="subsList"><p style="color:#aaa;font-size:13px;">No submissions yet.</p></div>
        </div>
      </div>

      <!-- UPLOAD SCORES -->
      <div class="page" id="t-scores">
        <div class="card" style="max-width:600px;">
          <div class="card-title" style="margin-bottom:4px;">Upload Exam Scores</div>
          <div class="card-sub" style="margin-bottom:18px;">Scores are sent for Principal/Admin approval before parents can view them</div>
          <div class="fg-row">
            <div class="fg"><label>Student</label><select id="scStudent"><option value="">— Select Student —</option></select></div>
            <div class="fg"><label>Subject</label><input type="text" id="scSubject" placeholder="e.g. Mathematics"/></div>
          </div>
          <div class="fg-row">
            <div class="fg"><label>Exam Type</label><select id="scType">
              <option>1st C.A</option><option>2nd C.A</option><option>Mid-Term Exam</option>
              <option>End of Term Exam</option><option>Mock Exam</option>
            </select></div>
            <div class="fg"><label>Term</label><select id="scTerm">
              <option>First Term</option><option>Second Term</option><option>Third Term</option>
            </select></div>
          </div>
          <div class="fg-row">
            <div class="fg"><label>Score Obtained</label><input type="number" id="scScore" placeholder="e.g. 78" min="0"/></div>
            <div class="fg"><label>Total Marks</label><input type="number" id="scTotal" value="100" min="1"/></div>
          </div>
          <div class="fg"><label>Academic Session</label><input type="text" id="scSession" value="2025/2026"/></div>
          <div class="fg"><label>Remark / Comment (optional)</label><input type="text" id="scRemark" placeholder="e.g. Excellent performance, keep it up!"/></div>
          <button class="btn btn-p" onclick="uploadScore()" style="margin-bottom:8px;"><i class="ti ti-upload"></i> Submit for Approval</button>
          <p style="font-size:11px;color:#888;">⏳ Score will be reviewed by the Principal/Admin before it is visible to parents and students.</p>
        </div>
      </div>

      <!-- VIEW RESULTS -->
      <div class="page" id="t-results">
        <div class="card">
          <div class="card-hd"><div><div class="card-title">All Uploaded Results</div><div class="card-sub">Track approval status of submitted scores</div></div></div>
          <div class="tbl-wrap"><table class="tbl">
            <thead><tr><th>Student</th><th>Subject</th><th>Type</th><th>Score</th><th>Term</th><th>Status</th></tr></thead>
            <tbody id="resultsTbody"><tr><td colspan="6" style="text-align:center;color:#aaa;padding:20px;">No results uploaded yet.</td></tr></tbody>
          </table></div>
        </div>
      </div>

    </div><!-- /main -->
  </div><!-- /shell -->
</div><!-- /appView -->

<script>
// ── DATA STORE (localStorage for demo) ──────────────────────
const store = {{
  get: k => JSON.parse(localStorage.getItem('gsa_t_'+k)||'null'),
  set: (k,v) => localStorage.setItem('gsa_t_'+k, JSON.stringify(v)),
  push: (k,v) => {{ const a=store.get(k)||[]; a.push(v); store.set(k,a); }},
}};

// Demo teacher
const DEMO = {{email:'teacher@gsa.com',password:'teacher123',name:'Mrs. Adaeze Okonkwo',subject:'Mathematics · JSS 2',initials:'AO'}};

function teacherLogin(){{
  const e=document.getElementById('tEmail').value.trim();
  const p=document.getElementById('tPass').value;
  const err=document.getElementById('loginErr');
  if(e===DEMO.email && p===DEMO.password){{
    store.set('loggedIn',true);
    document.getElementById('loginView').classList.add('hidden');
    document.getElementById('appView').classList.remove('hidden');
    initTeacher();
  }} else {{
    err.textContent='Invalid email or password.';
    err.classList.remove('hidden');
  }}
}}

function teacherLogout(){{
  store.set('loggedIn',false);
  document.getElementById('loginView').classList.remove('hidden');
  document.getElementById('appView').classList.add('hidden');
}}

function initTeacher(){{
  document.getElementById('tAv').textContent=DEMO.initials;
  document.getElementById('tName').textContent=DEMO.name;
  document.getElementById('tSubject').textContent=DEMO.subject;
  document.getElementById('tGreetName').textContent=DEMO.name.split(' ')[1];
  refreshDash(); populateStudentDropdown();
}}

function tShow(pg){{
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.getElementById('t-'+pg).classList.add('active');
  document.querySelectorAll('.sb-link').forEach(l=>l.classList.remove('on'));
  if(pg==='dashboard') refreshDash();
  if(pg==='students') renderStudents();
  if(pg==='assignments'||pg==='createAssign') renderAssignments();
  if(pg==='submissions') renderSubmissions();
  if(pg==='scores') populateStudentDropdown();
  if(pg==='results') renderResults();
}}

// ── STUDENTS ──────────────────────────────────────────────
function addStudent(){{
  const first=document.getElementById('sFirstName').value.trim();
  const last=document.getElementById('sLastName').value.trim();
  if(!first||!last){{alert('Enter student first and last name.');return;}}
  const s={{
    id:'S'+Date.now(),name:first+' '+last,
    cls:document.getElementById('sClass').value,
    gender:document.getElementById('sGender').value,
    parent:document.getElementById('sParent').value,
    parentPhone:document.getElementById('sParentPhone').value,
    parentEmail:document.getElementById('sParentEmail').value,
    admNo:document.getElementById('sAdmNo').value||'GSA/'+new Date().getFullYear()+'/'+Math.floor(Math.random()*999+1).toString().padStart(3,'0'),
    added:new Date().toISOString().split('T')[0]
  }};
  store.push('students',s);
  ['sFirstName','sLastName','sParent','sParentPhone','sParentEmail','sAdmNo'].forEach(id=>document.getElementById(id).value='');
  alert('✅ Student '+s.name+' added successfully!');
  tShow('students');
}}

function renderStudents(){{
  const students=store.get('students')||[];
  const tbody=document.getElementById('studentsTbody');
  if(!students.length){{tbody.innerHTML='<tr><td colspan="6" style="text-align:center;color:#aaa;padding:20px;">No students yet.</td></tr>';return;}}
  tbody.innerHTML=students.map((s,i)=>`<tr>
    <td style="color:#aaa;">${{i+1}}</td>
    <td><strong>${{s.name}}</strong><br/><span style="font-size:11px;color:#888;">${{s.admNo}}</span></td>
    <td>${{s.cls}}</td>
    <td>${{s.gender}}</td>
    <td style="font-size:12px;">${{s.parent}}<br/>${{s.parentPhone}}</td>
    <td><button class="btn btn-d btn-sm" onclick="removeStudent('${{s.id}}')">Remove</button></td>
  </tr>`).join('');
}}

function removeStudent(id){{
  if(!confirm('Remove this student?'))return;
  const arr=(store.get('students')||[]).filter(s=>s.id!==id);
  store.set('students',arr); renderStudents();
}}

function populateStudentDropdown(){{
  const sel=document.getElementById('scStudent');
  if(!sel)return;
  const students=store.get('students')||[];
  sel.innerHTML='<option value="">— Select Student —</option>'+students.map(s=>`<option value="${{s.id}}">${{s.name}} (${{s.cls}})</option>`).join('');
}}

// ── ASSIGNMENTS ────────────────────────────────────────────
function createAssignment(){{
  const title=document.getElementById('aTitle').value.trim();
  if(!title){{alert('Enter assignment title.');return;}}
  const a={{
    id:'A'+Date.now(),title,
    subject:document.getElementById('aSubject').value,
    cls:document.getElementById('aClass').value,
    desc:document.getElementById('aDesc').value,
    due:document.getElementById('aDue').value,
    maxScore:document.getElementById('aMax').value,
    created:new Date().toISOString().split('T')[0],
    submissions:[]
  }};
  store.push('assignments',a);
  ['aTitle','aSubject','aDesc','aDue'].forEach(id=>document.getElementById(id).value='');
  alert('✅ Assignment created and visible to students!');
  tShow('assignments');
}}

function renderAssignments(){{
  const items=store.get('assignments')||[];
  const el=document.getElementById('assignList');
  if(!el)return;
  if(!items.length){{el.innerHTML='<p style="color:#aaa;font-size:13px;">No assignments yet.</p>';return;}}
  el.innerHTML=items.map(a=>{{
    const subs=(store.get('submissions')||[]).filter(s=>s.assignId===a.id);
    return`<div class="assign-card">
      <div class="assign-title">${{a.title}}</div>
      <div class="assign-meta">📚 ${{a.subject}} · 🏫 ${{a.cls}} · 📅 Due: ${{a.due||'No deadline'}} · Max: ${{a.maxScore}} marks</div>
      <div class="assign-desc">${{a.desc||'No description.'}}</div>
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;">
        <span class="bdg bdg-info">${{subs.length}} submission(s)</span>
        <div style="display:flex;gap:6px;">
          <button class="btn btn-ok btn-sm" onclick="tShow('submissions')">View Submissions</button>
          <button class="btn btn-d btn-sm" onclick="removeAssign('${{a.id}}')">Delete</button>
        </div>
      </div>
    </div>`;
  }}).join('');
}}

function removeAssign(id){{
  if(!confirm('Delete this assignment?'))return;
  store.set('assignments',(store.get('assignments')||[]).filter(a=>a.id!==id));
  renderAssignments();
}}

// ── SUBMISSIONS ────────────────────────────────────────────
function renderSubmissions(){{
  const subs=store.get('submissions')||[];
  const el=document.getElementById('subsList');
  if(!el)return;
  if(!subs.length){{el.innerHTML='<p style="color:#aaa;font-size:13px;">No submissions yet.</p>';return;}}
  el.innerHTML=subs.map(s=>{{
    const assign=(store.get('assignments')||[]).find(a=>a.id===s.assignId)||{{}};
    return`<div class="assign-card">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
        <div>
          <div class="assign-title">${{s.studentName}} <span style="font-weight:400;color:#888;">— ${{assign.title||'Assignment'}}</span></div>
          <div class="assign-meta">Submitted: ${{s.submittedAt}} · Subject: ${{assign.subject||'—'}}</div>
          <div class="assign-desc" style="background:#f8f9fc;border-radius:8px;padding:10px;margin:8px 0;">${{s.answer}}</div>
          ${{s.grade?`<span class="bdg bdg-ok">Graded: ${{s.grade}}/${{assign.maxScore||100}}</span>`:'<span class="bdg bdg-warn">Awaiting Grade</span>'}}
        </div>
        ${{!s.grade?`<div style="display:flex;gap:8px;align-items:center;"><input type="number" id="grade_${{s.id}}" placeholder="Score" min="0" max="${{assign.maxScore||100}}" style="width:80px;padding:7px;border:1px solid #ddd;border-radius:7px;font-size:13px;"/><button class="btn btn-ok btn-sm" onclick="gradeSubmission('${{s.id}}')">Grade</button></div>`:''}}
      </div>
    </div>`;
  }}).join('');
}}

function gradeSubmission(id){{
  const grade=document.getElementById('grade_'+id).value;
  if(!grade){{alert('Enter a grade.');return;}}
  const subs=store.get('submissions')||[];
  const idx=subs.findIndex(s=>s.id===id);
  if(idx>-1){{subs[idx].grade=grade;store.set('submissions',subs);}}
  alert('✅ Grade saved!');
  renderSubmissions();
}}

// ── SCORES / RESULTS ──────────────────────────────────────
function uploadScore(){{
  const sid=document.getElementById('scStudent').value;
  const students=store.get('students')||[];
  const student=students.find(s=>s.id===sid);
  if(!student){{alert('Select a student.');return;}}
  const score=document.getElementById('scScore').value;
  const total=document.getElementById('scTotal').value;
  if(!score||!total){{alert('Enter score and total marks.');return;}}
  const r={{
    id:'R'+Date.now(),
    studentId:sid,studentName:student.name,studentCls:student.cls,
    subject:document.getElementById('scSubject').value,
    type:document.getElementById('scType').value,
    term:document.getElementById('scTerm').value,
    session:document.getElementById('scSession').value,
    score:Number(score),total:Number(total),
    remark:document.getElementById('scRemark').value,
    status:'pending',  // pending | approved
    uploadedAt:new Date().toISOString().split('T')[0]
  }};
  store.push('results',r);
  ['scScore','scRemark'].forEach(id=>document.getElementById(id).value='');
  alert('✅ Score submitted for approval!\\n⏳ Principal/Admin will review before it is visible to parents.');
  tShow('results');
}}

function renderResults(){{
  const results=store.get('results')||[];
  const tbody=document.getElementById('resultsTbody');
  if(!results.length){{tbody.innerHTML='<tr><td colspan="6" style="text-align:center;color:#aaa;padding:20px;">No results uploaded yet.</td></tr>';return;}}
  tbody.innerHTML=results.map(r=>`<tr>
    <td><strong>${{r.studentName}}</strong><br/><span style="font-size:11px;color:#888;">${{r.studentCls}}</span></td>
    <td>${{r.subject}}</td>
    <td>${{r.type}}</td>
    <td><strong style="color:var(--pc);">${{r.score}}/${{r.total}}</strong> <span style="font-size:11px;color:#888;">(${{ Math.round(r.score/r.total*100)}}%)</span></td>
    <td>${{r.term}} · ${{r.session}}</td>
    <td><span class="bdg ${{r.status==='approved'?'bdg-ok':'bdg-warn'}}">${{r.status==='approved'?'✓ Approved':'⏳ Pending'}}</span></td>
  </tr>`).join('');
}}

// ── DASHBOARD REFRESH ──────────────────────────────────────
function refreshDash(){{
  const students=store.get('students')||[];
  const assigns=store.get('assignments')||[];
  const subs=store.get('submissions')||[];
  const pending=subs.filter(s=>!s.grade);
  document.getElementById('dashStudents').textContent=students.length;
  document.getElementById('dashAssign').textContent=assigns.length;
  document.getElementById('dashSubs').textContent=subs.length;
  document.getElementById('dashPending').textContent=pending.length;
  const subEl=document.getElementById('dashSubsList');
  subEl.innerHTML=pending.length?pending.slice(0,3).map(s=>{{
    const a=(store.get('assignments')||[]).find(x=>x.id===s.assignId)||{{}};
    return`<div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #f5f5f5;font-size:13px;">
      <div><strong>${{s.studentName}}</strong> — ${{a.title||'Assignment'}}</div>
      <span class="bdg bdg-warn">Ungraded</span>
    </div>`;
  }}).join(''):'<p style="color:#aaa;font-size:13px;">No pending submissions.</p>';
  const aEl=document.getElementById('dashAssignList');
  aEl.innerHTML=assigns.length?assigns.slice(0,3).map(a=>`<div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #f5f5f5;font-size:13px;">
    <div><strong>${{a.title}}</strong><span style="color:#888;"> — ${{a.cls}}</span></div>
    <span style="font-size:11px;color:#888;">Due ${{a.due||'—'}}</span>
  </div>`).join(''):'<p style="color:#aaa;font-size:13px;">No assignments yet.</p>';
}}

// Auto-login if session exists
if(store.get('loggedIn')){{
  document.getElementById('loginView').classList.add('hidden');
  document.getElementById('appView').classList.remove('hidden');
  initTeacher();
}}
</script>
</body>
</html>
""")

# ══════════════════════════════════════════════════════════════
# PARENT PORTAL
# ══════════════════════════════════════════════════════════════
write("templates/portals/parent.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Parent Portal · Golden Stars Academy</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css"/>
<style>
{PORTAL_CSS}
:root{{--pc:#16a34a;--pc-light:#dcfce7;}}
</style>
</head>
<body>

<!-- LOGIN -->
<div id="loginView">
  <div style="min-height:100vh;background:linear-gradient(135deg,#052e16,#16a34a);display:flex;align-items:center;justify-content:center;padding:20px;">
    <div class="login-box">
      <div style="display:flex;justify-content:center;margin-bottom:14px;">{LOGO_SVG.replace('width="36" height="36"','width="64" height="64"')}</div>
      <h1>Parent Portal</h1>
      <div class="sub">Golden Stars Academy — Parent/Guardian Login</div>
      <div id="loginErr" class="flash flash-err hidden"></div>
      <div class="fg"><label>Email Address</label><input type="email" id="pEmail" placeholder="parent@email.com"/></div>
      <div class="fg"><label>Password / Admission Number</label><input type="password" id="pPass" placeholder="••••••••"/></div>
      <button class="btn-full" onclick="parentLogin()">Sign In</button>
      <div style="text-align:center;margin-top:14px;">
        <a href="/" style="font-size:12px;color:#888;">← Back to Website</a>
      </div>
      <div style="background:#f5f6f8;border-radius:8px;padding:10px;margin-top:14px;font-size:11px;color:#888;text-align:center;">
        Demo: parent@gsa.com / parent123
      </div>
    </div>
  </div>
</div>

<!-- APP -->
<div id="appView" class="hidden">
  <div class="pnav">
    <div class="pnav-logo">{LOGO_SVG}<div class="pnav-title">Golden Stars Academy<small>Parent Portal</small></div></div>
    <div class="pnav-user">
      <div class="pnav-av" style="background:var(--pc)">P</div>
      <div><div class="pnav-name" id="pName">Parent</div><div class="pnav-role">Parent / Guardian</div></div>
      <button class="logout-btn" onclick="parentLogout()">Sign Out</button>
    </div>
  </div>

  <div class="shell">
    <div class="sidebar">
      <div class="sb-sec">Overview</div>
      <div class="sb-link on" onclick="pShow('dashboard')"><i class="ti ti-dashboard"></i> Dashboard</div>
      <div class="sb-link" onclick="pShow('ward')"><i class="ti ti-user-circle"></i> My Ward</div>
      <div class="sb-sec">Academics</div>
      <div class="sb-link" onclick="pShow('results')"><i class="ti ti-award"></i> Results &amp; Scores</div>
      <div class="sb-link" onclick="pShow('assignments')"><i class="ti ti-clipboard-list"></i> Assignments</div>
      <div class="sb-sec">School</div>
      <div class="sb-link" onclick="pShow('notices')"><i class="ti ti-bell"></i> Notices</div>
      <div class="sb-link" onclick="pShow('fees')"><i class="ti ti-cash"></i> Fee Statement</div>
    </div>

    <div class="main">

      <!-- DASHBOARD -->
      <div class="page active" id="p-dashboard">
        <h2 style="font-size:18px;font-weight:700;margin-bottom:5px;">Welcome back! 👋</h2>
        <p style="font-size:13px;color:#888;margin-bottom:18px;">Here's a quick overview of your ward's progress.</p>
        <div class="sg">
          <div class="sc"><div class="sc-icon">📊</div><div class="sc-val" id="pTotalResults">0</div><div class="sc-lbl">Results Available</div></div>
          <div class="sc"><div class="sc-icon">📋</div><div class="sc-val" id="pTotalAssign">0</div><div class="sc-lbl">Assignments</div></div>
          <div class="sc"><div class="sc-icon">✅</div><div class="sc-val" id="pSubmitted">0</div><div class="sc-lbl">Submitted</div></div>
          <div class="sc"><div class="sc-icon">📢</div><div class="sc-val" id="pNotices">0</div><div class="sc-lbl">Notices</div></div>
        </div>
        <div class="card">
          <div class="card-hd"><div><div class="card-title">Latest Approved Results</div><div class="card-sub">Only results approved by the Principal are shown</div></div><button class="btn btn-p btn-sm" onclick="pShow('results')">View All</button></div>
          <div id="dashResults"><p style="color:#aaa;font-size:13px;">No approved results yet.</p></div>
        </div>
        <div class="card">
          <div class="card-hd"><div><div class="card-title">Pending Assignments</div></div><button class="btn btn-p btn-sm" onclick="pShow('assignments')">View All</button></div>
          <div id="dashAssign"><p style="color:#aaa;font-size:13px;">No assignments.</p></div>
        </div>
      </div>

      <!-- MY WARD -->
      <div class="page" id="p-ward">
        <div class="card" style="max-width:480px;">
          <div class="card-title" style="margin-bottom:18px;">My Ward's Profile</div>
          <div id="wardProfile"><p style="color:#aaa;font-size:13px;">No student linked to this account. Contact the school.</p></div>
        </div>
      </div>

      <!-- RESULTS -->
      <div class="page" id="p-results">
        <div class="card">
          <div class="card-hd"><div><div class="card-title">Results &amp; Scores</div><div class="card-sub">Only Principal-approved results are visible here</div></div></div>
          <div id="resultsList"><p style="color:#aaa;font-size:13px;">No approved results available yet.</p></div>
        </div>
      </div>

      <!-- ASSIGNMENTS -->
      <div class="page" id="p-assignments">
        <div class="card">
          <div class="card-hd"><div><div class="card-title">Assignments</div><div class="card-sub">Active homework and classwork for your ward's class</div></div></div>
          <div id="pAssignList"><p style="color:#aaa;font-size:13px;">No assignments at this time.</p></div>
        </div>
      </div>

      <!-- NOTICES -->
      <div class="page" id="p-notices">
        <div class="card">
          <div class="card-title" style="margin-bottom:16px;">School Notices &amp; Announcements</div>
          <div id="noticesList"><p style="color:#aaa;font-size:13px;">Loading notices...</p></div>
        </div>
      </div>

      <!-- FEES -->
      <div class="page" id="p-fees">
        <div class="card">
          <div class="card-title" style="margin-bottom:16px;">Fee Statement</div>
          <div id="feesList"><p style="color:#aaa;font-size:13px;">Loading fee schedule...</p></div>
        </div>
      </div>

    </div>
  </div>
</div>

<script>
const DEMO={{email:'parent@gsa.com',password:'parent123',name:'Mrs. Okonkwo',wardName:'Chioma Okonkwo',wardClass:'JSS 2',wardAdm:'GSA/2024/001'}};
const store={{get:k=>JSON.parse(localStorage.getItem('gsa_t_'+k)||'null'),set:(k,v)=>localStorage.setItem('gsa_t_'+k,JSON.stringify(v))}};

function parentLogin(){{
  const e=document.getElementById('pEmail').value.trim();
  const p=document.getElementById('pPass').value;
  const err=document.getElementById('loginErr');
  if(e===DEMO.email&&p===DEMO.password){{
    document.getElementById('loginView').classList.add('hidden');
    document.getElementById('appView').classList.remove('hidden');
    initParent();
  }} else {{
    err.textContent='Invalid email or password.'; err.classList.remove('hidden');
  }}
}}

function parentLogout(){{
  document.getElementById('loginView').classList.remove('hidden');
  document.getElementById('appView').classList.add('hidden');
}}

function initParent(){{
  document.getElementById('pName').textContent=DEMO.name;
  refreshDashP(); renderWard(); loadNotices(); loadFees();
}}

function pShow(pg){{
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.getElementById('p-'+pg).classList.add('active');
  if(pg==='results')renderResults();
  if(pg==='assignments')renderPAssign();
  if(pg==='notices')loadNotices();
  if(pg==='fees')loadFees();
  if(pg==='dashboard')refreshDashP();
}}

function renderWard(){{
  // Find student by matching parent email or use demo
  const students=store.get('students')||[];
  const found=students.find(s=>s.parentEmail===DEMO.email)||null;
  const s=found||{{name:DEMO.wardName,cls:DEMO.wardClass,admNo:DEMO.wardAdm,parent:DEMO.name,gender:'Female'}};
  document.getElementById('wardProfile').innerHTML=`
    <div style="display:flex;align-items:center;gap:16px;margin-bottom:18px;">
      <div style="width:60px;height:60px;border-radius:50%;background:var(--pc);display:flex;align-items:center;justify-content:center;color:#fff;font-size:24px;font-weight:700;">${{s.name[0]}}</div>
      <div><div style="font-size:16px;font-weight:700;">${{s.name}}</div><div style="font-size:13px;color:#888;">${{s.cls}} · ${{s.admNo}}</div></div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
      <div style="background:#f5f6f8;border-radius:8px;padding:12px;"><div style="font-size:11px;color:#888;margin-bottom:3px;">CLASS</div><div style="font-weight:600;">${{s.cls}}</div></div>
      <div style="background:#f5f6f8;border-radius:8px;padding:12px;"><div style="font-size:11px;color:#888;margin-bottom:3px;">ADMISSION NO.</div><div style="font-weight:600;">${{s.admNo}}</div></div>
      <div style="background:#f5f6f8;border-radius:8px;padding:12px;"><div style="font-size:11px;color:#888;margin-bottom:3px;">GENDER</div><div style="font-weight:600;">${{s.gender||'—'}}</div></div>
      <div style="background:#f5f6f8;border-radius:8px;padding:12px;"><div style="font-size:11px;color:#888;margin-bottom:3px;">PARENT</div><div style="font-weight:600;">${{s.parent||DEMO.name}}</div></div>
    </div>`;
}}

function renderResults(){{
  const results=(store.get('results')||[]).filter(r=>r.status==='approved');
  const el=document.getElementById('resultsList');
  if(!results.length){{el.innerHTML='<p style="color:#aaa;font-size:13px;">No approved results available. Results appear here after the Principal/Admin approves them.</p>';return;}}
  // Group by term
  const byTerm={{}};
  results.forEach(r=>{{if(!byTerm[r.term])byTerm[r.term]=[];byTerm[r.term].push(r);}});
  el.innerHTML=Object.entries(byTerm).map(([term,rs])=>`
    <div class="result-card">
      <div class="result-hd"><h3>${{term}} · ${{rs[0].session}}</h3><span style="font-size:12px;opacity:.8;">${{rs[0].studentName}}</span></div>
      <div class="result-body">
        ${{rs.map(r=>{{
          const pct=Math.round(r.score/r.total*100);
          const color=pct>=70?'#16a34a':pct>=50?'#f59e0b':'#dc2626';
          return`<div class="score-row">
            <span style="min-width:140px;">${{r.subject}} <span style="font-size:10px;color:#888;">(${{r.type}})</span></span>
            <div class="score-bar-wrap"><div class="score-bar" style="width:${{pct}}%;background:${{color}};"></div></div>
            <strong style="min-width:60px;text-align:right;color:${{color}};">${{r.score}}/${{r.total}}</strong>
            <span style="min-width:40px;text-align:right;font-size:11px;color:${{color}};">${{pct}}%</span>
          </div>`;
        }}).join('')}}
        <div style="padding:10px 18px;background:#f8f9fc;display:flex;justify-content:space-between;font-size:13px;">
          <span>Average</span>
          <strong>${{Math.round(rs.reduce((a,r)=>a+r.score/r.total*100,0)/rs.length)}}%</strong>
        </div>
      </div>
    </div>`).join('');
}}

function renderPAssign(){{
  const assigns=store.get('assignments')||[];
  const subs=store.get('submissions')||[];
  const el=document.getElementById('pAssignList');
  if(!assigns.length){{el.innerHTML='<p style="color:#aaa;font-size:13px;">No assignments at this time.</p>';return;}}
  el.innerHTML=assigns.map(a=>{{
    const sub=subs.find(s=>s.assignId===a.id&&s.studentName===DEMO.wardName);
    return`<div class="assign-card">
      <div class="assign-title">${{a.title}}</div>
      <div class="assign-meta">📚 ${{a.subject}} · 🏫 ${{a.cls}} · 📅 Due: ${{a.due||'No deadline'}}</div>
      <div class="assign-desc">${{a.desc||'See teacher for details.'}}</div>
      ${{sub?`<span class="bdg bdg-ok">✓ Submitted — Grade: ${{sub.grade||'Awaiting grade'}}</span>`:
        `<span class="bdg bdg-warn">⏳ Not yet submitted</span>`}}
    </div>`;
  }}).join('');
}}

function loadNotices(){{
  fetch('/api/news').then(r=>r.json()).then(items=>{{
    const el=document.getElementById('noticesList');
    if(!items.length){{el.innerHTML='<p style="color:#aaa;font-size:13px;">No notices at this time.</p>';return;}}
    el.innerHTML=items.map(n=>`<div style="padding:14px 0;border-bottom:1px solid #f5f5f5;">
      <div style="font-weight:700;font-size:14px;margin-bottom:4px;">${{n.title}}</div>
      <div style="font-size:13px;color:#555;line-height:1.6;margin-bottom:5px;">${{n.body}}</div>
      <div style="font-size:11px;color:#aaa;">${{n.date}}</div>
    </div>`).join('');
    document.getElementById('pNotices').textContent=items.length;
  }}).catch(()=>{{document.getElementById('noticesList').innerHTML='<p style="color:#aaa;font-size:13px;">Could not load notices.</p>';}});
}}

function loadFees(){{
  fetch('/api/fees').then(r=>r.json()).then(items=>{{
    const el=document.getElementById('feesList');
    if(!items.length){{el.innerHTML='<p style="color:#aaa;font-size:13px;">Fee schedule not yet published. Contact the school office.</p>';return;}}
    el.innerHTML=`<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Level</th><th>Term</th><th>Session</th><th>Amount (₦)</th><th>Status</th></tr></thead>
    <tbody>${{items.map(f=>`<tr><td><strong>${{f.level}}</strong></td><td>${{f.term}}</td><td>${{f.session}}</td>
    <td><strong style="color:var(--pc);">₦${{Number(f.amount).toLocaleString()}}</strong></td>
    <td><span class="bdg bdg-ok">✓ Approved</span></td></tr>`).join('')}}</tbody></table></div>`;
  }}).catch(()=>{{}});
}}

function refreshDashP(){{
  const results=(store.get('results')||[]).filter(r=>r.status==='approved');
  const assigns=store.get('assignments')||[];
  const subs=store.get('submissions')||[];
  document.getElementById('pTotalResults').textContent=results.length;
  document.getElementById('pTotalAssign').textContent=assigns.length;
  document.getElementById('pSubmitted').textContent=subs.length;
  const rEl=document.getElementById('dashResults');
  rEl.innerHTML=results.length?results.slice(0,3).map(r=>`<div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #f5f5f5;font-size:13px;">
    <div><strong>${{r.subject}}</strong> — ${{r.type}} · ${{r.term}}</div>
    <strong style="color:var(--pc);">${{r.score}}/${{r.total}}</strong>
  </div>`).join(''):'<p style="color:#aaa;font-size:13px;">No approved results yet.</p>';
  const aEl=document.getElementById('dashAssign');
  aEl.innerHTML=assigns.length?assigns.slice(0,3).map(a=>`<div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #f5f5f5;font-size:13px;">
    <div><strong>${{a.title}}</strong><span style="color:#888;"> — ${{a.subject}}</span></div>
    <span style="font-size:11px;color:#888;">Due ${{a.due||'—'}}</span>
  </div>`).join(''):'<p style="color:#aaa;font-size:13px;">No assignments.</p>';
}}
initParent();
</script>
</body>
</html>
""")

# ══════════════════════════════════════════════════════════════
# STUDENT PORTAL
# ══════════════════════════════════════════════════════════════
write("templates/portals/student.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Student Portal · Golden Stars Academy</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css"/>
<style>
{PORTAL_CSS}
:root{{--pc:#0891b2;--pc-light:#e0f2fe;}}
</style>
</head>
<body>

<!-- LOGIN -->
<div id="loginView">
  <div style="min-height:100vh;background:linear-gradient(135deg,#0c4a6e,#0891b2);display:flex;align-items:center;justify-content:center;padding:20px;">
    <div class="login-box">
      <div style="display:flex;justify-content:center;margin-bottom:14px;">{LOGO_SVG.replace('width="36" height="36"','width="64" height="64"')}</div>
      <h1>Student Portal</h1>
      <div class="sub">Golden Stars Academy — Student Login</div>
      <div id="loginErr" class="flash flash-err hidden"></div>
      <div class="fg"><label>Admission Number / Student ID</label><input type="text" id="sId" placeholder="e.g. GSA/2024/001"/></div>
      <div class="fg"><label>Password</label><input type="password" id="sPass" placeholder="••••••••"/></div>
      <button class="btn-full" onclick="studentLogin()">Sign In</button>
      <div style="text-align:center;margin-top:14px;">
        <a href="/" style="font-size:12px;color:#888;">← Back to Website</a>
      </div>
      <div style="background:#f5f6f8;border-radius:8px;padding:10px;margin-top:14px;font-size:11px;color:#888;text-align:center;">
        Demo: GSA/2024/001 / student123
      </div>
    </div>
  </div>
</div>

<!-- APP -->
<div id="appView" class="hidden">
  <div class="pnav">
    <div class="pnav-logo">{LOGO_SVG}<div class="pnav-title">Golden Stars Academy<small>Student Portal</small></div></div>
    <div class="pnav-user">
      <div class="pnav-av" style="background:var(--pc)">S</div>
      <div><div class="pnav-name" id="sName">Student</div><div class="pnav-role" id="sClass">Class</div></div>
      <button class="logout-btn" onclick="studentLogout()">Sign Out</button>
    </div>
  </div>

  <div class="shell">
    <div class="sidebar">
      <div class="sb-sec">Main</div>
      <div class="sb-link on" onclick="sShow('dashboard')"><i class="ti ti-dashboard"></i> Dashboard</div>
      <div class="sb-link" onclick="sShow('profile')"><i class="ti ti-user-circle"></i> My Profile</div>
      <div class="sb-sec">Academics</div>
      <div class="sb-link" onclick="sShow('assignments')"><i class="ti ti-clipboard-list"></i> My Assignments</div>
      <div class="sb-link" onclick="sShow('submit')"><i class="ti ti-send"></i> Submit Work</div>
      <div class="sb-link" onclick="sShow('results')"><i class="ti ti-award"></i> My Results</div>
      <div class="sb-sec">School</div>
      <div class="sb-link" onclick="sShow('notices')"><i class="ti ti-bell"></i> Notices</div>
      <div class="sb-link" onclick="sShow('calendar')"><i class="ti ti-calendar"></i> Calendar</div>
    </div>

    <div class="main">

      <!-- DASHBOARD -->
      <div class="page active" id="s-dashboard">
        <h2 style="font-size:18px;font-weight:700;margin-bottom:5px;">Hello, <span id="sGreet">Student</span>! 🌟</h2>
        <p style="font-size:13px;color:#888;margin-bottom:18px;">Here's your academic snapshot.</p>
        <div class="sg">
          <div class="sc"><div class="sc-icon">📋</div><div class="sc-val" id="sDashAssign">0</div><div class="sc-lbl">Assignments</div></div>
          <div class="sc"><div class="sc-icon">✅</div><div class="sc-val" id="sDashSubmitted">0</div><div class="sc-lbl">Submitted</div></div>
          <div class="sc"><div class="sc-icon">⏳</div><div class="sc-val" id="sDashPending">0</div><div class="sc-lbl">Pending</div></div>
          <div class="sc"><div class="sc-icon">📊</div><div class="sc-val" id="sDashResults">0</div><div class="sc-lbl">Results</div></div>
        </div>
        <div class="card">
          <div class="card-hd"><div><div class="card-title">Pending Assignments</div><div class="card-sub">Complete and submit before the deadline</div></div><button class="btn btn-p btn-sm" onclick="sShow('assignments')">View All</button></div>
          <div id="sDashAssignList"><p style="color:#aaa;font-size:13px;">No pending assignments.</p></div>
        </div>
        <div class="card">
          <div class="card-hd"><div><div class="card-title">Recent Results</div><div class="card-sub">Approved results from your teachers</div></div><button class="btn btn-p btn-sm" onclick="sShow('results')">View All</button></div>
          <div id="sDashResults"><p style="color:#aaa;font-size:13px;">No results yet.</p></div>
        </div>
      </div>

      <!-- PROFILE -->
      <div class="page" id="s-profile">
        <div class="card" style="max-width:440px;">
          <div class="card-title" style="margin-bottom:18px;">My Profile</div>
          <div id="sProfileContent"></div>
        </div>
      </div>

      <!-- ASSIGNMENTS -->
      <div class="page" id="s-assignments">
        <div class="card">
          <div class="card-hd"><div><div class="card-title">My Assignments</div><div class="card-sub">All homework and classwork assigned to you</div></div></div>
          <div id="sAssignList"><p style="color:#aaa;font-size:13px;">No assignments at this time.</p></div>
        </div>
      </div>

      <!-- SUBMIT WORK -->
      <div class="page" id="s-submit">
        <div class="card" style="max-width:580px;">
          <div class="card-title" style="margin-bottom:4px;">Submit Assignment</div>
          <div class="card-sub" style="margin-bottom:18px;">Your submission will be sent directly to your teacher for grading</div>
          <div class="fg"><label>Select Assignment</label><select id="subAssign"><option value="">— Choose assignment —</option></select></div>
          <div class="fg"><label>Your Answer / Work</label><textarea id="subAnswer" placeholder="Type your answer here, or describe what you have done..." style="min-height:140px;"></textarea></div>
          <div class="fg"><label>Additional Notes (optional)</label><input type="text" id="subNote" placeholder="Any notes for your teacher..."/></div>
          <button class="btn btn-p" onclick="submitWork()" style="margin-bottom:8px;"><i class="ti ti-send"></i> Submit to Teacher</button>
          <p style="font-size:11px;color:#888;">Your teacher will receive your submission and grade it. Check back here for your grade.</p>
        </div>
      </div>

      <!-- RESULTS -->
      <div class="page" id="s-results">
        <div class="card">
          <div class="card-hd"><div><div class="card-title">My Results</div><div class="card-sub">Results appear here after Principal/Admin approval</div></div></div>
          <div id="sResultsList"><p style="color:#aaa;font-size:13px;">No approved results yet.</p></div>
        </div>
      </div>

      <!-- NOTICES -->
      <div class="page" id="s-notices">
        <div class="card">
          <div class="card-title" style="margin-bottom:16px;">School Notices</div>
          <div id="sNoticesList"><p style="color:#aaa;font-size:13px;">Loading...</p></div>
        </div>
      </div>

      <!-- CALENDAR -->
      <div class="page" id="s-calendar">
        <div class="card">
          <div class="card-title" style="margin-bottom:16px;">Academic Calendar</div>
          <div id="sCalList"><p style="color:#aaa;font-size:13px;">Loading...</p></div>
        </div>
      </div>

    </div>
  </div>
</div>

<script>
const DEMO={{id:'GSA/2024/001',password:'student123',name:'Chioma Okonkwo',cls:'JSS 2',gender:'Female',parent:'Mrs. Okonkwo'}};
const store={{get:k=>JSON.parse(localStorage.getItem('gsa_t_'+k)||'null'),set:(k,v)=>localStorage.setItem('gsa_t_'+k,JSON.stringify(v)),push:(k,v)=>{{const a=store.get(k)||[];a.push(v);store.set(k,a);}}}};

function studentLogin(){{
  const id=document.getElementById('sId').value.trim();
  const p=document.getElementById('sPass').value;
  const err=document.getElementById('loginErr');
  if(id===DEMO.id&&p===DEMO.password){{
    document.getElementById('loginView').classList.add('hidden');
    document.getElementById('appView').classList.remove('hidden');
    initStudent();
  }} else {{
    err.textContent='Invalid student ID or password.'; err.classList.remove('hidden');
  }}
}}

function studentLogout(){{
  document.getElementById('loginView').classList.remove('hidden');
  document.getElementById('appView').classList.add('hidden');
}}

function initStudent(){{
  document.getElementById('sName').textContent=DEMO.name;
  document.getElementById('sClass').textContent=DEMO.cls;
  document.getElementById('sGreet').textContent=DEMO.name.split(' ')[0];
  renderProfile(); populateAssignDropdown(); refreshDashS();
}}

function sShow(pg){{
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.getElementById('s-'+pg).classList.add('active');
  if(pg==='assignments')renderSAssign();
  if(pg==='submit')populateAssignDropdown();
  if(pg==='results')renderSResults();
  if(pg==='notices')loadSNotices();
  if(pg==='calendar')loadSCal();
  if(pg==='dashboard')refreshDashS();
}}

function renderProfile(){{
  document.getElementById('sProfileContent').innerHTML=`
    <div style="display:flex;align-items:center;gap:16px;margin-bottom:18px;">
      <div style="width:60px;height:60px;border-radius:50%;background:var(--pc);display:flex;align-items:center;justify-content:center;color:#fff;font-size:24px;font-weight:700;">${{DEMO.name[0]}}</div>
      <div><div style="font-size:16px;font-weight:700;">${{DEMO.name}}</div><div style="font-size:13px;color:#888;">${{DEMO.cls}}</div></div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
      <div style="background:#f5f6f8;border-radius:8px;padding:12px;"><div style="font-size:11px;color:#888;margin-bottom:3px;">ADMISSION NO.</div><div style="font-weight:600;">${{DEMO.id}}</div></div>
      <div style="background:#f5f6f8;border-radius:8px;padding:12px;"><div style="font-size:11px;color:#888;margin-bottom:3px;">CLASS</div><div style="font-weight:600;">${{DEMO.cls}}</div></div>
      <div style="background:#f5f6f8;border-radius:8px;padding:12px;"><div style="font-size:11px;color:#888;margin-bottom:3px;">GENDER</div><div style="font-weight:600;">${{DEMO.gender}}</div></div>
      <div style="background:#f5f6f8;border-radius:8px;padding:12px;"><div style="font-size:11px;color:#888;margin-bottom:3px;">PARENT/GUARDIAN</div><div style="font-weight:600;">${{DEMO.parent}}</div></div>
    </div>`;
}}

function renderSAssign(){{
  const assigns=store.get('assignments')||[];
  const subs=store.get('submissions')||[];
  const el=document.getElementById('sAssignList');
  if(!assigns.length){{el.innerHTML='<p style="color:#aaa;font-size:13px;">No assignments at this time.</p>';return;}}
  el.innerHTML=assigns.map(a=>{{
    const sub=subs.find(s=>s.assignId===a.id&&s.studentName===DEMO.name);
    const overdue=a.due&&new Date(a.due)<new Date()&&!sub;
    return`<div class="assign-card" style="${{overdue?'border-left:3px solid #dc2626;':''}}">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
        <div style="flex:1;">
          <div class="assign-title">${{a.title}} ${{overdue?'<span class="bdg bdg-err">Overdue</span>':''}}</div>
          <div class="assign-meta">📚 ${{a.subject}} · 🏫 ${{a.cls}} · 📅 Due: ${{a.due||'No deadline'}} · Max: ${{a.maxScore}} marks</div>
          <div class="assign-desc">${{a.desc||'See your teacher for instructions.'}}</div>
        </div>
        ${{sub?`<span class="bdg bdg-ok">✓ Submitted — Grade: ${{sub.grade?sub.grade+'/'+((store.get('assignments')||[]).find(x=>x.id===a.id)||{{}}).maxScore:'Awaiting'}}</span>`:
          `<button class="btn btn-p btn-sm" onclick="quickSubmit('${{a.id}}','${{a.title}}')">Submit</button>`}}
      </div>
    </div>`;
  }}).join('');
}}

function quickSubmit(aid,title){{
  document.getElementById('subAssign').value=aid;
  sShow('submit');
}}

function populateAssignDropdown(){{
  const assigns=store.get('assignments')||[];
  const subs=store.get('submissions')||[];
  const pending=assigns.filter(a=>!subs.find(s=>s.assignId===a.id&&s.studentName===DEMO.name));
  const sel=document.getElementById('subAssign');
  sel.innerHTML='<option value="">— Choose assignment —</option>'+pending.map(a=>`<option value="${{a.id}}">${{a.title}} (${{a.subject}})</option>`).join('');
}}

function submitWork(){{
  const aid=document.getElementById('subAssign').value;
  const answer=document.getElementById('subAnswer').value.trim();
  if(!aid){{alert('Select an assignment.');return;}}
  if(!answer){{alert('Write your answer before submitting.');return;}}
  const already=(store.get('submissions')||[]).find(s=>s.assignId===aid&&s.studentName===DEMO.name);
  if(already){{alert('You already submitted this assignment.');return;}}
  store.push('submissions',{{
    id:'SUB'+Date.now(),assignId:aid,
    studentName:DEMO.name,studentCls:DEMO.cls,
    answer,note:document.getElementById('subNote').value,
    submittedAt:new Date().toISOString().split('T')[0],grade:null
  }});
  document.getElementById('subAnswer').value='';
  document.getElementById('subNote').value='';
  alert('✅ Assignment submitted successfully!\\nYour teacher will review and grade it.');
  sShow('assignments');
}}

function renderSResults(){{
  const results=(store.get('results')||[]).filter(r=>r.status==='approved'&&r.studentName===DEMO.name);
  const el=document.getElementById('sResultsList');
  if(!results.length){{el.innerHTML='<p style="color:#aaa;font-size:13px;">No approved results yet. Results appear here after the Principal approves them.</p>';return;}}
  const byTerm={{}};
  results.forEach(r=>{{if(!byTerm[r.term])byTerm[r.term]=[];byTerm[r.term].push(r);}});
  el.innerHTML=Object.entries(byTerm).map(([term,rs])=>`
    <div class="result-card" style="margin-bottom:16px;">
      <div class="result-hd"><h3>${{term}} · ${{rs[0].session}}</h3></div>
      ${{rs.map(r=>{{
        const pct=Math.round(r.score/r.total*100);
        const col=pct>=70?'#16a34a':pct>=50?'#f59e0b':'#dc2626';
        const grade=pct>=70?'A':pct>=60?'B':pct>=50?'C':pct>=45?'D':'F';
        return`<div class="score-row">
          <span style="min-width:130px;">${{r.subject}}</span>
          <div class="score-bar-wrap"><div class="score-bar" style="width:${{pct}}%;background:${{col}};"></div></div>
          <strong style="min-width:55px;text-align:right;color:${{col}};">${{r.score}}/${{r.total}}</strong>
          <span class="bdg" style="background:${{col}}22;color:${{col}};min-width:30px;text-align:center;">${{grade}}</span>
        </div>`;
      }}).join('')}}
    </div>`).join('');
}}

function loadSNotices(){{
  fetch('/api/news').then(r=>r.json()).then(items=>{{
    const el=document.getElementById('sNoticesList');
    el.innerHTML=items.length?items.map(n=>`<div style="padding:12px 0;border-bottom:1px solid #f5f5f5;">
      <div style="font-weight:700;font-size:14px;margin-bottom:3px;">${{n.title}}</div>
      <div style="font-size:13px;color:#555;line-height:1.6;margin-bottom:4px;">${{n.body}}</div>
      <div style="font-size:11px;color:#aaa;">${{n.date}}</div>
    </div>`).join(''):'<p style="color:#aaa;font-size:13px;">No notices.</p>';
  }}).catch(()=>{{}});
}}

function loadSCal(){{
  fetch('/api/calendar').then(r=>r.json()).then(items=>{{
    const TC={{Resumption:'#16a34a',Holiday:'#9333ea',Exam:'#dc2626',Event:'#0891b2',Closure:'#b45309'}};
    const el=document.getElementById('sCalList');
    el.innerHTML=items.length?items.sort((a,b)=>a.date.localeCompare(b.date)).map(c=>`
      <div style="display:flex;gap:12px;align-items:flex-start;padding:12px 0;border-bottom:1px solid #f5f5f5;">
        <span style="background:${{TC[c.type]||'#666'}}22;color:${{TC[c.type]||'#666'}};padding:3px 10px;border-radius:10px;font-size:11px;font-weight:700;flex-shrink:0;">${{c.type}}</span>
        <div><div style="font-weight:700;font-size:13px;">${{c.title}}</div>
        <div style="font-size:12px;color:#888;">${{c.date}}${{c.note?' · '+c.note:''}}</div></div>
      </div>`).join(''):'<p style="color:#aaa;font-size:13px;">No calendar entries.</p>';
  }}).catch(()=>{{}});
}}

function refreshDashS(){{
  const assigns=store.get('assignments')||[];
  const subs=(store.get('submissions')||[]).filter(s=>s.studentName===DEMO.name);
  const results=(store.get('results')||[]).filter(r=>r.status==='approved'&&r.studentName===DEMO.name);
  const pending=assigns.filter(a=>!subs.find(s=>s.assignId===a.id));
  document.getElementById('sDashAssign').textContent=assigns.length;
  document.getElementById('sDashSubmitted').textContent=subs.length;
  document.getElementById('sDashPending').textContent=pending.length;
  document.getElementById('sDashResults').textContent=results.length;
  const aEl=document.getElementById('sDashAssignList');
  aEl.innerHTML=pending.length?pending.slice(0,3).map(a=>`<div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #f5f5f5;font-size:13px;">
    <div><strong>${{a.title}}</strong><span style="color:#888;"> — ${{a.subject}}</span></div>
    <div style="display:flex;align-items:center;gap:8px;"><span style="font-size:11px;color:#888;">Due ${{a.due||'—'}}</span>
    <button class="btn btn-p btn-sm" onclick="quickSubmit('${{a.id}}','${{a.title}}')">Submit</button></div>
  </div>`).join(''):'<p style="color:#aaa;font-size:13px;">All assignments submitted! ✓</p>';
  const rEl=document.getElementById('sDashResults');
  rEl.innerHTML=results.length?results.slice(0,3).map(r=>`<div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #f5f5f5;font-size:13px;">
    <div><strong>${{r.subject}}</strong> — ${{r.type}}</div>
    <strong style="color:var(--pc);">${{r.score}}/${{r.total}}</strong>
  </div>`).join(''):'<p style="color:#aaa;font-size:13px;">No results yet.</p>';
}}

initStudent();
</script>
</body>
</html>
""")

print("\n✅ All portal files created!")
print("📁 templates/portals/teacher.html")
print("📁 templates/portals/parent.html")
print("📁 templates/portals/student.html")
print("\n🚀 Now run: python update_routes.py")