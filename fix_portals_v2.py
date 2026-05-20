import os

def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK {path}")

# ── ADMIN PARENTS (with edit + search) ───────────────────────
admin_parents = '''{% extends "admin/base.html" %}
{% block title %}Parent Accounts{% endblock %}
{% block page_title %}Parent Accounts{% endblock %}
{% block content %}
<div class="card-hd">
  <div>
    <div class="card-title">Parent Accounts</div>
    <div class="card-sub">Create parent logins linked to student records</div>
  </div>
  <button class="btn btn-p" onclick="showForm('createForm')">
    <i class="ti ti-plus"></i> Add Parent
  </button>
</div>

<!-- CREATE FORM -->
<div class="card" id="createForm" style="display:none;border-left:4px solid #1a3a6b">
  <div class="card-hd"><div class="card-title"><i class="ti ti-user-plus"></i> Create Parent Account</div></div>
  <form method="post" action="/admin/parents/create">
    <div class="fg-row">
      <div class="fg"><label>Parent Name *</label><input type="text" name="name" required placeholder="Full name"></div>
      <div class="fg"><label>Email *</label><input type="email" name="email" required placeholder="parent@email.com"></div>
    </div>
    <div class="fg-row">
      <div class="fg"><label>Password *</label><input type="password" name="password" required placeholder="Set a password"></div>
      <div class="fg"><label>Phone Number</label><input type="text" name="phone" placeholder="+234..."></div>
    </div>
    <div class="fg">
      <label>Link Students to This Parent</label>
      <input type="text" id="searchCreate" placeholder="Search by name, class or admission no..." oninput="filterStudents('gridCreate','searchCreate')"
        style="margin-bottom:8px;padding:8px 12px;border:1px solid #ddd;border-radius:7px;width:100%;font-size:13px">
      <div id="gridCreate" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:8px;background:#f8f9fc;border:1px solid #ddd;border-radius:7px;padding:12px;max-height:220px;overflow-y:auto">
        {% for s in students %}
        <label class="student-item" data-name="{{ s.full_name|lower }}" data-class="{{ s.class_name|lower }}" data-adm="{{ s.admission_no|lower }}"
          style="display:flex;align-items:center;gap:8px;cursor:pointer;padding:7px 9px;border-radius:6px;border:1px solid #eee;background:#fff;font-size:13px">
          <input type="checkbox" name="student_check" value="{{ s.id }}" onchange="updateIds('gridCreate','studentIdsField','selectedDisplay')" style="width:15px;height:15px;cursor:pointer;flex-shrink:0">
          <span>
            <strong>{{ s.full_name }}</strong>
            <small style="display:block;color:#888">{{ s.class_name }} &bull; {{ s.admission_no }}</small>
          </span>
        </label>
        {% else %}
        <p style="color:#aaa;font-size:13px;padding:8px">No students yet. Add via Staff portal first.</p>
        {% endfor %}
      </div>
      <input type="hidden" name="student_ids" id="studentIdsField">
      <div style="font-size:12px;color:#888;margin-top:5px">Selected: <span id="selectedDisplay" style="color:#1a3a6b;font-weight:600">none</span></div>
    </div>
    <div style="display:flex;gap:10px;margin-top:10px">
      <button type="submit" class="btn btn-p"><i class="ti ti-check"></i> Create Account</button>
      <button type="button" class="btn btn-o" onclick="hideAll()">Cancel</button>
    </div>
  </form>
</div>

<!-- EDIT FORMS (one per parent, hidden) -->
{% for p in parents %}
<div class="card" id="editForm{{ p.id }}" style="display:none;border-left:4px solid #f59e0b">
  <div class="card-hd"><div class="card-title"><i class="ti ti-edit"></i> Edit Parent: {{ p.name }}</div></div>
  <form method="post" action="/admin/parents/{{ p.id }}/edit">
    <div class="fg-row">
      <div class="fg"><label>Parent Name *</label><input type="text" name="name" required value="{{ p.name }}"></div>
      <div class="fg"><label>Email *</label><input type="email" name="email" required value="{{ p.email }}"></div>
    </div>
    <div class="fg-row">
      <div class="fg"><label>New Password <small style="color:#888">(leave blank to keep current)</small></label><input type="password" name="password" placeholder="Leave blank to keep"></div>
      <div class="fg"><label>Phone</label><input type="text" name="phone" value="{{ p.phone or '' }}"></div>
    </div>
    <div class="fg">
      <label>Linked Students</label>
      <input type="text" id="searchEdit{{ p.id }}" placeholder="Search students..." oninput="filterStudents('gridEdit{{ p.id }}','searchEdit{{ p.id }}')"
        style="margin-bottom:8px;padding:8px 12px;border:1px solid #ddd;border-radius:7px;width:100%;font-size:13px">
      <div id="gridEdit{{ p.id }}" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:8px;background:#f8f9fc;border:1px solid #ddd;border-radius:7px;padding:12px;max-height:220px;overflow-y:auto">
        {% set current_ids = p.student_ids.split(",") if p.student_ids else [] %}
        {% for s in students %}
        <label class="student-item" data-name="{{ s.full_name|lower }}" data-class="{{ s.class_name|lower }}" data-adm="{{ s.admission_no|lower }}"
          style="display:flex;align-items:center;gap:8px;cursor:pointer;padding:7px 9px;border-radius:6px;border:1px solid #eee;background:#fff;font-size:13px">
          <input type="checkbox" name="student_check" value="{{ s.id }}"
            {{ "checked" if s.id|string in current_ids else "" }}
            onchange="updateIds('gridEdit{{ p.id }}','editIds{{ p.id }}','editDisplay{{ p.id }}')"
            style="width:15px;height:15px;cursor:pointer;flex-shrink:0">
          <span>
            <strong>{{ s.full_name }}</strong>
            <small style="display:block;color:#888">{{ s.class_name }} &bull; {{ s.admission_no }}</small>
          </span>
        </label>
        {% endfor %}
      </div>
      <input type="hidden" name="student_ids" id="editIds{{ p.id }}" value="{{ p.student_ids }}">
      <div style="font-size:12px;color:#888;margin-top:5px">Selected: <span id="editDisplay{{ p.id }}" style="color:#1a3a6b;font-weight:600">{{ p.student_ids or "none" }}</span></div>
    </div>
    <div style="display:flex;gap:10px;margin-top:10px">
      <button type="submit" class="btn btn-p"><i class="ti ti-check"></i> Save Changes</button>
      <button type="button" class="btn btn-o" onclick="hideAll()">Cancel</button>
    </div>
  </form>
</div>
{% endfor %}

<!-- PARENTS TABLE -->
<div class="card">
  <div class="card-hd">
    <div>
      <div class="card-title">All Parent Accounts</div>
      <div class="card-sub">{{ parents|length }} parent(s) registered</div>
    </div>
    <input type="text" placeholder="Search parents..." oninput="filterTable(this,'parentsTbl')"
      style="padding:7px 12px;border:1px solid #ddd;border-radius:7px;font-size:13px;width:220px">
  </div>
  <div class="tbl-wrap">
    <table class="tbl" id="parentsTbl">
      <thead>
        <tr>
          <th>#</th><th>Parent</th><th>Email</th><th>Phone</th>
          <th>Linked Students</th><th>Status</th><th>Created</th><th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {% for p in parents %}
        <tr>
          <td>{{ loop.index }}</td>
          <td>
            <div style="display:flex;align-items:center;gap:10px">
              <div style="width:34px;height:34px;border-radius:50%;background:#1a3a6b;color:#ffd700;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;flex-shrink:0">
                {{ p.name[:1].upper() }}
              </div>
              <div>
                <div style="font-weight:600">{{ p.name }}</div>
                <div style="font-size:11px;color:#888">{{ p.phone or "No phone" }}</div>
              </div>
            </div>
          </td>
          <td style="color:#555">{{ p.email }}</td>
          <td>{{ p.phone or "—" }}</td>
          <td>
            {% if p.student_ids %}
              {% for sid in p.student_ids.split(",") %}
                {% if sid.strip().isdigit() %}
                  {% set found = students | selectattr("id","equalto",sid.strip()|int) | first | default(none) %}
                  {% if found %}
                  <span class="badge b-ic" style="margin:1px;display:inline-block">{{ found.full_name }}<small style="opacity:.7"> ({{ found.class_name }})</small></span>
                  {% endif %}
                {% endif %}
              {% endfor %}
            {% else %}
              <span style="color:#aaa;font-size:12px">None linked</span>
            {% endif %}
          </td>
          <td><span class="badge {{ "b-active" if p.status=="active" else "b-inactive" }}">{{ p.status|title }}</span></td>
          <td style="color:#888;font-size:12px">{{ p.created }}</td>
          <td>
            <div style="display:flex;gap:6px">
              <button class="btn btn-o btn-sm" onclick="showForm('editForm{{ p.id }}')">
                <i class="ti ti-edit"></i> Edit
              </button>
              <form method="post" action="/admin/parents/{{ p.id }}/delete" onsubmit="return confirm(\'Delete {{ p.name }}?\')">
                <button type="submit" class="btn btn-d btn-sm"><i class="ti ti-trash"></i></button>
              </form>
            </div>
          </td>
        </tr>
        {% else %}
        <tr>
          <td colspan="8" style="text-align:center;padding:40px;color:#aaa">
            <i class="ti ti-user-heart" style="font-size:32px;display:block;margin-bottom:8px"></i>
            No parent accounts yet.
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>

<script>
function showForm(id) {
  hideAll();
  document.getElementById(id).style.display = 'block';
  document.getElementById(id).scrollIntoView({behavior:'smooth', block:'start'});
}
function hideAll() {
  document.getElementById('createForm').style.display = 'none';
  {% for p in parents %}
  document.getElementById('editForm{{ p.id }}').style.display = 'none';
  {% endfor %}
}
function updateIds(gridId, fieldId, displayId) {
  const checked = [...document.querySelectorAll('#' + gridId + ' input[type=checkbox]:checked')].map(c => c.value);
  document.getElementById(fieldId).value = checked.join(',');
  document.getElementById(displayId).textContent = checked.length ? checked.join(', ') : 'none';
}
function filterStudents(gridId, searchId) {
  const q = document.getElementById(searchId).value.toLowerCase();
  document.querySelectorAll('#' + gridId + ' .student-item').forEach(el => {
    const match = el.dataset.name.includes(q) || el.dataset.class.includes(q) || el.dataset.adm.includes(q);
    el.style.display = match ? 'flex' : 'none';
  });
}
function filterTable(input, tableId) {
  const q = input.value.toLowerCase();
  document.querySelectorAll('#' + tableId + ' tbody tr').forEach(row => {
    row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
  });
}
</script>
{% endblock %}'''

