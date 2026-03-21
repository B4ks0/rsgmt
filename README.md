# 🏥 RS Gunung Maria Tomohon - Appointment System with AI OCR

Sistem Janji Temu Digital untuk **RS Gunung Maria Tomohon** yang dirancang dengan antarmuka premium, integrasi kecerdasan buatan (AI) untuk pengenalan identitas, dan manajemen jadwal dokter yang dinamis.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-092e20.svg)](https://www.djangoproject.com/)
[![Tesseract OCR](https://img.shields.io/badge/OCR-Tesseract-red.svg)](https://github.com/tesseract-ocr/tesseract)

## ✨ Fitur Utama

### 1. 👁️ AI KTP Scanner (OCR)
- **Auto-Fill NIK**: Sistem secara otomatis membaca 16 digit NIK dari foto KTP menggunakan **Tesseract OCR**.
- **Multi-Pass Strategy**: Algoritma cerdas yang mencoba berbagai mode pemrosesan gambar (*Upscaling, Contrast, Sharpening*) untuk hasil akurasi maksimal.
- **Fail-Safe Mechanism**: Notifikasi otomatis jika identitas sulit terbaca, memberikan opsi input manual yang lancar.

### 2. 👨‍⚕️ Sistem Dokter Cerdas
- **Dynamic Dependent Dropdown**: Pilihan dokter otomatis terfilter berdasarkan Poli/Departemen yang dipilih (menggunakan AJAX).
- **Auto-Random Pick**: Jika pasien tidak memiliki preferensi tertentu, sistem akan menyarankan satu dokter secara acak dari departemen tersebut.
- **Profil Detail & Jadwal Lengkap**: Halaman profil dokter yang menampilkan biografi, pengalaman, dan tabel jadwal mingguan lengkap (Senin-Minggu).

### 3. 🎨 UI/UX Premium
- **Responsive Design**: Tampilan yang dioptimalkan untuk perangkat *Mobile* maupun *Desktop*.
- **Modern Aesthetics**: Menggunakan palet warna yang harmonis, bayangan lembut (*Soft Shadows*), dan animasi mikro untuk pengalaman pengguna yang menyenangkan.

### 4. 📊 Dashboard Admin
- Manajemen janji temu pasien.
- Pengolahan data dokter dan departemen.
- Statistik dan riwayat pembayaran.

---

## 🚀 Instalasi & Persiapan

### Prasyarat
- Python 3.10+
- Django 4.2+
- **Tesseract OCR Engine** terinstall di sistem (khusus Windows: pastikan path mengarah ke `C:\Program Files\Tesseract-OCR\tesseract.exe`).

### Langkah Instalasi

1. **Clone Repository**
   ```bash
   git clone https://github.com/B4ks0/rsgmt.git
   cd rsgmt
   ```

2. **Setup Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/scripts/activate  # atau venv\Scripts\activate untuk Windows
   ```

3. **Install Dependensi**
   ```bash
   pip install -r requirements.txt
   ```

4. **Migrasi Database**
   ```bash
   python manage.py migrate
   ```

5. **Jalankan Server**
   ```bash
   python manage.py runserver
   ```

## 📸 Demo Fitur OCR
Sistem ini menggunakan teknik pengolahan gambar berbasis `Pillow` sebelum dikirim ke mesin OCR:
- **Upscaling 2x**: Menambah detail pada KTP resolusi rendah.
- **Grayscale & Thresholding**: Memisahkan teks dari latar belakang secara tajam.
- **Sharpening**: Memperjelas sudut-sudut font agar mudah terbaca oleh mesin.

---

## 🛡️ Lisensi
Aplikasi ini dikembangkan khusus untuk **RS Gunung Maria Tomohon**.

## 📞 Kontak
Jika ada kendala dalam penggunaan sistem, silakan hubungi tim IT RS Gunung Maria atau buka *issue* di repository ini.

---
*Created with ❤️ for RS Gunung Maria Tomohon*
