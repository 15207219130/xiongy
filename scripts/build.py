"""Build a portable academic site with no third-party dependencies."""
from pathlib import Path
import html
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
profile = json.loads((ROOT / "data/profile.json").read_text())


def e(value):
    return html.escape(str(value), quote=True)


def section(section_id, title, body, number=None):
    marker = f'<span class="section-number" aria-hidden="true">{number}</span>' if number else ''
    return f'<section class="content-section" id="{section_id}" aria-labelledby="{section_id}-title"><h2 id="{section_id}-title">{marker}{title}</h2>{body}</section>'


def entries(items):
    return '<ol class="entry-list">' + ''.join(f'<li>{item}</li>' for item in items) + '</ol>'


def paper(p):
    return (f'<div class="entry-title"><a href="{e(p["url"])}">{e(p["title"])}</a></div>'
            f'<p class="entry-meta"><em>{e(p["journal"])}</em> · {e(p["year"])} · {e(p["detail"])}</p>'
            f'<a class="paper-link" href="{e(p["url"])}" aria-label="Read paper: {e(p["title"])}">Read paper <span aria-hidden="true">↗</span></a>')


research = ('<div class="research-lines"><div><h3>Methods</h3><p>Optimization under uncertainty<br>Machine learning</p></div>'
            '<div><h3>Applications</h3><p>Sustainable logistics<br>Renewable energy<br>Telecommunication networks</p></div></div>')
publications = entries([paper(p) for p in profile['publications']])
working = entries([
    f'<div class="entry-title">{e(p["title"])}</div><p class="entry-meta"><span class="status">{e(p["status"])}</span>'
    + (f' · <em>{e(p["journal"])}</em>' if p['journal'] else '') + '</p>'
    for p in profile['working_papers']
])
education = ''.join(
    f'<article class="record"><div class="record-heading"><h3>{e(p["institution"])}</h3><span class="date">{e(p["dates"])}</span></div>'
    f'<p>{e(p["degree"])}</p><p class="entry-meta">{e(p["location"])} · {e(p["note"])}</p></article>'
    for p in profile['education']
)
teaching = '<p class="section-intro">Teaching Assistant · McMaster University · September 2025–Present</p>'
teaching += '<ul class="compact-list">' + ''.join(
    f'<li><div>{e(p["course"])}' + (f'<span class="course-level">{e(p["level"])}</span>' if p['level'] else '')
    + f'</div><span class="date">{e(p["term"])}</span></li>' for p in profile['teaching']
) + '</ul>'
talks = entries([
    f'<div class="entry-title">{e(p["title"])}</div><p class="entry-meta">{e(p["event"])}<br>{e(p["location"])} · {e(p["date"])}</p>'
    for p in profile['talks']
])
experience = ''.join(
    f'<article class="record"><div class="record-heading"><h3>{e(p["organization"])}</h3><span class="date">{e(p["dates"])}</span></div>'
    f'<p>{e(p["role"])}</p><p class="entry-meta">{e(p["location"])}</p><ul class="experience-list">'
    + ''.join(f'<li>{e(item)}</li>' for item in p['items']) + '</ul></article>'
    for p in profile['experience']
)
awards = '<ul class="compact-list awards">' + ''.join(
    f'<li><span>{e(p["name"])}</span><span class="date">{e(p["date"])}</span></li>' for p in profile['awards']
) + '</ul>'
collaborators = '<ul class="collaborators">' + ''.join(f'<li>{e(p)}</li>' for p in profile['collaborators']) + '</ul>'
about = (f'<p class="eyebrow">RESEARCH & ACADEMIC PROFILE</p><h2 class="intro-heading" id="about-title">Decisions under uncertainty.</h2>'
         f'<p class="intro-lead">I am a PhD student in <strong>{e(profile["program"])}</strong> at {e(profile["university"])}, supervised by {e(profile["advisor"])}.</p>'
         '<p>My research interests lie in optimization under uncertainty and machine learning, with applications in sustainable logistics, renewable energy, and telecommunication networks.</p>'
         '<p>Before joining McMaster, I received my master’s degree in Management Science and Engineering and bachelor’s degree in Safety Engineering from Zhongnan University of Economics and Law.</p>')

sections = [('research', 'Research interests', research), ('publications', 'Publications', publications),
            ('working-papers', 'Working papers', working), ('education', 'Education', education),
            ('teaching', 'Teaching', teaching), ('talks', 'Talks & presentations', talks),
            ('experience', 'Industry experience', experience), ('awards', 'Honors & awards', awards)]
home = f'<section class="intro" id="about" aria-labelledby="about-title">{about}</section>'
home += ''.join(section(key, title, body, f'{i:02d}') for i, (key, title, body) in enumerate(sections, 1))
cv = (f'<section class="cv-header"><p class="eyebrow">CURRICULUM VITAE</p><h2>{e(profile["name"])}</h2>'
      f'<p>{e(profile["program"])} · {e(profile["university"])}<br>{e(profile["location"])} · '
      f'<a href="mailto:{e(profile["email"])}">{e(profile["email"])}</a></p>'
      '<div class="cv-toolbar"><a href="index.html">← Back to homepage</a><button type="button" id="print-cv">Print / save as PDF</button></div></section>')
cv += ''.join(section(key, title, body) for key, title, body in [sections[3], sections[0], *sections[1:3], *sections[4:]])
cv += section('collaborators', 'Collaborators', collaborators)
cv += '<script src="assets/print.js" defer></script>'

template = (ROOT / 'templates/page.html').read_text()
OUT.mkdir(exist_ok=True)
shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)
for filename, content, css_class in [('index.html', home, 'home-page'), ('cv.html', cv, 'cv-page')]:
    nav_prefix = 'index.html' if filename == 'cv.html' else ''
    nav_items = [('about', 'About'), ('research', 'Research'), ('publications', 'Publications'),
                 ('working-papers', 'Working papers'), ('education', 'Education'), ('teaching', 'Teaching'),
                 ('talks', 'Talks'), ('experience', 'Experience'), ('awards', 'Awards')]
    navigation = ''.join(f'<a href="{nav_prefix}#{key}">{label}</a>' for key, label in nav_items)
    replacements = {**{k: e(v) for k, v in profile.items() if isinstance(v, str)}, 'content': content,
                    'navigation': navigation, 'body_class': css_class,
                    'title': e(f'{profile["name"]} | ' + ('Curriculum Vitae' if filename == 'cv.html' else profile['university']))}
    output = template
    for key, value in replacements.items():
        output = output.replace('{{' + key + '}}', value)
    (OUT / filename).write_text(output)
(OUT / '.nojekyll').touch()
shutil.copy(ROOT / 'vendor/minimal-light/LICENSE', OUT / 'MINIMAL-LIGHT-LICENSE.txt')
print(f'Built {OUT}/index.html and cv.html from data/profile.json')
