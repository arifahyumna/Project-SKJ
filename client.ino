#include "DHT.h"   // HARUS di paling atas
#include <WiFi.h>

// ===== WIFI CONFIG =====
const char* ssid = "UGM-Hotspot";
const char* password = ""; // isi jika ada

// ===== SERVER CONFIG =====
const char* host = "10.6.6.41";
const int port = 5012;

// ===== DHT CONFIG =====
#define DHTPIN 4       // pin data ke GPIO4
#define DHTTYPE DHT11  // tipe sensor

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  Serial.println("Program DHT11 - Deteksi Suhu");

  dht.begin();

  // ===== CONNECT WIFI =====
  Serial.println("Menghubungkan ke WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("\nWiFi terhubung!");
  Serial.print("IP ESP32: ");
  Serial.println(WiFi.localIP());
}

void loop() {

  // ===== BACA SENSOR =====
  float suhu = dht.readTemperature();

  if (isnan(suhu)) {
    Serial.println("Gagal membaca sensor!");
    delay(10000);
    return;
  }

  Serial.print("Suhu: ");
  Serial.print(suhu);
  Serial.println(" °C");

  Serial.println("----------------------");

  // ===== KIRIM KE SERVER =====
  WiFiClient client;

  Serial.println("Menghubungi server...");
  if (client.connect(host, port)) {
    Serial.println("Terhubung ke server");

    // Format data (bisa kamu ubah nanti)
    String data = "Suhu: " + String(suhu) + " C";

    client.println(data);  // kirim data

    client.stop(); // langsung putus
    Serial.println("Data terkirim & koneksi ditutup");
  } else {
    Serial.println("Gagal konek ke server");
  }

  // ===== DELAY 10 DETIK =====
  delay(10000);
}
