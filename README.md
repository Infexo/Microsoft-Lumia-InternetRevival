<div align="center">

# 🌐 Lumia 540: 2026 Internet Revival Proxy

**A lightweight Python proxy that reconnects the Microsoft Lumia 540 to the modern internet.**

No bootloader hacks. No OS mods. Just a local proxy that bridges a legacy browser to the 2026 web.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Proxy-000000?style=flat-square&logo=flask)
![Windows Phone](https://img.shields.io/badge/Windows%20Phone-8.1%20/%2010-0078D6?style=flat-square&logo=windows&logoColor=white)

</div>

---

## The Problem

By 2026, the Lumia 540's built-in browser only supports **TLS 1.0/1.1** — modern websites require **TLS 1.3**. Most sites also depend on heavy JavaScript and bot protection (Cloudflare). The result: **"Connection Closed"** on virtually everything.

## The Solution

A **Flask proxy server** runs on a PC on the same Wi-Fi network. The Lumia talks to it over plain HTTP. The PC fetches pages using modern TLS, strips JavaScript and bloat, and returns clean HTML the Lumia can actually render.

[Lumia 540 (HTTP)] <--> [PC running Flask Proxy (Modern TLS)] <--> [2026 Internet]


## Results & Limitations

| Scenario | Status | Example |
|---|---|---|
| Static / text-based sites | ✅ Works | Wikipedia loads and browses perfectly |
| JS-rendered pages | ⚠️ Blank | Content drawn client-side gets stripped |
| Bot-protected sites | ❌ Blocked | Reddit, Hacker News (Cloudflare rejects the request) |

## Setup (Windows)

1. **Install Python 3.x** — check "Add to PATH" during install
2. **Install dependencies:**
   ```bash
   pip install flask requests beautifulsoup4 readability-lxml lxml
3. **Run the proxy:**  
   ```bash
   python app.py
4. **Find your PC's IP via ipconfig** (e.g., 192.168.1.105)
5. On the Lumia: **Settings → Wi-Fi → Edit network → Proxy On**
   - **Server:** your PC's IP
   - **Port:** 8080
6. Open IE on the Lumia and go to `http://[YOUR_PC_IP]:8080`

## Screenshots

| Proxy Homepage | Wikipedia Loaded |
|----------------|------------------|
| ![Proxy Homepage](proxy.jpg) | ![Wikipedia](wiki.png) |

## Credits

- Proxy architecture inspired by retro-computing network patterns
- Content extraction powered by `readability-lxml` and `BeautifulSoup4`
