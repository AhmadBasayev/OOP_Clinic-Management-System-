# CLINIC MANAGEMENT SYSTEM

def admin_only(func):
    def wrapper(self, *args, **kwargs):
        if self.role != "admin":
            print("Akses ditolak! Fitur ini hanya untuk admin.")
            return
        return func(self, *args, **kwargs)
    return wrapper


# CLASS USER
class User:
    jumlah_user = 0

    def __init__(self, nama, umur, alamat, role):
        self.nama = nama
        self.umur = umur
        self.alamat = alamat
        self.role = role
        User.jumlah_user += 1

    def tampilkan_info(self):
        print(f"Nama   : {self.nama}")
        print(f"Umur   : {self.umur}")
        print(f"Alamat : {self.alamat}")
        print(f"Role   : {self.role}")


# CLASS DOKTER
class Dokter(User):
    jumlah_dokter = 0

    def __init__(self, nama, umur, alamat, spesialisasi):
        super().__init__(nama, umur, alamat, "dokter")
        self.spesialisasi = spesialisasi
        Dokter.jumlah_dokter += 1

    def tampilkan_info(self):
        print("\n=== DATA DOKTER ===")
        print(f"Nama         : {self.nama}")
        print(f"Umur         : {self.umur}")
        print(f"Alamat       : {self.alamat}")
        print(f"Spesialisasi : {self.spesialisasi}")

    def periksa_pasien(self, klinik, pasien, keluhan, diagnosis):
        # Dokter hanya membuat data pemeriksaan (keluhan & diagnosis).
        # Urusan mengisi resep & pembayaran dilakukan oleh Admin.
        return klinik.buat_pemeriksaan(pasien, self, keluhan, diagnosis)


# CLASS PASIEN
class Pasien(User):
    jumlah_pasien = 0

    def __init__(self, nama, umur, alamat):
        super().__init__(nama, umur, alamat, "pasien")
        self.__nomor_rekam_medis = f"RM-{Pasien.jumlah_pasien + 1:04d}"
        Pasien.jumlah_pasien += 1

    def tampilkan_info(self):
        print("\n=== DATA PASIEN ===")
        print(f"Nama           : {self.nama}")
        print(f"Umur           : {self.umur}")
        print(f"Alamat         : {self.alamat}")
        print(f"No Rekam Medis : {self.__nomor_rekam_medis}")

    def get_nomor_rekam_medis(self):
        return self.__nomor_rekam_medis  # encapsulation / privat, indikasi (__)


# CLASS ADMIN
class Admin(User):
    jumlah_admin = 0

    def __init__(self, nama, umur, alamat):
        super().__init__(nama, umur, alamat, "admin")
        Admin.jumlah_admin += 1

    def tampilkan_info(self):
        print("\n=== DATA ADMIN ===")
        print(f"Nama   : {self.nama}")
        print(f"Umur   : {self.umur}")
        print(f"Alamat : {self.alamat}")

    @admin_only
    def tambah_dokter(self, klinik, dokter):
        klinik.tambah_dokter(dokter)

    @admin_only
    def tambah_pasien(self, klinik, pasien):
        klinik.tambah_pasien(pasien)

    @admin_only
    def tambah_obat_ke_inventaris(self, klinik, obat):
        klinik.tambah_obat(obat)

    @admin_only
    def tambahkan_obat_ke_resep(self, pemeriksaan, obat, jumlah):
        # Admin yang mengambilkan & mencatat obat ke resep,
        # berdasarkan diagnosis yang sudah dibuat dokter.
        pemeriksaan.tambah_obat(obat, jumlah)

    @admin_only
    def proses_pembayaran(self, klinik, pemeriksaan, biaya_dokter, jumlah_bayar):
        return klinik.buat_pembayaran(pemeriksaan, biaya_dokter, jumlah_bayar)

    @admin_only
    def terima_pembayaran(self, pembayaran):
        pembayaran.bayar()


# CLASS OBAT
class Obat:
    jumlah_obat = 0

    def __init__(self, nama, harga, stok):
        self.nama = nama
        self.harga = harga
        self._stok = stok  # protected attribute, indikasi tanda (_)
        Obat.jumlah_obat += 1

    def tampilkan_info(self):
        print(f"{self.nama} | Harga: Rp{self.harga:,} | Stok: {self._stok}")

    def kurangi_stok(self, jumlah):
        if jumlah <= 0:
            print("Jumlah obat tidak valid.")
            return False
        if jumlah > self._stok:
            print("Stok obat tidak mencukupi.")
            return False
        self._stok -= jumlah
        return True

    def tambah_stok(self, jumlah):
        if jumlah > 0:
            self._stok += jumlah


