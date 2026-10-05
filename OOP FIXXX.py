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
        return self.__nomor_rekam_medis


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
    def proses_pembayaran(self, klinik, pemeriksaan, biaya_dokter):
        return klinik.buat_pembayaran(pemeriksaan, biaya_dokter)

    @admin_only
    def terima_pembayaran(self, pembayaran):
        pembayaran.bayar()


# CLASS OBAT
class Obat:
    jumlah_obat = 0

    def __init__(self, nama, harga, stok):
        self.nama = nama
        self.harga = harga
        self._stok = stok  # protected attribute
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
            print(f"- {obat.nama} x{jumlah}")

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

    def __init__(self, pemeriksaan, biaya_dokter):
        self.pemeriksaan = pemeriksaan
        self.biaya_dokter = biaya_dokter
        self.total_obat = pemeriksaan.resep.hitung_total_obat()
        self.total = self.biaya_dokter + self.total_obat
        self.status = "Belum Dibayar"
        Pembayaran.jumlah_transaksi += 1

    def bayar(self):
        self.status = "Sudah Dibayar"
        print(f"\nPembayaran sebesar Rp{self.total:,} berhasil.")

    def tampilkan_pembayaran(self):
        print("\n=== PEMBAYARAN ===")
        print(f"Biaya Dokter : Rp{self.biaya_dokter:,}")
        print(f"Biaya Obat   : Rp{self.total_obat:,}")
        print(f"Total        : Rp{self.total:,}")
        print(f"Status       : {self.status}")


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

    def buat_pembayaran(self, pemeriksaan, biaya_dokter):
        pembayaran = Pembayaran(pemeriksaan, biaya_dokter)
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
        for obat in self.daftar_obat:
            obat.tampilkan_info()


def main():
    klinik = Klinik("Klinik Sehat Bersama")

    # Membuat user: dokter, pasien, admin
    dokter1 = Dokter("Dr. Budi", 35, "Purworejo", "Dokter Umum")
    pasien1 = Pasien("Ahmad", 20, "Purworejo")
    admin1 = Admin("Siti", 28, "Purworejo")

    # Admin yang mendaftarkan dokter & pasien ke klinik
    admin1.tambah_dokter(klinik, dokter1)
    admin1.tambah_pasien(klinik, pasien1)

    # Membuat obat, lalu Admin yang mendaftarkannya ke inventaris
    obat1 = Obat("Paracetamol", 10000, 20)
    obat2 = Obat("Amoxicillin", 15000, 10)
    admin1.tambah_obat_ke_inventaris(klinik, obat1)
    admin1.tambah_obat_ke_inventaris(klinik, obat2)

    # DOKTER hanya memeriksa & mendiagnosis pasien
    pemeriksaan = dokter1.periksa_pasien(klinik, pasien1, "Demam dan sakit kepala", "Flu")

    # ADMIN mengisi resep sesuai diagnosis dokter
    admin1.tambahkan_obat_ke_resep(pemeriksaan, obat1, 2)
    admin1.tambahkan_obat_ke_resep(pemeriksaan, obat2, 1)

    # Menampilkan hasil pemeriksaan
    pemeriksaan.tampilkan_detail()

    # ADMIN memproses & menerima pembayaran
    pembayaran = admin1.proses_pembayaran(klinik, pemeriksaan, 50000)
    pembayaran.tampilkan_pembayaran()
    admin1.terima_pembayaran(pembayaran)

    # Menampilkan nomor rekam medis
    print("\nNomor Rekam Medis:", pasien1.get_nomor_rekam_medis())

    print("   DEMO: PEMBUKTIAN DECORATOR @admin_only")
    print("=" * 5)

    print("\n[Percobaan 1] Pasien mencoba memproses pembayaran:")
    Admin.proses_pembayaran(pasien1, klinik, pemeriksaan, 50000)

    print("\n[Percobaan 2] Dokter mencoba mengisi resep:")
    Admin.tambahkan_obat_ke_resep(dokter1, pemeriksaan, obat1, 1)

    print("\n[Percobaan 3] Admin asli memproses pembayaran:")
    pembayaran_demo = Admin.proses_pembayaran(admin1, klinik, pemeriksaan, 50000)

    if pembayaran_demo:
        print(" BERHASIL: pembayaran dibuat oleh admin.")


if __name__ == "__main__":
    main()