"""
Run this script once from your golden-stars/ folder:
    python create_templates.py

It creates all required template files automatically.
"""
import os

BASE = "templates"
ADMIN = os.path.join(BASE, "admin")
os.makedirs(ADMIN, exist_ok=True)
os.makedirs(os.path.join(BASE), exist_ok=True)

# ── HELPER ────────────────────────────────────────────────────
def write(path, content):
    full = os.path.join(*path) if isinstance(path, tuple) else path
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"✅ Created: {full}")

# ══════════════════════════════════════════════════════════════
# BASE LAYOUT
# ══════════════════════════════════════════════════════════════
write((ADMIN, "base.html"), """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{% block title %}Admin{% endblock %} · Golden Stars Academy</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css"/>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Segoe UI',Arial,sans-serif;background:#f5f6f8;color:#1c1c2e;display:flex;min-height:100vh;font-size:14px;}
.sb{width:220px;background:#1a3a6b;color:#fff;display:flex;flex-direction:column;position:fixed;top:0;left:0;height:100vh;overflow-y:auto;z-index:100;flex-shrink:0;}
.sb-top{padding:14px 16px;border-bottom:1px solid rgba(255,255,255,.1);display:flex;align-items:center;gap:10px;}
.sb-logo{width:38px;height:38px;border-radius:50%;object-fit:contain;flex-shrink:0;}
.sb-brand{font-size:12px;font-weight:700;line-height:1.3;}
.sb-brand small{display:block;font-size:10px;opacity:.45;font-weight:400;}
.sb-nav{flex:1;padding:8px 0;}
.sb-sec{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:rgba(255,255,255,.3);padding:10px 16px 3px;}
.sb-a{display:flex;align-items:center;gap:9px;padding:9px 16px;color:rgba(255,255,255,.72);font-size:12px;text-decoration:none;border-left:3px solid transparent;transition:all .15s;}
.sb-a:hover{background:rgba(255,255,255,.08);color:#fff;}
.sb-a.on{background:rgba(255,255,255,.14);border-left-color:#ffd700;color:#fff;font-weight:600;}
.sb-a i{font-size:16px;}
.sb-foot{padding:12px 14px;border-top:1px solid rgba(255,255,255,.1);}
.sb-av{width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:11px;color:#fff;flex-shrink:0;}
.sb-user{display:flex;align-items:center;gap:8px;margin-bottom:9px;}
.sb-uname{font-size:12px;font-weight:700;line-height:1.2;}
.sb-urole{font-size:10px;opacity:.45;}
.sb-out{width:100%;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.13);color:#fff;padding:6px;border-radius:6px;font-size:11px;cursor:pointer;font-family:inherit;}
.sb-out:hover{background:rgba(255,255,255,.14);}
.main{margin-left:220px;flex:1;display:flex;flex-direction:column;min-height:100vh;}
.topbar{background:#fff;padding:11px 22px;border-bottom:1px solid #eee;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:50;box-shadow:0 1px 4px rgba(0,0,0,.05);}
.topbar-title{font-size:14px;font-weight:700;color:#1a3a6b;}
.topbar-sub{font-size:11px;color:#aaa;margin-top:1px;}
.badge{display:inline-block;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600;}
.b-sa{background:#ede9fe;color:#7c3aed;}
.b-ic{background:#dcfce7;color:#16a34a;}
.b-me{background:#e0f2fe;color:#0891b2;}
.b-bu{background:#fef3c7;color:#b45309;}
.b-active{background:#dcfce7;color:#16a34a;}
.b-inactive{background:#fee2e2;color:#dc2626;}
.b-approved{background:#dcfce7;color:#16a34a;}
.b-pending{background:#fef3c7;color:#b45309;}
.content{flex:1;padding:22px;}
.flash{padding:11px 15px;border-radius:8px;font-size:13px;margin-bottom:14px;display:flex;align-items:center;gap:8px;}
.flash-ok{background:#dcfce7;color:#166534;border:1px solid #bbf7d0;}
.flash-err{background:#fee2e2;color:#991b1b;border:1px solid #fecaca;}
.card{background:#fff;border-radius:12px;padding:22px;box-shadow:0 1px 5px rgba(0,0,0,.05);margin-bottom:18px;}
.card-hd{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;flex-wrap:wrap;gap:10px;}
.card-title{font-size:16px;font-weight:700;}
.card-sub{font-size:12px;color:#888;margin-top:2px;}
.tbl{width:100%;border-collapse:collapse;font-size:13px;}
.tbl th{padding:10px 13px;text-align:left;font-weight:600;font-size:11px;color:#666;border-bottom:1px solid #eee;background:#f8f9fc;text-transform:uppercase;letter-spacing:.03em;}
.tbl td{padding:11px 13px;border-bottom:1px solid #f2f2f5;vertical-align:middle;}
.tbl tr:hover td{background:#fafbff;}
.tbl-wrap{overflow-x:auto;}
.fg{margin-bottom:14px;}
.fg label{display:block;font-size:12px;font-weight:600;color:#555;margin-bottom:4px;}
.fg input,.fg select,.fg textarea{width:100%;padding:9px 12px;border:1px solid #ddd;border-radius:7px;font-size:13px;outline:none;font-family:inherit;background:#fff;}
.fg input:focus,.fg select:focus,.fg textarea:focus{border-color:#1a3a6b;}
.fg textarea{resize:vertical;min-height:80px;}
.fg input[type=file]{padding:6px;}
.fg-row{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 18px;border-radius:7px;border:none;font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;text-decoration:none;transition:opacity .15s;}
.btn:hover{opacity:.88;}
.btn-p{background:#1a3a6b;color:#fff;}
.btn-d{background:#dc2626;color:#fff;}
.btn-ok{background:#16a34a;color:#fff;}
.btn-o{background:transparent;border:1.5px solid #1a3a6b;color:#1a3a6b;}
.btn-sm{padding:5px 11px;font-size:12px;}
.sg{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:13px;margin-bottom:22px;}
.sc{background:#fff;border-radius:11px;padding:16px;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,.05);}
.sc-icon{font-size:24px;margin-bottom:5px;}
.sc-val{font-size:24px;font-weight:700;}
.sc-lbl{font-size:11px;color:#888;margin-top:2px;}
.prev{width:90px;height:90px;border-radius:8px;object-fit:contain;border:1px solid #eee;background:#f8f9fc;display:block;margin-top:7px;}
.info-box{background:#e8eef8;border:1px solid #c7d7f0;border-radius:8px;padding:12px 16px;font-size:13px;color:#1a3a6b;margin-bottom:14px;}
</style>
</head>
<body>
<div class="sb">
  <div class="sb-top">
    {% if school_logo and school_logo.url %}
      <img class="sb-logo" src="{{ school_logo.url }}" alt="{{ school_logo.alt_text }}"/>
    {% else %}
      <svg class="sb-logo" viewBox="0 0 300 340" xmlns="http://www.w3.org/2000/svg" style="background:rgba(255,255,255,.08);border-radius:50%">
        <path d="M150 8 L272 54 L272 182 Q272 284 150 332 Q28 284 28 182 L28 54 Z" fill="#E8B830"/>
        <path d="M150 22 L258 62 L258 182 Q258 272 150 316 Q42 272 42 182 L42 62 Z" fill="#CC2200"/>
        <path d="M65 110 L235 110 L235 215 Q235 255 150 285 Q65 255 65 215 Z" fill="#1a3575"/>
        <polygon points="150,95 155,110 171,110 158,120 163,135 150,126 137,135 142,120 129,110 145,110" fill="#F5C518"/>
      </svg>
    {% endif %}
    <div class="sb-brand">Golden Stars<small>Admin Portal</small></div>
  </div>
  <nav class="sb-nav">
    <div class="sb-sec">Main</div>
    <a href="/admin" class="sb-a {% if request.url.path=='/admin' %}on{% endif %}"><i class="ti ti-dashboard"></i> Dashboard</a>
    <a href="/" class="sb-a" target="_blank"><i class="ti ti-world"></i> View Website</a>
    {% if current_user.role=='superadmin' %}
    <div class="sb-sec">Administration</div>
    <a href="/admin/users"    class="sb-a {% if '/admin/users' in request.url.path %}on{% endif %}"><i class="ti ti-users"></i> User Management</a>
    <a href="/admin/logos"    class="sb-a {% if '/admin/logos' in request.url.path %}on{% endif %}"><i class="ti ti-photo-star"></i> Logo Manager</a>
    <a href="/admin/siteinfo" class="sb-a {% if '/admin/siteinfo' in request.url.path %}on{% endif %}"><i class="ti ti-settings"></i> Site Information</a>
    {% endif %}
    {% if current_user.role in ['superadmin','ict'] %}
    <div class="sb-sec">Content</div>
    <a href="/admin/news"     class="sb-a {% if '/admin/news' in request.url.path %}on{% endif %}"><i class="ti ti-news"></i> News</a>
    <a href="/admin/calendar" class="sb-a {% if '/admin/calendar' in request.url.path %}on{% endif %}"><i class="ti ti-calendar-event"></i> Calendar</a>
    {% if current_user.role=='ict' %}
    <a href="/admin/siteinfo" class="sb-a {% if '/admin/siteinfo' in request.url.path %}on{% endif %}"><i class="ti ti-settings"></i> Site Information</a>
    <a href="/admin/logos"    class="sb-a {% if '/admin/logos' in request.url.path %}on{% endif %}"><i class="ti ti-photo-star"></i> Logo Manager</a>
    {% endif %}
    {% endif %}
    {% if current_user.role in ['superadmin','media','ict'] %}
    <div class="sb-sec">Media</div>
    <a href="/admin/gallery" class="sb-a {% if '/admin/gallery' in request.url.path %}on{% endif %}"><i class="ti ti-camera"></i> Gallery &amp; Team</a>
    {% endif %}
    {% if current_user.role in ['superadmin','bursar'] %}
    <div class="sb-sec">Finance</div>
    <a href="/admin/fees" class="sb-a {% if '/admin/fees' in request.url.path %}on{% endif %}"><i class="ti ti-cash"></i> Fee Management</a>
    {% endif %}
  </nav>
  <div class="sb-foot">
    <div class="sb-user">
      {% set rc={'superadmin':'#7c3aed','ict':'#16a34a','media':'#0891b2','bursar':'#b45309'} %}
      <div class="sb-av" style="background:{{ rc.get(current_user.role,'#1a3a6b') }}">{{ current_user.avatar or current_user.name[0] }}</div>
      <div><div class="sb-uname">{{ current_user.name }}</div><div class="sb-urole">{{ current_user.role }}</div></div>
    </div>
    <a href="/admin/logout"><button class="sb-out">Sign Out</button></a>
  </div>
</div>
<div class="main">
  <div class="topbar">
    <div><div class="topbar-title">{% block page_title %}Dashboard{% endblock %}</div><div class="topbar-sub">Golden Stars Academy — Admin Panel</div></div>
    {% set ri={'superadmin':'👑','ict':'🖥️','media':'📸','bursar':'💰'} %}
    {% set bc={'superadmin':'b-sa','ict':'b-ic','media':'b-me','bursar':'b-bu'} %}
    <span class="badge {{ bc.get(current_user.role,'b-ic') }}">{{ ri.get(current_user.role,'') }} {{ current_user.role|title }}</span>
  </div>
  <div class="content">
    {% for f in flash_msgs %}
    <div class="flash {{ 'flash-ok' if f.cat=='success' else 'flash-err' }}">
      <i class="ti ti-{{ 'circle-check' if f.cat=='success' else 'alert-circle' }}"></i> {{ f.msg }}
    </div>
    {% endfor %}
    {% block content %}{% endblock %}
  </div>
</div>
</body>
</html>
""")

