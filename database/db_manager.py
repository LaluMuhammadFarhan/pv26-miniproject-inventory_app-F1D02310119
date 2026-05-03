"""
db_manager.py - Modul pengelolaan database SQLite untuk Aplikasi Manajemen Inventaris
"""

import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventaris.db")


def get_connection():
    """Membuat dan mengembalikan koneksi ke database SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    """Inisialisasi tabel database jika belum ada."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS barang (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kode_barang TEXT NOT NULL UNIQUE,
            nama_barang TEXT NOT NULL,
            kategori TEXT NOT NULL,
            jumlah INTEGER NOT NULL DEFAULT 0,
            satuan TEXT NOT NULL,
            harga_satuan REAL NOT NULL DEFAULT 0.0,
            lokasi TEXT,
            keterangan TEXT,
            tanggal_masuk TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def tambah_barang(data: dict) -> bool:
    """Menambahkan barang baru ke database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO barang (kode_barang, nama_barang, kategori, jumlah, satuan,
                                harga_satuan, lokasi, keterangan, tanggal_masuk)
            VALUES (:kode_barang, :nama_barang, :kategori, :jumlah, :satuan,
                    :harga_satuan, :lokasi, :keterangan, :tanggal_masuk)
        """, data)
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def update_barang(id_barang: int, data: dict) -> bool:
    """Memperbarui data barang berdasarkan ID."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE barang SET
                kode_barang = :kode_barang,
                nama_barang = :nama_barang,
                kategori = :kategori,
                jumlah = :jumlah,
                satuan = :satuan,
                harga_satuan = :harga_satuan,
                lokasi = :lokasi,
                keterangan = :keterangan,
                tanggal_masuk = :tanggal_masuk
            WHERE id = :id
        """, {**data, "id": id_barang})
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def hapus_barang(id_barang: int) -> bool:
    """Menghapus barang berdasarkan ID."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM barang WHERE id = ?", (id_barang,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def ambil_semua_barang(keyword: str = "") -> list:
    """Mengambil semua data barang, dengan opsional filter pencarian."""
    conn = get_connection()
    cursor = conn.cursor()
    if keyword:
        query = """
            SELECT * FROM barang
            WHERE nama_barang LIKE ? OR kode_barang LIKE ? OR kategori LIKE ?
            ORDER BY id DESC
        """
        like = f"%{keyword}%"
        cursor.execute(query, (like, like, like))
    else:
        cursor.execute("SELECT * FROM barang ORDER BY id DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def ambil_barang_by_id(id_barang: int) -> dict | None:
    """Mengambil satu data barang berdasarkan ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM barang WHERE id = ?", (id_barang,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def ambil_statistik() -> dict:
    """Mengambil statistik ringkas inventaris."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total_item FROM barang")
    total_item = cursor.fetchone()["total_item"]
    cursor.execute("SELECT SUM(jumlah) as total_stok FROM barang")
    total_stok = cursor.fetchone()["total_stok"] or 0
    cursor.execute("SELECT SUM(jumlah * harga_satuan) as total_nilai FROM barang")
    total_nilai = cursor.fetchone()["total_nilai"] or 0.0
    cursor.execute("SELECT COUNT(DISTINCT kategori) as total_kategori FROM barang")
    total_kategori = cursor.fetchone()["total_kategori"]
    conn.close()
    return {
        "total_item": total_item,
        "total_stok": total_stok,
        "total_nilai": total_nilai,
        "total_kategori": total_kategori,
    }
