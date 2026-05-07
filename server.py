import socket
import sqlite3
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5012

# Koneksi Database SQLite
conn_db = sqlite3.connect("sensor.db")
cursor = conn_db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    ip_address TEXT,
    data TEXT
)
""")

conn_db.commit()

# Server TCP
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

    # Timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Decode data
    sensor_value = data.decode()

    # Simpan ke Database
    cursor.execute("""
    INSERT INTO sensor_data (timestamp, ip_address, data)
    VALUES (?, ?, ?)
    """, (timestamp, addr[0], sensor_value))

    conn_db.commit()

    print("Data diterima:", sensor_value)

    conn.close()
    print("Koneksi ditutup\n")