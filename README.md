# Yi Xiong — Academic Website

A customized version of [Minimal Light](https://github.com/yaoyao-liu/minimal-light), using its static HTML edition and stylesheet. Content comes from Yi Xiong's supplied CV. The homepage and printable CV share a single content source.

Website: https://15207219130.github.io/xiongy/

GitHub repository: https://github.com/15207219130/xiongy

## Build and preview

Requires Python 3.9 or later; no packages to install.

```sh
python3 scripts/build.py
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. The CV page has a **Print / save as PDF** button. Choose Save as PDF in the browser print dialog. A compiled LaTeX CV is not included because the supplied source depends on a missing `resume.cls`.

## Edit content

- `data/profile.json`: profile, publications, working papers, education, teaching, talks, experience, awards, collaborators.
- `scripts/build.py`: biography and research-interest prose; HTML rendering.
- `templates/page.html`: shared page layout and metadata.
- `assets/css/site.css`: custom typography, layout, colors, mobile and print styles.
- `assets/css/minimal-light.css`: retained upstream template stylesheet, with its Google Fonts imports removed to avoid external font dependencies.

Run the build after editing. Generated files are in `dist/`; do not edit them directly. The website uses university email and omits telephone numbers. A typographic YX mark is used until a portrait is supplied. No unverified social-profile links or paper author lists are shown.

## Publish with GitHub Pages

1. Use the `15207219130/xiongy` GitHub repository.
2. Push this project to its `main` branch.
3. In **Settings → Pages → Build and deployment**, select **GitHub Actions**.
4. Run **Deploy academic website to GitHub Pages**, or push a change to `main`.

The workflow builds and deploys `dist/`. Relative asset links also work when hosted under a repository subpath. Only the built output is published; source and design notes are not included in the website. `.openai/hosting.json` identifies the separate owner-private Sites preview and is not needed by GitHub Pages.

## Template provenance

- Upstream: https://github.com/yaoyao-liu/minimal-light
- Revision: `1ea07f39518ac44644406380c83da6f89037c4fc`
- License: CC0 1.0, retained in `vendor/minimal-light/LICENSE`.
- Original HTML reference: `vendor/minimal-light/original-index.html` (not published).
- Adaptations: personal content; semantic main/section structure; purple accents; responsive navigation; typographic profile mark; printable CV; dependency-free build. Upstream demo content, analytics, CNAME, sample CV, and third-party icon dependencies are not used.

## Publication links

Verified publisher destinations are recorded in `data/profile.json`. Bibliographic details and working-paper statuses follow the supplied CV. Update these when papers change status. Author lists were absent from the CV and have not been inferred.