write("templates/admin/parents.html", admin_parents)

# ── LOGIN PAGES WITH SCHOOL LOGO ──────────────────────────────
LOGIN_BASE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} &mdash; Golden Stars Academy</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{{min-height:100vh;background:linear-gradient(135deg,#1a2540 0%,#2d4a7a 100%);display:flex;align-items:center;justify-content:center;padding:20px;}}
.login-card{{background:#fff;border-radius:18px;padding:2.5rem 2rem;width:100%;max-width:430px;box-shadow:0 24px 64px rgba(0,0,0,.35);}}
.logo-wrap{{text-align:center;margin-bottom:1.5rem;}}
.logo-wrap img{{max-height:80px;max-width:180px;object-fit:contain;}}
.logo-fallback{{width:80px;height:80px;border-radius:50%;background:#1a2540;display:inline-flex;align-items:center;justify-content:center;font-size:2rem;}}
.school-name{{font-weight:700;color:#1a2540;font-size:1.15rem;margin-top:.5rem;}}
.portal-badge{{background:#1a2540;color:#c9a84c;padding:4px 16px;border-radius:20px;font-size:.78rem;font-weight:700;letter-spacing:.5px;display:inline-block;margin-top:6px;}}
.form-label{{font-weight:600;font-size:.875rem;color:#374151;}}
.form-control{{border-radius:8px;padding:.65rem .9rem;font-size:.9rem;border:1.5px solid #e5e7eb;}}
.form-control:focus{{border-color:#c9a84c;box-shadow:0 0 0 3px rgba(201,168,76,.15);}}
.btn-login{{background:#c9a84c;color:#fff;border:none;width:100%;padding:.8rem;border-radius:8px;font-weight:700;font-size:1rem;letter-spacing:.3px;transition:background .2s;}}
.btn-login:hover{{background:#b8942e;color:#fff;}}
.divider{{text-align:center;color:#9ca3af;font-size:.8rem;margin:1rem 0;}}
.back-link{{text-align:center;margin-top:1rem;}}
.back-link a{{color:#6b7280;font-size:.82rem;text-decoration:none;}}
.back-link a:hover{{color:#1a2540;}}
</style>
</head>
<body>
<div class="login-card">
  <div class="logo-wrap">
    {{% if school_logo and school_logo.url %}}
      <img src="{{{{ school_logo.url }}}}" alt="{{{{ school_logo.alt_text or 'Golden Stars Academy' }}}}">
    {{% else %}}
      <div class="logo-fallback">&#127983;</div>
    {{% endif %}}
    <div class="school-name">Golden Stars Academy</div>
    <div class="portal-badge">{portal_label}</div>
  </div>

  {{% for m in flash_msgs %}}
  <div class="alert alert-{{{{ 'danger' if m.cat=='error' else 'success' }}}} py-2 small mb-3">{{{{ m.msg }}}}</div>
  {{% endfor %}}

  <form method="post" action="{form_action}">
    {form_fields}
    <div class="mb-4">
      <label class="form-label">Password</label>
      <input type="password" name="password" class="form-control" placeholder="&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;" required>
    </div>
    <button type="submit" class="btn btn-login">Sign In &rarr;</button>
  </form>
  <div class="back-link">
    <a href="/">&#8592; Back to School Website</a>
  </div>
</div>
</body></html>'''

staff_fields = '''    <div class="mb-3">
      <label class="form-label">Email Address</label>
      <input type="email" name="email" class="form-control" placeholder="staff@goldenstarsacademy.com" required autofocus>
    </div>'''

parent_fields = '''    <div class="mb-3">
      <label class="form-label">Email Address</label>
      <input type="email" name="email" class="form-control" placeholder="parent@email.com" required autofocus>
    </div>'''

student_fields = '''    <div class="mb-3">
      <label class="form-label">Admission Number</label>
      <input type="text" name="admission_no" class="form-control" placeholder="e.g. GSA/2024/001" required autofocus>
      <div class="form-text" style="font-size:.78rem;color:#9ca3af">Default password is your admission number</div>
    </div>'''

write("templates/portals/staff_login.html",
      LOGIN_BASE.format(title="Staff Login", portal_label="Staff Portal",
                        form_action="/staff/login", form_fields=staff_fields))

write("templates/portals/parent_login.html",
      LOGIN_BASE.format(title="Parent Login", portal_label="Parent Portal",
                        form_action="/parent/login", form_fields=parent_fields))

write("templates/portals/student_login.html",
      LOGIN_BASE.format(title="Student Login", portal_label="Student Portal",
                        form_action="/student/login", form_fields=student_fields))

print("\nDone! Now add the edit route to main.py")