# CLASS RESEP (COMPOSITION DENGAN PEMERIKSAAN)
class Resep:
    def __init__(self):
        self.daftar_obat = []

    def tambah_obat(self, obat, jumlah):
        if obat.kurangi_stok(jumlah):
            self.daftar_obat.append({"obat": obat, "jumlah": jumlah})
            print(f"{jumlah} {obat.nama} ditambahkan ke resep.")

    def tampilkan_resep(self):
        print("\n=== RESEP ===")
        if not self.daftar_obat:
            print("Tidak ada obat.")
            return
        for item in self.daftar_obat:
            obat = item["obat"]
            jumlah = item["jumlah"]
            subtotal = obat.harga * jumlah
            print(f"- {obat.nama} x{jumlah} = Rp{subtotal:,}")

    def hitung_total_obat(self):
        total = 0
        for item in self.daftar_obat:
            total += item["obat"].harga * item["jumlah"]
        return total


# CLASS PEMERIKSAAN
class Pemeriksaan:
    jumlah_pemeriksaan = 0

    def __init__(self, pasien, dokter, keluhan, diagnosis):
        self.pasien = pasien
        self.dokter = dokter
        self.keluhan = keluhan
        self.diagnosis = diagnosis
        self.resep = Resep()  # composition
        Pemeriksaan.jumlah_pemeriksaan += 1

    def tambah_obat(self, obat, jumlah):
        self.resep.tambah_obat(obat, jumlah)

    def tampilkan_detail(self):
        print("\n=== HASIL PEMERIKSAAN ===")
        print(f"Pasien    : {self.pasien.nama}")
        print(f"Dokter    : {self.dokter.nama}")
        print(f"Keluhan   : {self.keluhan}")
        print(f"Diagnosis : {self.diagnosis}")
        self.resep.tampilkan_resep()


# CLASS PEMBAYARAN
class Pembayaran:
    jumlah_transaksi = 0

    def __init__(self, pemeriksaan, biaya_dokter, jumlah_bayar):
        self.pemeriksaan = pemeriksaan
        self.biaya_dokter = biaya_dokter
        self.total_obat = pemeriksaan.resep.hitung_total_obat()
        self.total = self.biaya_dokter + self.total_obat
        self.jumlah_bayar = jumlah_bayar
        self.kembalian = self.jumlah_bayar - self.total
        self.status = "Belum Dibayar"
        Pembayaran.jumlah_transaksi += 1

    def bayar(self):
        if self.jumlah_bayar >= self.total:
            self.status = "Lunas"
            print(f"\nPembayaran sebesar Rp{self.total:,} berhasil.")
            print(f"Kembalian: Rp{self.kembalian:,}")
        else:
            self.status = "Belum Lunas"
            print("\nUang pembayaran tidak mencukupi. Transaksi belum lunas.")

    def tampilkan_pembayaran(self):
        print("\n=== PEMBAYARAN ===")
        print(f"Biaya Dokter     : Rp{self.biaya_dokter:,}")
        print(f"Biaya Obat       : Rp{self.total_obat:,}")
        print(f"Total            : Rp{self.total:,}")
        print(f"Uang Dibayarkan  : Rp{self.jumlah_bayar:,}")
        print(f"Status           : {self.status}")


