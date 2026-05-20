html = open('templates/index.html', encoding='utf-8').read()
lines = html.split('\n')
for i, line in enumerate(lines, 1):
    low = line.lower()
    if any(x in low for x in ['showpage', 'pg-home', 'page active', 'bootstrap', 'herocarousel', 'carousel-wrap', 'class="page']):
        print(f'{i}: {line[:120]}')