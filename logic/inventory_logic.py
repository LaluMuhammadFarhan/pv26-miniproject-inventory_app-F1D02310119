"""
inventory_logic.py - Lapisan logika bisnis untuk Aplikasi Manajemen Inventaris
"""

from database import db_manager


KATEGORI_LIST = [
    "Elektronik",
    "Perabot Kantor",
    "Alat Tulis",
    "Perlengkapan Kebersihan",
    "Peralatan IT",
    "Bahan Baku",
    "Produk Jadi",
    "Lainnya",
]

SATUAN_LIST = [
    "pcs",
    "unit",
    "buah",
    "lusin",
    "rim",
    "kg",
    "liter",
    "meter",
    "box",
    "set",
]


def validasi_data_barang(data: dict) -> tuple[bool, str]:
    """
    Memvalidasi data barang sebelum disimpan ke database.
    Mengembalikan (True, '') jika valid, atau (False, pesan_error).
    """
    if not data.get("kode_barang", "").strip():
        return False, "Kode barang tidak boleh kosong."
    if not data.get("nama_barang", "").strip():
        return False, "Nama barang tidak boleh kosong."
    if not data.get("kategori", "").strip():
        return False, "Kategori tidak boleh kosong."
    if not data.get("satuan", "").strip():
        return False, "Satuan tidak boleh kosong."
    if not data.get("tanggal_masuk", "").strip():
        return False, "Tanggal masuk tidak boleh kosong."

    try:
        jumlah = int(data.get("jumlah", 0))
        if jumlah < 0:
            return False, "Jumlah tidak boleh negatif."
    except (ValueError, TypeError):
        return False, "Jumlah harus berupa angka bulat."

    try:
        harga = float(data.get("harga_satuan", 0))
        if harga < 0:
            return False, "Harga satuan tidak boleh negatif."
    except (ValueError, TypeError):
        return False, "Harga satuan harus berupa angka."

    return True, ""


def proses_tambah_barang(data: dict) -> tuple[bool, str]:
    """Memproses penambahan barang baru."""
    valid, pesan = validasi_data_barang(data)
    if not valid:
        return False, pesan

    data["jumlah"] = int(data["jumlah"])
    data["harga_satuan"] = float(data["harga_satuan"])

    berhasil = db_manager.tambah_barang(data)
    if berhasil:
        return True, "Barang berhasil ditambahkan."
    return False, f"Kode barang '{data['kode_barang']}' sudah digunakan. Gunakan kode lain."


def proses_edit_barang(id_barang: int, data: dict) -> tuple[bool, str]:
    """Memproses pembaruan data barang."""
    valid, pesan = validasi_data_barang(data)
    if not valid:
        return False, pesan

    data["jumlah"] = int(data["jumlah"])
    data["harga_satuan"] = float(data["harga_satuan"])

    berhasil = db_manager.update_barang(id_barang, data)
    if berhasil:
        return True, "Data barang berhasil diperbarui."
    return False, "Gagal memperbarui data barang."


def proses_hapus_barang(id_barang: int) -> tuple[bool, str]:
    """Memproses penghapusan barang."""
    berhasil = db_manager.hapus_barang(id_barang)
    if berhasil:
        return True, "Barang berhasil dihapus."
    return False, "Gagal menghapus barang."


def format_rupiah(nilai: float) -> str:
    """Memformat angka menjadi format Rupiah Indonesia."""
    return f"Rp {nilai:,.0f}".replace(",", ".")


def get_daftar_barang(keyword: str = "") -> list:
    """Mengambil daftar barang dari database."""
    return db_manager.ambil_semua_barang(keyword)


def get_statistik() -> dict:
    """Mengambil statistik inventaris dari database."""
    stats = db_manager.ambil_statistik()
    stats["total_nilai_fmt"] = format_rupiah(stats["total_nilai"])
    return stats