# CLASS KLINIK
class Klinik:
    def __init__(self, nama):
        self.nama = nama
        self.daftar_dokter = []
        self.daftar_pasien = []
        self.daftar_admin = []
        self.daftar_obat = []
        self.daftar_pemeriksaan = []
        self.daftar_pembayaran = []

    def tambah_dokter(self, dokter):
        self.daftar_dokter.append(dokter)
        print(f"Dokter {dokter.nama} berhasil ditambahkan.")

    def tambah_pasien(self, pasien):
        self.daftar_pasien.append(pasien)
        print(f"Pasien {pasien.nama} berhasil ditambahkan.")

    def tambah_admin(self, admin):
        self.daftar_admin.append(admin)
        print(f"Admin {admin.nama} berhasil ditambahkan.")

    def tambah_obat(self, obat):
        self.daftar_obat.append(obat)
        print(f"Obat {obat.nama} berhasil ditambahkan.")

    def buat_pemeriksaan(self, pasien, dokter, keluhan, diagnosis):
        pemeriksaan = Pemeriksaan(pasien, dokter, keluhan, diagnosis)
        self.daftar_pemeriksaan.append(pemeriksaan)
        print("Pemeriksaan berhasil dibuat.")
        return pemeriksaan

    def buat_pembayaran(self, pemeriksaan, biaya_dokter, jumlah_bayar):
        pembayaran = Pembayaran(pemeriksaan, biaya_dokter, jumlah_bayar)
        self.daftar_pembayaran.append(pembayaran)
        return pembayaran

    def tampilkan_dokter(self):
        print("\n=== DAFTAR DOKTER ===")
        for dokter in self.daftar_dokter:
            dokter.tampilkan_info()

    def tampilkan_pasien(self):
        print("\n=== DAFTAR PASIEN ===")
        for pasien in self.daftar_pasien:
            pasien.tampilkan_info()

    def tampilkan_admin(self):
        print("\n=== DAFTAR ADMIN ===")
        for admin in self.daftar_admin:
            admin.tampilkan_info()

    def tampilkan_obat(self):
        print("\n=== DAFTAR OBAT ===")
        for i, obat in enumerate(self.daftar_obat, start=1):
            print(f"{i}. ", end="")
            obat.tampilkan_info()


# FUNGSI BANTU INPUT
def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Input harus berupa angka. Coba lagi.")


def input_ya_tidak(prompt):
    while True:
        jawab = input(prompt).strip().lower()
        if jawab in ("y", "ya"):
            return True
        if jawab in ("n", "t", "tidak"):
            return False
        print("Jawab dengan y (ya) atau n (tidak).")


# PROSES SATU PASIEN (dipanggil berulang untuk tiap pasien)
def layani_pasien(klinik, admin1, dokter1, nomor_antrian):
    print("\n\n" + "#" * 55)
    print(f"                 PASIEN KE-{nomor_antrian}")
    print("#" * 55)

    print("\n" + "=" * 55)
    print("              DATA PASIEN")
    print("=" * 55)

    nama_pasien = input("Nama pasien       : ")
    umur_pasien = input_int("Umur pasien       : ")
    alamat_pasien = input("Alamat pasien     : ")

    pasien = Pasien(nama_pasien, umur_pasien, alamat_pasien)
    admin1.tambah_pasien(klinik, pasien)
    print("No. Rekam Medis   :", pasien.get_nomor_rekam_medis())


    print("\n" + "=" * 55)
    print("           PEMERIKSAAN PASIEN")
    print("=" * 55)

    keluhan = input("Keluhan pasien    : ")
    diagnosis = input("Diagnosis         : ")

    pemeriksaan = dokter1.periksa_pasien(klinik, pasien, keluhan, diagnosis)


    print("\n" + "=" * 55)
    print("             RESEP OBAT")
    print("=" * 55)

    klinik.tampilkan_obat()

    jumlah_item_resep = input_int("\nJumlah jenis obat yang diresepkan : ")

    for i in range(jumlah_item_resep):
        print(f"\nItem resep ke-{i + 1}")
        nomor = input_int("Pilih nomor obat (lihat daftar di atas) : ")

        if nomor < 1 or nomor > len(klinik.daftar_obat):
            print("Nomor obat tidak valid, dilewati.")
            continue

        obat_dipilih = klinik.daftar_obat[nomor - 1]
        jumlah_diresepkan = input_int(f"Jumlah {obat_dipilih.nama} yang diresepkan : ")

        admin1.tambahkan_obat_ke_resep(pemeriksaan, obat_dipilih, jumlah_diresepkan)

    pemeriksaan.tampilkan_detail()


    print("\n" + "=" * 55)
    print("              PEMBAYARAN")
    print("=" * 55)

    biaya_dokter = input_int("Biaya pemeriksaan dokter : Rp")

    total_sementara = biaya_dokter + pemeriksaan.resep.hitung_total_obat()
    print(f"Total yang harus dibayar : Rp{total_sementara:,}")

    jumlah_bayar = input_int("Uang dibayarkan          : Rp")

    pembayaran = admin1.proses_pembayaran(klinik, pemeriksaan, biaya_dokter, jumlah_bayar)
    pembayaran.tampilkan_pembayaran()
    admin1.terima_pembayaran(pembayaran)


    print("\n" + "=" * 65)
    print(f"            LAPORAN PASIEN KE-{nomor_antrian}")
    print("=" * 65)

    pasien.tampilkan_info()
    pemeriksaan.tampilkan_detail()
    pembayaran.tampilkan_pembayaran()

    return pasien, pemeriksaan, pembayaran


