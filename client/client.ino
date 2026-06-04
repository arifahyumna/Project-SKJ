#include "DHT.h"  
#include <WiFi.h>


const char* ssid = "UGM-Hotspot";
const char* password = "";


const char* host = "10.6.6.41";
const int port = 5012;


#define DHTPIN 4       
#define DHTTYPE DHT11 


#define GASPIN 34      

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  Serial.println("Program DHT11 & MQ - Deteksi Suhu, Kelembaban, Gas");

  dht.begin();
  pinMode(GASPIN, INPUT);

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
  float suhu = dht.readTemperature();
  float kelembaban = dht.readHumidity();
  int gasVal = analogRead(GASPIN);

  if (isnan(suhu) || isnan(kelembaban)) {
    Serial.println("Gagal membaca sensor DHT!");
    delay(10000);
    return;
  }

  Serial.print("Suhu       : ");
  Serial.print(suhu);
  Serial.println(" °C");
  
  Serial.print("Kelembaban : ");
  Serial.print(kelembaban);
  Serial.println(" %");

  Serial.print("Gas (Analog): ");
  Serial.println(gasVal);

  Serial.println("----------------------");

  
  WiFiClient client;

  Serial.println("Menghubungi server...");
  if (client.connect(host, port)) {
    Serial.println("Terhubung ke server");

    
    String data = String(gasVal) + "," + String(suhu) + "," + String(kelembaban);

    client.println(data);  

    client.stop(); 
    Serial.println("Data terkirim & koneksi ditutup");
  } else {
    Serial.println("Gagal konek ke server");
  }

 
  delay(10000);
}
