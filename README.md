# Sistem Manajemen Inventaris

Aplikasi desktop berbasis GUI untuk mengelola data inventaris barang, dibangun menggunakan Python dan PySide6.

---

## Identitas Mahasiswa

| Field | Detail |
|-------|--------|
| **Nama** | Lalu Muhammad Farhan |
| **NIM** | F1D02310119 |
| **Mata Kuliah** | Pemrograman Visual |
| **Topik Project** | Manajemen Inventaris |

---

## Deskripsi Aplikasi

**Sistem Manajemen Inventaris** adalah aplikasi desktop yang memungkinkan pengguna untuk:

- Mencatat dan mengelola data barang inventaris secara terorganisir
- Menyimpan informasi lengkap barang: kode, nama, kategori, jumlah stok, satuan, harga satuan, lokasi penyimpanan, dan tanggal masuk
- Melakukan pencarian barang secara real-time berdasarkan nama, kode, atau kategori
- Melihat statistik ringkas inventaris (total jenis barang, total stok, total nilai, jumlah kategori)
- Mengelola data dengan operasi Tambah, Edit, dan Hapus

Data disimpan secara persisten menggunakan database SQLite sehingga tetap tersedia setelah aplikasi ditutup dan dibuka kembali.

---

## Struktur Project

```
inventory_app/
├── main.py                      # Entry point aplikasi
├── README.md                    # Dokumentasi project
├── database/
│   ├── __init__.py
│   ├── db_manager.py            # Koneksi & operasi SQLite
│   └── inventaris.db            # File database (dibuat otomatis)
├── logic/
│   ├── __init__.py
│   └── inventory_logic.py       # Logika bisnis & validasi
├── ui/
│   ├── __init__.py
│   ├── main_window.py           # Jendela utama aplikasi
│   └── dialogs.py               # Dialog form tambah/edit & tentang
└── styles/
    └── style.qss                # Stylesheet QSS eksternal
```

Struktur mengikuti prinsip **Separation of Concerns (SoC)**:

| Lapisan | File | Tanggung Jawab |
|---------|------|----------------|
| **Database** | `database/db_manager.py` | Koneksi SQLite, query CRUD |
| **Logika** | `logic/inventory_logic.py` | Validasi data, format output |
| **UI** | `ui/main_window.py`, `ui/dialogs.py` | Tampilan & interaksi pengguna |
| **Style** | `styles/style.qss` | Tema visual aplikasi |

---

## Fitur Wajib yang Diimplementasikan

1. **Form input 9 field** — QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QDateEdit, QTextEdit
2. **Signals & Slots** — `clicked`, `textChanged`, `itemSelectionChanged`, `doubleClicked`, `timeout` (debounce search)
3. **Layout terstruktur** — QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox
4. **Tampilan data** — QTableWidget dengan sorting, warna stok habis, kartu statistik
5. **SQLite CRUD** — Create, Read, Update, Delete; data persisten di `inventaris.db`
6. **Menu bar + Tentang** — Menu File, Data, Bantuan → Tentang Aplikasi
7. **Dialog terpisah** — `DialogBarang` untuk tambah/edit, `DialogTentang` untuk info aplikasi
8. **Dialog konfirmasi** — QMessageBox untuk konfirmasi hapus dan keluar aplikasi
9. **Nama & NIM di UI** — Ditampilkan di header, tidak dapat diedit pengguna
10. **QSS eksternal** — `styles/style.qss` dimuat secara dinamis di `main.py`
11. **Separation of Concerns** — UI, logika, database, dan style dipisah ke modul berbeda

---

## Cara Menjalankan

### 1. Prasyarat

Pastikan Python 3.10+ sudah terinstal di sistem Anda.

```bash
python --version
```

### 2. Install Dependensi

```bash
pip install PySide6
```

### 3. Jalankan Aplikasi

```bash
cd inventory_app
python main.py
```

> Database `inventaris.db` akan **dibuat secara otomatis** di folder `database/` saat aplikasi pertama kali dijalankan. Tidak perlu konfigurasi tambahan.

---

## Teknologi yang Digunakan

| Teknologi | Versi | Kegunaan |
|-----------|-------|----------|
| **Python** | 3.10+ | Bahasa pemrograman utama |
| **PySide6** | 6.x | Framework GUI (Qt for Python) |
| **SQLite3** | Built-in | Database penyimpanan data lokal |
| **QSS** | — | Styling antarmuka (Qt Style Sheets) |

---

## Tampilan Aplikasi

### Jendela Utama
- Header dengan nama & NIM mahasiswa
- Kartu statistik inventaris (total item, stok, nilai, kategori)
- Toolbar dengan tombol Tambah, Edit, Hapus, Refresh, dan kotak pencarian
- Tabel data barang dengan sorting dan pewarnaan stok habis

### Dialog Tambah/Edit Barang
- Form terorganisir dalam grup: Identitas Barang, Stok & Harga, Keterangan
- Kalender popup untuk pemilihan tanggal
- Validasi input sebelum data disimpan

---

## Lisensi

Project ini dibuat untuk keperluan tugas akademik mata kuliah Pemrograman Visual.
