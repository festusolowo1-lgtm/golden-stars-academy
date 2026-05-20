import os

def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK {path}")

# ── ADMIN PARENTS ─────────────────────────────────────────────
admin_parents = '''{% extends "admin/base.html" %}
{% block title %}Parent Accounts{% endblock %}
{% block page_title %}Parent Accounts{% endblock %}
{% block content %}
<div class="card-hd">
  <div>
    <div class="card-title">Parent Accounts</div>
    <div class="card-sub">Create parent logins linked to student records</div>
  </div>
  <button class="btn btn-p" onclick="document.getElementById('createForm').style.display=document.getElementById('createForm').style.display=='none'?'block':'none'">
    <i class="ti ti-plus"></i> Add Parent
  </button>
</div>

<!-- CREATE FORM -->
<div class="card" id="createForm" style="display:none;border-left:4px solid #1a3a6b">
  <div class="card-hd"><div class="card-title">Create Parent Account</div></div>
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
      <label>Link Students</label>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px;background:#f8f9fc;border:1px solid #ddd;border-radius:7px;padding:12px;max-height:200px;overflow-y:auto" id="studentGrid">
        {% for s in students %}
        <label style="display:flex;align-items:center;gap:8px;cursor:pointer;padding:6px 8px;border-radius:6px;border:1px solid #eee;background:#fff;font-size:13px">
          <input type="checkbox" name="student_check" value="{{ s.id }}" onchange="updateIds()" style="width:16px;height:16px;cursor:pointer">
          <span><strong>{{ s.full_name }}</strong><br><small class="card-sub">{{ s.class_name }} &bull; Adm: {{ s.admission_no }}</small></span>
        </label>
        {% else %}
        <p class="card-sub" style="padding:8px">No students added yet. Add students via the Staff portal first.</p>
        {% endfor %}
      </div>
      <input type="hidden" name="student_ids" id="studentIdsField">
      <div style="font-size:12px;color:#888;margin-top:5px">Selected IDs: <span id="selectedDisplay" style="color:#1a3a6b;font-weight:600">none</span></div>
    </div>
    <div style="display:flex;gap:10px;margin-top:8px">
      <button type="submit" class="btn btn-p"><i class="ti ti-check"></i> Create Account</button>
      <button type="button" class="btn btn-o" onclick="document.getElementById('createForm').style.display='none'">Cancel</button>
    </div>
  </form>
</div>

<!-- PARENTS TABLE -->
<div class="card">
  <div class="card-hd">
    <div>
      <div class="card-title">All Parent Accounts</div>
      <div class="card-sub">{{ parents|length }} parent(s) registered</div>
    </div>
  </div>
  <div class="tbl-wrap">
    <table class="tbl">
      <thead>
        <tr>
          <th>#</th>
          <th>Parent</th>
          <th>Email</th>
          <th>Phone</th>
          <th>Linked Students</th>
          <th>Status</th>
          <th>Created</th>
          <th>Actions</th>
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
                  {% set found = students | selectattr("id", "equalto", sid.strip()|int) | first | default(none) %}
                  {% if found %}
                  <span class="badge b-ic" style="margin:1px">{{ found.full_name }} ({{ found.class_name }})</span>
                  {% endif %}
                {% endif %}
              {% endfor %}
            {% else %}
              <span style="color:#aaa">None linked</span>
            {% endif %}
          </td>
          <td><span class="badge {{ "b-active" if p.status=="active" else "b-inactive" }}">{{ p.status|title }}</span></td>
          <td style="color:#888;font-size:12px">{{ p.created }}</td>
          <td>
            <form method="post" action="/admin/parents/{{ p.id }}/delete" onsubmit="return confirm(\'Delete {{ p.name }}? This cannot be undone.\')">
              <button type="submit" class="btn btn-d btn-sm"><i class="ti ti-trash"></i> Delete</button>
            </form>
          </td>
        </tr>
        {% else %}
        <tr>
          <td colspan="8" style="text-align:center;padding:40px;color:#aaa">
            <i class="ti ti-user-heart" style="font-size:32px;display:block;margin-bottom:8px"></i>
            No parent accounts yet. Click "Add Parent" to create one.
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>

<script>
function updateIds() {
  const checked = [...document.querySelectorAll('input[name="student_check"]:checked')].map(c => c.value);
  document.getElementById('studentIdsField').value = checked.join(',');
  document.getElementById('selectedDisplay').textContent = checked.length ? checked.join(', ') : 'none';
}
</script>
{% endblock %}'''

