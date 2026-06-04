"""
web_monitor.py — jalankan bersamaan dengan server.py
Akses di http://localhost:8080
"""
from flask import Flask, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__, static_folder="static")
DB_PATH = "sensor.db"

def query_db(sql, args=()):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(sql, args)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

@app.route("/api/latest")
def latest():
    """50 data terbaru untuk grafik real-time"""
    rows = query_db("""
        SELECT timestamp, sensor_gas, sensor_suhu, sensor_kelembaban
        FROM sensor_data
        WHERE sensor_suhu IS NOT NULL OR sensor_kelembaban IS NOT NULL OR sensor_gas IS NOT NULL
        ORDER BY id DESC LIMIT 50
    """)
    return jsonify(list(reversed(rows)))

@app.route("/api/average")
def average():
    """Rata-rata per 10 data untuk suhu dan kelembaban"""
    rows = query_db("""
        SELECT
            ((id - 1) / 10) AS batch,
            MIN(timestamp) AS timestamp,
            ROUND(AVG(sensor_suhu), 2) AS avg_suhu,
            ROUND(AVG(sensor_kelembaban), 2) AS avg_kelembaban,
            COUNT(*) AS n
        FROM sensor_data
        WHERE sensor_suhu IS NOT NULL OR sensor_kelembaban IS NOT NULL
        GROUP BY batch
        ORDER BY batch DESC LIMIT 20
    """)
    return jsonify(list(reversed(rows)))

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(host="0.0.0.0", port=8080, debug=False)
