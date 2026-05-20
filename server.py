import socket
import sqlite3
import re
import json
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5012

# Koneksi Database SQLite
conn_db = sqlite3.connect("sensor.db")
cursor = conn_db.cursor()

# Buat tabel dengan skema baru jika belum ada
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    ip_address TEXT,
    sensor_gas REAL,
    sensor_suhu REAL,
    sensor_kelembaban REAL,
    raw_data TEXT
)
""")

# Migrasi otomatis: cek dan tambahkan kolom jika tabel sudah ada dengan skema lama
for col, col_type in [("sensor_gas", "REAL"), ("sensor_suhu", "REAL"), ("sensor_kelembaban", "REAL"), ("raw_data", "TEXT")]:
    try:
        cursor.execute(f"ALTER TABLE sensor_data ADD COLUMN {col} {col_type}")
    except sqlite3.OperationalError:
        # Kolom sudah ada
        pass

conn_db.commit()

def parse_sensor_data(raw_data_str):
    """
    Fungsi parser untuk mengekstrak data sensor gas, suhu, dan kelembaban.
    Mendukung format JSON, key-value (misal gas:300, suhu:28), atau CSV (gas,suhu,kelembaban).
    """
    gas = None
    suhu = None
    kelembaban = None

    data_str = raw_data_str.strip()

    # 1. Coba parse sebagai JSON
    try:
        parsed = json.loads(data_str)
        if isinstance(parsed, dict):
            for k, v in parsed.items():
                k_lower = k.lower()
                if "gas" in k_lower:
                    gas = float(v)
                elif "suhu" in k_lower or "temp" in k_lower:
                    suhu = float(v)
                elif "kelembaban" in k_lower or "humi" in k_lower:
                    kelembaban = float(v)
            return gas, suhu, kelembaban
    except (json.JSONDecodeError, ValueError, TypeError):
        pass

    # 2. Coba parse key-value pairs (contoh: "gas:300, suhu:28.5, kelembaban:60" atau "gas=300; suhu=28.5")
    matches = re.findall(r'(\w+)\s*[:=]\s*([0-9.-]+)', data_str)
    if matches:
        for key, val in matches:
            key_lower = key.lower()
            try:
                if "gas" in key_lower:
                    gas = float(val)
                elif "suhu" in key_lower or "temp" in key_lower:
                    suhu = float(val)
                elif "kelembaban" in key_lower or "humi" in key_lower:
                    kelembaban = float(val)
            except ValueError:
                pass
        if gas is not None or suhu is not None or kelembaban is not None:
            return gas, suhu, kelembaban

    # 3. Coba parse CSV / Comma-separated (contoh: "300,28.5,60")
    # Memisahkan berdasarkan koma, titik koma, atau spasi
    parts = re.split(r'[,\s;]+', data_str)
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) == 3:
        try:
            gas = float(parts[0])
            suhu = float(parts[1])
            kelembaban = float(parts[2])
            return gas, suhu, kelembaban
        except ValueError:
            pass

    return gas, suhu, kelembaban

# Server TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)

print(f"Server standby di {HOST}:{PORT}")

try:
    while True:
        conn, addr = server.accept()
        print(f"Terhubung dari {addr}")

        try:
            data = b""
            while True:
                packet = conn.recv(1024)
                if not packet:
                    break
                data += packet

            # Timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Decode data
            raw_data_str = data.decode('utf-8', errors='ignore')

            # Parse sensor data
            gas, suhu, kelembaban = parse_sensor_data(raw_data_str)

            # Simpan ke Database
            cursor.execute("""
            INSERT INTO sensor_data (timestamp, ip_address, sensor_gas, sensor_suhu, sensor_kelembaban, raw_data)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (timestamp, addr[0], gas, suhu, kelembaban, raw_data_str))
            conn_db.commit()

            # Tampilkan data di console
            print("Data diterima:")
            print(f"  - Raw Data        : {raw_data_str.strip()}")
            print(f"  - Sensor Gas      : {gas if gas is not None else 'N/A'}")
            print(f"  - Sensor Suhu     : {suhu if suhu is not None else 'N/A'} °C")
            print(f"  - Sensor Kelembaban: {kelembaban if kelembaban is not None else 'N/A'} %")

        except Exception as e:
            print(f"Error memproses data dari {addr}: {e}")
        finally:
            conn.close()
            print("Koneksi ditutup\n")
finally:
    conn_db.close()
    server.close()