# ── ADMIN STAFF LIST ──────────────────────────────────────────
admin_staff = '''{% extends "admin/base.html" %}
{% block title %}Staff Accounts{% endblock %}
{% block page_title %}Staff Accounts{% endblock %}
{% block content %}
<div class="card-hd">
  <div>
    <div class="card-title">Staff Accounts</div>
    <div class="card-sub">Teacher and staff portal access management</div>
  </div>
  <button class="btn btn-p" onclick="document.getElementById('createForm').style.display=document.getElementById('createForm').style.display=='none'?'block':'none'">
    <i class="ti ti-plus"></i> Add Staff
  </button>
</div>

<!-- CREATE FORM -->
<div class="card" id="createForm" style="display:none;border-left:4px solid #1a3a6b">
  <div class="card-hd"><div class="card-title">Create Staff Account</div></div>
  <form method="post" action="/admin/staff/create">
    <div class="fg-row">
      <div class="fg"><label>Full Name *</label><input type="text" name="name" required placeholder="e.g. Mr. John Adamu"></div>
      <div class="fg"><label>Email *</label><input type="email" name="email" required placeholder="teacher@school.com"></div>
    </div>
    <div class="fg-row">
      <div class="fg"><label>Password *</label><input type="password" name="password" required placeholder="Set a secure password"></div>
      <div class="fg"><label>Role *</label>
        <select name="role">
          <option value="teacher">Teacher</option>
          <option value="headteacher">Head Teacher</option>
          <option value="principal">Principal</option>
        </select>
      </div>
    </div>
    <div class="fg-row">
      <div class="fg"><label>Subject</label><input type="text" name="subject" placeholder="e.g. Mathematics"></div>
      <div class="fg"><label>Form Class</label><input type="text" name="class_name" placeholder="e.g. JSS 1A"></div>
    </div>
    <div class="fg">
      <label>Section</label>
      <select name="section">
        <option value="">— Select Section —</option>
        <option value="Primary">Primary</option>
        <option value="Secondary">Secondary</option>
      </select>
    </div>
    <div style="display:flex;gap:10px;margin-top:8px">
      <button type="submit" class="btn btn-p"><i class="ti ti-check"></i> Create Account</button>
      <button type="button" class="btn btn-o" onclick="document.getElementById('createForm').style.display='none'">Cancel</button>
    </div>
  </form>
</div>

<!-- STAFF TABLE -->
<div class="card">
  <div class="card-hd">
    <div>
      <div class="card-title">All Staff Accounts</div>
      <div class="card-sub">{{ staff|length }} staff member(s)</div>
    </div>
    <a href="/staff/login" target="_blank" class="btn btn-o btn-sm"><i class="ti ti-external-link"></i> Staff Portal</a>
  </div>
  <div class="tbl-wrap">
    <table class="tbl">
      <thead>
        <tr>
          <th>#</th>
          <th>Staff Member</th>
          <th>Email</th>
          <th>Role</th>
          <th>Subject</th>
          <th>Class</th>
          <th>Section</th>
          <th>Status</th>
          <th>Created</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {% for s in staff %}
        <tr>
          <td>{{ loop.index }}</td>
          <td>
            <div style="display:flex;align-items:center;gap:10px">
              <div style="width:34px;height:34px;border-radius:50%;background:#1a3a6b;color:#ffd700;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;flex-shrink:0">
                {{ s.name[:1].upper() }}
              </div>
              <div style="font-weight:600">{{ s.name }}</div>
            </div>
          </td>
          <td style="color:#555">{{ s.email }}</td>
          <td>
            {% set rc = {"teacher":"b-ic","headteacher":"b-me","principal":"b-sa"} %}
            <span class="badge {{ rc.get(s.role,"b-ic") }}">{{ s.role|title }}</span>
          </td>
          <td>{{ s.subject or "—" }}</td>
          <td>{{ s.class_name or "—" }}</td>
          <td>{{ s.section or "—" }}</td>
          <td><span class="badge {{ "b-active" if s.status=="active" else "b-inactive" }}">{{ s.status|title }}</span></td>
          <td style="color:#888;font-size:12px">{{ s.created }}</td>
          <td>
            <form method="post" action="/admin/staff/{{ s.id }}/delete" onsubmit="return confirm(\'Delete {{ s.name }}?\')">
              <button type="submit" class="btn btn-d btn-sm"><i class="ti ti-trash"></i> Delete</button>
            </form>
          </td>
        </tr>
        {% else %}
        <tr>
          <td colspan="10" style="text-align:center;padding:40px;color:#aaa">
            <i class="ti ti-users" style="font-size:32px;display:block;margin-bottom:8px"></i>
            No staff accounts yet. Click "Add Staff" to create one.
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}'''