# ══════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════
write((ADMIN, "login.html"), """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Admin Login · Golden Stars Academy</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css"/>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Segoe UI',Arial,sans-serif;background:#1a3a6b;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:16px;}
.box{background:#fff;border-radius:18px;padding:34px;width:100%;max-width:380px;box-shadow:0 20px 60px rgba(0,0,0,.3);}
.logo-wrap{display:flex;justify-content:center;margin-bottom:12px;}
h1{font-size:17px;font-weight:700;color:#1a3a6b;text-align:center;margin-bottom:3px;}
.sub{font-size:12px;color:#888;text-align:center;margin-bottom:24px;}
.fg{margin-bottom:14px;}
.fg label{display:block;font-size:12px;font-weight:600;color:#555;margin-bottom:4px;}
.fg input{width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:7px;font-size:13px;outline:none;font-family:inherit;}
.fg input:focus{border-color:#1a3a6b;}
.btn-full{width:100%;padding:12px;background:#1a3a6b;color:#fff;border:none;border-radius:7px;font-size:14px;font-weight:600;cursor:pointer;font-family:inherit;}
.btn-full:hover{opacity:.9;}
.err{background:#fee2e2;color:#991b1b;border:1px solid #fecaca;border-radius:7px;padding:9px 13px;font-size:12px;margin-bottom:14px;display:flex;align-items:center;gap:7px;}
.foot{text-align:center;font-size:11px;color:#aaa;margin-top:14px;}
</style>
</head>
<body>
<div class="box">
  <div class="logo-wrap">
    {% if school_logo and school_logo.url %}
      <img src="{{ school_logo.url }}" alt="{{ school_logo.alt_text }}" style="width:70px;height:70px;border-radius:50%;object-fit:contain;"/>
    {% else %}
      <svg width="70" height="70" viewBox="0 0 300 340" xmlns="http://www.w3.org/2000/svg" style="border-radius:50%">
        <path d="M150 8 L272 54 L272 182 Q272 284 150 332 Q28 284 28 182 L28 54 Z" fill="#E8B830"/>
        <path d="M150 22 L258 62 L258 182 Q258 272 150 316 Q42 272 42 182 L42 62 Z" fill="#CC2200"/>
        <path d="M150 72 L245 104 L245 210 Q245 260 150 296 Q55 260 55 210 L55 104 Z" fill="#fff"/>
        <path d="M65 110 L235 110 L235 215 Q235 255 150 285 Q65 255 65 215 Z" fill="#1a3575"/>
        <polygon points="150,95 155,110 171,110 158,120 163,135 150,126 137,135 142,120 129,110 145,110" fill="#F5C518"/>
        <text x="150" y="276" text-anchor="middle" font-family="Georgia,serif" font-size="13" font-weight="bold" fill="#1a3575" letter-spacing="1.5">GOD IS ABLE</text>
        <path id="la1" d="M68 62 A96 96 0 0 1 232 62" fill="none"/>
        <text font-family="Georgia,serif" font-size="14" font-weight="bold" fill="#fff"><textPath href="#la1" startOffset="10%">GOLDEN STARS</textPath></text>
        <path id="la2" d="M80 85 A84 84 0 0 1 220 85" fill="none"/>
        <text font-family="Georgia,serif" font-size="11" font-weight="bold" fill="#F5C518"><textPath href="#la2" startOffset="18%">ACADEMY · ABUJA</textPath></text>
        <path d="M150 8 L272 54 L272 182 Q272 284 150 332 Q28 284 28 182 L28 54 Z" fill="none" stroke="#E8B830" stroke-width="3.5"/>
      </svg>
    {% endif %}
  </div>
  <h1>Golden Stars Academy</h1>
  <div class="sub">Admin Portal — Staff Login</div>
  {% for f in flash_msgs %}<div class="err"><i class="ti ti-alert-circle"></i>{{ f.msg }}</div>{% endfor %}
  <form method="post" action="/admin/login">
    <div class="fg"><label>Email Address</label><input type="email" name="email" placeholder="your@goldenstarsacademy.com" required autofocus/></div>
    <div class="fg"><label>Password</label><input type="password" name="password" placeholder="••••••••" required/></div>
    <button type="submit" class="btn-full">Sign In</button>
  </form>
  <div class="foot">🔐 Secured · Golden Stars Academy · GRA Gbessa, Abuja</div>
</div>
</body>
</html>
""")

# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════
write((ADMIN, "dashboard.html"), """
{% extends "admin/base.html" %}
{% block title %}Dashboard{% endblock %}
{% block page_title %}Dashboard{% endblock %}
{% block content %}
{% if access_error %}<div class="flash flash-err"><i class="ti ti-lock"></i> Access denied.</div>{% endif %}
<div class="sg">
  <div class="sc"><div class="sc-icon">👥</div><div class="sc-val">{{ counts.users }}</div><div class="sc-lbl">Admin Users</div></div>
  <div class="sc"><div class="sc-icon">📰</div><div class="sc-val">{{ counts.news }}</div><div class="sc-lbl">News Posts</div></div>
  <div class="sc"><div class="sc-icon">💰</div><div class="sc-val">{{ counts.fees }}</div><div class="sc-lbl">Fee Entries</div></div>
  <div class="sc"><div class="sc-icon">📸</div><div class="sc-val">{{ counts.gallery }}</div><div class="sc-lbl">Gallery Photos</div></div>
  <div class="sc"><div class="sc-icon">📅</div><div class="sc-val">{{ counts.calendar }}</div><div class="sc-lbl">Calendar Events</div></div>
</div>
{% if pending_fees %}
<div class="card">
  <div class="card-hd"><div><div class="card-title">⏳ Pending Fee Approvals</div><div class="card-sub">Require Super Admin approval before publishing</div></div>{% if current_user.role=='superadmin' %}<a href="/admin/fees" class="btn btn-p btn-sm"><i class="ti ti-check"></i> Review</a>{% endif %}</div>
  <div class="tbl-wrap"><table class="tbl"><thead><tr><th>Level</th><th>Term</th><th>Amount (₦)</th><th>By</th></tr></thead>
  <tbody>{% for f in pending_fees %}<tr><td><strong>{{ f.level }}</strong></td><td>{{ f.term }}</td><td><strong>₦{{ '{:,.0f}'.format(f.amount) }}</strong></td><td>{{ f.updated_by }}</td></tr>{% endfor %}</tbody></table></div>
</div>{% endif %}
<div class="card">
  <div class="card-hd"><div><div class="card-title">📰 Recent News</div></div><a href="/admin/news/create" class="btn btn-p btn-sm"><i class="ti ti-plus"></i> New Post</a></div>
  {% if recent_news %}
  <div class="tbl-wrap"><table class="tbl"><thead><tr><th>Title</th><th>Author</th><th>Date</th><th>Status</th></tr></thead>
  <tbody>{% for n in recent_news %}<tr><td><strong>{{ n.title }}</strong></td><td>{{ n.author }}</td><td>{{ n.date }}</td><td><span class="badge {{ 'b-active' if n.published else 'b-inactive' }}">{{ 'Published' if n.published else 'Draft' }}</span></td></tr>{% endfor %}</tbody></table></div>
  {% else %}<p style="color:#aaa;font-size:13px;">No posts yet. <a href="/admin/news/create" style="color:#1a3a6b;font-weight:600;">Create the first one →</a></p>{% endif %}
</div>
{% endblock %}
""")

