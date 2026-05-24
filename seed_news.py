import os
from datetime import timedelta

import django
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from hospital.models import News


news_items = [
    {
        "title": "RS Gunung Maria Tomohon Tingkatkan Layanan Pendaftaran Rawat Jalan",
        "slug": "rs-gunung-maria-tingkatkan-layanan-pendaftaran-rawat-jalan",
        "excerpt": "Pendaftaran rawat jalan kini dibuat lebih tertata untuk membantu pasien mendapatkan pelayanan dengan lebih nyaman.",
        "thumbnail_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=900&h=560&fit=crop&q=80",
        "content_image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=1100&h=650&fit=crop&q=80",
        "content": (
            "RS Gunung Maria Tomohon terus melakukan penyesuaian layanan pendaftaran rawat jalan agar pasien dan keluarga dapat memperoleh alur pelayanan yang lebih jelas. "
            "Penguatan ini mencakup penataan meja informasi, pemutakhiran data pasien, serta koordinasi antarloket untuk mengurangi waktu tunggu.\n\n"
            "Tim pelayanan juga mengingatkan pasien untuk membawa identitas diri, kartu jaminan kesehatan bila ada, dan dokumen rujukan yang masih berlaku. "
            "Kelengkapan dokumen membantu petugas memverifikasi data dengan lebih cepat dan mengarahkan pasien ke poli tujuan.\n\n"
            "Manajemen rumah sakit berharap pembaruan alur ini dapat meningkatkan kenyamanan pasien, terutama pada jam kunjungan yang padat. "
            "Evaluasi layanan akan dilakukan berkala berdasarkan masukan pasien dan pengamatan petugas di lapangan."
        ),
        "days_ago": 0,
    },
    {
        "title": "Edukasi Cuci Tangan untuk Pengunjung dan Keluarga Pasien",
        "slug": "edukasi-cuci-tangan-untuk-pengunjung-dan-keluarga-pasien",
        "excerpt": "Kampanye kebersihan tangan digelar untuk memperkuat budaya pencegahan infeksi di lingkungan rumah sakit.",
        "thumbnail_url": "https://images.unsplash.com/photo-1584483766114-2cea6facdf57?w=900&h=560&fit=crop&q=80",
        "content_image_url": "https://images.unsplash.com/photo-1583947581924-860bda6a26df?w=1100&h=650&fit=crop&q=80",
        "content": (
            "Kebersihan tangan adalah langkah sederhana yang memiliki dampak besar dalam mencegah penyebaran kuman. "
            "Melalui edukasi singkat di area layanan, pengunjung dan keluarga pasien diajak memahami kapan harus mencuci tangan dan bagaimana melakukannya dengan benar.\n\n"
            "Petugas menjelaskan bahwa cuci tangan perlu dilakukan sebelum dan sesudah menyentuh pasien, setelah menggunakan toilet, setelah batuk atau bersin, serta sebelum makan. "
            "Selain air mengalir dan sabun, hand sanitizer berbasis alkohol juga dapat digunakan ketika tangan tidak tampak kotor.\n\n"
            "Rumah sakit mengajak seluruh pengunjung untuk ikut menjaga lingkungan perawatan tetap aman. "
            "Kedisiplinan kecil dari banyak orang dapat membantu melindungi pasien, tenaga kesehatan, dan keluarga yang mendampingi."
        ),
        "days_ago": 2,
    },
    {
        "title": "Pemeriksaan Tekanan Darah Rutin Bantu Deteksi Risiko Sejak Dini",
        "slug": "pemeriksaan-tekanan-darah-rutin-bantu-deteksi-risiko-sejak-dini",
        "excerpt": "Deteksi hipertensi sejak awal menjadi salah satu cara penting mencegah komplikasi jangka panjang.",
        "thumbnail_url": "https://images.unsplash.com/photo-1631815588090-d4bfec5b1ccb?w=900&h=560&fit=crop&q=80",
        "content_image_url": "https://images.unsplash.com/photo-1511174511562-5f97f4f4e0c8?w=1100&h=650&fit=crop&q=80",
        "content": (
            "Tekanan darah tinggi sering tidak menimbulkan gejala, tetapi dapat meningkatkan risiko penyakit jantung, stroke, dan gangguan ginjal. "
            "Karena itu, pemeriksaan tekanan darah secara rutin sangat dianjurkan, terutama bagi masyarakat dengan riwayat keluarga hipertensi atau usia di atas 40 tahun.\n\n"
            "Pasien dianjurkan beristirahat beberapa menit sebelum pemeriksaan, tidak merokok atau minum kopi sesaat sebelumnya, dan menyampaikan riwayat obat yang sedang dikonsumsi. "
            "Informasi tersebut membantu tenaga kesehatan membaca hasil pemeriksaan dengan lebih tepat.\n\n"
            "Selain pemeriksaan berkala, pola makan rendah garam, aktivitas fisik teratur, cukup tidur, dan berhenti merokok menjadi bagian penting dari pencegahan. "
            "Bila hasil tekanan darah berulang kali tinggi, pasien sebaiknya berkonsultasi dengan dokter."
        ),
        "days_ago": 4,
    },
    {
        "title": "Jadwal Poliklinik Diperbarui untuk Memudahkan Perencanaan Kunjungan",
        "slug": "jadwal-poliklinik-diperbarui-untuk-memudahkan-kunjungan",
        "excerpt": "Informasi jadwal praktik dokter diperbarui agar pasien dapat merencanakan kunjungan dengan lebih baik.",
        "thumbnail_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=900&h=560&fit=crop&q=80",
        "content_image_url": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=1100&h=650&fit=crop&q=80",
        "content": (
            "RS Gunung Maria Tomohon memperbarui informasi jadwal poliklinik sebagai bagian dari upaya meningkatkan keterbukaan informasi bagi pasien. "
            "Dengan jadwal yang lebih mudah diakses, pasien dapat memilih waktu kunjungan yang sesuai dan menyiapkan dokumen yang dibutuhkan.\n\n"
            "Perubahan jadwal dapat terjadi karena kegiatan pelayanan, kondisi darurat, atau penyesuaian internal. "
            "Pasien disarankan melakukan konfirmasi terlebih dahulu melalui kanal informasi rumah sakit sebelum datang, terutama untuk kunjungan yang membutuhkan persiapan khusus.\n\n"
            "Rumah sakit akan terus menyempurnakan penyampaian informasi agar pasien memperoleh pengalaman layanan yang lebih tertib, jelas, dan nyaman."
        ),
        "days_ago": 6,
    },
    {
        "title": "Peringatan Hari Kesehatan: Ajak Masyarakat Lebih Peduli Pemeriksaan Berkala",
        "slug": "peringatan-hari-kesehatan-ajak-masyarakat-peduli-pemeriksaan-berkala",
        "excerpt": "Pemeriksaan kesehatan berkala membantu menemukan faktor risiko sebelum berkembang menjadi penyakit serius.",
        "thumbnail_url": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=900&h=560&fit=crop&q=80",
        "content_image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=1100&h=650&fit=crop&q=80",
        "content": (
            "Dalam momentum peringatan hari kesehatan, masyarakat diajak untuk tidak menunggu sakit sebelum memeriksakan diri. "
            "Pemeriksaan berkala seperti tekanan darah, gula darah, kolesterol, dan indeks massa tubuh dapat membantu mengenali risiko sejak dini.\n\n"
            "Deteksi dini memberi peluang lebih besar untuk melakukan perubahan gaya hidup dan mendapatkan penanganan yang sesuai. "
            "Banyak penyakit kronis berkembang perlahan dan baru terasa ketika kondisi sudah lebih berat.\n\n"
            "Rumah sakit mendorong masyarakat untuk menjadikan pemeriksaan kesehatan sebagai bagian dari rutinitas, bukan sekadar respons saat keluhan muncul. "
            "Langkah pencegahan yang konsisten dapat membantu menjaga kualitas hidup dalam jangka panjang."
        ),
        "days_ago": 8,
    },
    {
        "title": "Kesiapsiagaan Instalasi Gawat Darurat Selama Periode Libur",
        "slug": "kesiapsiagaan-instalasi-gawat-darurat-selama-periode-libur",
        "excerpt": "IGD tetap bersiaga melayani kondisi kegawatdaruratan dengan koordinasi lintas unit selama periode libur.",
        "thumbnail_url": "https://images.unsplash.com/photo-1587351021759-3e566b6af7cc?w=900&h=560&fit=crop&q=80",
        "content_image_url": "https://images.unsplash.com/photo-1516549655169-df83a0774514?w=1100&h=650&fit=crop&q=80",
        "content": (
            "Instalasi Gawat Darurat RS Gunung Maria Tomohon tetap bersiaga melayani pasien yang membutuhkan penanganan segera selama periode libur. "
            "Koordinasi dilakukan antara tenaga medis, perawat, farmasi, laboratorium, dan unit pendukung lain agar respons pelayanan tetap berjalan baik.\n\n"
            "Masyarakat diimbau segera mencari pertolongan medis bila mengalami nyeri dada hebat, sesak napas berat, penurunan kesadaran, kelemahan anggota tubuh mendadak, perdarahan aktif, atau cedera serius. "
            "Kondisi tersebut memerlukan evaluasi cepat oleh tenaga kesehatan.\n\n"
            "Untuk keluhan ringan yang tidak bersifat darurat, pasien dapat memanfaatkan layanan poliklinik sesuai jadwal yang tersedia. "
            "Pemilahan layanan membantu IGD fokus pada kasus yang benar-benar membutuhkan penanganan segera."
        ),
        "days_ago": 11,
    },
    {
        "title": "Layanan Informasi Pasien Diperkuat Lewat Kanal Digital Rumah Sakit",
        "slug": "layanan-informasi-pasien-diperkuat-lewat-kanal-digital-rumah-sakit",
        "excerpt": "Kanal digital membantu pasien memperoleh informasi umum rumah sakit dengan lebih cepat dan praktis.",
        "thumbnail_url": "https://images.unsplash.com/photo-1577563908411-5077b6dc7624?w=900&h=560&fit=crop&q=80",
        "content_image_url": "https://images.unsplash.com/photo-1551434678-e076c223a692?w=1100&h=650&fit=crop&q=80",
        "content": (
            "RS Gunung Maria Tomohon memperkuat layanan informasi melalui kanal digital agar masyarakat lebih mudah mendapatkan informasi umum seperti jadwal, layanan, dan pengumuman terbaru. "
            "Langkah ini menjadi bagian dari upaya menghadirkan komunikasi yang lebih cepat dan mudah dipahami.\n\n"
            "Pasien tetap dianjurkan melakukan konfirmasi langsung untuk informasi yang bersifat personal, administratif, atau membutuhkan verifikasi data. "
            "Hal ini penting untuk menjaga keamanan informasi dan memastikan jawaban yang diberikan sesuai kondisi pasien.\n\n"
            "Ke depan, pengembangan kanal digital akan terus disesuaikan dengan kebutuhan pengguna. "
            "Masukan dari pasien dan keluarga menjadi bahan penting dalam menyempurnakan layanan informasi rumah sakit."
        ),
        "days_ago": 14,
    },
    {
        "title": "Tim Gizi Ingatkan Pentingnya Sarapan Seimbang Sebelum Beraktivitas",
        "slug": "tim-gizi-ingatkan-pentingnya-sarapan-seimbang-sebelum-beraktivitas",
        "excerpt": "Sarapan dengan komposisi seimbang membantu menjaga energi, konsentrasi, dan kebiasaan makan yang lebih sehat.",
        "thumbnail_url": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=900&h=560&fit=crop&q=80",
        "content_image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=1100&h=650&fit=crop&q=80",
        "content": (
            "Sarapan sering dilewatkan karena aktivitas pagi yang padat, padahal asupan pertama hari itu membantu tubuh memperoleh energi untuk memulai kegiatan. "
            "Tim gizi mengingatkan bahwa sarapan seimbang tidak harus mahal atau rumit.\n\n"
            "Pilihan sarapan dapat terdiri dari sumber karbohidrat, protein, sayur atau buah, serta air putih yang cukup. "
            "Contohnya nasi dengan telur dan sayur, roti gandum dengan sumber protein, atau bubur dengan lauk yang tidak terlalu tinggi garam.\n\n"
            "Masyarakat juga dianjurkan membatasi minuman tinggi gula di pagi hari. "
            "Kebiasaan sederhana yang dilakukan konsisten dapat membantu menjaga berat badan, konsentrasi, dan kesehatan metabolik."
        ),
        "days_ago": 18,
    },
]


created = 0
updated = 0
now = timezone.now()

for item in news_items:
    days_ago = item.pop("days_ago")
    item["is_published"] = True
    obj, is_new = News.objects.update_or_create(slug=item["slug"], defaults=item)
    published_at = now - timedelta(days=days_ago)
    News.objects.filter(pk=obj.pk).update(created_at=published_at, updated_at=published_at)
    if is_new:
        created += 1
        print(f"  [+] {obj.title}")
    else:
        updated += 1
        print(f"  [=] diperbarui: {obj.title}")

print(f"\nSelesai: {created} berita baru, {updated} berita diperbarui, total seed {len(news_items)}.")
