"# Project Kapita Selekta Sistem Jaringan dan Komputer - Kelompok 2"
anggota kelompok :
- Aldi Rawi Albidunanda (23/521351/PA/22421) ( electronics ) 
- Arifah Yumna (23/516607/PA/22104) ( server programmer )
- Devan Cahya Pratama Gunawan (23/513353/PA/21934) ( hardware programmer )

  Project ini merupakan sistem monitoring suhu berbasis ESP32 dan sensor DHT11 yang dirancang untuk membaca data suhu kemudian mengirimkannya ke server lokal kampus dengan alamat IP 10.6.6.41 dengan port 5012. Sistem ini memanfaatkan koneksi jaringan kampus sehingga data dapat dipantau secara real-time melalui server yang telah disediakan. Implementasi sensor pada project ini masih bersifat percobaan dan pengembangan awal, sehingga jenis sensor maupun fitur sistem masih dapat dikembangkan lebih lanjut sesuai kebutuhan di masa mendatang. Pada versi saat ini, data suhu yang dikirim ke server belum disimpan ke dalam database atau media penyimpanan permanen, sehingga data akan hilang ketika koneksi terputus atau sistem mengalami disconnect. Untuk pengembangan berikutnya, sistem direncanakan akan memiliki fitur penyimpanan data suhu agar riwayat monitoring dapat direkam dan dianalisis secara berkelanjutan.
  Ke depannya, sistem ini masih dapat dikembangkan dengan menambahkan berbagai jenis sensor lain agar fungsi monitoring menjadi lebih lengkap dan bermanfaat. Selain sensor suhu, sistem dapat ditambahkan sensor gas atau kualitas udara seperti MQ-135 untuk mendeteksi polusi udara, asap, atau kadar gas tertentu di lingkungan sekitar. Penggunaan sensor kelembapan, sensor cahaya, maupun sensor api juga dapat dipertimbangkan untuk memperluas kemampuan monitoring lingkungan secara real-time. Selain penambahan sensor, sistem juga dapat dikembangkan dengan fitur penyimpanan data ke database, tampilan grafik monitoring berbasis web. Dengan pengembangan tersebut, sistem tidak hanya berfungsi sebagai percobaan pembacaan suhu sederhana, tetapi juga dapat menjadi dasar implementasi sistem monitoring lingkungan berbasis Internet of Things (IoT) yang lebih kompleks dan aplikatif.

Flow Sementara 
<img width="232" height="555" alt="ks skj flow awal" src="https://github.com/user-attachments/assets/2ede87e2-db23-4044-97b4-5e052ad2de63" />