# ══════════════════════════════════════════════════════════════
# USERS
# ══════════════════════════════════════════════════════════════
write((ADMIN, "users.html"), """
{% extends "admin/base.html" %}
{% block title %}Users{% endblock %}
{% block page_title %}User Management{% endblock %}
{% block content %}
<div class="card">
  <div class="card-hd">
    <div><div class="card-title">All Admin Users</div><div class="card-sub">Only Super Admin can create, activate, or delete users</div></div>
    <a href="/admin/users/create" class="btn btn-p"><i class="ti ti-user-plus"></i> Create User</a>
  </div>
  <div class="tbl-wrap"><table class="tbl">
    <thead><tr><th>User</th><th>Email</th><th>Role</th><th>Status</th><th>Created</th><th>Actions</th></tr></thead>
    <tbody>
    {% set rc={'superadmin':'#7c3aed','ict':'#16a34a','media':'#0891b2','bursar':'#b45309'} %}
    {% set ri={'superadmin':'👑','ict':'🖥️','media':'📸','bursar':'💰'} %}
    {% set bc={'superadmin':'b-sa','ict':'b-ic','media':'b-me','bursar':'b-bu'} %}
    {% for u in users %}
    <tr>
      <td style="display:flex;align-items:center;gap:9px;padding:12px 13px;">
        <div style="width:32px;height:32px;border-radius:50%;background:{{ rc.get(u.role,'#666') }};display:flex;align-items:center;justify-content:center;font-weight:700;font-size:11px;color:#fff;flex-shrink:0;">{{ u.avatar or u.name[0] }}</div>
        <span style="font-weight:600;">{{ u.name }}</span>
      </td>
      <td>{{ u.email }}</td>
      <td><span class="badge {{ bc.get(u.role,'b-ic') }}">{{ ri.get(u.role,'') }} {{ u.role|title }}</span></td>
      <td><span class="badge {{ 'b-active' if u.status=='active' else 'b-inactive' }}">{{ u.status }}</span></td>
      <td style="color:#aaa;font-size:12px;">{{ u.created }}</td>
      <td>
        {% if u.role != 'superadmin' %}
        <div style="display:flex;gap:6px;">
          <form method="post" action="/admin/users/{{ u.id }}/toggle">
            <button class="btn btn-o btn-sm" type="submit">{{ 'Deactivate' if u.status=='active' else 'Activate' }}</button>
          </form>
          <form method="post" action="/admin/users/{{ u.id }}/delete" onsubmit="return confirm('Delete {{ u.name }}?')">
            <button class="btn btn-d btn-sm" type="submit"><i class="ti ti-trash"></i></button>
          </form>
        </div>
        {% else %}<span style="font-size:11px;color:#aaa;">Protected</span>{% endif %}
      </td>
    </tr>
    {% endfor %}
    </tbody>
  </table></div>
</div>
{% endblock %}
""")

# ══════════════════════════════════════════════════════════════
# USER FORM
# ══════════════════════════════════════════════════════════════
write((ADMIN, "user_form.html"), """
{% extends "admin/base.html" %}
{% block title %}Create User{% endblock %}
{% block page_title %}Create New User{% endblock %}
{% block content %}
<div class="card" style="max-width:520px;">
  <div class="card-sub" style="margin-bottom:20px;">New users receive access based on their assigned role.</div>
  <form method="post" action="/admin/users/create">
    <div class="fg"><label>Full Name</label><input type="text" name="name" placeholder="e.g. Ngozi Okafor" required/></div>
    <div class="fg"><label>Email Address</label><input type="email" name="email" placeholder="staff@goldenstarsacademy.com" required/></div>
    <div class="fg"><label>Password</label><input type="password" name="password" placeholder="Minimum 8 characters" required/></div>
    <div class="fg">
      <label>Role</label>
      <select name="role" onchange="showHint(this.value)">
        <option value="media">📸 Media Officer</option>
        <option value="bursar">💰 Bursar</option>
        <option value="ict">🖥️ ICT Officer</option>
      </select>
    </div>
    <div class="info-box" id="hint">📸 Can upload event photos and manage the gallery and team pages.</div>
    <div style="display:flex;gap:10px;">
      <button type="submit" class="btn btn-p"><i class="ti ti-user-check"></i> Create User</button>
      <a href="/admin/users" class="btn btn-o">Cancel</a>
    </div>
  </form>
</div>
<script>
const h={media:'📸 Can upload event photos and manage the gallery and team pages.',bursar:'💰 Can create and update student fee schedules. Fees require Super Admin approval.',ict:'🖥️ Can update site info, news, calendar, gallery, logos, and page images.'};
function showHint(r){document.getElementById('hint').textContent=h[r]||'';}
</script>
{% endblock %}
""")

