html = open('templates/index.html', encoding='utf-8').read()
lines = html.split('\n')

# Find the showPage function and surrounding JS
for i, line in enumerate(lines, 1):
    if i >= 988 and i <= 1010:
        print(f'{i}: {line[:150]}')

print("\n--- Checking for broken script tags ---")
import re
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
print(f"Total script blocks found: {len(scripts)}")
for idx, s in enumerate(scripts):
    lines_in = s.strip().split('\n')
    print(f"Script {idx+1}: {len(lines_in)} lines, starts with: {lines_in[0][:80] if lines_in else 'empty'}")

print("\n--- Checking page CSS ---")
for i, line in enumerate(html.split('\n'), 1):
    if '.page{' in line or '.page {' in line:
        print(f'{i}: {line[:150]}')