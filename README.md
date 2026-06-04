"# Project Kapita Selekta Sistem Jaringan dan Komputer - Kelompok 2"

SISTEM MONITORING KUALITAS LINGKUNGAN ( SUHU, UDARA, DAN KELEMBAPAN)
 
anggota kelompok :
- Aldi Rawi Albidunanda (23/521351/PA/22421) ( electronics ) 
- Arifah Yumna (23/516607/PA/22104) ( server programmer )
- Devan Cahya Pratama Gunawan (23/513353/PA/21934) ( hardware programmer )

Flow sensor ke esp32 (sementara)
<img width="174" height="471" alt="KS SKJ" src="https://github.com/user-attachments/assets/4c9d6387-112e-472a-a8bb-7b51d51d8b75" />

<p align="justify">
Project ini merupakan sistem monitoring suhu berbasis ESP32 dan sensor DHT11 yang dirancang untuk membaca data suhu kemudian mengirimkannya ke server lokal kampus dengan alamat IP 10.6.6.41 dengan port 5012. Sistem ini memanfaatkan koneksi jaringan kampus sehingga data dapat dipantau secara real-time melalui server yang telah disediakan. Implementasi sensor pada project ini masih bersifat percobaan dan pengembangan awal, sehingga jenis sensor maupun fitur sistem masih dapat dikembangkan lebih lanjut sesuai kebutuhan di masa mendatang. Pada versi saat ini, data suhu yang dikirim ke server belum disimpan ke dalam database atau media penyimpanan permanen, sehingga data akan hilang ketika koneksi terputus atau sistem mengalami disconnect. Untuk pengembangan berikutnya, sistem direncanakan akan memiliki fitur penyimpanan data suhu agar riwayat monitoring dapat direkam dan dianalisis secara berkelanjutan.Ke depannya, sistem ini masih dapat dikembangkan dengan menambahkan berbagai jenis sensor lain agar fungsi monitoring menjadi lebih lengkap dan bermanfaat. Selain sensor suhu, sistem dapat ditambahkan sensor gas atau kualitas udara seperti MQ-135 untuk mendeteksi polusi udara, asap, atau kadar gas tertentu di lingkungan sekitar. Penggunaan sensor kelembapan, sensor cahaya, maupun sensor api juga dapat dipertimbangkan untuk memperluas kemampuan monitoring lingkungan secara real time. Selain penambahan sensor, sistem juga dapat dikembangkan dengan fitur penyimpanan data ke database, tampilan grafik monitoring berbasis web. Dengan pengembangan tersebut, sistem tidak hanya berfungsi sebagai percobaan pembacaan suhu sederhana, tetapi juga dapat menjadi dasar implementasi sistem monitoring lingkungan berbasis Internet of Things (IoT) yang lebih kompleks dan aplikatif.
</p>
Flow Sensor DHT11 & MQ135 ke ESP32
<img width="754" height="888" alt="flow dht11   mq135 ke esp32" src="https://github.com/user-attachments/assets/56c41cd9-4269-41c2-9637-e57c36f98ff9" />

Rangkaian DHT11 & MQ-135 ke ESP32

<img width="662" height="570" alt="rangkaian dht11   mq135" src="https://github.com/user-attachments/assets/67942e5e-e64b-4d16-998a-8fa98924311f" />



flow chart program esp32 
<img width="1168" height="619" alt="flowchart " src="https://github.com/user-attachments/assets/37d44304-6f90-4af7-a797-34e13ba8cf05" />

