import random


def generate_random_emoji():
    categories = [
        (0x1F600, 0x1F64F),  # wajah
        (0x1F300, 0x1F5FF),  # Simbol & Pictographs
        (0x1F680, 0x1F6FF),  # Transportasi & Simbol Transportasi
        (0x1F700, 0x1F77F),  # Alat & Simbol Teknikal
        (0x1F900, 0x1F9FF),  # Simbol Keagamaan & Rohani
        (0x1F4F0, 0x1F4FF),  # Simbol Kantor
        (0x1F320, 0x1F32F),  # Simbol Meteorologi
        (0x1F3E0, 0x1F3EF),  # Simbol Olahraga
        (0x1F600, 0x1F64F),  # Simbol Cinta & Perasaan
        (0x1F340, 0x1F35F),  # Simbol Makanan & Minuman
        (0x1F400, 0x1F4D3),  # Simbol Pustaka
        (0x1F4E0, 0x1F4E9),  # Simbol Media
        (0x1F500, 0x1F53D),  # Simbol Matematika & Ilmiah
        (0x1F550, 0x1F567),  # Simbol Jam & Waktu
        (0x1F600, 0x1F636),  # Simbol Hewan
        (0x1F700, 0x1F773),  # Simbol Alam
        (0x1F600, 0x1F636),  # Simbol Transportasi Darat
        (0x1F680, 0x1F6C5),  # Simbol Pesawat & Transportasi Udara
        (0x1F774, 0x1F77F),  # Simbol Kapal & Transportasi Air
        (0x1F780, 0x1F7FF),  # Simbol Olahraga Ekstrem
        (0x1F900, 0x1F94F),  # Simbol Musik & Alat Musik
        (0x1F600, 0x1F64F),  # Simbol Profesi
        (0x1F980, 0x1F981),  # Simbol Benda
        (0x1F985, 0x1F991),  # Simbol Buah & Sayuran
        (0x1F992, 0x1F997),  # Simbol Makanan & Minuman
        (0x1F6A0, 0x1F6A3),  # Simbol Transportasi Laut
        (0x1F6F0, 0x1F6F3),  # Simbol Transportasi Udara
        (0x1F600, 0x1F636),  # Simbol Kegiatan Luar Ruangan
        (0x1F300, 0x1F320),  # Simbol Alat Musik
        (0x1F200, 0x1F251),  # Simbol Kepemimpinan & Otoritas
        (0x1F6B4, 0x1F6B6),  # Simbol Transportasi Publik
        (0x1F30D, 0x1F30F),  # Simbol Planet
        (0x1F31D, 0x1F31F),  # Simbol Bulan
        (0x1F320, 0x1F32F),  # Simbol Teleskop
        (0x1F400, 0x1F407),  # Simbol Binatang Air
        (0x1F408, 0x1F40F),  # Simbol Binatang Tanah
        (0x1F410, 0x1F417),  # Simbol Binatang Udara
        (0x1F910, 0x1F918),  # Simbol Aktivitas Manusia
        (0x1F919, 0x1F91F),  # Simbol Tangan & Jari
        (0x1F920, 0x1F927),  # Simbol Orang
    ]

    category = random.choice(categories)
    unique_code = random.randint(category[0], category[1])
    return chr(unique_code)