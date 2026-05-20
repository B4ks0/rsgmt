import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from hospital.models import Article

articles = [
    {
        'title': 'Hipertensi: Mengenal Si Pembunuh Senyap dan Cara Mencegahnya',
        'slug': 'hipertensi-mengenal-si-pembunuh-senyap',
        'thumbnail_url': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800&h=500&fit=crop&q=80',
        'content': (
            'Hipertensi atau tekanan darah tinggi adalah kondisi ketika tekanan darah di arteri secara persisten berada di atas 130/80 mmHg. '
            'Penyakit ini sering disebut "silent killer" karena mayoritas penderitanya tidak merasakan gejala apa pun, '
            'namun kerusakan pada organ tubuh terus berlangsung secara diam-diam.\n\n'
            'Penyebab hipertensi terbagi menjadi dua jenis. Hipertensi primer tidak memiliki penyebab yang jelas dan berkembang perlahan selama bertahun-tahun. '
            'Sementara hipertensi sekunder dipicu oleh kondisi tertentu seperti penyakit ginjal, gangguan tiroid, atau efek samping obat-obatan tertentu.\n\n'
            'Faktor risiko yang paling umum meliputi usia di atas 40 tahun, riwayat keluarga dengan hipertensi, kegemukan, kurang aktivitas fisik, '
            'konsumsi garam berlebihan, merokok, dan stres kronis. Pola makan tinggi natrium juga menjadi kontributor utama meningkatnya tekanan darah.\n\n'
            'Untuk mencegah dan mengendalikan hipertensi, dokter menyarankan perubahan gaya hidup secara menyeluruh. Kurangi asupan garam hingga di bawah 5 gram per hari, '
            'perbanyak konsumsi buah dan sayuran, rutin berolahraga minimal 30 menit sehari, batasi konsumsi alkohol, dan berhenti merokok.\n\n'
            'Jika tekanan darah tidak dapat dikendalikan hanya dengan perubahan gaya hidup, dokter akan meresepkan obat antihipertensi. '
            'Penting untuk tidak menghentikan konsumsi obat tanpa seizin dokter meskipun tekanan darah sudah terasa normal.'
        ),
        'is_published': True,
    },
    {
        'title': 'Diabetes Melitus: Gejala, Penyebab, dan Cara Pengelolaannya',
        'slug': 'diabetes-melitus-gejala-penyebab-pengelolaan',
        'thumbnail_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=500&fit=crop&q=80',
        'content': (
            'Diabetes melitus adalah penyakit metabolik kronis yang ditandai dengan kadar gula darah tinggi akibat tubuh tidak dapat memproduksi atau menggunakan insulin secara efektif. '
            'Di Indonesia, jumlah penderita diabetes terus meningkat setiap tahunnya dan menjadi salah satu beban kesehatan terbesar.\n\n'
            'Terdapat tiga jenis utama diabetes. Diabetes tipe 1 terjadi ketika sistem imun menyerang sel penghasil insulin di pankreas. '
            'Diabetes tipe 2 yang paling umum terjadi karena resistensi insulin dan sering berkaitan dengan gaya hidup. '
            'Diabetes gestasional muncul selama kehamilan dan umumnya hilang setelah melahirkan.\n\n'
            'Gejala umum diabetes meliputi sering buang air kecil terutama malam hari, rasa haus yang berlebihan, penurunan berat badan tanpa sebab jelas, '
            'mudah lelah, penglihatan kabur, dan luka yang sulit sembuh. Pada diabetes tipe 2, gejala sering muncul perlahan.\n\n'
            'Pengelolaan diabetes mencakup pemantauan kadar gula darah secara rutin, pola makan sehat rendah gula dan karbohidrat sederhana, '
            'olahraga teratur, dan konsumsi obat atau insulin sesuai anjuran dokter.\n\n'
            'Komplikasi diabetes yang tidak terkontrol dapat berdampak serius pada ginjal, mata, saraf, dan jantung. '
            'Oleh karena itu, pemeriksaan rutin dan kepatuhan terhadap rencana pengobatan sangat penting untuk menjaga kualitas hidup penderita diabetes.'
        ),
        'is_published': True,
    },
    {
        'title': '5 Kebiasaan Sehat untuk Menjaga Kesehatan Jantung Anda',
        'slug': '5-kebiasaan-sehat-menjaga-kesehatan-jantung',
        'thumbnail_url': 'https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800&h=500&fit=crop&q=80',
        'content': (
            'Jantung adalah organ vital yang bekerja tanpa henti sepanjang hidup kita. Menjaga kesehatan jantung bukan hanya tentang menghindari penyakit, '
            'tetapi tentang membangun kebiasaan hidup yang mendukung fungsi jantung secara optimal sejak dini.\n\n'
            'Pertama, rutin berolahraga aerobik. Olahraga seperti jalan cepat, bersepeda, berenang, atau jogging selama minimal 150 menit per minggu '
            'terbukti meningkatkan efisiensi kerja jantung, menurunkan tekanan darah, dan memperbaiki kadar kolesterol.\n\n'
            'Kedua, konsumsi makanan ramah jantung. Perbanyak asupan ikan berlemak seperti salmon dan sarden yang kaya omega-3, sayuran hijau, '
            'buah-buahan, kacang-kacangan, dan biji-bijian utuh. Kurangi makanan tinggi lemak jenuh, garam, dan gula tambahan.\n\n'
            'Ketiga, berhenti merokok. Merokok merusak dinding pembuluh darah, meningkatkan tekanan darah, dan menurunkan kadar oksigen dalam darah. '
            'Risiko penyakit jantung pada perokok dua hingga empat kali lebih tinggi dibandingkan yang tidak merokok.\n\n'
            'Keempat, kelola stres dengan baik. Stres kronis meningkatkan hormon kortisol yang berdampak buruk pada jantung. '
            'Meditasi, yoga, dan hobi yang menyenangkan adalah cara efektif mengelola stres sehari-hari.\n\n'
            'Kelima, lakukan pemeriksaan kesehatan rutin. Cek tekanan darah, kadar kolesterol, dan gula darah secara berkala meski tidak ada keluhan. '
            'Deteksi dini faktor risiko memungkinkan penanganan lebih awal sebelum berkembang menjadi penyakit jantung yang serius.'
        ),
        'is_published': True,
    },
    {
        'title': 'Manfaat Olahraga Rutin bagi Kesehatan Fisik dan Mental',
        'slug': 'manfaat-olahraga-rutin-kesehatan-fisik-mental',
        'thumbnail_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=500&fit=crop&q=80',
        'content': (
            'Olahraga bukan sekadar aktivitas untuk membentuk tubuh ideal. Penelitian ilmiah telah membuktikan bahwa berolahraga secara rutin '
            'memberikan manfaat luar biasa bagi kesehatan fisik maupun mental yang sering kali melampaui ekspektasi banyak orang.\n\n'
            'Dari sisi fisik, olahraga memperkuat otot dan tulang, meningkatkan kapasitas paru-paru, memperbaiki sirkulasi darah, '
            'dan membantu mengontrol berat badan. Aktivitas fisik juga meningkatkan sensitivitas insulin dan memperkuat sistem imun.\n\n'
            'Manfaat olahraga bagi kesehatan mental tidak kalah signifikan. Saat berolahraga, otak melepaskan endorfin, serotonin, dan dopamin '
            'yang dikenal sebagai hormon kebahagiaan. Penelitian menunjukkan olahraga rutin efektif mengurangi gejala depresi dan kecemasan.\n\n'
            'Tidak perlu olahraga berat untuk mendapatkan manfaat tersebut. Berjalan kaki 30 menit sehari, bersepeda santai, atau melakukan peregangan ringan '
            'sudah cukup untuk memulai. Yang terpenting adalah konsistensi.\n\n'
            'Untuk membangun kebiasaan olahraga, mulailah dengan aktivitas yang Anda nikmati, tetapkan jadwal yang realistis, '
            'dan ajak teman atau keluarga agar lebih menyenangkan. Dalam 21 hari, olahraga akan menjadi kebiasaan yang sulit ditinggalkan.'
        ),
        'is_published': True,
    },
    {
        'title': 'Pentingnya Tidur Berkualitas untuk Kesehatan Optimal',
        'slug': 'pentingnya-tidur-berkualitas-kesehatan-optimal',
        'thumbnail_url': 'https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=800&h=500&fit=crop&q=80',
        'content': (
            'Di era modern yang serba sibuk, tidur sering menjadi yang pertama dikorbankan. Padahal, tidur berkualitas adalah fondasi kesehatan '
            'yang tidak bisa digantikan oleh suplemen atau gaya hidup sehat lainnya. Saat tidur, tubuh menjalankan proses pemulihan dan regenerasi yang krusial.\n\n'
            'Selama tidur, otak memproses dan mengonsolidasi memori yang dipelajari sepanjang hari. Sistem imun memperkuat pertahanannya '
            'dengan memproduksi sitokin yang melawan infeksi dan peradangan. Tubuh juga melepaskan hormon pertumbuhan yang memperbaiki jaringan.\n\n'
            'Kurang tidur dalam jangka panjang meningkatkan risiko obesitas, diabetes, penyakit jantung, hipertensi, dan gangguan kesehatan mental. '
            'Orang yang tidur kurang dari 6 jam per malam memiliki risiko lebih tinggi mengalami berbagai penyakit kronis.\n\n'
            'Untuk meningkatkan kualitas tidur, terapkan rutinitas tidur yang konsisten. Tidur dan bangun pada jam yang sama setiap hari. '
            'Ciptakan lingkungan tidur yang gelap, sejuk, dan tenang. Hindari layar gadget minimal satu jam sebelum tidur.\n\n'
            'Orang dewasa membutuhkan 7-9 jam tidur per malam. Jika Anda sering mengantuk di siang hari atau sulit berkonsentrasi, '
            'konsultasikan dengan dokter karena bisa jadi ada gangguan tidur seperti insomnia atau sleep apnea yang perlu ditangani.'
        ),
        'is_published': True,
    },
    {
        'title': 'Panduan Gizi Seimbang untuk Hidup Sehat Setiap Hari',
        'slug': 'panduan-gizi-seimbang-hidup-sehat',
        'thumbnail_url': 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800&h=500&fit=crop&q=80',
        'content': (
            'Gizi seimbang adalah pola makan yang mengandung semua zat gizi yang dibutuhkan tubuh dalam jumlah yang tepat. '
            'Konsep ini kini dikenal dengan pedoman Isi Piringku yang dikeluarkan oleh Kementerian Kesehatan RI.\n\n'
            'Setengah piring sebaiknya diisi dengan sayur dan buah-buahan yang mengandung vitamin, mineral, serat, dan antioksidan. '
            'Pilihlah beragam warna sayur dan buah untuk mendapatkan variasi nutrisi yang optimal.\n\n'
            'Seperempat piring diisi dengan karbohidrat kompleks seperti nasi merah, ubi, kentang, jagung, atau roti gandum utuh. '
            'Karbohidrat kompleks dicerna lebih lambat sehingga membuat kenyang lebih lama dan tidak menyebabkan lonjakan gula darah yang drastis.\n\n'
            'Seperempat piring sisanya diisi dengan sumber protein hewani maupun nabati seperti ikan, ayam tanpa kulit, telur, tahu, tempe, dan kacang-kacangan. '
            'Protein berperan penting dalam pembentukan otot, produksi enzim dan hormon, serta perbaikan sel-sel tubuh.\n\n'
            'Jangan lupa minum air putih minimal 8 gelas atau 2 liter per hari. Batasi minuman manis, soda, dan jus kemasan yang tinggi gula. '
            'Membatasi gula, garam, dan lemak jahat adalah kunci utama pola makan sehat yang berkelanjutan.'
        ),
        'is_published': True,
    },
    {
        'title': 'Menjaga Kesehatan Mental di Tengah Kesibukan Modern',
        'slug': 'menjaga-kesehatan-mental-kesibukan-modern',
        'thumbnail_url': 'https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=800&h=500&fit=crop&q=80',
        'content': (
            'Kesehatan mental adalah komponen fundamental dari kesehatan secara keseluruhan, namun masih sering diabaikan atau bahkan dianggap tabu. '
            'Padahal, WHO mendefinisikan kesehatan sebagai keadaan sejahtera fisik, mental, dan sosial, bukan hanya bebas dari penyakit.\n\n'
            'Kehidupan modern membawa tekanan tersendiri. Tuntutan pekerjaan, persaingan sosial media, dan berbagai tanggung jawab '
            'dapat terakumulasi menjadi stres kronis yang jika tidak dikelola dapat berkembang menjadi gangguan kecemasan, depresi, atau burnout.\n\n'
            'Beberapa langkah sederhana yang terbukti efektif menjaga kesehatan mental adalah menetapkan batasan yang sehat antara pekerjaan dan waktu pribadi, '
            'meluangkan waktu untuk aktivitas yang Anda nikmati, dan menjaga hubungan sosial yang bermakna.\n\n'
            'Praktik mindfulness dan meditasi telah mendapatkan banyak dukungan ilmiah sebagai cara efektif mengurangi kecemasan. '
            'Cukup 10-15 menit sehari untuk duduk diam dan fokus pada pernapasan dapat membuat perbedaan signifikan dalam jangka panjang.\n\n'
            'Jangan ragu untuk mencari bantuan profesional jika Anda merasa kewalahan. Psikolog dan psikiater adalah tenaga medis terlatih yang siap membantu. '
            'Mencari bantuan bukan tanda kelemahan, melainkan tanda keberanian dan kepedulian terhadap diri sendiri.'
        ),
        'is_published': True,
    },
    {
        'title': 'Kolesterol Tinggi: Bahaya, Gejala, dan Cara Mengatasinya',
        'slug': 'kolesterol-tinggi-bahaya-gejala-cara-mengatasi',
        'thumbnail_url': 'https://images.unsplash.com/photo-1532938911079-1bb14698d8f4?w=800&h=500&fit=crop&q=80',
        'content': (
            'Kolesterol adalah zat lemak alami yang diproduksi oleh hati dan juga diperoleh dari makanan. '
            'Tubuh membutuhkan kolesterol untuk membangun sel dan memproduksi hormon. Namun kadar yang terlalu tinggi dapat menjadi ancaman serius bagi kesehatan.\n\n'
            'Terdapat dua jenis kolesterol utama: LDL atau kolesterol jahat yang dapat menumpuk di dinding arteri, '
            'dan HDL atau kolesterol baik yang membantu mengangkut kolesterol berlebih kembali ke hati untuk dibuang.\n\n'
            'Kolesterol tinggi umumnya tidak menimbulkan gejala yang terasa hingga terjadi komplikasi serius. '
            'Inilah mengapa pemeriksaan kadar kolesterol secara rutin sangat penting, terutama bagi mereka yang berusia di atas 35 tahun.\n\n'
            'Perubahan gaya hidup adalah langkah pertama dalam mengatasi kolesterol tinggi. Kurangi makanan tinggi lemak jenuh dan lemak trans. '
            'Perbanyak konsumsi serat larut dari oat, kacang-kacangan, apel, dan pir yang terbukti membantu menurunkan kadar LDL.\n\n'
            'Jika perubahan gaya hidup tidak cukup, dokter dapat meresepkan obat penurun kolesterol seperti statin. '
            'Dengan penanganan yang tepat, kolesterol tinggi dapat dikendalikan dan risiko komplikasi dapat diminimalkan secara signifikan.'
        ),
        'is_published': True,
    },
    {
        'title': 'Vaksinasi Dewasa: Mengapa Imunisasi Tidak Hanya untuk Anak-anak',
        'slug': 'vaksinasi-dewasa-imunisasi-bukan-hanya-anak',
        'thumbnail_url': 'https://images.unsplash.com/photo-1607619056574-7b8d3ee536b2?w=800&h=500&fit=crop&q=80',
        'content': (
            'Banyak orang beranggapan bahwa vaksinasi hanya diperlukan oleh bayi dan anak-anak. Padahal, orang dewasa juga membutuhkan vaksin '
            'untuk melindungi diri dari berbagai penyakit infeksi, terutama seiring bertambahnya usia ketika sistem imun mulai melemah.\n\n'
            'Beberapa vaksin yang direkomendasikan untuk orang dewasa antara lain vaksin influenza yang sebaiknya diberikan setiap tahun, '
            'vaksin pneumonia untuk usia di atas 65 tahun, vaksin hepatitis B dan A, vaksin HPV untuk wanita, serta booster tetanus setiap 10 tahun.\n\n'
            'Vaksinasi dewasa penting karena kekebalan dari vaksin masa kecil dapat memudar seiring waktu. '
            'Kondisi medis tertentu seperti diabetes atau penyakit jantung juga meningkatkan kerentanan terhadap infeksi serius.\n\n'
            'Vaksin bekerja dengan cara memperkenalkan antigen kepada sistem imun tanpa menyebabkan sakit. '
            'Sistem imun kemudian mempelajari cara melawan kuman tersebut sehingga ketika terpapar penyakit sebenarnya, tubuh sudah siap melawan.\n\n'
            'Keamanan vaksin telah melalui serangkaian uji klinis ketat sebelum disetujui. Efek samping yang umum seperti nyeri di tempat suntikan '
            'atau demam ringan umumnya hanya berlangsung 1-2 hari dan jauh lebih ringan dibandingkan dampak penyakit yang dicegah.'
        ),
        'is_published': True,
    },
    {
        'title': 'Mengenali Gejala Stroke dan Langkah Pertolongan Pertama yang Tepat',
        'slug': 'mengenali-gejala-stroke-pertolongan-pertama',
        'thumbnail_url': 'https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=800&h=500&fit=crop&q=80',
        'content': (
            'Stroke adalah kondisi darurat medis yang terjadi ketika aliran darah ke otak terganggu, baik karena penyumbatan pembuluh darah '
            'maupun pecahnya pembuluh darah. Setiap menit sangat berharga karena sel-sel otak mati dengan cepat ketika kekurangan oksigen.\n\n'
            'Mengenali gejala stroke sejak dini adalah kunci penyelamatan jiwa. Gunakan metode FAST: Face (wajah turun sebelah), '
            'Arms (satu lengan lemah atau sulit diangkat), Speech (bicara pelo atau tidak jelas), Time (segera hubungi layanan darurat).\n\n'
            'Jika Anda menyaksikan seseorang mengalami gejala-gejala tersebut, segera bawa ke rumah sakit terdekat secepat mungkin. '
            'Jangan menunggu gejalanya mereda sendiri karena penanganan yang terlambat dapat menyebabkan kerusakan otak permanen.\n\n'
            'Faktor risiko stroke yang dapat dimodifikasi meliputi hipertensi, merokok, diabetes, kolesterol tinggi, obesitas, dan kurang olahraga. '
            'Hipertensi adalah faktor risiko terbesar stroke, sehingga menjaga tekanan darah dalam batas normal adalah pencegahan paling efektif.\n\n'
            'Setelah sembuh dari stroke, sebagian besar pasien memerlukan rehabilitasi intensif yang mencakup fisioterapi, terapi wicara, '
            'dan terapi okupasi. Dukungan keluarga sangat menentukan seberapa jauh pemulihan yang dapat dicapai.'
        ),
        'is_published': True,
    },
]

created = 0
for data in articles:
    obj, is_new = Article.objects.get_or_create(slug=data['slug'], defaults=data)
    if is_new:
        created += 1
        print(f'  [+] {obj.title}')
    else:
        print(f'  [=] sudah ada: {obj.title}')

print(f'\nSelesai: {created} artikel baru dibuat dari {len(articles)} total.')