# ══════════════════════════════════════════════════════════════
# LOGOS
# ══════════════════════════════════════════════════════════════
write((ADMIN, "logos.html"), """
{% extends "admin/base.html" %}
{% block title %}Logo Manager{% endblock %}
{% block page_title %}Logo Manager{% endblock %}
{% block content %}
<div class="info-box"><i class="ti ti-info-circle"></i> The school logo appears in the header, footer, admin sidebar and login page. The web designer logo appears in the footer.</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;flex-wrap:wrap;">
  <div class="card">
    <div class="card-title" style="margin-bottom:4px;">🏫 School Logo</div>
    <div class="card-sub" style="margin-bottom:16px;">Header, footer, admin sidebar &amp; login page</div>
    {% if school and school.url %}<img src="{{ school.url }}" class="prev" style="width:80px;height:80px;border-radius:50%;margin-bottom:14px;"/><p style="font-size:12px;color:#888;margin-bottom:14px;">Updated by {{ school.updated_by }} · {{ school.updated_at }}</p>{% else %}<p style="font-size:13px;color:#aaa;margin-bottom:16px;">No logo uploaded. Using built-in SVG.</p>{% endif %}
    <form method="post" action="/admin/logos" enctype="multipart/form-data">
      <input type="hidden" name="logo_type" value="school"/>
      <div class="fg"><label>Upload (PNG or SVG recommended)</label><input type="file" name="logo_file" accept="image/*"/></div>
      <div class="fg"><label>Or paste URL</label><input type="text" name="logo_url" value="{{ school.url if school else '' }}" placeholder="https://..."/></div>
      <div class="fg"><label>Alt Text</label><input type="text" name="alt_text" value="{{ school.alt_text if school else 'Golden Stars Academy' }}"/></div>
      <button type="submit" class="btn btn-p"><i class="ti ti-upload"></i> Update School Logo</button>
    </form>
  </div>
  <div class="card">
    <div class="card-title" style="margin-bottom:4px;">🎨 Web Designer Logo</div>
    <div class="card-sub" style="margin-bottom:16px;">Appears in website footer "Powered by" section</div>
    {% if designer and designer.url %}<img src="{{ designer.url }}" class="prev" style="width:80px;height:80px;border-radius:8px;margin-bottom:14px;"/><p style="font-size:12px;color:#888;margin-bottom:14px;">Updated by {{ designer.updated_by }} · {{ designer.updated_at }}</p>{% else %}<p style="font-size:13px;color:#aaa;margin-bottom:16px;">No logo uploaded. Showing text only.</p>{% endif %}
    <form method="post" action="/admin/logos" enctype="multipart/form-data">
      <input type="hidden" name="logo_type" value="webdesigner"/>
      <div class="fg"><label>Upload Designer Logo</label><input type="file" name="logo_file" accept="image/*"/></div>
      <div class="fg"><label>Or paste URL</label><input type="text" name="logo_url" value="{{ designer.url if designer else '' }}" placeholder="https://..."/></div>
      <div class="fg"><label>Company Name / Alt Text</label><input type="text" name="alt_text" value="{{ designer.alt_text if designer else 'Eled Global' }}"/></div>
      <button type="submit" class="btn btn-p"><i class="ti ti-upload"></i> Update Designer Logo</button>
    </form>
  </div>
</div>
{% endblock %}
""")

# ══════════════════════════════════════════════════════════════
# NEWS LIST
# ══════════════════════════════════════════════════════════════
write((ADMIN, "news.html"), """
{% extends "admin/base.html" %}
{% block title %}News{% endblock %}
{% block page_title %}News &amp; Announcements{% endblock %}
{% block content %}
<div class="card">
  <div class="card-hd">
    <div><div class="card-title">All News Posts</div><div class="card-sub">Published posts appear live on the website</div></div>
    <a href="/admin/news/create" class="btn btn-p"><i class="ti ti-plus"></i> New Post</a>
  </div>
  {% if items %}
  <div class="tbl-wrap"><table class="tbl">
    <thead><tr><th>Title</th><th>Author</th><th>Date</th><th>Status</th><th>Actions</th></tr></thead>
    <tbody>{% for n in items %}<tr>
      <td><strong>{{ n.title }}</strong>{% if n.image_url %}<span style="font-size:10px;color:#0891b2;margin-left:6px;">📷</span>{% endif %}</td>
      <td>{{ n.author }}</td><td>{{ n.date }}</td>
      <td><span class="badge {{ 'b-active' if n.published else 'b-inactive' }}">{{ 'Published' if n.published else 'Draft' }}</span></td>
      <td><div style="display:flex;gap:6px;">
        <a href="/admin/news/{{ n.id }}/edit" class="btn btn-o btn-sm"><i class="ti ti-edit"></i></a>
        <form method="post" action="/admin/news/{{ n.id }}/delete" onsubmit="return confirm('Delete?')">
          <button class="btn btn-d btn-sm" type="submit"><i class="ti ti-trash"></i></button>
        </form>
      </div></td>
    </tr>{% endfor %}</tbody>
  </table></div>
  {% else %}<p style="color:#aaa;font-size:13px;">No posts yet.</p>{% endif %}
</div>
{% endblock %}
""")