# PROGRAM UTAMA
def main():
    print("=" * 55)
    print("     SELAMAT DATANG DI CLINIC MANAGEMENT SYSTEM")
    print("=" * 55)

    nama_klinik = input("\nNama klinik       : ")
    klinik = Klinik(nama_klinik)


    # SETUP (dilakukan sekali di awal)
    print("\n" + "=" * 55)
    print("              DATA ADMIN (PETUGAS)")
    print("=" * 55)

    nama_admin = input("Nama admin        : ")
    umur_admin = input_int("Umur admin        : ")
    alamat_admin = input("Alamat admin      : ")

    admin1 = Admin(nama_admin, umur_admin, alamat_admin)
    klinik.tambah_admin(admin1)

    print("\n" + "=" * 55)
    print("              DATA DOKTER")
    print("=" * 55)

    nama_dokter = input("Nama dokter       : ")
    umur_dokter = input_int("Umur dokter       : ")
    alamat_dokter = input("Alamat dokter     : ")
    spesialisasi = input("Spesialisasi      : ")

    dokter1 = Dokter(nama_dokter, umur_dokter, alamat_dokter, spesialisasi)
    admin1.tambah_dokter(klinik, dokter1)


    print("\n" + "=" * 55)
    print("              DATA OBAT")
    print("=" * 55)

    jumlah_jenis_obat = input_int("Jumlah jenis obat : ")

    for i in range(jumlah_jenis_obat):
        print(f"\nObat ke-{i + 1}")
        nama_obat = input("Nama obat         : ")
        harga_obat = input_int("Harga obat        : Rp")
        stok_obat = input_int("Stok obat         : ")

        obat = Obat(nama_obat, harga_obat, stok_obat)
        admin1.tambah_obat_ke_inventaris(klinik, obat)


    # LOOP PASIEN (diulang sampai admin memilih berhenti)

    nomor_antrian = 1
    pasien, pemeriksaan, pembayaran = layani_pasien(klinik, admin1, dokter1, nomor_antrian)

    while input_ya_tidak("\nLanjut ke pasien berikutnya? (y/n) : "):
        nomor_antrian += 1
        pasien, pemeriksaan, pembayaran = layani_pasien(klinik, admin1, dokter1, nomor_antrian)


    # LAPORAN AKHIR KLINIK

    print("\n\n" + "=" * 65)
    print(f"             LAPORAN AKHIR {klinik.nama.upper()}")
    print("=" * 65)

    admin1.tampilkan_info()
    dokter1.tampilkan_info()

    # Semua pasien beserta nomor rekam medisnya (RM-0001, RM-0002, dst)
    klinik.tampilkan_pasien()

    # Stok obat yang tersisa setelah semua pasien dilayani
    klinik.tampilkan_obat()

    total_pendapatan = 0
    for p in klinik.daftar_pembayaran:
        if p.status == "Lunas":
            total_pendapatan += p.total

    print("\n=== REKAP ===")
    print(f"Jumlah pasien dilayani : {Pasien.jumlah_pasien}")
    print(f"Jumlah transaksi       : {Pembayaran.jumlah_transaksi}")
    print(f"Total pendapatan lunas : Rp{total_pendapatan:,}")

    print("\n" + "=" * 65)
    print("          TERIMA KASIH TELAH BEROBAT")
    print("=" * 65)


    #DEMO PEMBUKTIAN @admin_only

    print("\n" + "=" * 55)
    print("   DEMO: PEMBUKTIAN DECORATOR @admin_only")
    print("=" * 55)

    print("\n[Percobaan] Pasien mencoba memproses pembayaran:")
    Admin.proses_pembayaran(pasien, klinik, pemeriksaan, pembayaran.biaya_dokter, pembayaran.jumlah_bayar)

    print("\n[Percobaan] Dokter mencoba mengisi resep:")
    if klinik.daftar_obat:
        Admin.tambahkan_obat_ke_resep(dokter1, pemeriksaan, klinik.daftar_obat[0], 1)


if __name__ == "__main__":
    main()
