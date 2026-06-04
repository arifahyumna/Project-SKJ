from server import parse_sensor_data

test_cases = [
    ("CSV Format", "350,28.4,65.2"),
    ("JSON Format", '{"gas": 420.5, "suhu": 29.1, "kelembaban": 58.0}'),
    ("Key-Value Colon Format", "gas: 210.3; suhu: 27.5; kelembaban: 60.1"),
    ("Key-Value Equals Format", "gas=180.0, suhu=26.2, kelembaban=70.0"),
    ("Malformed Format", "gas: abc, temp: 25, hum: 50"),
    ("Partial Format", "gas: 250, suhu: 30.0")
]

print("=== SENSOR PARSING DEMONSTRATION ===")
for desc, payload in test_cases:
    gas, suhu, kelembaban = parse_sensor_data(payload)
    print(f"\n{desc}:")
    print(f"  Input Payload: {payload!r}")
    print(f"  - Parsed Gas        : {gas}")
    print(f"  - Parsed Suhu       : {suhu} °C" if suhu is not None else "  - Parsed Suhu       : None")
    print(f"  - Parsed Kelembaban : {kelembaban} %" if kelembaban is not None else "  - Parsed Kelembaban : None")
print("\n====================================")
