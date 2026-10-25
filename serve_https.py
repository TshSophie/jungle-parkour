#!/usr/bin/env python3
"""局域网 HTTPS 服务：手机用前置摄像头必须 HTTPS（非 localhost 视为不安全上下文）。
证书按当前局域网 IP 自动生成，IP 变化时自动重新生成。"""
import socket, subprocess, os, sys, ssl
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8443
HERE = os.path.dirname(os.path.abspath(__file__))
CERT = os.path.join(HERE, "cert.pem")
KEY = os.path.join(HERE, "key.pem")
IP_FILE = os.path.join(HERE, ".lan_ip")

def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

def gen_cert(ip):
    openssl = None
    for p in [
        r"D:\installed\WorkBuddy\resources\vendor\PortableGit\usr\bin\openssl.exe",
        r"C:\Users\tanso\.workbuddy\binaries\PortableGit\versions\1.3.0\usr\bin\openssl.exe",
        r"D:\installed\anaconda3\Library\bin\openssl.exe",
    ]:
        if os.path.exists(p):
            openssl = p
            break
    if not openssl:
        raise RuntimeError("未找到 openssl")
    cmd = [
        openssl, "req", "-x509", "-newkey", "rsa:2048", "-nodes",
        "-keyout", KEY, "-out", CERT, "-days", "365",
        "-subj", f"/CN={ip}",
        "-addext", f"subjectAltName=IP:{ip},DNS:localhost",
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(IP_FILE, "w") as f:
        f.write(ip)

def ensure_cert(ip):
    need = True
    if os.path.exists(CERT) and os.path.exists(KEY) and os.path.exists(IP_FILE):
        with open(IP_FILE) as f:
            need = f.read().strip() != ip
    if need:
        print(f"[cert] IP 变化（{ip}），重新生成自签证书…")
        gen_cert(ip)
    else:
        print(f"[cert] 复用已有证书（IP {ip}）")

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=HERE, **k)
    def log_message(self, *a):
        pass  # 安静

def main():
    ip = lan_ip()
    ensure_cert(ip)
    httpd = HTTPServer(("0.0.0.0", PORT), Handler)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT, KEY)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    print(f"[https] 服务已启动：https://{ip}:{PORT}/  (局域网 + 摄像头可用)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
