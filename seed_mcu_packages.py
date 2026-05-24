import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from hospital.models import McuPackage


packages = [
    {
        "title": "Paket MCU Basic",
        "slug": "paket-mcu-basic",
        "excerpt": "Paket pemeriksaan dasar untuk memantau kondisi kesehatan umum secara praktis dan terarah.",
        "price_label": "Mulai Rp 350.000",
        "duration": "60-90 menit",
        "thumbnail_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=900&h=560&fit=crop&q=80",
        "content_image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=1100&h=650&fit=crop&q=80",
        "content": (
            "Paket MCU Basic dirancang untuk pasien yang ingin melakukan pemeriksaan kesehatan awal tanpa rangkaian tes yang terlalu panjang. "
            "Paket ini cocok untuk pemantauan rutin, kebutuhan administrasi sederhana, atau sebagai langkah awal mengenali kondisi tubuh.\n\n"
            "Hasil pemeriksaan dapat membantu dokter melihat gambaran umum kesehatan pasien dan memberi saran lanjutan bila ditemukan faktor risiko tertentu."
        ),
        "checklist": "Konsultasi dokter umum\nPemeriksaan tanda vital\nPemeriksaan fisik umum\nDarah rutin\nGula darah sewaktu\nAsam urat\nKolesterol total",
        "preparation": "Istirahat cukup sebelum pemeriksaan\nBawa identitas diri\nSampaikan obat yang sedang dikonsumsi\nDatang 15 menit sebelum jadwal",
        "order": 1,
        "is_featured": True,
        "is_published": True,
    },
    {
        "title": "Paket MCU Silver",
        "slug": "paket-mcu-silver",
        "excerpt": "Paket pemeriksaan lanjutan dengan cakupan laboratorium dan penilaian risiko metabolik yang lebih lengkap.",
        "price_label": "Mulai Rp 650.000",
        "duration": "90-120 menit",
        "thumbnail_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=900&h=560&fit=crop&q=80",
        "content_image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=1100&h=650&fit=crop&q=80",
        "content": (
            "Paket MCU Silver cocok untuk pasien dewasa yang ingin pemeriksaan lebih menyeluruh dibanding paket dasar. "
            "Rangkaian tes membantu memantau fungsi tubuh, kadar gula, profil lemak, dan kondisi umum yang sering berkaitan dengan gaya hidup.\n\n"
            "Paket ini dapat menjadi pilihan untuk pemeriksaan tahunan, terutama bagi pasien dengan aktivitas kerja padat atau riwayat keluarga penyakit kronis."
        ),
        "checklist": "Konsultasi dokter umum\nPemeriksaan fisik umum\nDarah rutin lengkap\nGula darah puasa\nKolesterol total, HDL, LDL, trigliserida\nFungsi hati sederhana\nFungsi ginjal sederhana\nUrinalisis",
        "preparation": "Puasa 8-10 jam bila pemeriksaan dijadwalkan pagi\nMinum air putih tetap diperbolehkan\nHindari olahraga berat sehari sebelumnya\nBawa hasil pemeriksaan lama bila ada",
        "order": 2,
        "is_featured": False,
        "is_published": True,
    },
    {
        "title": "Paket MCU Gold",
        "slug": "paket-mcu-gold",
        "excerpt": "Paket komprehensif untuk evaluasi kesehatan tahunan dengan tambahan pemeriksaan jantung dan rontgen.",
        "price_label": "Mulai Rp 1.250.000",
        "duration": "2-3 jam",
        "thumbnail_url": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=900&h=560&fit=crop&q=80",
        "content_image_url": "https://images.unsplash.com/photo-1511174511562-5f97f4f4e0c8?w=1100&h=650&fit=crop&q=80",
        "content": (
            "Paket MCU Gold memberi gambaran kesehatan yang lebih luas melalui kombinasi konsultasi dokter, laboratorium, pemeriksaan urine, rontgen, dan rekam jantung. "
            "Paket ini cocok untuk pemeriksaan berkala perusahaan maupun individu yang ingin evaluasi tahunan lebih lengkap.\n\n"
            "Dokter akan membantu membaca hasil pemeriksaan dan memberi rekomendasi langkah berikutnya sesuai kondisi pasien."
        ),
        "checklist": "Konsultasi dokter umum\nPemeriksaan fisik lengkap\nDarah rutin lengkap\nGula darah puasa dan 2 jam PP\nProfil lipid lengkap\nFungsi hati\nFungsi ginjal\nUrinalisis\nFoto thorax\nEKG",
        "preparation": "Puasa 8-10 jam sebelum pemeriksaan\nGunakan pakaian nyaman\nHindari kafein sebelum EKG\nBawa daftar obat rutin dan riwayat alergi",
        "order": 3,
        "is_featured": False,
        "is_published": True,
    },
    {
        "title": "Paket MCU Eksekutif",
        "slug": "paket-mcu-eksekutif",
        "excerpt": "Paket pemeriksaan premium untuk pemantauan kesehatan menyeluruh dengan alur layanan lebih personal.",
        "price_label": "Mulai Rp 2.100.000",
        "duration": "3-4 jam",
        "thumbnail_url": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=900&h=560&fit=crop&q=80",
        "content_image_url": "https://images.unsplash.com/photo-1551076805-e1869033e561?w=1100&h=650&fit=crop&q=80",
        "content": (
            "Paket MCU Eksekutif disiapkan untuk pasien yang membutuhkan evaluasi lebih menyeluruh dengan kenyamanan alur pemeriksaan yang lebih personal. "
            "Paket ini menggabungkan pemeriksaan laboratorium lengkap, evaluasi jantung, radiologi, dan konsultasi dokter.\n\n"
            "Rangkaian pemeriksaan dapat membantu mengenali risiko penyakit tidak menular sejak dini sehingga pasien dapat mengambil langkah pencegahan yang tepat."
        ),
        "checklist": "Konsultasi dokter umum\nPemeriksaan fisik lengkap\nDarah rutin lengkap\nProfil lipid lengkap\nFungsi hati lengkap\nFungsi ginjal lengkap\nGula darah puasa dan HbA1c\nUrinalisis\nFoto thorax\nEKG\nUSG abdomen",
        "preparation": "Puasa 8-10 jam sebelum pemeriksaan\nMinum air putih cukup untuk persiapan urine dan USG\nGunakan pakaian dua bagian yang nyaman\nKonfirmasi jadwal minimal satu hari sebelumnya",
        "order": 4,
        "is_featured": False,
        "is_published": True,
    },
]


created = 0
updated = 0
for data in packages:
    obj, is_new = McuPackage.objects.update_or_create(slug=data["slug"], defaults=data)
    if is_new:
        created += 1
        print(f"  [+] {obj.title}")
    else:
        updated += 1
        print(f"  [=] diperbarui: {obj.title}")

print(f"\nSelesai: {created} paket baru, {updated} paket diperbarui, total seed {len(packages)}.")
