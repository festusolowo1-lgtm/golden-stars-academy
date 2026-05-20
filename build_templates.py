import os

os.makedirs("templates/portals", exist_ok=True)
os.makedirs("templates/admin", exist_ok=True)

def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK {path}")

# ── LOGIN BASE ──────────────────────────────────────────────
def login_page(title, portal_label, form_action, extra_field=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - Golden Stars Academy</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{{min-height:100vh;background:linear-gradient(135deg,#1a2540 0%,#2d4a7a 100%);display:flex;align-items:center;justify-content:center;}}
.card{{border:none;border-radius:16px;padding:2.5rem;width:100%;max-width:420px;box-shadow:0 20px 60px rgba(0,0,0,.3);}}
.btn-login{{background:#c9a84c;color:#fff;border:none;width:100%;padding:.75rem;border-radius:8px;font-weight:600;}}
.btn-login:hover{{background:#b8942e;color:#fff;}}
.form-control:focus{{border-color:#c9a84c;box-shadow:0 0 0 .2rem rgba(201,168,76,.25);}}
.badge-portal{{background:#1a2540;color:#c9a84c;padding:4px 14px;border-radius:20px;font-size:.8rem;font-weight:600;}}
</style>
</head>
<body>
<div class="card">
  <div class="text-center mb-4">
    {{% if school_logo and school_logo.url %}}
      <img src="{{{{ school_logo.url }}}}" alt="Logo" style="max-height:65px">
    {{% else %}}
      <div style="font-size:2.5rem">&#127983;</div>
    {{% endif %}}
    <div class="fw-bold mt-2" style="color:#1a2540;font-size:1.1rem">Golden Stars Academy</div>
    <span class="badge-portal d-inline-block mt-1">{portal_label}</span>
  </div>
  {{% for m in flash_msgs %}}
  <div class="alert alert-{{{{ \'danger\' if m.cat==\'error\' else \'success\' }}}} py-2 small">{{{{ m.msg }}}}</div>
  {{% endfor %}}
  <form method="post" action="{form_action}">
    {extra_field}
    <div class="mb-4">
      <label class="form-label fw-semibold">Password</label>
      <input type="password" name="password" class="form-control" placeholder="&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;" required>
    </div>
    <button type="submit" class="btn btn-login">Sign In &rarr;</button>
  </form>
  <div class="text-center mt-3">
    <a href="/" class="text-muted small">&#8592; Back to Website</a>
  </div>
</div>
</body></html>'''

email_field = '''    <div class="mb-3">
      <label class="form-label fw-semibold">Email Address</label>
      <input type="email" name="email" class="form-control" placeholder="email@example.com" required autofocus>
    </div>'''

adm_field = '''    <div class="mb-3">
      <label class="form-label fw-semibold">Admission Number</label>
      <input type="text" name="admission_no" class="form-control" placeholder="e.g. GSA/2024/001" required autofocus>
    </div>
    <div class="mb-1 form-text text-muted small">Default password = your admission number</div>'''

write("templates/portals/staff_login.html",   login_page("Staff Login",   "Staff Portal",   "/staff/login",   email_field))
write("templates/portals/parent_login.html",  login_page("Parent Login",  "Parent Portal",  "/parent/login",  email_field))
write("templates/portals/student_login.html", login_page("Student Login", "Student Portal", "/student/login", adm_field))

# ── PORTAL HEAD ─────────────────────────────────────────────
HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t} - Golden Stars Academy</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css" rel="stylesheet">
<style>
:root{{--gold:#c9a84c;--dark:#1a2540;}}
body{{background:#f0f4f8;font-family:"Segoe UI",sans-serif;}}
.pnav{{background:var(--dark);}}
.pnav .brand span{{color:var(--gold);font-weight:700;}}
.sidebar{{min-height:100vh;background:#1e2d4a;padding-top:1rem;}}
.sidebar .nav-link{{color:#a0aec0;border-radius:8px;margin:2px 8px;padding:10px 14px;}}
.sidebar .nav-link:hover,.sidebar .nav-link.active{{background:rgba(201,168,76,.15);color:var(--gold);}}
.sidebar .nav-link i{{margin-right:8px;}}
.card{{border:none;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,.07);}}
.table th{{background:#f8f9fa;font-size:.82rem;text-transform:uppercase;letter-spacing:.5px;}}
.btn-gold{{background:var(--gold);color:#fff;border:none;}}
.btn-gold:hover{{background:#b8942e;color:#fff;}}
.flash-box{{position:fixed;top:70px;right:20px;z-index:9999;min-width:300px;}}
</style>
</head>'''

# ── STAFF SIDEBAR ────────────────────────────────────────────
def staff_sidebar(active):
    links = [
        ("dashboard",   "ti-dashboard",      "/staff/dashboard", "Dashboard"),
        ("students",    "ti-users",           "/staff/students",  "Students"),
        ("assignments", "ti-clipboard-list",  "/staff/assignments","Assignments"),
        ("results",     "ti-chart-bar",       "/staff/results",   "Results"),
    ]
    nav = ""
    for key, icon, url, label in links:
        cls = "active" if key == active else ""
        nav += f'<a class="nav-link {cls}" href="{url}"><i class="ti {icon}"></i> {label}</a>\n'
    return nav

def staff_layout(title, active, inner):
    sidebar_nav = staff_sidebar(active)
    return HEAD.format(t=title) + f'''
<body>
<nav class="navbar pnav px-3">
  <span class="navbar-brand brand text-light"><i class="ti ti-school text-warning"></i> <span>Staff Portal</span></span>
  <div class="d-flex align-items-center gap-2">
    {{% if staff is defined %}}<span class="text-light small d-none d-md-inline">{{{{ staff.name }}}}</span>{{% endif %}}
    <a href="/staff/logout" class="btn btn-sm btn-outline-light"><i class="ti ti-logout"></i></a>
  </div>
</nav>
{{% for m in flash_msgs %}}
<div class="flash-box alert alert-{{{{ \'danger\' if m.cat==\'error\' else \'success\' }}}} alert-dismissible fade show">{{{{ m.msg }}}}<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>
{{% endfor %}}
<div class="container-fluid">
  <div class="row">
    <div class="col-md-2 sidebar d-none d-md-block">
      <nav class="nav flex-column mt-2">
        {sidebar_nav}
        <hr style="border-color:#2d4a7a">
        <a class="nav-link" href="/staff/logout"><i class="ti ti-logout"></i> Logout</a>
      </nav>
    </div>
    <div class="col-md-10 p-4">
      {inner}
    </div>
  </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body></html>'''

# ── STAFF DASHBOARD ──────────────────────────────────────────
inner_dash = '''
<h4 class="fw-bold mb-1">Welcome, {{ staff.name }}</h4>
<p class="text-muted mb-4">{{ staff.subject }} &bull; Class: {{ staff.class_name or "Not assigned" }}</p>
<div class="row g-3 mb-4">
  <div class="col-6 col-md-3">
    <div class="card p-3 text-center" style="border-left:4px solid #c9a84c">
      <div class="fs-2 fw-bold text-warning">{{ students|length }}</div>
      <div class="small text-muted">My Students</div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="card p-3 text-center" style="border-left:4px solid #4299e1">
      <div class="fs-2 fw-bold text-primary">{{ assignments|length }}</div>
      <div class="small text-muted">Assignments</div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="card p-3 text-center" style="border-left:4px solid #e53e3e">
      <div class="fs-2 fw-bold text-danger">{{ pending_subs|length }}</div>
      <div class="small text-muted">Pending Grading</div>
    </div>
  </div>
</div>
<div class="row g-3">
  <div class="col-md-4">
    <div class="card p-3 text-center h-100">
      <i class="ti ti-users fs-1 text-warning"></i>
      <h6 class="mt-2">Manage Students</h6>
      <p class="small text-muted">Add, view or remove students</p>
      <a href="/staff/students" class="btn btn-gold btn-sm">Open</a>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card p-3 text-center h-100">
      <i class="ti ti-clipboard-list fs-1 text-primary"></i>
      <h6 class="mt-2">Assignments</h6>
      <p class="small text-muted">Create tasks and grade submissions</p>
      <a href="/staff/assignments" class="btn btn-gold btn-sm">Open</a>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card p-3 text-center h-100">
      <i class="ti ti-chart-bar fs-1 text-success"></i>
      <h6 class="mt-2">Upload Results</h6>
      <p class="small text-muted">Enter CA and exam scores</p>
      <a href="/staff/results" class="btn btn-gold btn-sm">Open</a>
    </div>
  </div>
</div>'''

write("templates/portals/staff_dashboard.html", staff_layout("Dashboard", "dashboard", inner_dash))

# ── STAFF STUDENTS ───────────────────────────────────────────
inner_students = '''
<div class="d-flex justify-content-between align-items-center mb-3">
  <h4 class="fw-bold mb-0">Students</h4>
  <button class="btn btn-gold btn-sm" data-bs-toggle="modal" data-bs-target="#addModal">
    <i class="ti ti-plus"></i> Add Student
  </button>
</div>
<div class="card">
  <div class="table-responsive">
    <table class="table table-hover mb-0">
      <thead><tr><th>#</th><th>Name</th><th>Admission No.</th><th>Class</th><th>Gender</th><th>Parent Email</th><th></th></tr></thead>
      <tbody>
        {% for s in students %}
        <tr>
          <td>{{ loop.index }}</td>
          <td class="fw-semibold">{{ s.full_name }}</td>
          <td><span class="badge bg-light text-dark">{{ s.admission_no }}</span></td>
          <td>{{ s.class_name }}</td>
          <td>{{ s.gender }}</td>
          <td class="small text-muted">{{ s.parent_email or "—" }}</td>
          <td>
            <form method="post" action="/staff/students/{{ s.id }}/delete" onsubmit="return confirm(\'Remove?\')">
              <button class="btn btn-sm btn-outline-danger"><i class="ti ti-trash"></i></button>
            </form>
          </td>
        </tr>
        {% else %}
        <tr><td colspan="7" class="text-center text-muted py-4">No students yet.</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
<div class="modal fade" id="addModal" tabindex="-1">
  <div class="modal-dialog"><div class="modal-content">
    <div class="modal-header"><h5 class="modal-title">Add Student</h5><button class="btn-close" data-bs-dismiss="modal"></button></div>
    <form method="post" action="/staff/students/add">
      <div class="modal-body row g-3">
        <div class="col-12"><label class="form-label">Full Name *</label><input type="text" name="full_name" class="form-control" required></div>
        <div class="col-6"><label class="form-label">Admission No. *</label><input type="text" name="admission_no" class="form-control" required placeholder="GSA/2024/001"></div>
        <div class="col-6"><label class="form-label">Class *</label><input type="text" name="class_name" class="form-control" required placeholder="JSS 1A"></div>
        <div class="col-6"><label class="form-label">Level *</label>
          <select name="level" class="form-select"><option>Primary</option><option>JSS</option><option>SSS</option></select>
        </div>
        <div class="col-6"><label class="form-label">Gender *</label>
          <select name="gender" class="form-select"><option>Male</option><option>Female</option></select>
        </div>
        <div class="col-6"><label class="form-label">Parent Email</label><input type="email" name="parent_email" class="form-control"></div>
        <div class="col-6"><label class="form-label">Parent Phone</label><input type="text" name="parent_phone" class="form-control"></div>
        <div class="col-6"><label class="form-label">Session</label><input type="text" name="session" class="form-control" value="2025/2026"></div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button type="submit" class="btn btn-gold">Add Student</button>
      </div>
    </form>
  </div></div>
</div>'''

write("templates/portals/staff_students.html", staff_layout("Students", "students", inner_students))

# ── STAFF ASSIGNMENTS ────────────────────────────────────────
inner_assignments = '''
<div class="d-flex justify-content-between align-items-center mb-3">
  <h4 class="fw-bold mb-0">Assignments</h4>
  <button class="btn btn-gold btn-sm" data-bs-toggle="modal" data-bs-target="#createModal">
    <i class="ti ti-plus"></i> Create
  </button>
</div>
<div class="card">
  <div class="table-responsive">
    <table class="table table-hover mb-0">
      <thead><tr><th>Title</th><th>Subject</th><th>Class</th><th>Due Date</th><th>Term</th><th>Actions</th></tr></thead>
      <tbody>
        {% for a in items %}
        <tr>
          <td class="fw-semibold">{{ a.title }}</td>
          <td>{{ a.subject }}</td>
          <td><span class="badge bg-light text-dark">{{ a.class_name }}</span></td>
          <td>{{ a.due_date }}</td>
          <td><span class="badge bg-info text-dark">{{ a.term }}</span></td>
          <td><a href="/staff/assignments/{{ a.id }}/submissions" class="btn btn-sm btn-outline-primary"><i class="ti ti-eye"></i> Submissions</a></td>
        </tr>
        {% else %}
        <tr><td colspan="6" class="text-center text-muted py-4">No assignments yet.</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
<div class="modal fade" id="createModal" tabindex="-1">
  <div class="modal-dialog"><div class="modal-content">
    <div class="modal-header"><h5 class="modal-title">Create Assignment</h5><button class="btn-close" data-bs-dismiss="modal"></button></div>
    <form method="post" action="/staff/assignments/create">
      <div class="modal-body row g-3">
        <div class="col-12"><label class="form-label">Title *</label><input type="text" name="title" class="form-control" required></div>
        <div class="col-12"><label class="form-label">Description</label><textarea name="description" class="form-control" rows="3"></textarea></div>
        <div class="col-6"><label class="form-label">Subject *</label><input type="text" name="subject" class="form-control" required></div>
        <div class="col-6"><label class="form-label">Class *</label><input type="text" name="class_name" class="form-control" required></div>
        <div class="col-6"><label class="form-label">Due Date *</label><input type="date" name="due_date" class="form-control" required></div>
        <div class="col-6"><label class="form-label">Term</label>
          <select name="term" class="form-select"><option>First Term</option><option>Second Term</option><option selected>Third Term</option></select>
        </div>
        <div class="col-6"><label class="form-label">Session</label><input type="text" name="session" class="form-control" value="2025/2026"></div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button type="submit" class="btn btn-gold">Create</button>
      </div>
    </form>
  </div></div>
</div>'''

write("templates/portals/staff_assignments.html", staff_layout("Assignments", "assignments", inner_assignments))

# ── STAFF SUBMISSIONS ────────────────────────────────────────
staff_subs = HEAD.format(t="Submissions") + '''
<body>
<nav class="navbar pnav px-3">
  <span class="navbar-brand brand text-light"><i class="ti ti-school text-warning"></i> <span>Staff Portal</span></span>
  <a href="/staff/assignments" class="btn btn-sm btn-outline-light"><i class="ti ti-arrow-left"></i> Back</a>
</nav>
{% for m in flash_msgs %}
<div class="flash-box alert alert-{{ "danger" if m.cat=="error" else "success" }} alert-dismissible fade show">{{ m.msg }}<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>
{% endfor %}
<div class="container py-4">
  <div class="card p-3 mb-4">
    <h5 class="fw-bold mb-1">{{ assignment.title }}</h5>
    <p class="text-muted small mb-0">{{ assignment.subject }} | Class: {{ assignment.class_name }} | Due: {{ assignment.due_date }}</p>
  </div>
  <div class="card">
    <div class="table-responsive">
      <table class="table table-hover mb-0">
        <thead><tr><th>Student</th><th>Submitted</th><th>Answer</th><th>File</th><th>Grade</th><th>Status</th><th>Action</th></tr></thead>
        <tbody>
          {% for s in subs %}
          <tr>
            <td class="fw-semibold">{{ s.student_name }}</td>
            <td class="small text-muted">{{ s.submitted_at }}</td>
            <td class="small" style="max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{ s.content or "—" }}</td>
            <td>{% if s.file_url %}<a href="{{ s.file_url }}" target="_blank" class="btn btn-sm btn-outline-secondary"><i class="ti ti-download"></i></a>{% else %}—{% endif %}</td>
            <td>{% if s.grade %}<span class="badge bg-success">{{ s.grade }}</span>{% else %}<span class="text-muted">—</span>{% endif %}</td>
            <td><span class="badge {{ "bg-success" if s.status=="graded" else "bg-warning text-dark" }}">{{ s.status|title }}</span></td>
            <td>
              <button class="btn btn-sm btn-gold" data-bs-toggle="modal" data-bs-target="#gm{{ s.id }}">Grade</button>
              <div class="modal fade" id="gm{{ s.id }}" tabindex="-1">
                <div class="modal-dialog"><div class="modal-content">
                  <div class="modal-header"><h6>Grade: {{ s.student_name }}</h6><button class="btn-close" data-bs-dismiss="modal"></button></div>
                  <form method="post" action="/staff/submissions/{{ s.id }}/grade">
                    <div class="modal-body">
                      <label class="form-label">Grade</label>
                      <input type="text" name="grade" class="form-control mb-2" value="{{ s.grade }}" required placeholder="A, B+, 85">
                      <label class="form-label">Feedback</label>
                      <textarea name="feedback" class="form-control" rows="2">{{ s.feedback }}</textarea>
                    </div>
                    <div class="modal-footer">
                      <button class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancel</button>
                      <button class="btn btn-gold btn-sm">Save</button>
                    </div>
                  </form>
                </div></div>
              </div>
            </td>
          </tr>
          {% else %}
          <tr><td colspan="7" class="text-center text-muted py-4">No submissions yet.</td></tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body></html>'''

write("templates/portals/staff_submissions.html", staff_subs)

# ── STAFF RESULTS ────────────────────────────────────────────
inner_results = '''
<div class="d-flex justify-content-between align-items-center mb-3">
  <h4 class="fw-bold mb-0">Upload Results</h4>
  <button class="btn btn-gold btn-sm" data-bs-toggle="modal" data-bs-target="#upModal">
    <i class="ti ti-upload"></i> Upload
  </button>
</div>
<div class="alert alert-info small mb-3"><i class="ti ti-info-circle"></i> Results require Principal/Admin approval before parents and students can see them.</div>
<div class="card">
  <div class="table-responsive">
    <table class="table table-hover mb-0">
      <thead><tr><th>Student</th><th>Class</th><th>Subject</th><th>CA1</th><th>CA2</th><th>Exam</th><th>Total</th><th>Grade</th><th>Term</th><th>Status</th></tr></thead>
      <tbody>
        {% for r in results %}
        <tr>
          <td>{{ r.student_name }}</td>
          <td>{{ r.class_name }}</td>
          <td>{{ r.subject }}</td>
          <td>{{ r.ca1 }}</td><td>{{ r.ca2 }}</td><td>{{ r.exam }}</td>
          <td class="fw-bold">{{ r.total }}</td>
          <td><span class="badge bg-{{ "success" if r.grade=="A" else "primary" if r.grade=="B" else "warning text-dark" if r.grade=="C" else "danger" }}">{{ r.grade }}</span></td>
          <td class="small">{{ r.term }}</td>
          <td><span class="badge {{ "bg-success" if r.approved else "bg-warning text-dark" }}">{{ "Approved" if r.approved else "Pending" }}</span></td>
        </tr>
        {% else %}
        <tr><td colspan="10" class="text-center text-muted py-4">No results uploaded yet.</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
<div class="modal fade" id="upModal" tabindex="-1">
  <div class="modal-dialog"><div class="modal-content">
    <div class="modal-header"><h5 class="modal-title">Upload Result</h5><button class="btn-close" data-bs-dismiss="modal"></button></div>
    <form method="post" action="/staff/results/upload">
      <div class="modal-body row g-3">
        <div class="col-12"><label class="form-label">Student *</label>
          <select name="student_id" class="form-select" required>
            <option value="">Select student...</option>
            {% for s in students %}<option value="{{ s.id }}">{{ s.full_name }} ({{ s.class_name }})</option>{% endfor %}
          </select>
        </div>
        <div class="col-6"><label class="form-label">Subject *</label><input type="text" name="subject" class="form-control" required></div>
        <div class="col-6"><label class="form-label">Term</label>
          <select name="term" class="form-select"><option>First Term</option><option>Second Term</option><option selected>Third Term</option></select>
        </div>
        <div class="col-4"><label class="form-label">CA1 /20</label><input type="number" name="ca1" class="form-control" min="0" max="20" value="0"></div>
        <div class="col-4"><label class="form-label">CA2 /20</label><input type="number" name="ca2" class="form-control" min="0" max="20" value="0"></div>
        <div class="col-4"><label class="form-label">Exam /60</label><input type="number" name="exam" class="form-control" min="0" max="60" value="0"></div>
        <div class="col-6"><label class="form-label">Session</label><input type="text" name="session" class="form-control" value="2025/2026"></div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button type="submit" class="btn btn-gold">Upload</button>
      </div>
    </form>
  </div></div>
</div>'''

write("templates/portals/staff_results.html", staff_layout("Results", "results", inner_results))

# ── PARENT DASHBOARD ─────────────────────────────────────────
parent_dash = HEAD.format(t="Parent Dashboard") + '''
<body>
<nav class="navbar pnav px-3">
  <span class="navbar-brand brand text-light"><i class="ti ti-school text-warning"></i> <span>Parent Portal</span></span>
  <div class="d-flex align-items-center gap-2">
    <span class="text-light small">{{ parent.name }}</span>
    <a href="/parent/logout" class="btn btn-sm btn-outline-light"><i class="ti ti-logout"></i></a>
  </div>
</nav>
{% for m in flash_msgs %}
<div class="flash-box alert alert-{{ "danger" if m.cat=="error" else "success" }} alert-dismissible fade show">{{ m.msg }}<button class="btn-close" data-bs-dismiss="alert"></button></div>
{% endfor %}
<div class="container py-4">
  <h4 class="fw-bold mb-1">Hello, {{ parent.name }}</h4>
  <p class="text-muted mb-4">Your ward\'s academic summary</p>
  {% if not students %}
  <div class="alert alert-warning"><i class="ti ti-alert-circle"></i> No students linked. Contact admin.</div>
  {% endif %}
  {% for student in students %}
  <div class="card mb-4">
    <div class="card-header d-flex align-items-center gap-3" style="background:#1a2540;color:#fff;border-radius:12px 12px 0 0">
      <div style="width:44px;height:44px;border-radius:50%;background:#c9a84c;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:1.2rem">
        {{ student.full_name[:1] }}
      </div>
      <div>
        <div class="fw-bold">{{ student.full_name }}</div>
        <div class="small opacity-75">{{ student.class_name }} | Adm: {{ student.admission_no }}</div>
      </div>
    </div>
    <div class="card-body">
      <h6 class="fw-bold mb-3"><i class="ti ti-chart-bar text-warning"></i> Exam Results</h6>
      {% if results[student.id] %}
      <div class="table-responsive">
        <table class="table table-sm table-bordered mb-0">
          <thead class="table-light"><tr><th>Subject</th><th>CA1</th><th>CA2</th><th>Exam</th><th>Total</th><th>Grade</th><th>Remark</th><th>Term</th></tr></thead>
          <tbody>
            {% for r in results[student.id] %}
            <tr>
              <td>{{ r.subject }}</td>
              <td>{{ r.ca1 }}</td><td>{{ r.ca2 }}</td><td>{{ r.exam }}</td>
              <td class="fw-bold">{{ r.total }}</td>
              <td><span class="badge bg-{{ "success" if r.grade=="A" else "primary" if r.grade=="B" else "warning text-dark" if r.grade=="C" else "danger" }}">{{ r.grade }}</span></td>
              <td>{{ r.remark }}</td>
              <td class="small text-muted">{{ r.term }}</td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
      {% else %}
      <p class="text-muted small">No approved results yet.</p>
      {% endif %}
    </div>
  </div>
  {% endfor %}
  <div class="text-center mt-3"><a href="/" class="text-muted small">&#8592; Back to School Website</a></div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body></html>'''

write("templates/portals/parent_dashboard.html", parent_dash)

# ── STUDENT DASHBOARD ────────────────────────────────────────
student_dash = HEAD.format(t="Student Dashboard") + '''
<body>
<nav class="navbar pnav px-3">
  <span class="navbar-brand brand text-light"><i class="ti ti-school text-warning"></i> <span>Student Portal</span></span>
  <div class="d-flex align-items-center gap-2">
    <span class="text-light small">{{ student.full_name }}</span>
    <a href="/student/logout" class="btn btn-sm btn-outline-light"><i class="ti ti-logout"></i></a>
  </div>
</nav>
{% for m in flash_msgs %}
<div class="flash-box alert alert-{{ "danger" if m.cat=="error" else "success" }} alert-dismissible fade show">{{ m.msg }}<button class="btn-close" data-bs-dismiss="alert"></button></div>
{% endfor %}
<div class="container py-4">
  <div class="card p-3 mb-4" style="border-left:4px solid #c9a84c">
    <div class="d-flex align-items-center gap-3">
      <div style="width:54px;height:54px;border-radius:50%;background:#1a2540;color:#c9a84c;display:flex;align-items:center;justify-content:center;font-size:1.4rem;font-weight:700">
        {{ student.full_name[:1] }}
      </div>
      <div>
        <div class="fw-bold fs-5">{{ student.full_name }}</div>
        <div class="text-muted small">{{ student.class_name }} | Adm: {{ student.admission_no }} | {{ student.session }}</div>
      </div>
    </div>
  </div>

  <h5 class="fw-bold mb-3"><i class="ti ti-clipboard-list text-primary"></i> Assignments</h5>
  {% for a in assignments %}
  <div class="card mb-3">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start">
        <div>
          <h6 class="fw-bold mb-1">{{ a.title }}</h6>
          <p class="text-muted small mb-1">{{ a.subject }} | Due: {{ a.due_date }} | {{ a.term }}</p>
          {% if a.description %}<p class="small mb-0">{{ a.description }}</p>{% endif %}
        </div>
        {% if my_subs.get(a.id) %}
          <span class="badge {{ "bg-success" if my_subs[a.id].status=="graded" else "bg-warning text-dark" }}">
            {{ "Graded: " + my_subs[a.id].grade if my_subs[a.id].status=="graded" else "Submitted" }}
          </span>
        {% else %}
          <button class="btn btn-gold btn-sm" data-bs-toggle="modal" data-bs-target="#sm{{ a.id }}">Submit</button>
        {% endif %}
      </div>
      {% if my_subs.get(a.id) and my_subs[a.id].feedback %}
      <div class="alert alert-light small mt-2 mb-0"><strong>Feedback:</strong> {{ my_subs[a.id].feedback }}</div>
      {% endif %}
    </div>
  </div>
  <div class="modal fade" id="sm{{ a.id }}" tabindex="-1">
    <div class="modal-dialog"><div class="modal-content">
      <div class="modal-header"><h6>Submit: {{ a.title }}</h6><button class="btn-close" data-bs-dismiss="modal"></button></div>
      <form method="post" action="/student/assignments/{{ a.id }}/submit" enctype="multipart/form-data">
        <div class="modal-body">
          <label class="form-label">Your Answer</label>
          <textarea name="content" class="form-control mb-2" rows="4"></textarea>
          <label class="form-label">Attach File (optional)</label>
          <input type="file" name="file" class="form-control">
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn btn-gold btn-sm">Submit</button>
        </div>
      </form>
    </div></div>
  </div>
  {% else %}
  <div class="alert alert-light">No assignments for your class yet.</div>
  {% endfor %}

  <h5 class="fw-bold mt-4 mb-3"><i class="ti ti-chart-bar text-success"></i> My Results</h5>
  {% if results %}
  <div class="card">
    <div class="table-responsive">
      <table class="table table-sm table-bordered mb-0">
        <thead class="table-light"><tr><th>Subject</th><th>CA1</th><th>CA2</th><th>Exam</th><th>Total</th><th>Grade</th><th>Remark</th><th>Term</th></tr></thead>
        <tbody>
          {% for r in results %}
          <tr>
            <td>{{ r.subject }}</td>
            <td>{{ r.ca1 }}</td><td>{{ r.ca2 }}</td><td>{{ r.exam }}</td>
            <td class="fw-bold">{{ r.total }}</td>
            <td><span class="badge bg-{{ "success" if r.grade=="A" else "primary" if r.grade=="B" else "warning text-dark" if r.grade=="C" else "danger" }}">{{ r.grade }}</span></td>
            <td>{{ r.remark }}</td>
            <td class="small text-muted">{{ r.term }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
  {% else %}
  <div class="alert alert-light">No approved results yet.</div>
  {% endif %}

  <div class="text-center mt-4"><a href="/" class="text-muted small">&#8592; Back to School Website</a></div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body></html>'''

write("templates/portals/student_dashboard.html", student_dash)

# ── ADMIN TEMPLATES ──────────────────────────────────────────
admin_results_html = '''{% extends "admin/base.html" %}
{% block title %}Results Approval{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h4 class="fw-bold mb-0"><i class="ti ti-chart-bar text-warning"></i> Results Approval</h4>
  {% if pending %}
  <form method="post" action="/admin/results/0/approve-all" onsubmit="return confirm(\'Approve ALL pending results?\')">
    <button class="btn btn-success btn-sm"><i class="ti ti-check-all"></i> Approve All ({{ pending|length }})</button>
  </form>
  {% endif %}
</div>
<h6 class="fw-bold mb-2 text-danger">Pending ({{ pending|length }})</h6>
<div class="card mb-4">
  <div class="table-responsive">
    <table class="table table-hover mb-0">
      <thead><tr><th>Student</th><th>Class</th><th>Subject</th><th>CA1</th><th>CA2</th><th>Exam</th><th>Total</th><th>Grade</th><th>Term</th><th>By</th><th>Action</th></tr></thead>
      <tbody>
        {% for r in pending %}
        <tr>
          <td>{{ r.student_name }}</td>
          <td>{{ r.class_name }}</td>
          <td>{{ r.subject }}</td>
          <td>{{ r.ca1 }}</td><td>{{ r.ca2 }}</td><td>{{ r.exam }}</td>
          <td class="fw-bold">{{ r.total }}</td>
          <td><span class="badge bg-warning text-dark">{{ r.grade }}</span></td>
          <td>{{ r.term }}</td>
          <td class="small text-muted">{{ r.uploaded_by }}</td>
          <td>
            <form method="post" action="/admin/results/{{ r.id }}/approve">
              <button class="btn btn-sm btn-success"><i class="ti ti-check"></i> Approve</button>
            </form>
          </td>
        </tr>
        {% else %}
        <tr><td colspan="11" class="text-center text-muted py-3">No pending results.</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
<h6 class="fw-bold mb-2 text-success">Recently Approved (last 50)</h6>
<div class="card">
  <div class="table-responsive">
    <table class="table table-sm mb-0">
      <thead><tr><th>Student</th><th>Class</th><th>Subject</th><th>Total</th><th>Grade</th><th>Term</th></tr></thead>
      <tbody>
        {% for r in approved %}
        <tr>
          <td>{{ r.student_name }}</td><td>{{ r.class_name }}</td><td>{{ r.subject }}</td>
          <td class="fw-bold">{{ r.total }}</td>
          <td><span class="badge bg-success">{{ r.grade }}</span></td>
          <td>{{ r.term }}</td>
        </tr>
        {% else %}
        <tr><td colspan="6" class="text-center text-muted py-3">None yet.</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}'''

admin_staff_html = '''{% extends "admin/base.html" %}
{% block title %}Staff Accounts{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h4 class="fw-bold mb-0"><i class="ti ti-users text-warning"></i> Staff Accounts</h4>
  <button class="btn btn-gold btn-sm" data-bs-toggle="modal" data-bs-target="#csModal">
    <i class="ti ti-plus"></i> Add Staff
  </button>
</div>
<div class="card">
  <div class="table-responsive">
    <table class="table table-hover mb-0">
      <thead><tr><th>#</th><th>Name</th><th>Email</th><th>Role</th><th>Subject</th><th>Class</th><th>Status</th><th>Created</th><th></th></tr></thead>
      <tbody>
        {% for s in staff %}
        <tr>
          <td>{{ loop.index }}</td>
          <td class="fw-semibold">{{ s.name }}</td>
          <td class="small text-muted">{{ s.email }}</td>
          <td><span class="badge bg-primary">{{ s.role|title }}</span></td>
          <td>{{ s.subject or "—" }}</td>
          <td>{{ s.class_name or "—" }}</td>
          <td><span class="badge {{ "bg-success" if s.status=="active" else "bg-secondary" }}">{{ s.status|title }}</span></td>
          <td class="small text-muted">{{ s.created }}</td>
          <td>
            <form method="post" action="/admin/staff/{{ s.id }}/delete" onsubmit="return confirm(\'Delete?\')">
              <button class="btn btn-sm btn-outline-danger"><i class="ti ti-trash"></i></button>
            </form>
          </td>
        </tr>
        {% else %}
        <tr><td colspan="9" class="text-center text-muted py-4">No staff accounts yet.</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
<div class="modal fade" id="csModal" tabindex="-1">
  <div class="modal-dialog"><div class="modal-content">
    <div class="modal-header"><h5 class="modal-title">Create Staff Account</h5><button class="btn-close" data-bs-dismiss="modal"></button></div>
    <form method="post" action="/admin/staff/create">
      <div class="modal-body row g-3">
        <div class="col-12"><label class="form-label">Full Name *</label><input type="text" name="name" class="form-control" required></div>
        <div class="col-6"><label class="form-label">Email *</label><input type="email" name="email" class="form-control" required></div>
        <div class="col-6"><label class="form-label">Password *</label><input type="password" name="password" class="form-control" required></div>
        <div class="col-6"><label class="form-label">Role</label>
          <select name="role" class="form-select">
            <option value="teacher">Teacher</option>
            <option value="headteacher">Head Teacher</option>
            <option value="principal">Principal</option>
          </select>
        </div>
        <div class="col-6"><label class="form-label">Subject</label><input type="text" name="subject" class="form-control" placeholder="e.g. Mathematics"></div>
        <div class="col-6"><label class="form-label">Form Class</label><input type="text" name="class_name" class="form-control" placeholder="e.g. JSS 1A"></div>
        <div class="col-6"><label class="form-label">Section</label>
          <select name="section" class="form-select">
            <option value="">— Select —</option>
            <option value="Primary">Primary</option>
            <option value="Secondary">Secondary</option>
          </select>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button type="submit" class="btn btn-gold">Create</button>
      </div>
    </form>
  </div></div>
</div>
{% endblock %}'''

admin_parents_html = '''{% extends "admin/base.html" %}
{% block title %}Parent Accounts{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h4 class="fw-bold mb-0"><i class="ti ti-user-heart text-warning"></i> Parent Accounts</h4>
  <button class="btn btn-gold btn-sm" data-bs-toggle="modal" data-bs-target="#cpModal">
    <i class="ti ti-plus"></i> Add Parent
  </button>
</div>
<div class="card">
  <div class="table-responsive">
    <table class="table table-hover mb-0">
      <thead><tr><th>#</th><th>Name</th><th>Email</th><th>Phone</th><th>Student IDs</th><th>Status</th><th>Created</th><th></th></tr></thead>
      <tbody>
        {% for p in parents %}
        <tr>
          <td>{{ loop.index }}</td>
          <td class="fw-semibold">{{ p.name }}</td>
          <td class="small text-muted">{{ p.email }}</td>
          <td class="small">{{ p.phone or "—" }}</td>
          <td class="small text-muted">{{ p.student_ids or "—" }}</td>
          <td><span class="badge {{ "bg-success" if p.status=="active" else "bg-secondary" }}">{{ p.status|title }}</span></td>
          <td class="small text-muted">{{ p.created }}</td>
          <td>
            <form method="post" action="/admin/parents/{{ p.id }}/delete" onsubmit="return confirm(\'Delete?\')">
              <button class="btn btn-sm btn-outline-danger"><i class="ti ti-trash"></i></button>
            </form>
          </td>
        </tr>
        {% else %}
        <tr><td colspan="8" class="text-center text-muted py-4">No parent accounts yet.</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
<div class="modal fade" id="cpModal" tabindex="-1">
  <div class="modal-dialog"><div class="modal-content">
    <div class="modal-header"><h5 class="modal-title">Create Parent Account</h5><button class="btn-close" data-bs-dismiss="modal"></button></div>
    <form method="post" action="/admin/parents/create">
      <div class="modal-body row g-3">
        <div class="col-12"><label class="form-label">Parent Name *</label><input type="text" name="name" class="form-control" required></div>
        <div class="col-6"><label class="form-label">Email *</label><input type="email" name="email" class="form-control" required></div>
        <div class="col-6"><label class="form-label">Password *</label><input type="password" name="password" class="form-control" required></div>
        <div class="col-6"><label class="form-label">Phone</label><input type="text" name="phone" class="form-control"></div>
        <div class="col-12">
          <label class="form-label">Link Students (comma-separated IDs)</label>
          <input type="text" name="student_ids" class="form-control" placeholder="e.g. 1,3,7">
          <div class="form-text mt-1">Available students:</div>
          <div class="small text-muted" style="max-height:100px;overflow-y:auto">
            {% for s in students %}
            <span class="badge bg-light text-dark me-1 mb-1">ID {{ s.id }}: {{ s.full_name }} ({{ s.class_name }})</span>
            {% endfor %}
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button type="submit" class="btn btn-gold">Create</button>
      </div>
    </form>
  </div></div>
</div>
{% endblock %}'''

write("templates/admin/results.html",     admin_results_html)
write("templates/admin/staff_list.html",  admin_staff_html)
write("templates/admin/parents.html",     admin_parents_html)

print("\nAll 13 templates created! Run: python -m uvicorn main:app --reload")