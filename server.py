import socket
import sqlite3
import re
import json
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5012

conn_db = sqlite3.connect("sensor.db")
cursor = conn_db.cursor()

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
conn_db.commit()

def parse_sensor_data(raw_data_str):
    """
    Parser satu langkah: ekstrak nilai gas, suhu, kelembaban dari format apapun
    (JSON dict, key=value/key:value, atau CSV tiga angka) menggunakan regex tunggal.
    """
    data_str = raw_data_str.strip()
    gas = suhu = kelembaban = None

    # Kumpulkan semua pasangan key-value dari berbagai format sekaligus
    # Tangkap: JSON "key":val, key:val, key=val — semua dalam satu regex
    kv = {k.lower(): float(v)
          for k, v in re.findall(r'"?(\w+)"?\s*[:=]\s*([0-9.-]+)', data_str)
          if _is_float(v)}

    if kv:
        for k, v in kv.items():
            if "gas" in k:
                gas = v
            elif "suhu" in k or "temp" in k:
                suhu = v
            elif "kelembaban" in k or "humi" in k:
                kelembaban = v
    else:
        # Fallback: tiga angka CSV / spasi / titik-koma
        parts = re.split(r'[,\s;]+', data_str)
        nums = [p for p in parts if _is_float(p)]
        if len(nums) >= 3:
            gas, suhu, kelembaban = float(nums[0]), float(nums[1]), float(nums[2])

    return gas, suhu, kelembaban

def _is_float(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False

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

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            raw_data_str = data.decode('utf-8', errors='ignore')
            gas, suhu, kelembaban = parse_sensor_data(raw_data_str)

            cursor.execute("""
            INSERT INTO sensor_data (timestamp, ip_address, sensor_gas, sensor_suhu, sensor_kelembaban, raw_data)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (timestamp, addr[0], gas, suhu, kelembaban, raw_data_str))
            conn_db.commit()

            print("Data diterima:")
            print(f"  - Raw Data         : {raw_data_str.strip()}")
            print(f"  - Sensor Gas       : {gas if gas is not None else 'N/A'}")
            print(f"  - Sensor Suhu      : {suhu if suhu is not None else 'N/A'} °C")
            print(f"  - Sensor Kelembaban: {kelembaban if kelembaban is not None else 'N/A'} %")

        except Exception as e:
            print(f"Error memproses data dari {addr}: {e}")
        finally:
            conn.close()
            print("Koneksi ditutup\n")
finally:
    conn_db.close()
    server.close()