# ══════════════════════════════════════════════════════════════
# NEWS FORM
# ══════════════════════════════════════════════════════════════
write((ADMIN, "news_form.html"), """
{% extends "admin/base.html" %}
{% block title %}{{ 'Edit' if item else 'New' }} Post{% endblock %}
{% block page_title %}{{ 'Edit' if item else 'Create' }} News Post{% endblock %}
{% block content %}
<div class="card" style="max-width:640px;">
  <form method="post" action="{{ '/admin/news/' + item.id|string + '/edit' if item else '/admin/news/create' }}" enctype="multipart/form-data">
    <div class="fg"><label>Headline</label><input type="text" name="title" value="{{ item.title if item else '' }}" placeholder="e.g. Admission Portal Now Open" required/></div>
    <div class="fg"><label>Body / Content</label><textarea name="body" placeholder="Write the announcement..." required>{{ item.body if item else '' }}</textarea></div>
    <div class="fg"><label>Image (optional)</label><input type="file" name="image" accept="image/*"/>{% if item and item.image_url %}<img src="{{ item.image_url }}" class="prev"/>{% endif %}</div>
    <div class="fg" style="display:flex;align-items:center;gap:10px;">
      <input type="checkbox" name="published" id="pub" value="1" style="width:auto;" {{ 'checked' if not item or item.published else '' }}/>
      <label for="pub" style="cursor:pointer;">Publish immediately (visible on website)</label>
    </div>
    <div style="display:flex;gap:10px;">
      <button type="submit" class="btn btn-p"><i class="ti ti-send"></i> {{ 'Update' if item else 'Publish' }}</button>
      <a href="/admin/news" class="btn btn-o">Cancel</a>
    </div>
  </form>
</div>
{% endblock %}
""")

# ══════════════════════════════════════════════════════════════
# FEES LIST
# ══════════════════════════════════════════════════════════════
write((ADMIN, "fees.html"), """
{% extends "admin/base.html" %}
{% block title %}Fees{% endblock %}
{% block page_title %}Fee Management{% endblock %}
{% block content %}
<div class="card">
  <div class="card-hd">
    <div><div class="card-title">Fee Schedule</div><div class="card-sub">Only approved fees are published to the website</div></div>
    <a href="/admin/fees/create" class="btn btn-p"><i class="ti ti-plus"></i> New Entry</a>
  </div>
  <div class="tbl-wrap"><table class="tbl">
    <thead><tr><th>Level</th><th>Term</th><th>Session</th><th>Amount (₦)</th><th>Status</th><th>Updated By</th><th>Actions</th></tr></thead>
    <tbody>{% for f in items %}<tr>
      <td><strong>{{ f.level }}</strong></td><td>{{ f.term }}</td><td>{{ f.session }}</td>
      <td><strong style="color:#1a3a6b;">₦{{ '{:,.0f}'.format(f.amount) }}</strong></td>
      <td><span class="badge {{ 'b-approved' if f.status=='approved' else 'b-pending' }}">{{ f.status }}</span></td>
      <td style="font-size:12px;color:#888;">{{ f.updated_by }}<br/>{{ f.updated_at }}</td>
      <td><div style="display:flex;gap:5px;flex-wrap:wrap;">
        <a href="/admin/fees/{{ f.id }}/edit" class="btn btn-o btn-sm"><i class="ti ti-edit"></i></a>
        {% if f.status=='pending' and current_user.role=='superadmin' %}
        <form method="post" action="/admin/fees/{{ f.id }}/approve"><button class="btn btn-ok btn-sm"><i class="ti ti-check"></i> Approve</button></form>
        {% endif %}
        {% if current_user.role=='superadmin' %}
        <form method="post" action="/admin/fees/{{ f.id }}/delete" onsubmit="return confirm('Delete?')"><button class="btn btn-d btn-sm"><i class="ti ti-trash"></i></button></form>
        {% endif %}
      </div></td>
    </tr>{% endfor %}</tbody>
  </table></div>
</div>
{% endblock %}
""")

# ══════════════════════════════════════════════════════════════
# FEE FORM
# ══════════════════════════════════════════════════════════════
write((ADMIN, "fee_form.html"), """
{% extends "admin/base.html" %}
{% block title %}Fee Entry{% endblock %}
{% block page_title %}{{ 'Edit' if item else 'New' }} Fee Entry{% endblock %}
{% block content %}
<div class="card" style="max-width:520px;">
  <div class="card-sub" style="margin-bottom:18px;">Fee entries require Super Admin approval before appearing on the website.</div>
  <form method="post" action="{{ '/admin/fees/' + item.id|string + '/edit' if item else '/admin/fees/create' }}">
    <div class="fg-row">
      <div class="fg"><label>Level</label><select name="level">{% for l in ['Toddler','Nursery','Primary','JSS','SSS'] %}<option {{ 'selected' if item and item.level==l }}>{{ l }}</option>{% endfor %}</select></div>
      <div class="fg"><label>Term</label><select name="term">{% for t in ['First Term','Second Term','Third Term'] %}<option {{ 'selected' if item and item.term==t }}>{{ t }}</option>{% endfor %}</select></div>
    </div>
    <div class="fg-row">
      <div class="fg"><label>Session</label><input type="text" name="session" value="{{ item.session if item else '2025/2026' }}"/></div>
      <div class="fg"><label>Amount (₦)</label><input type="number" name="amount" value="{{ item.amount if item else '' }}" required/></div>
    </div>
    <div class="fg"><label>Status</label><select name="status">
      <option value="pending" {{ 'selected' if not item or item.status=='pending' }}>Pending</option>
      <option value="approved" {{ 'selected' if item and item.status=='approved' }}>Approved</option>
    </select></div>
    <div style="display:flex;gap:10px;">
      <button type="submit" class="btn btn-p"><i class="ti ti-device-floppy"></i> Save</button>
      <a href="/admin/fees" class="btn btn-o">Cancel</a>
    </div>
  </form>
</div>
{% endblock %}
""")

