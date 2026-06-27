#!/usr/bin/env python3
"""
blog_publish.py — Converts blog-post.md to HTML and pushes to GitHub Pages repo
Usage: python scripts/blog_publish.py <slug>
"""

import json
import os
import re
import subprocess
import sys
from datetime import date
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN    = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME', 'RodeShop')
GITHUB_BLOG_REPO = os.getenv('GITHUB_BLOG_REPO', 'RodeShop/pageready')
PAGES_URL       = os.getenv('GITHUB_PAGES_URL', 'https://rodeshop.github.io/pageready')


def md_to_html_body(md):
    """Convert markdown to HTML body content."""
    lines = md.strip().split('\n')
    out = []
    in_ul = False

    def close_list():
        nonlocal in_ul
        if in_ul:
            out.append('</ul>')
            in_ul = False

    def inline(text):
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
        return text

    for line in lines:
        line = line.rstrip()
        if line.startswith('### '):
            close_list(); out.append(f'<h3>{inline(line[4:])}</h3>')
        elif line.startswith('## '):
            close_list(); out.append(f'<h2>{inline(line[3:])}</h2>')
        elif line.startswith('# '):
            close_list(); out.append(f'<h1>{inline(line[2:])}</h1>')
        elif line.startswith('- ') or line.startswith('* '):
            if not in_ul:
                out.append('<ul>'); in_ul = True
            out.append(f'<li>{inline(line[2:])}</li>')
        elif line == '':
            close_list(); out.append('')
        else:
            close_list(); out.append(f'<p>{inline(line)}</p>')

    close_list()
    return '\n'.join(out)


def build_html(spec, blog_md, gumroad_url, post_slug):
    title = spec.get('title', 'Notion Template')
    audience = spec.get('target_audience', 'Professionals')
    today = date.today().strftime('%B %d, %Y')
    body = md_to_html_body(blog_md)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — RodeShop Blog</title>
  <meta name="description" content="Notion template for {audience}. {spec.get("tagline", "")}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Inter', sans-serif; color: #1e293b; background: #fff; }}
    nav {{ padding: 18px 40px; border-bottom: 1px solid #f1f5f9; display: flex; align-items: center; justify-content: space-between; }}
    .logo {{ font-size: 17px; font-weight: 800; color: #0f172a; text-decoration: none; }}
    .logo span {{ color: #059669; }}
    .back {{ font-size: 13px; color: #64748b; text-decoration: none; }}
    .back:hover {{ color: #059669; }}
    article {{ max-width: 720px; margin: 56px auto; padding: 0 24px 80px; }}
    .post-meta {{ font-size: 13px; color: #94a3b8; margin-bottom: 32px; }}
    h1 {{ font-size: clamp(28px, 4vw, 42px); font-weight: 800; letter-spacing: -0.8px; margin-bottom: 16px; line-height: 1.15; }}
    h2 {{ font-size: 22px; font-weight: 700; margin: 40px 0 14px; color: #0f172a; }}
    h3 {{ font-size: 18px; font-weight: 700; margin: 32px 0 10px; color: #1e293b; }}
    p  {{ font-size: 16px; line-height: 1.8; color: #374151; margin-bottom: 18px; }}
    ul {{ margin: 14px 0 18px 22px; }}
    li {{ font-size: 16px; line-height: 1.8; color: #374151; margin-bottom: 6px; }}
    strong {{ color: #0f172a; }}
    a {{ color: #059669; }}
    .cta-box {{ background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 14px;
               padding: 32px; margin: 48px 0; text-align: center; }}
    .cta-box h3 {{ margin: 0 0 12px; font-size: 20px; color: #0f172a; }}
    .cta-box p  {{ margin: 0 0 24px; color: #475569; }}
    .cta-btn {{ display: inline-block; background: #059669; color: #fff;
               padding: 14px 32px; border-radius: 9px; font-weight: 700;
               font-size: 15px; text-decoration: none; }}
    .cta-btn:hover {{ background: #047857; }}
    footer {{ text-align: center; font-size: 13px; color: #94a3b8;
             padding: 32px 0; border-top: 1px solid #f1f5f9; }}
  </style>
</head>
<body>
<nav>
  <a class="logo" href="/pageready/">Rode<span>Shop</span></a>
  <a class="back" href="/pageready/">← All Templates</a>
</nav>
<article>
  <p class="post-meta">Published {today} &nbsp;·&nbsp; Notion Templates &nbsp;·&nbsp; RodeShop</p>
  {body}

  <div class="cta-box">
    <h3>Get the {title}</h3>
    <p>One-time payment · Instant access · Works with Notion Free</p>
    <a class="cta-btn" href="{gumroad_url}">Get the Template — ${spec.get("price", 29)} →</a>
  </div>
</article>
<footer>&copy; 2026 RodeShop · <a href="/pageready/">rodeshop.github.io/pageready</a></footer>
</body>
</html>'''


def git_push(file_path, commit_msg):
    repo_url = f'https://{GITHUB_TOKEN}@github.com/{GITHUB_BLOG_REPO}.git'
    # We're already in the gumroad repo — just add, commit, push
    cmds = [
        ['git', 'add', file_path],
        ['git', 'commit', '-m', commit_msg],
        ['git', 'push', repo_url, 'master'],
    ]
    for cmd in cmds:
        display = ' '.join(cmd).replace(GITHUB_TOKEN, '***')
        print(f'  $ {display}')
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 and 'nothing to commit' not in result.stdout:
            print(f'  stderr: {result.stderr[:200]}')


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/blog_publish.py <slug>')
        sys.exit(1)

    slug = sys.argv[1]
    ready_dir = f'products/ready/{slug}'
    spec_path    = f'{ready_dir}/spec.json'
    blog_md_path = f'{ready_dir}/blog-post.md'
    gumroad_path = f'{ready_dir}/gumroad_result.json'

    for path in [spec_path, blog_md_path, gumroad_path]:
        if not os.path.exists(path):
            print(f'Error: {path} not found')
            sys.exit(1)

    with open(spec_path, encoding='utf-8') as f:
        spec = json.load(f)
    with open(blog_md_path, encoding='utf-8') as f:
        blog_md = f.read()
    with open(gumroad_path, encoding='utf-8') as f:
        gumroad = json.load(f)

    gumroad_url = gumroad.get('gumroad_short_url', '')
    post_slug = slug  # use product slug as blog post slug

    # Build HTML
    html = build_html(spec, blog_md, gumroad_url, post_slug)

    # Save to blog/ in repo root (served by GitHub Pages)
    os.makedirs('blog', exist_ok=True)
    html_path = f'blog/{post_slug}.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  Blog post created: {html_path}')

    # Commit and push
    commit_msg = f'Blog: {spec["title"]}'
    git_push(html_path, commit_msg)

    post_url = f'{PAGES_URL}/blog/{post_slug}.html'
    print(f'\n  Published: {post_url}')

    # Save URL to result
    gumroad['blog_url'] = post_url
    with open(gumroad_path, 'w', encoding='utf-8') as f:
        json.dump(gumroad, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
