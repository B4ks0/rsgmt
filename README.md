# RS Gunung Maria Tomohon — Sistem Informasi Rumah Sakit

Sistem informasi dan pendaftaran janji temu digital untuk **RS Gunung Maria Tomohon**. Dilengkapi dengan antarmuka publik, manajemen jadwal dokter dinamis, dan dashboard admin backend yang lengkap.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-092e20.svg)](https://www.djangoproject.com/)
[![MySQL](https://img.shields.io/badge/Database-MySQL-4479A1.svg)](https://www.mysql.com/)
[![Bootstrap](https://img.shields.io/badge/UI-Bootstrap%205.3-7952B3.svg)](https://getbootstrap.com/)

---

## Fitur

### Website Publik
- Halaman beranda, tentang, layanan, dan mitra
- Daftar dokter dengan filter poli dan hari praktik
- Halaman profil dokter dengan jadwal mingguan
- Formulir pendaftaran janji temu online dengan kalender interaktif
- Pemilihan dokter otomatis berdasarkan departemen (AJAX)
- Formulir kontak

### Dashboard Admin (`/dashboard/`)
- Login & logout dengan proteksi `is_staff`
- Statistik ringkas (total pasien, dokter, janji temu, pending)
- Manajemen janji temu: tambah, edit, ubah status, hapus (dengan undo toast)
- Manajemen pasien: tambah, edit
- Manajemen dokter: tambah, edit, hapus, beserta jadwal praktik inline
- Manajemen poli / departemen
- Daftar pesan kontak masuk dengan modal detail
- Sistem toast notifikasi bertumpuk (maks. 3) dengan fitur undo hapus 7 detik

---

## Tech Stack

| Komponen | Teknologi |
|---|---|
| Backend | Python 3.11+, Django 5.x |
| Database | MySQL 8.x |
| Frontend | Bootstrap 5.3.3, Bootstrap Icons 1.11.3 |
| Image processing | Pillow |
| DB connector | mysqlclient |
| Config | python-dotenv |

---

## Prasyarat

Pastikan hal berikut sudah terinstal sebelum setup:

- **Python 3.11+** — [python.org/downloads](https://www.python.org/downloads/)
- **MySQL 8.x** — via [Laragon](https://laragon.org/) (Windows, direkomendasikan), XAMPP, atau MySQL Community Server
- **Git** — [git-scm.com](https://git-scm.com/)
- **pip** — sudah termasuk dalam instalasi Python modern

> **Catatan Windows:** Gunakan Laragon untuk MySQL. Pastikan service MySQL sudah berjalan sebelum menjalankan server Django.

---

## Setup & Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/B4ks0/rsgmt.git
cd rsgmt
```

### 2. Buat Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

Pastikan prompt terminal berubah menjadi `(venv)` sebelum melanjutkan.

### 3. Install Dependensi Python

```bash
pip install -r requirements.txt
```

Paket yang akan terinstal:
- `Django>=4.2,<6.1`
- `Pillow>=10.0.0`
- `mysqlclient>=2.2.0`
- `python-dotenv>=1.0.0`

> **Windows:** Jika `mysqlclient` gagal build, install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) terlebih dahulu, atau pastikan MySQL sudah terinstal via Laragon.

### 4. Konfigurasi Environment (.env)

Salin file contoh:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Buka `.env` dan isi sesuai lingkungan lokal:

```env
# Database
DB_NAME=rsgumato
DB_USER=root
DB_PASSWORD=           # kosongkan jika MySQL tidak pakai password (default Laragon)
DB_HOST=127.0.0.1
DB_PORT=3306

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Generate SECRET_KEY baru (wajib di production):**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Buat Database MySQL

Buka MySQL client (Laragon → HeidiSQL, phpMyAdmin, atau command line):

```sql
CREATE DATABASE rsgumato CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Jalankan Migrasi

```bash
python manage.py migrate
```

Output yang diharapkan:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, hospital, sessions
Running migrations:
  Applying hospital.0001_initial... OK
  ...
  Applying hospital.0008_appointment_is_new_patient... OK
```

### 7. Import Data Awal (Opsional)

Jika tersedia file `hospital_data.json` (data dokter, jadwal, departemen):

```bash
python manage.py loaddata hospital_data.json
```

Atau gunakan seed script bawaan:

```bash
python seed.py
```

### 8. Buat Akun Admin

```bash
python manage.py createsuperuser
```

Masukkan username, email (opsional), dan password. Akun ini digunakan untuk login ke `/dashboard/login/`.

> Akun harus memiliki `is_staff = True` untuk dapat mengakses backend dashboard. Superuser otomatis memiliki akses penuh.

Untuk menambah akun staff biasa (bukan superuser):

```bash
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.create_user('namauser', password='passwordkuat')
u.is_staff = True
u.save()
print('Akun staff berhasil dibuat.')
"
```

### 9. Kumpulkan Static Files (Production)

```bash
python manage.py collectstatic
```

### 10. Jalankan Server Development

```bash
python manage.py runserver
```

Akses aplikasi di:

| URL | Keterangan |
|---|---|
| `http://127.0.0.1:8000/` | Halaman publik |
| `http://127.0.0.1:8000/dashboard/login/` | Login admin |
| `http://127.0.0.1:8000/dashboard/` | Dashboard admin (perlu login) |

---

## Struktur Direktori

```
rsgmt/
├── config/                        # Konfigurasi Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── hospital/                      # Aplikasi utama
│   ├── migrations/                # Migrasi database (0001–0008)
│   ├── models.py                  # Model: Doctor, Patient, Appointment, dll.
│   ├── views.py                   # Semua view (publik + backend admin)
│   ├── forms.py                   # Form: AppointmentForm, BackendDoctorForm, dll.
│   └── urls.py                    # URL routing lengkap
├── templates/
│   └── hospital/
│       ├── home.html              # Beranda
│       ├── appointment_form.html  # Formulir janji temu publik
│       ├── doctors.html           # Daftar dokter
│       ├── doctor_detail.html     # Profil dokter
│       ├── about.html
│       ├── services.html
│       ├── mitra_list.html
│       └── backend/               # Template dashboard admin
│           ├── base_backend.html  # Base template + sidebar + toast system
│           ├── dashboard.html     # Dashboard utama dengan live poll
│           ├── doctor_form.html   # Form dokter + jadwal inline + crop foto
│           ├── patient_form.html
│           ├── department_form.html
│           ├── appointment_form.html
│           ├── generic_list.html  # Tabel generik (dokter, pasien, poli)
│           ├── contact_list.html  # Pesan kontak + modal detail
│           ├── login.html
│           └── includes/
│               └── _sidebar.html
├── static/
│   └── hospital/
│       ├── css/site.css           # CSS kustom frontend
│       ├── img/                   # Gambar statis
│       └── img/kerjasama/        # Logo mitra
├── media/                         # Upload runtime (foto dokter, KTP)
├── slideshow/                     # Gambar slideshow beranda (1.png – N.png)
├── .env.example                   # Template environment
├── requirements.txt               # Dependensi Python
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── seed.py                        # Script seed data
```

---

## URL Endpoints

### Publik

| URL | Keterangan |
|---|---|
| `GET /` | Beranda |
| `GET /about/` | Tentang RS |
| `GET /services/` | Layanan |
| `GET /mitra/` | Mitra kerja sama |
| `GET /doctors/` | Daftar dokter (filter poli & hari) |
| `GET /doctors/<uuid>/` | Profil & jadwal dokter |
| `GET/POST /appointments/` | Pendaftaran janji temu |

### API (AJAX)

| URL | Method | Keterangan |
|---|---|---|
| `/api/submit-contact/` | `POST` | Kirim pesan kontak |
| `/api/get-doctors-by-dept/?department_id=` | `GET` | Dokter berdasarkan poli |
| `/api/get-doctor-available-dates/?doctor_id=` | `GET` | Tanggal praktik 60 hari ke depan |

### Backend Admin

| URL | Keterangan |
|---|---|
| `/dashboard/login/` | Login |
| `/dashboard/logout/` | Logout |
| `/dashboard/` | Dashboard utama |
| `/dashboard/patients/` | Kelola pasien |
| `/dashboard/patients/add/` | Tambah pasien |
| `/dashboard/patients/<uuid>/edit/` | Edit pasien |
| `/dashboard/doctors/` | Kelola dokter |
| `/dashboard/doctors/add/` | Tambah dokter + jadwal |
| `/dashboard/doctors/<uuid>/edit/` | Edit dokter + jadwal |
| `/dashboard/doctors/<uuid>/delete/` | Hapus dokter |
| `/dashboard/departments/` | Kelola poli |
| `/dashboard/departments/add/` | Tambah poli |
| `/dashboard/departments/<id>/edit/` | Edit poli + daftar dokter |
| `/dashboard/appointments/add/` | Tambah janji temu |
| `/dashboard/appointments/<uuid>/edit/` | Edit janji temu |
| `/dashboard/appointments/<uuid>/delete/` | Hapus janji temu |
| `/dashboard/contacts/` | Pesan kontak masuk |
| `/dashboard/contacts/<id>/detail/` | Detail pesan (JSON, untuk modal) |
| `/dashboard/payments/` | Info pembayaran |

---

## Skema Database

```
Specialization ──< Doctor >── Department
                      │
                 DoctorSchedule
                 ScheduleException

Patient ──< Appointment >── Doctor
                │               └── Department
                ├── Payment
                ├── Notification
                └── Review

ContactMessage  (independen)
```

### Model Utama

| Model | PK | Keterangan |
|---|---|---|
| `Department` | Auto int | Poli / departemen |
| `Specialization` | Auto int | Spesialisasi dokter |
| `Doctor` | UUID | Profil dokter, foto, aktif/tidak |
| `DoctorSchedule` | UUID | Jadwal praktik per hari (0=Senin … 6=Minggu) |
| `ScheduleException` | UUID | Override tanggal (libur / jadwal khusus) |
| `Patient` | UUID | Data pasien |
| `Appointment` | UUID | Janji temu, status: `requested/confirmed/completed/cancelled` |
| `Payment` | UUID | Catatan pembayaran per janji temu |
| `ContactMessage` | Auto int | Pesan dari formulir kontak publik |

---

## Deployment dengan Docker

```bash
docker-compose up --build
```

Docker Compose akan otomatis:
1. Membangun container Python + Django
2. Menjalankan container MySQL
3. Menjalankan migrasi database
4. Mengimpor `hospital_data.json` jika tersedia
5. Menjalankan server di port `8000`

Akses di `http://localhost:8000`.

---

## Troubleshooting

### `OperationalError: (2002, "Can't connect to server on '127.0.0.1'")`
MySQL belum berjalan. Buka Laragon / XAMPP → klik **Start All** atau start MySQL secara manual.

### `ModuleNotFoundError: No module named 'MySQLdb'`
```bash
pip install mysqlclient
```
Jika gagal build di Windows, install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

### `ImproperlyConfigured: The SECRET_KEY setting must not be empty`
File `.env` belum dibuat atau `SECRET_KEY` masih placeholder. Ikuti kembali langkah 4.

### Static files tidak muncul di browser
Pastikan `DEBUG=True` di `.env`. Django melayani static files secara otomatis saat mode development.

### Upload foto dokter tidak tersimpan
Pastikan direktori `media/` ada dan bisa ditulis:
```bash
mkdir media
```

### Migrasi gagal: `Table already exists`
```bash
python manage.py migrate --fake-initial
```

### Akses dashboard ditolak meski sudah login
Pastikan akun yang digunakan memiliki `is_staff = True`:
```bash
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.get(username='namauser')
u.is_staff = True
u.save()
print('is_staff diaktifkan.')
"
```

---

## Kontribusi

1. Fork repository
2. Buat branch fitur: `git checkout -b feature/nama-fitur`
3. Commit perubahan: `git commit -m "feat: deskripsi singkat"`
4. Push ke branch: `git push origin feature/nama-fitur`
5. Buat Pull Request

---

## Lisensi

Sistem ini dikembangkan khusus untuk operasional **RS Gunung Maria Tomohon**, Sulawesi Utara, Indonesia.

---

*Developed for RS Gunung Maria Tomohon · Tomohon, Sulawesi Utara*
