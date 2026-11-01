# Analisis-Bike-Sharing
Deskripsi Proyek 
Repositori ini berisi proyek analisis data yang berfokus pada eksplorasi data penyewaan sepeda. Hal ini bertujuan untuk mengungkap wawasan mengenai faktor-faktor yang memengaruhi penyewaan sepeda, seperti kondisi cuaca, hari libur, musim, hari biasa dan lainnya. Selain itu, repositori ini juga mencakup analisis pengelompokan untuk mengelompokkan data berdasarkan fitur-fitur utama.

# Struktur Direktori
submission
├───dashboard
| ├───main_data.csv
| └───dashboard.py
├───data
| ├───data_1.csv
| └───data_2.csv
├───notebook.ipynb
├───README.md
└───requirements.txt
└───url.txt

# Dataset
hour.csv : Pada data set ini berisikan informasi tentang berapa jam penyewa menyewa sepeda.
day.csv : Pada data set ini berisikan informasi mengenai suhu, kelembapan pada saat menyewa sepeda setiap harinya.

# Visualisasi
**Correlation matrix:**
 Pada Visualisasi menunjukan Correlation Matrix dari dataset utama yang digunakan untuk menganalisis penyewaan sepeda. Matriks ini memperlihatkan hubungan antara suhu (temp), kelembaban (hum), kecepatan angin (windspeed), dan total penyewaan (cnt) yang berpotensi mempengaruhi jumlah penyewaan sepeda.

**Histogram Penyewaan Sepeda:**
 Pada visualisasi ini menunjukan distribusi total penyewaan sepeda per hari.

**Box Plot Penyewaan Sepeda per Musim:**
  Grafik ini memvisualisasikan penyewaan sepeda berdasarkan musim yang berbeda.
  
**Dampak Cuaca pada Penyewaan Sepeda:**
  Yang dimana mengkatagorikan penyewaan sepeda berdasarkan kondisi cuaca.
  
**Distribusi Penyewaan Sepeda berdasarkan Situasi Cuaca:**
  Visualisasi ini menggambarkan distribusi total penyewaan sepeda yang dipengaruhi oleh situasi cuaca. 
  
 **Rata-rata Penyewaan Sepeda berdasarkan Musim dan Cuaca:**
  Visualisasi ini menggambarkan rata-rata penyewaan sepeda yang dipengaruhi oleh musim dan kondisi cuaca. Diagram batang ini memberikan pemahaman tentang bagaimana musim dan cuaca memengaruhi jumlah penyewaan sepeda.
  
# Instalasi
1. # Mengkloning repositori ini ke mesin lokal
   
   Pastikan untuk mengcopy link dibawah ini: https://github.com/tatatititutu-a/Analisis-Bike-Sharing

2. # Langkah-Langkah Setup di Google Colab
   
   Pastikan untuk install library yang memang diperlukan lalu jalankan kode berikut ini:
   !pip install -r requirements.txt
   
3. # Menajalankan Dashboard

   Ketika library sudah terinstall, lalu jalankan aplikasi streamlit dengan perintah berikut:
   !streamlit run dashboard/app.py & npx localtunnel --port 8501

4. # Link Dashboard
   
   Untuk Link Dasboard bisa di akses melalui url : (https://p5xxobcvh3xewscpsmjelt.streamlit.app/)

5. # Menjalankan Aplikasi Streamlit (Opsional)
   
   Jika ingin menjalankan aplikasi Streamlit (di luar Google Colab), masuk ke direktori repositori Anda, lalu jalankan perintah berikut: `streamlit run dashboard/app.py`.
