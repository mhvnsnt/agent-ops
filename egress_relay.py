import socket, threading, os, base64, select
from urllib.parse import urlparse

pu = urlparse(os.environ["HTTPS_PROXY"])
UP = (pu.hostname, pu.port)
AUTH = base64.b64encode(f"{pu.username}:{pu.password}".encode()).decode()

def handle(client):
    try:
        req = b""
        while b"\r\n\r\n" not in req:
            chunk = client.recv(4096)
            if not chunk: client.close(); return
            req += chunk
        line = req.split(b"\r\n")[0].decode("latin1")
        method, target, _ = line.split(" ", 2)
        if method.upper() != "CONNECT":
            client.sendall(b"HTTP/1.1 405 NA\r\n\r\n"); client.close(); return
        up = socket.create_connection(UP, timeout=30)
        up.sendall(f"CONNECT {target} HTTP/1.1\r\nHost: {target}\r\nProxy-Authorization: Basic {AUTH}\r\nProxy-Connection: keep-alive\r\n\r\n".encode())
        resp = b""
        while b"\r\n\r\n" not in resp:
            chunk = up.recv(4096)
            if not chunk: client.close(); up.close(); return
            resp += chunk
        status = resp.split(b"\r\n")[0]
        if b" 200 " not in status and not status.endswith(b" 200"):
            client.sendall(b"HTTP/1.1 502 Bad Gateway\r\n\r\n"); client.close(); up.close(); return
        client.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
        def pipe(a, b):
            try:
                while True:
                    r, _, _ = select.select([a], [], [], 60)
                    if not r: break
                    data = a.recv(65536)
                    if not data: break
                    b.sendall(data)
            except OSError:
                pass
            finally:
                try: b.shutdown(socket.SHUT_WR)
                except OSError: pass
        t = threading.Thread(target=pipe, args=(client, up), daemon=True); t.start()
        pipe(up, client)
        client.close(); up.close()
    except OSError:
        try: client.close()
        except OSError: pass

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("127.0.0.1", 18080))
srv.listen(50)
print("relay up on 127.0.0.1:18080", flush=True)
while True:
    c, _ = srv.accept()
    threading.Thread(target=handle, args=(c,), daemon=True).start()