# ══════════════════════════════════════════════════════════════
# GALLERY
# ══════════════════════════════════════════════════════════════
write((ADMIN, "gallery.html"), """
{% extends "admin/base.html" %}
{% block title %}Gallery{% endblock %}
{% block page_title %}Gallery &amp; Team Manager{% endblock %}
{% block content %}
<div class="info-box">Use categories <strong>Board Members</strong>, <strong>Management-Primary</strong>, <strong>Management-Secondary</strong> for team pages. Gallery categories: Academics, Sports, Cultural Events, Facilities, Excursions, Celebrations.</div>
<div class="card">
  <div class="card-hd">
    <div><div class="card-title">All Photos &amp; Team Members</div><div class="card-sub">{{ items|length }} items — synced live to the website</div></div>
    <a href="/admin/gallery/upload" class="btn btn-p"><i class="ti ti-upload"></i> Upload Photo</a>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:14px;">
    {% for g in items %}
    <div style="background:#fff;border:1px solid #eee;border-radius:11px;overflow:hidden;">
      <div style="height:110px;background:#1a3a6b;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;">
        {% if g.url %}<img src="{{ g.url }}" alt="{{ g.title }}" style="width:100%;height:100%;object-fit:cover;"/>{% else %}<span style="font-size:32px;opacity:.25;">🖼️</span>{% endif %}
        <span style="position:absolute;top:6px;right:6px;background:rgba(0,0,0,.55);color:#fff;font-size:10px;padding:2px 7px;border-radius:8px;">{{ g.category }}</span>
      </div>
      <div style="padding:10px 12px;">
        <p style="font-size:12px;font-weight:600;margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{ g.title }}</p>
        {% if g.role %}<p style="font-size:11px;color:#0891b2;">{{ g.role }}</p>{% endif %}
        <p style="font-size:11px;color:#aaa;margin-bottom:8px;">{{ g.date }}</p>
        <form method="post" action="/admin/gallery/{{ g.id }}/delete" onsubmit="return confirm('Remove?')">
          <button class="btn btn-d btn-sm" style="width:100%;">Remove</button>
        </form>
      </div>
    </div>
    {% else %}<p style="color:#aaa;font-size:13px;grid-column:1/-1;">No photos yet.</p>{% endfor %}
  </div>
</div>
{% endblock %}
""")

# ══════════════════════════════════════════════════════════════
# GALLERY FORM
# ══════════════════════════════════════════════════════════════
write((ADMIN, "gallery_form.html"), """
{% extends "admin/base.html" %}
{% block title %}Upload Photo{% endblock %}
{% block page_title %}Upload Photo{% endblock %}
{% block content %}
<div class="card" style="max-width:560px;">
  <form method="post" action="/admin/gallery/upload" enctype="multipart/form-data">
    <div class="fg"><label>Title / Caption</label><input type="text" name="title" placeholder="e.g. Award Ceremony JSS Three" required/></div>
    <div class="fg"><label>Category / Page Target</label>
      <select name="category" onchange="toggleTeam(this.value)">
        <optgroup label="Gallery">
          <option>Academics</option><option>Sports</option><option>Cultural Events</option>
          <option>Facilities</option><option>Excursions</option><option>Celebrations</option><option>Meet the Team</option>
        </optgroup>
        <optgroup label="Team Pages">
          <option>Board Members</option><option>Management-Primary</option><option>Management-Secondary</option>
        </optgroup>
      </select>
    </div>
    <div class="fg"><label>Upload from Device</label><input type="file" name="image" accept="image/*" onchange="previewImg(this)"/>
    <img id="prev" style="display:none;width:90px;height:90px;border-radius:8px;object-fit:cover;border:1px solid #eee;margin-top:7px;"/></div>
    <div class="fg"><label>Or Paste Image URL</label><input type="text" name="image_url" placeholder="https://..."/></div>
    <div id="teamFields" style="display:none;">
      <div class="fg"><label>Role / Position</label><input type="text" name="role" placeholder="e.g. Headmistress — Primary Section"/></div>
      <div class="fg"><label>Short Bio (optional)</label><textarea name="bio" placeholder="Brief description..."></textarea></div>
    </div>
    <div style="display:flex;gap:10px;">
      <button type="submit" class="btn btn-p"><i class="ti ti-upload"></i> Upload</button>
      <a href="/admin/gallery" class="btn btn-o">Cancel</a>
    </div>
  </form>
</div>
<script>
function previewImg(i){const r=new FileReader();r.onload=e=>{const p=document.getElementById('prev');p.src=e.target.result;p.style.display='block';};if(i.files[0])r.readAsDataURL(i.files[0]);}
function toggleTeam(v){const t=['Board Members','Management-Primary','Management-Secondary','Meet the Team'];document.getElementById('teamFields').style.display=t.includes(v)?'block':'none';}
</script>
{% endblock %}
""")

# ══════════════════════════════════════════════════════════════
# CALENDAR
# ══════════════════════════════════════════════════════════════
write((ADMIN, "calendar.html"), """
{% extends "admin/base.html" %}
{% block title %}Calendar{% endblock %}
{% block page_title %}Academic Calendar{% endblock %}
{% block content %}
<div class="card">
  <div class="card-hd">
    <div><div class="card-title">Calendar Events</div><div class="card-sub">Displayed on the Academic Calendar page of the website</div></div>
    <a href="/admin/calendar/create" class="btn btn-p"><i class="ti ti-plus"></i> Add Entry</a>
  </div>
  {% set tc={'Resumption':'#16a34a','Holiday':'#9333ea','Exam':'#dc2626','Event':'#0891b2','Closure':'#b45309'} %}
  {% if items %}
  <div class="tbl-wrap"><table class="tbl">
    <thead><tr><th>Type</th><th>Title</th><th>Date</th><th>Note</th><th>Action</th></tr></thead>
    <tbody>{% for c in items %}<tr>
      <td><span style="background:{{ tc.get(c.type,'#666') }}22;color:{{ tc.get(c.type,'#666') }};padding:3px 10px;border-radius:10px;font-size:11px;font-weight:700;">{{ c.type }}</span></td>
      <td><strong>{{ c.title }}</strong></td><td>{{ c.date }}</td>
      <td style="font-size:12px;color:#888;">{{ c.note or '—' }}</td>
      <td><form method="post" action="/admin/calendar/{{ c.id }}/delete" onsubmit="return confirm('Remove?')"><button class="btn btn-d btn-sm"><i class="ti ti-trash"></i></button></form></td>
    </tr>{% endfor %}</tbody>
  </table></div>
  {% else %}<p style="color:#aaa;font-size:13px;">No entries yet.</p>{% endif %}
</div>
{% endblock %}
""")

