#!/usr/bin/env python3
from flask import Flask, request, Response, redirect
import requests as req
from readability import Document
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
import traceback

app = Flask(__name__)

UPSTREAM_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'identity',
}
TIMEOUT = 15

def proxy_url(original_url):
    return f"/browse?url={quote(original_url, safe='')}"

def rewrite_links(soup, base_url):
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith(('javascript:', 'mailto:', 'tel:', '#')): continue
        a['href'] = proxy_url(urljoin(base_url, href))
    for form in soup.find_all('form', action=True):
        form['action'] = proxy_url(urljoin(base_url, form['action']))

def strip_heavy_content(soup):
    for tag_name in ['script', 'style', 'link', 'iframe', 'video', 'audio', 'canvas', 'svg', 'noscript', 'object', 'embed']:
        for tag in soup.find_all(tag_name): tag.decompose()
    for img in soup.find_all('img'):
        alt = img.get('alt', '')
        if alt: img.replace_with(f'[IMG: {alt}]')
        else: img.decompose()

RETRO_CSS = "body{font-family:'Segoe UI',Tahoma,sans-serif;font-size:15px;margin:6px;color:#111;background:#fff;word-wrap:break-word;}a{color:#0066cc;}h1,h2,h3{margin:0.5em 0 0.3em 0;}pre,code{white-space:pre-wrap;background:#f0f0f0;padding:2px 4px;}.nav-bar{background:#0078d7;color:#fff;padding:6px;margin:-6px -6px 8px -6px;}.nav-bar input[type=text]{width:65%;padding:4px;}.nav-bar button{padding:4px 10px;}.error{color:#cc0000;background:#fff0f0;padding:8px;border:1px solid #cc0000;}.meta{color:#666;font-size:12px;}"

NAV_BAR = '<div class="nav-bar"><form action="/browse" method="get"><input type="text" name="url" value="{url}" placeholder="https://example.com"><button type="submit">Go</button></form><a href="/" style="color:#fff;font-size:12px">Home</a></div>'

def make_page(title, body_html, current_url=""):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{RETRO_CSS}</style></head><body>{NAV_BAR.format(url=current_url)}{body_html}</body></html>"""

@app.route('/')
def index():
    links = [("https://lite.cnn.com", "CNN Lite"),("https://text.npr.org", "NPR Text"),("https://en.wikipedia.org", "Wikipedia"),("https://news.ycombinator.com", "Hacker News"),("https://old.reddit.com", "Reddit (Old)"),("https://wiby.me", "Wiby.me (Retro Search)")]
    link_html = "\n".join(f'<li><a href="{proxy_url(url)}">{name}</a></li>' for url, name in links)
    body = f"<h1>Lumia Retro Web Proxy</h1><p>Enter a URL above or try these:</p><ul>{link_html}</ul><hr><p class='meta'>Running on local network. Served to Lumia over plain HTTP.</p>"
    return make_page("Retro Proxy Home", body)

@app.route('/browse')
def browse():
    url = request.args.get('url', '').strip()
    if not url: return redirect('/')
    if not url.startswith(('http://', 'https://')): url = 'https://' + url
    try:
        resp = req.get(url, headers=UPSTREAM_HEADERS, timeout=TIMEOUT, allow_redirects=True, verify=True)
        resp.raise_for_status()
        if 'text/html' not in resp.headers.get('Content-Type', ''):
            return make_page("Error", f'<p>Non-HTML content.</p>', url)
        doc = Document(resp.text)
        title = doc.title()
        soup = BeautifulSoup(doc.summary(), 'html.parser')
        strip_heavy_content(soup)
        rewrite_links(soup, resp.url)
        meta = f'<p class="meta">Source: {resp.url}</p>'
        return make_page(title, f"<h2>{title}</h2>{meta}<hr>{soup}", url)
    except Exception as e:
        return make_page("Error", f'<div class="error"><strong>{type(e).__name__}:</strong> {e}</div>', url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)