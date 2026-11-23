"""Responsive, server-rendered reader over the published-story projection."""
from html import escape
from urllib.parse import quote

STYLE = '''
:root{color-scheme:light;--ink:#18382c;--muted:#56665d;--line:#d3ddd5;--paper:#f6f7f1}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.65 system-ui,sans-serif}
a{color:#1d6345;text-underline-offset:.2em}a:focus-visible{outline:3px solid #a67515;outline-offset:4px}
header,main,footer{max-width:940px;margin:auto;padding:24px}header{border-bottom:1px solid var(--line)}
.brand{font:700 30px Georgia,serif;letter-spacing:.08em;text-decoration:none}.tagline,.meta{color:var(--muted);font-size:14px}
h1,h2,h3{font-family:Georgia,serif;line-height:1.2}h1{font-size:clamp(30px,6vw,48px);overflow-wrap:anywhere}
h2{font-size:27px}h3{font-size:22px}article.card{padding:20px 0;border-bottom:1px solid var(--line)}
article.card h2{margin:6px 0}.badge{font-size:13px;background:#dfebe0;border-radius:4px;padding:3px 9px}
.notice{border-left:4px solid #8c6621;background:#faf0d9;padding:12px 18px}.item{margin:22px 0}
.item p{margin:6px 0}.sources li{margin-bottom:12px;overflow-wrap:anywhere}.history{padding:18px;background:#e9eee7}
small{font-size:14px}footer{border-top:1px solid var(--line);font-size:14px;color:var(--muted)}
@media(max-width:600px){header,main,footer{padding:18px}.brand{font-size:25px}body{font-size:16px}}
'''


def e(value):
    return escape(str(value), quote=True)


def layout(title, content):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{e(title)} · EPSTMC</title><style>{STYLE}</style></head><body>'
            '<header><a class="brand" href="/">EPSTMC</a>'
            '<p class="tagline">Evidence. Context. What could happen next.</p></header>'
            f'<main id="main">{content}</main><footer>Sources support reporting; scenarios describe '
            'conditional possibilities. Read the original evidence and publication history.</footer></body></html>')


def feed_page(feed):
    content = '<h1>The evidence desk</h1><p>Published stories, their sources and the context behind them.</p>'
    if not feed['items']:
        content += '<p>No stories have been published yet.</p>'
    for story in feed['items']:
        sid = story['story_id']
        content += (f'<article class="card"><span class="badge">{e(story["kind"].title())}</span>'
                    f'<h2><a href="/stories/{sid}">{e(story["content"]["title"])}</a></h2>'
                    f'<p class="meta">Version {story["version"]} · <time>{e(story["published_at"])}</time></p>'
                    f'<p>{e(story["summary"])}</p></article>')
    if feed['next_cursor']:
        content += f'<p><a href="/?cursor={quote(feed["next_cursor"], safe="")}">Older stories</a></p>'
    content += '<p><a href="/api/v1/feed">Read the feed as JSON</a></p>'
    return layout('The evidence desk', content)


def story_page(story, history):
    payload = story['content']
    sid = story['story_id']
    content = f'<p><a href="/">← All stories</a></p><h1>{e(payload["title"])}</h1>'
    content += (f'<p class="meta">Published version {story["version"]} · '
                f'<time>{e(story["published_at"])}</time></p>'
                f'<p class="notice"><strong>{e(story["kind"].title())}:</strong> {e(story["summary"])}</p>')
    latest = history['versions'][0]
    if latest['version'] != story['version']:
        content += (f'<p class="notice">You are reading an earlier publication. '
                    f'<a href="/stories/{sid}">Read the latest version ({latest["version"]}).</a></p>')
    for section, heading in (('facts', 'What happened'), ('history', 'Historical context'),
                             ('scenarios', 'What could happen next')):
        content += f'<section><h2>{heading}</h2>'
        for item in payload[section]:
            refs = ', '.join(f'<a href="#source-{e(ref)}">{e(ref)}</a>' for ref in item['source_ids'])
            content += '<div class="item">'
            if section == 'scenarios':
                content += (f'<p>If {e(item["condition"])}, {e(item["text"])}</p>'
                            f'<p><strong>Timeframe:</strong> {e(item["timeframe"])}</p>'
                            f'<p><strong>Watch for:</strong> {e(item["signal"])}</p>')
            else:
                content += f'<p>{e(item["text"])}</p>'
                if section == 'history':
                    content += (f'<p><strong>Comparison:</strong> {e(item["comparison"])}</p>'
                                f'<p><strong>Limitations:</strong> {e(item["limitations"])}</p>')
            content += f'<p><small>Evidence: {refs}</small></p></div>'
        content += '</section>'
    content += '<section><h2>Original sources</h2><ul class="sources">'
    for source in payload['sources']:
        content += (f'<li id="source-{e(source["id"])}"><a href="{e(source["url"])}" '
                    f'rel="noopener noreferrer">{e(source["title"])}</a> '
                    f'<small>({e(source["publication_date"])})</small></li>')
    content += '</ul></section><section class="history"><h2>Publication history</h2><ol>'
    for version in history['versions']:
        content += (f'<li><a href="/stories/{sid}?version={version["version"]}">Version {version["version"]}</a>'
                    f' · {e(version["kind"])} · {e(version["published_at"])}'
                    f'<p>{e(version["summary"])}</p></li>')
    content += (f'</ol></section><p><a href="/api/v1/stories/{sid}/versions/{story["version"]}">'
                'This publication as JSON</a></p>')
    return layout(payload['title'], content)
