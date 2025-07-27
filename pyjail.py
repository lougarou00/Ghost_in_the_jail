#!/usr/bin/env python3

import socket
import re
import threading
import sys
import os

# Restriction setup
banned = "import|chr|os|sys|system|builtin|exec|eval|subprocess|pty|popen|read|get_data|for|in|join|chr"
search_func = lambda word: re.compile(r"\b({0})\b".format(word), flags=re.IGNORECASE).search

def handle_client(conn, addr):
    try:
        conn.sendall(sys.version.encode() + b"\n")
        conn.sendall(b"Tell me something\n")

        for _ in range(2):
            conn.sendall(b">>> ")
            data = b""
            while not data.endswith(b"\n"):
                part = conn.recv(1024)
                if not part:
                    return
                data += part
            text = data.decode().strip().lower()
            check = search_func(banned)(''.join(text.split("__")))
            if check:
                conn.sendall(f"Stupid, you can't use {check.group(0)}!\n".encode())
                break
            if re.match("^(_?[A-Za-z0-9])*[A-Za-z](_?[A-Za-z0-9])*$", text):
                conn.sendall(b"You aren't getting through that easily, come on.\n")
                break
            else:
                try:
                    exec(text, {'globals': globals(), '__builtins__': {}}, {'print': lambda *args: conn.sendall(' '.join(map(str, args)).encode() + b"\n")})
                except Exception as e:
                    conn.sendall(f"Error: {str(e)}\n".encode())
    finally:
        conn.close()

def main():
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 1337))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        print(f"Challenge running on port {port}...")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
