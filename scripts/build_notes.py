#!/usr/bin/env python3
"""Build the static notes, homepage index, and RSS feed using the standard library."""
from datetime import datetime, timezone
from email.utils import format_datetime
from html import escape, unescape
from pathlib import Path
import json
import math
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://carlosgeorges.com'
notes = json.loads((ROOT / 'content/notes.json').read_text())
index_path = ROOT / 'index.html'
home = index_path.read_text()
header = home[home.index('  <header class="site-header"'):home.index('  <main id="main">')]
header = header.replace('href="#', 'href="/#')
footer = home[home.index('  <footer class="site-footer"'):home.index('\n</body>')]
rows = []

for number, note in enumerate(notes, start=1):
    body = (ROOT / 'content/notes' / f'{note["slug"]}.html').read_text().strip()
    body = body.replace('<table>', '<div class="table-wrap"><table>').replace('</table>', '</table></div>')
    sections = []

    def index_section(match):
        heading = match.group(1)
        text = unescape(re.sub(r'<[^>]+>', '', heading))
        anchor = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
        if not anchor or any(item[0] == anchor for item in sections):
            anchor = f'section-{len(sections) + 1}'
        sections.append((anchor, text))
        return f'<h2 id="{anchor}">{heading}</h2>'

    body = re.sub(r'<h2>(.*?)</h2>', index_section, body, flags=re.S)
    section_links = '\n'.join(
        f'              <li><a href="#{anchor}">{escape(text)}</a></li>'
        for anchor, text in sections
    )
    contents = f'''          <nav class="article-contents" aria-label="In this note">
            <span class="label">IN THIS NOTE</span>
            <ol>
{section_links}
            </ol>
          </nav>''' if sections else ''
    word_count = len(re.sub(r'<[^>]+>', ' ', body).split())
    minutes = max(1, math.ceil(word_count / 220))
    published = datetime.fromisoformat(note['date'])
    display_date = f"{published:%B} {published.day}, {published.year}"
    title = escape(note['title'])
    deck = escape(note['deck'])
    canonical = f'{ORIGIN}/notes/{note["slug"]}.html'
    next_note = notes[number % len(notes)]
    related = ''
    if note['source_url']:
        related = f'<div class="article-source"><span class="label">SOURCE</span><strong><a href="{escape(note["source_url"], quote=True)}" target="_blank" rel="noopener noreferrer">{escape(note["source_label"])} <span aria-hidden="true">↗</span></a></strong></div>'
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#000000">
  <title>{title} — Carlos Georges</title>
  <meta name="description" content="{escape(note['deck'], quote=True)}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{escape(note['title'], quote=True)}">
  <meta property="og:description" content="{escape(note['deck'], quote=True)}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" type="application/rss+xml" title="Carlos Georges — notes" href="/feed.xml">
  <link rel="icon" href="/favicon.ico">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;450;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
  <link rel="stylesheet" href="/css/articles.css">
  <script defer src="/js/main.js"></script>
</head>
<body class="article-page" id="top">
  <div class="reading-progress" aria-hidden="true"></div>
  <a class="skip-link" href="#main">Skip to content</a>
{header}
  <main id="main">
    <div class="wrap article-top"><a class="back-link" href="/#notes"><span aria-hidden="true">←</span> All notes</a><span class="article-folio">NOTE {number:02d} / {len(notes):02d}</span></div>
    <article>
      <header class="wrap article-header">
        <p class="label article-category">{escape(note['category'])}</p>
        <h1>{title}</h1>
        <p class="article-deck">{deck}</p>
        <div class="article-meta"><span class="article-author">Carlos Georges</span><time datetime="{note['date']}">{display_date}</time><span>{minutes} min read</span></div>
      </header>
      <div class="wrap article-shell">
        <div class="article-body">
{body}
          <nav class="article-pagination" aria-label="Article navigation"><a class="article-back" href="/#notes"><span aria-hidden="true">←</span> All notes</a><a class="article-next" href="/notes/{next_note['slug']}.html"><span class="label">READ NEXT</span><strong>{escape(next_note['title'])}</strong><span class="article-next-arrow" aria-hidden="true">↗</span></a></nav>
        </div>
        <aside class="article-sidebar" aria-label="Project context">
{contents}
          <div><span class="label">CURRENT STATE</span><strong>{escape(note['status'])}</strong></div>
          <div><span class="label">WORKING WITH</span><strong>{escape(note['tools'])}</strong></div>
          {related}
        </aside>
      </div>
    </article>
  </main>
{footer}
</body>
</html>
'''
    html = '\n'.join(line.rstrip() for line in html.splitlines()) + '\n'
    (ROOT / 'notes' / f'{note["slug"]}.html').write_text(html)
    rows.append(f'''        <a class="note-row" href="/notes/{note['slug']}.html" data-topic="{note['topic']}">
          <span class="note-number">{number:02d}</span>
          <span class="note-main"><span class="label">{escape(note['category'])}</span><h3>{title}</h3><p>{escape(note['excerpt'])}</p></span>
          <span class="note-arrow" aria-hidden="true">↗</span>
        </a>''')

notes_block = '      <!-- NOTES:START -->\n      <div class="notes-list">\n' + '\n'.join(rows) + '\n      </div>\n      <!-- NOTES:END -->'
home, replacements = re.subn(r'      <!-- NOTES:START -->.*?      <!-- NOTES:END -->', notes_block, home, flags=re.S)
if replacements != 1:
    raise SystemExit('Expected exactly one notes index marker pair in index.html')
home = re.sub(r'(id="note-count"[^>]*>)\d+ notes', rf'\g<1>{len(notes)} notes', home)
index_path.write_text(home)

rss = ET.Element('rss', version='2.0')
channel = ET.SubElement(rss, 'channel')
for key, value in [('title', 'Carlos Georges — notes'), ('link', ORIGIN + '/#notes'), ('description', 'Hardware, Linux, and the details worth writing down.'), ('language', 'en-us')]:
    ET.SubElement(channel, key).text = value
for note in notes:
    item = ET.SubElement(channel, 'item')
    link = ORIGIN + '/notes/' + note['slug'] + '.html'
    for key, value in [('title', note['title']), ('link', link), ('guid', link), ('description', note['deck'])]:
        ET.SubElement(item, key).text = value
    date = datetime.fromisoformat(note['date']).replace(tzinfo=timezone.utc)
    ET.SubElement(item, 'pubDate').text = format_datetime(date)
ET.indent(rss, space='  ')
ET.ElementTree(rss).write(ROOT / 'feed.xml', encoding='utf-8', xml_declaration=True)
print(f'Built {len(notes)} notes, homepage index, and RSS feed.')
