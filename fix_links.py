with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('href="#"><i class="ti ti-user-circle"></i> Parent Login', 'href="/parent/login"><i class="ti ti-user-circle"></i> Parent Login')
html = html.replace('href="#"><i class="ti ti-users"></i> Staff', 'href="/staff/login"><i class="ti ti-users"></i> Staff')
html = html.replace('href="#"><i class="ti ti-school"></i> Student', 'href="/student/login"><i class="ti ti-school"></i> Student')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Links updated successfully!')