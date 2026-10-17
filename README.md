# Yi Xiong — Academic Pages

Live website: **https://15207219130.github.io/xiongy/**

This site uses the original [Academic Pages](https://github.com/academicpages/academicpages.github.io) Jekyll template through `jekyll-remote-theme`, pinned to revision `9c8f68fd2582abba41365ea1ca459bbb222d5a92`. It retains the template's standard layout, sidebar, navigation, typography, and responsive styling. There is no custom HTML generator or custom stylesheet.

## Edit the content

| Content | File |
| --- | --- |
| Name, affiliation, email, links | `_config.yml` |
| Biography and research interests | `_pages/about.md` |
| Publications | `_pages/publications.md` |
| Working papers | `_pages/working-papers.md` |
| Talks | `_pages/talks.md` |
| Teaching | `_pages/teaching.md` |
| Full CV | `_pages/cv.md` |
| Navigation | `_data/navigation.yml` |

`_data/profile.json` preserves the supplied CV as a structured reference; edit the Markdown pages to update displayed content. `images/profile.png` is the template's neutral placeholder; replace it with your portrait when ready. Two stock includes have small URL fixes so the favicon and sitemap work under `/xiongy/`.

## Preview locally

Install Ruby 3.3 and Bundler, then run:

```sh
bundle install
bundle exec jekyll serve
```

Open `http://localhost:4000/xiongy/`.

## Deployment

GitHub Actions builds Jekyll, checks rendered page links, and deploys `main` to GitHub Pages. Repository Settings → Pages must use **GitHub Actions** as its source.

The additional `_config_sites.yml` builds the existing private Sites preview at its domain root:

```sh
bundle exec jekyll build --config _config.yml,_config_sites.yml
python3 scripts/check_site.py dist https://yi-xiong-academic.stonypeach257.chatgpt.site ''
```

Theme attribution and the upstream MIT license are retained.
