import socket
from datetime import datetime

HOST = "0.0.0.0"   # biar bisa diakses dari ESP32
PORT = 5012

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"Server standby di {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"Terhubung dari {addr}")

    data = b""
    while True:
        packet = conn.recv(1024)
        if not packet:
            break
        data += packet

    # Tambahkan timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = f"[{timestamp}] {addr} -> {data.decode()}\n"

    # Simpan ke file
    with open("data_sensor.txt", "a") as f:
        f.write(log)

    print("Data diterima:", data.decode())

    conn.close()
    print("Koneksi ditutup\n")
