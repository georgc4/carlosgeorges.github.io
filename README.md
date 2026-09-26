# Carlos Georges — personal site

A static personal site and technical notebook. The checked-in HTML is ready for GitHub Pages; serving the site requires no build step or package installation.

## Preview

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open http://127.0.0.1:8765/.

## Edit the site

- `index.html`: homepage, career, projects, and background.
- `css/style.css`: shared styles and responsive homepage layout.
- `css/articles.css`: article typography, section navigation, and reading layout.
- `js/main.js`: mobile navigation and note filters. Content remains readable without JavaScript.
- `content/notes.json`: note titles, dates, summaries, status, and source links.
- `content/notes/*.html`: article body fragments.

After editing notes, run:

```sh
python3 scripts/build_notes.py
```

This generates `notes/*.html`, the marked notes list in `index.html`, and `feed.xml`. Commit those generated files along with the source changes. Existing note URLs remain stable.

## Content conventions

Use concrete outcomes and link the relevant commit, experiment, or paper. Keep simulated results distinct from hardware results, synthesis estimates distinct from physical measurements, and development features distinct from released products. Preserve collaborator credit and the scope of upstream contributions. Private project code, credentials, employer internals, and raw operational logs do not belong in this repository.

The current profile and employment descriptions were updated from the September 2026 resumes. Project notes were reconciled with the more recent commit history. The opening silicon quote comes from Carlos's 2024 site.