# ── ADMIN RESULTS ─────────────────────────────────────────────
admin_results = '''{% extends "admin/base.html" %}
{% block title %}Results Approval{% endblock %}
{% block page_title %}Results Approval{% endblock %}
{% block content %}
<div class="card-hd">
  <div>
    <div class="card-title">Results Approval</div>
    <div class="card-sub">Review and approve exam results uploaded by teachers</div>
  </div>
  {% if pending %}
  <form method="post" action="/admin/results/0/approve-all" onsubmit="return confirm(\'Approve ALL {{ pending|length }} pending results?\')">
    <button type="submit" class="btn btn-ok"><i class="ti ti-check-all"></i> Approve All ({{ pending|length }})</button>
  </form>
  {% endif %}
</div>

<!-- PENDING -->
<div class="card" style="border-left:4px solid #dc2626">
  <div class="card-hd">
    <div>
      <div class="card-title" style="color:#dc2626"><i class="ti ti-clock"></i> Pending Approval</div>
      <div class="card-sub">{{ pending|length }} result(s) awaiting your approval</div>
    </div>
  </div>
  {% if pending %}
  <div class="tbl-wrap">
    <table class="tbl">
      <thead>
        <tr><th>Student</th><th>Adm. No.</th><th>Class</th><th>Subject</th><th>CA1</th><th>CA2</th><th>Exam</th><th>Total</th><th>Grade</th><th>Term</th><th>Uploaded By</th><th>Action</th></tr>
      </thead>
      <tbody>
        {% for r in pending %}
        <tr>
          <td style="font-weight:600">{{ r.student_name }}</td>
          <td><span class="badge b-pending">{{ r.admission_no }}</span></td>
          <td>{{ r.class_name }}</td>
          <td>{{ r.subject }}</td>
          <td>{{ r.ca1 }}</td>
          <td>{{ r.ca2 }}</td>
          <td>{{ r.exam }}</td>
          <td style="font-weight:700">{{ r.total }}</td>
          <td>
            {% set gc = {"A":"b-active","B":"b-ic","C":"b-bu","D":"b-me","F":"b-inactive"} %}
            <span class="badge {{ gc.get(r.grade,"b-pending") }}">{{ r.grade }}</span>
          </td>
          <td style="font-size:12px">{{ r.term }}</td>
          <td style="font-size:12px;color:#888">{{ r.uploaded_by }}</td>
          <td>
            <form method="post" action="/admin/results/{{ r.id }}/approve">
              <button type="submit" class="btn btn-ok btn-sm"><i class="ti ti-check"></i> Approve</button>
            </form>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  {% else %}
  <div style="text-align:center;padding:30px;color:#aaa">
    <i class="ti ti-circle-check" style="font-size:36px;display:block;margin-bottom:8px;color:#16a34a"></i>
    All clear — no results pending approval.
  </div>
  {% endif %}
</div>

<!-- APPROVED -->
<div class="card" style="border-left:4px solid #16a34a">
  <div class="card-hd">
    <div>
      <div class="card-title" style="color:#16a34a"><i class="ti ti-circle-check"></i> Approved Results</div>
      <div class="card-sub">Last 50 approved — visible to parents and students</div>
    </div>
  </div>
  {% if approved %}
  <div class="tbl-wrap">
    <table class="tbl">
      <thead>
        <tr><th>Student</th><th>Class</th><th>Subject</th><th>CA1</th><th>CA2</th><th>Exam</th><th>Total</th><th>Grade</th><th>Remark</th><th>Term</th><th>Session</th></tr>
      </thead>
      <tbody>
        {% for r in approved %}
        <tr>
          <td style="font-weight:600">{{ r.student_name }}</td>
          <td>{{ r.class_name }}</td>
          <td>{{ r.subject }}</td>
          <td>{{ r.ca1 }}</td>
          <td>{{ r.ca2 }}</td>
          <td>{{ r.exam }}</td>
          <td style="font-weight:700">{{ r.total }}</td>
          <td>
            {% set gc = {"A":"b-active","B":"b-ic","C":"b-bu","D":"b-me","F":"b-inactive"} %}
            <span class="badge {{ gc.get(r.grade,"b-pending") }}">{{ r.grade }}</span>
          </td>
          <td style="font-size:12px">{{ r.remark }}</td>
          <td style="font-size:12px">{{ r.term }}</td>
          <td style="font-size:12px;color:#888">{{ r.session }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  {% else %}
  <div style="text-align:center;padding:30px;color:#aaa">No approved results yet.</div>
  {% endif %}
</div>
{% endblock %}'''

write("templates/admin/parents.html",    admin_parents)
write("templates/admin/staff_list.html", admin_staff)
write("templates/admin/results.html",    admin_results)

print("\nDone! Refresh your browser.")