<p align="justify">
Program ini dimulai dari blok Start dan langsung memasuki fase Setup. Pada tahap ini, ESP32 melakukan beberapa inisialisasi penting, yaitu mengaktifkan komunikasi serial dengan baud rate 115200, menginisialisasi sensor DHT11 melalui fungsi dht.begin(), menghubungkan perangkat ke jaringan WiFi “UGM-Hotspot”, menunggu hingga koneksi WiFi berhasil terbentuk, serta menampilkan alamat IP ESP32 di Serial Monitor.
Setelah setup selesai, program memasuki Main Loop yang berjalan secara terus-menerus. Dalam setiap iterasi, ESP32 pertama-tama membaca nilai suhu menggunakan perintah dht.readTemperature(). Hasil pembacaan kemudian dicek menggunakan fungsi isnan(). Apabila nilai suhu tidak valid, program akan mencetak pesan “Gagal membaca sensor!” dan menunggu selama 10 detik sebelum mencoba membaca sensor kembali. Jika pembacaan berhasil, program mencetak nilai suhu dalam format “Suhu: xx °C”. Selanjutnya, program mencoba membuat koneksi TCP ke server yang telah ditentukan. Jika koneksi berhasil, data suhu dikirimkan dalam bentuk string sederhana, kemudian koneksi langsung ditutup dan program mencetak pesan “Data terkirim & koneksi ditutup”. Sebaliknya, jika gagal terhubung ke server, hanya pesan “Gagal konek ke server” yang dicetak. Pada akhir setiap siklus, program selalu menunggu selama 10 detik sebelum kembali ke awal Main Loop untuk mengulangi proses pembacaan dan pengiriman data.
</p>

flow chart internal libraryv dht.h
<img width="1168" height="621" alt="proses library dht h" src="https://github.com/user-attachments/assets/de745bb2-56f0-4605-a40d-1243c5e32396" />

<p align="justify">
Diagram Alir Internal Library DHT.h menggambarkan proses pembacaan suhu DHT11 melalui protokol 1-Wire secara rinci. Proses dimulai ketika fungsi readTemperature() dipanggil dari program utama. Library terlebih dahulu melakukan pengecekan waktu atau cache: apakah sudah lebih dari 2 detik sejak pembacaan terakhir atau ada perintah force. Jika belum cukup waktu, library langsung mengembalikan nilai suhu lama yang tersimpan di cache dan proses selesai. Jika waktu sudah cukup atau force diaktifkan, maka fungsi _readSensor() akan dijalankan.
Pada tahap _readSensor(), library mengirim sinyal start ke sensor dengan mengatur pin sebagai OUTPUT, menarik pin LOW selama 18–20 milidetik, kemudian menarik HIGH selama 40 mikrosekon, dan mengubah pin menjadi INPUT dengan pull-up. Selanjutnya library menunggu respons dari sensor DHT11 berupa pola LOW 80 µs diikuti HIGH 80 µs. Apabila respons sensor tidak sesuai atau timeout, proses langsung dianggap gagal dan mengembalikan nilai NAN (Not a Number). Jika respons berhasil diterima, library melanjutkan ke tahap Baca 40 Bit Data. Pada tahap ini, untuk setiap dari 40 bit data (5 byte), library menunggu sinyal LOW, kemudian mengukur durasi sinyal HIGH. Jika durasi HIGH melebihi threshold tertentu maka bit dianggap bernilai 1, jika lebih pendek maka bernilai 0. Kelima byte data tersebut disimpan ke dalam array data[5].
Setelah data lengkap diterima, dilakukan pengecekan checksum: apakah byte ke-5 (data[4]) sama dengan hasil penjumlahan byte 0 hingga 3 (modulo 256). Jika checksum valid, library menghitung nilai suhu sebagai data[2] + (data[3] × 0.1) dan nilai kelembaban sebagai data[0] + (data[1] × 0.1), kemudian mengembalikan kedua nilai tersebut ke program utama. Jika checksum tidak sesuai, library mengembalikan nilai NAN sebagai indikasi error. Seluruh proses ini sangat bergantung pada timing yang ketat (hingga ±1 mikrosekon), karena protokol 1-Wire DHT11 sangat sensitif terhadap selisih waktu pulsa. Proses berakhir setelah nilai suhu berhasil dikembalikan atau terjadi kegagalan.
</p>

Output di server
<img width="1122" height="647" alt="output di server" src="https://github.com/user-attachments/assets/7b00a39a-26d1-47c5-9247-1304efa4b716" />


hasil kirim data dari Mq135 dan dht11 ke esp32 yang berhasil terkirim ke server
<img width="921" height="681" alt="hasil mq dan dht ke server" src="https://github.com/user-attachments/assets/e8b01166-2976-434d-b05e-9e62ad864bff" />


