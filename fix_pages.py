from pathlib import Path

html = Path("templates/index.html").read_text(encoding="utf-8")

# The illustrated carousel uses inline style backgrounds but the
# carousel-wrap closing div may have been broken. Let's verify and fix
# by ensuring carousel-wrap has proper structure.

# Check if carousel-wrap is properly closed before stats-bar
if '<div class="stats-bar">' in html:
    # Find carousel-wrap and ensure it closes before stats-bar
    cw_start = html.find('<div class="carousel-wrap"')
    stats_start = html.find('<div class="stats-bar">')
    
    if cw_start > 0 and stats_start > 0:
        carousel_section = html[cw_start:stats_start]
        # Count opening and closing divs
        opens = carousel_section.count('<div')
        closes = carousel_section.count('</div>')
        print(f"Carousel section: {opens} opening divs, {closes} closing divs")
        
        if opens != closes:
            diff = opens - closes
            print(f"Missing {diff} closing div(s) - fixing...")
            # Insert missing closing divs before stats-bar
            missing = '</div>\n' * diff
            html = html.replace('<div class="stats-bar">', missing + '<div class="stats-bar">', 1)
            Path("templates/index.html").write_text(html, encoding="utf-8")
            print("Fixed!")
        else:
            print("Div count is balanced - carousel structure OK")
    else:
        print("Could not find carousel-wrap or stats-bar")
else:
    print("Could not find stats-bar")

# Also fix admin sidebar
base_path = Path("templates/admin/base.html")
base = base_path.read_text(encoding="utf-8")

if "'/admin/staff'" in base and "'superadmin'" in base:
    # Check if already fixed
    if "['superadmin','ict']" in base and "Portals" in base:
        print("Sidebar already has ICT access")
    else:
        # Find the staff/parents links and ensure ICT can see them
        import re
        # Replace any pattern that restricts staff/parents to superadmin only
        old = "{% if current_user.role == 'superadmin' %}\n    <div class=\"sb-sec\">Portals</div>"
        new = "{% if current_user.role in ['superadmin','ict'] %}\n    <div class=\"sb-sec\">Portals</div>"
        if old in base:
            base = base.replace(old, new)
            base_path.write_text(base, encoding="utf-8")
            print("Sidebar fixed for ICT role")
        else:
            print("Searching for sidebar pattern...")
            # Try to find where staff link is
            idx = base.find("/admin/staff")
            if idx > 0:
                snippet = base[max(0,idx-200):idx+100]
                print(f"Context around /admin/staff:\n{snippet}")