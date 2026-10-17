"""Check rendered academic pages and same-site links after a Jekyll build."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse
import sys


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        self.urls.extend(value for key, value in attrs if key in ('href', 'src') and value)


root, origin, prefix = Path(sys.argv[1]), sys.argv[2].rstrip('/'), sys.argv[3].rstrip('/')
errors = []
for page in ('index.html', 'publications/index.html', 'working-papers/index.html',
             'teaching/index.html', 'talks/index.html', 'cv/index.html', 'sitemap/index.html'):
    if not (root / page).is_file():
        errors.append(f'Missing page: {page}')
html_files = list(root.rglob('*.html'))
for path in html_files:
    source = path.read_text()
    for sample in ('Your Name / Site Title', 'Your Sidebar Name', 'none@example.org',
                   'GitHub University', 'Decisions under uncertainty.', 'yourorcidurl'):
        if sample in source:
            errors.append(f'{path}: leftover sample {sample!r}')
    parser = Links()
    parser.feed(source)
    relative = path.relative_to(root).as_posix()
    page_url = origin + prefix + '/' + relative
    for href in parser.urls:
        target = urlparse(urljoin(page_url, href))
        if target.scheme not in ('http', 'https') or target.netloc != urlparse(origin).netloc:
            continue
        pathname = unquote(target.path)
        if prefix and not (pathname == prefix or pathname.startswith(prefix + '/')):
            errors.append(f'{relative}: URL escapes site prefix: {href}')
            continue
        local = root / pathname[len(prefix):].lstrip('/')
        if local.is_dir():
            local /= 'index.html'
        if not local.is_file():
            errors.append(f'{relative}: missing link target: {href}')
if errors:
    raise SystemExit('\n'.join(sorted(set(errors))))
print(f'Checked {len(html_files)} rendered pages; all required pages and local links pass.')