# ══════════════════════════════════════════════════════════════
# CALENDAR FORM
# ══════════════════════════════════════════════════════════════
write((ADMIN, "calendar_form.html"), """
{% extends "admin/base.html" %}
{% block title %}Add Event{% endblock %}
{% block page_title %}Add Calendar Entry{% endblock %}
{% block content %}
<div class="card" style="max-width:480px;">
  <form method="post" action="/admin/calendar/create">
    <div class="fg"><label>Event Type</label><select name="type">{% for t in ['Resumption','Holiday','Exam','Event','Closure'] %}<option>{{ t }}</option>{% endfor %}</select></div>
    <div class="fg"><label>Title</label><input type="text" name="title" placeholder="e.g. Third Term Resumption" required/></div>
    <div class="fg"><label>Date</label><input type="date" name="date" required/></div>
    <div class="fg"><label>Note (optional)</label><input type="text" name="note" placeholder="e.g. All students report by 7:30am"/></div>
    <div style="display:flex;gap:10px;">
      <button type="submit" class="btn btn-p"><i class="ti ti-calendar-plus"></i> Add Entry</button>
      <a href="/admin/calendar" class="btn btn-o">Cancel</a>
    </div>
  </form>
</div>
{% endblock %}
""")

# ══════════════════════════════════════════════════════════════
# SITE INFO
# ══════════════════════════════════════════════════════════════
write((ADMIN, "siteinfo.html"), """
{% extends "admin/base.html" %}
{% block title %}Site Information{% endblock %}
{% block page_title %}Site Information{% endblock %}
{% block content %}
<div class="info-box"><i class="ti ti-refresh"></i> Changes save instantly and reflect live on the public website.</div>
<form method="post" action="/admin/siteinfo">
  <div class="card">
    <div class="card-title" style="margin-bottom:16px;">📞 Contact Details</div>
    <div class="fg-row">
      <div class="fg"><label>Phone 1</label><input type="text" name="phone1" value="{{ data.phone1 }}"/></div>
      <div class="fg"><label>Phone 2</label><input type="text" name="phone2" value="{{ data.phone2 }}"/></div>
    </div>
    <div class="fg-row">
      <div class="fg"><label>Email</label><input type="email" name="email" value="{{ data.email }}"/></div>
      <div class="fg"><label>Tagline / Motto</label><input type="text" name="tagline" value="{{ data.tagline }}"/></div>
    </div>
    <div class="fg"><label>Full Address</label><textarea name="address" style="height:60px;">{{ data.address }}</textarea></div>
  </div>
  <div class="card">
    <div class="card-title" style="margin-bottom:16px;">📊 Live Statistics</div>
    <div class="fg-row">
      <div class="fg"><label>Nursery &amp; Primary Students</label><input type="text" name="nursery_count" value="{{ data.nursery_count }}" placeholder="e.g. 180"/></div>
      <div class="fg"><label>JSS Students</label><input type="text" name="jss_count" value="{{ data.jss_count }}" placeholder="e.g. 150"/></div>
    </div>
    <div class="fg-row">
      <div class="fg"><label>SSS Students</label><input type="text" name="sss_count" value="{{ data.sss_count }}" placeholder="e.g. 120"/></div>
      <div class="fg"><label>Teacher Count</label><input type="text" name="teacher_count" value="{{ data.teacher_count }}" placeholder="e.g. 42"/></div>
    </div>
  </div>
  <div class="card">
    <div class="card-title" style="margin-bottom:16px;">📱 Social Media</div>
    <div class="fg-row">
      <div class="fg"><label>Facebook URL</label><input type="text" name="facebook" value="{{ data.facebook }}"/></div>
      <div class="fg"><label>Instagram URL</label><input type="text" name="instagram" value="{{ data.instagram }}"/></div>
    </div>
    <div class="fg-row">
      <div class="fg"><label>WhatsApp Number</label><input type="text" name="whatsapp" value="{{ data.whatsapp }}"/></div>
      <div class="fg"><label>YouTube URL</label><input type="text" name="youtube" value="{{ data.youtube }}"/></div>
    </div>
  </div>
  <button type="submit" class="btn btn-p" style="padding:12px 28px;"><i class="ti ti-device-floppy"></i> Save All Changes</button>
</form>
{% endblock %}
""")

# ══════════════════════════════════════════════════════════════
# PUBLIC INDEX placeholder
# ══════════════════════════════════════════════════════════════
index_path = os.path.join(BASE, "index.html")
if not os.path.exists(index_path):
    write(index_path, """
<!DOCTYPE html>
<html><head><meta charset="UTF-8"/><title>Golden Stars Academy</title></head>
<body style="font-family:sans-serif;text-align:center;padding:60px;background:#1a3a6b;color:#fff;">
  <h1 style="color:#ffd700;">Golden Stars Academy</h1>
  <p style="margin:16px 0;">Public website coming soon.</p>
  <a href="/admin/login" style="background:#c0321a;color:#fff;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:700;">Go to Admin Panel</a>
</body></html>
""")

print("\n✅ All template files created successfully!")
print("📁 Run: python -m uvicorn main:app --reload")