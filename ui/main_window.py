"""
main_window.py - Jendela utama Aplikasi Manajemen Inventaris
"""

import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QStatusBar,
    QMessageBox, QMenuBar, QMenu, QFrame
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QAction, QFont, QColor

from logic.inventory_logic import (
    get_daftar_barang, get_statistik,
    proses_hapus_barang, format_rupiah
)
from ui.dialogs import DialogBarang, DialogTentang


# Identitas mahasiswa (ditampilkan di UI, tidak bisa diedit)
NAMA_MAHASISWA = "Lalu Muhammad Farhan"
NIM_MAHASISWA  = "F1D02310119"

# Kolom tabel
KOLOM_HEADER = [
    "ID", "Kode", "Nama Barang", "Kategori",
    "Jumlah", "Satuan", "Harga Satuan", "Total Nilai",
    "Lokasi", "Tgl Masuk"
]
KOLOM_KEY = [
    "id", "kode_barang", "nama_barang", "kategori",
    "jumlah", "satuan", "harga_satuan", "_total_nilai",
    "lokasi", "tanggal_masuk"
]


class MainWindow(QMainWindow):
    """Jendela utama aplikasi."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Manajemen Inventaris")
        self.setMinimumSize(1050, 640)
        self._selected_id = None

        self._build_menu()
        self._build_ui()
        self._build_statusbar()
        self._load_data()

    # ─── Menu Bar ─────────────────────────────────────────────────
    def _build_menu(self):
        menubar = self.menuBar()

        # Menu: File
        menu_file = menubar.addMenu("File")
        act_refresh = QAction("🔄 Refresh Data", self)
        act_refresh.setShortcut("F5")
        act_refresh.triggered.connect(self._load_data)
        menu_file.addAction(act_refresh)
        menu_file.addSeparator()
        act_keluar = QAction("❌ Keluar", self)
        act_keluar.setShortcut("Ctrl+Q")
        act_keluar.triggered.connect(self.close)
        menu_file.addAction(act_keluar)

        # Menu: Data
        menu_data = menubar.addMenu("Data")
        act_tambah = QAction("➕ Tambah Barang", self)
        act_tambah.setShortcut("Ctrl+N")
        act_tambah.triggered.connect(self._on_tambah)
        menu_data.addAction(act_tambah)
        act_edit = QAction("✏️ Edit Barang", self)
        act_edit.setShortcut("Ctrl+E")
        act_edit.triggered.connect(self._on_edit)
        menu_data.addAction(act_edit)
        act_hapus = QAction("🗑️ Hapus Barang", self)
        act_hapus.setShortcut("Delete")
        act_hapus.triggered.connect(self._on_hapus)
        menu_data.addAction(act_hapus)

        # Menu: Bantuan
        menu_bantuan = menubar.addMenu("Bantuan")
        act_tentang = QAction("ℹ️ Tentang Aplikasi", self)
        act_tentang.triggered.connect(self._on_tentang)
        menu_bantuan.addAction(act_tentang)

    # ─── UI Utama ─────────────────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_header())
        root.addWidget(self._build_stats())
        root.addWidget(self._build_toolbar())
        root.addWidget(self._build_table(), 1)

    def _build_header(self) -> QWidget:
        panel = QWidget()
        panel.setObjectName("headerPanel")
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(16, 10, 16, 10)

        # Judul aplikasi
        lbl_app = QLabel("📦  Sistem Manajemen Inventaris")
        lbl_app.setObjectName("appTitle")
        layout.addWidget(lbl_app)
        layout.addStretch()

        # Identitas mahasiswa (tidak bisa diedit)
        ident_layout = QVBoxLayout()
        ident_layout.setSpacing(2)
        lbl_nama = QLabel(f"👤  {NAMA_MAHASISWA}")
        lbl_nama.setObjectName("identitasLabel")
        lbl_nim = QLabel(f"🎓  NIM: {NIM_MAHASISWA}")
        lbl_nim.setObjectName("identitasLabel")
        ident_layout.addWidget(lbl_nama)
        ident_layout.addWidget(lbl_nim)
        layout.addLayout(ident_layout)

        return panel

    def _build_stats(self) -> QWidget:
        panel = QWidget()
        panel.setObjectName("statsPanel")
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(12)

        self._stat_item  = self._stat_card("—", "Total Jenis Barang")
        self._stat_stok  = self._stat_card("—", "Total Stok")
        self._stat_nilai = self._stat_card("—", "Total Nilai Inventaris")
        self._stat_kat   = self._stat_card("—", "Jumlah Kategori")

        for card in [self._stat_item, self._stat_stok, self._stat_nilai, self._stat_kat]:
            layout.addWidget(card)
        layout.addStretch()
        return panel

    def _stat_card(self, nilai: str, label: str) -> QWidget:
        card = QWidget()
        card.setObjectName("statCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(2)
        lbl_nilai = QLabel(nilai)
        lbl_nilai.setObjectName("statValue")
        lbl_nilai.setAlignment(Qt.AlignCenter)
        lbl_label = QLabel(label)
        lbl_label.setObjectName("statLabel")
        lbl_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_nilai)
        layout.addWidget(lbl_label)
        # simpan referensi ke label nilai agar bisa diperbarui
        card._lbl_nilai = lbl_nilai
        return card

    def _build_toolbar(self) -> QWidget:
        panel = QWidget()
        panel.setObjectName("toolbarPanel")
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)

        # Tombol aksi
        self.btn_tambah = QPushButton("➕  Tambah")
        self.btn_tambah.setObjectName("btnTambah")
        self.btn_tambah.setCursor(Qt.PointingHandCursor)

        self.btn_edit = QPushButton("✏️  Edit")
        self.btn_edit.setObjectName("btnEdit")
        self.btn_edit.setCursor(Qt.PointingHandCursor)

        self.btn_hapus = QPushButton("🗑️  Hapus")
        self.btn_hapus.setObjectName("btnHapus")
        self.btn_hapus.setCursor(Qt.PointingHandCursor)

        self.btn_refresh = QPushButton("🔄  Refresh")
        self.btn_refresh.setObjectName("btnRefresh")
        self.btn_refresh.setCursor(Qt.PointingHandCursor)

        layout.addWidget(self.btn_tambah)
        layout.addWidget(self.btn_edit)
        layout.addWidget(self.btn_hapus)
        layout.addWidget(self.btn_refresh)

        layout.addStretch()

        # Kotak pencarian
        lbl_cari = QLabel("🔍 Cari:")
        self.search_box = QLineEdit()
        self.search_box.setObjectName("searchBox")
        self.search_box.setPlaceholderText("Nama / kode / kategori...")
        self.search_box.setFixedWidth(260)

        layout.addWidget(lbl_cari)
        layout.addWidget(self.search_box)

        # ── Signals & Slots ──
        self.btn_tambah.clicked.connect(self._on_tambah)
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_hapus.clicked.connect(self._on_hapus)
        self.btn_refresh.clicked.connect(self._load_data)
        self.search_box.textChanged.connect(self._on_search)

        return panel

    def _build_table(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 8, 12, 8)

        self.table = QTableWidget()
        self.table.setColumnCount(len(KOLOM_HEADER))
        self.table.setHorizontalHeaderLabels(KOLOM_HEADER)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSortingEnabled(True)
        self.table.setColumnHidden(0, True)  # sembunyikan kolom ID

        # Lebar kolom
        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(2, QHeaderView.Stretch)  # Nama Barang
        for col in [1, 3, 4, 5, 6, 7, 8, 9]:
            hdr.setSectionResizeMode(col, QHeaderView.ResizeToContents)
        # Lebar minimum untuk kolom harga agar tidak terpotong
        self.table.setMinimumColumnWidth = lambda: None  # placeholder
        hdr.setMinimumSectionSize(130)

        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.doubleClicked.connect(self._on_edit)

        layout.addWidget(self.table)
        return container

    def _build_statusbar(self):
        self.statusBar().showMessage("Siap.")

    # ─── Data Loading ─────────────────────────────────────────────
    def _load_data(self, keyword: str = ""):
        self._selected_id = None
        barang_list = get_daftar_barang(keyword)
        self._populate_table(barang_list)
        self._update_stats()
        self.statusBar().showMessage(f"Menampilkan {len(barang_list)} data barang.")

    def _populate_table(self, data_list: list):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        for row_idx, barang in enumerate(data_list):
            self.table.insertRow(row_idx)
            # Hitung total nilai
            total = barang["jumlah"] * barang["harga_satuan"]
            barang["_total_nilai"] = format_rupiah(total)
            for col_idx, key in enumerate(KOLOM_KEY):
                nilai = barang.get(key, "") or ""
                if key == "harga_satuan":
                    nilai = format_rupiah(float(nilai))
                item = QTableWidgetItem(str(nilai))
                item.setTextAlignment(Qt.AlignCenter if col_idx not in [2, 8] else Qt.AlignLeft | Qt.AlignVCenter)
                # Warna merah untuk stok = 0
                if key == "jumlah" and int(barang.get("jumlah", 0)) == 0:
                    item.setForeground(QColor("#e53e3e"))
                    item.setFont(QFont("Segoe UI", 10, QFont.Bold))
                self.table.setItem(row_idx, col_idx, item)
        self.table.setSortingEnabled(True)

    def _update_stats(self):
        stats = get_statistik()
        self._stat_item._lbl_nilai.setText(str(stats["total_item"]))
        self._stat_stok._lbl_nilai.setText(str(stats["total_stok"]))
        self._stat_nilai._lbl_nilai.setText(stats["total_nilai_fmt"])
        self._stat_kat._lbl_nilai.setText(str(stats["total_kategori"]))

    # ─── Slots ────────────────────────────────────────────────────
    def _on_selection_changed(self):
        selected = self.table.selectedItems()
        if selected:
            row = self.table.currentRow()
            id_item = self.table.item(row, 0)
            self._selected_id = int(id_item.text()) if id_item else None
        else:
            self._selected_id = None

    def _on_search(self, teks: str):
        # Debounce ringan menggunakan QTimer
        if hasattr(self, "_search_timer"):
            self._search_timer.stop()
        self._search_timer = QTimer(self)
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(lambda: self._load_data(teks))
        self._search_timer.start(300)

    def _on_tambah(self):
        dialog = DialogBarang(self)
        if dialog.exec():
            self._load_data(self.search_box.text())

    def _on_edit(self):
        if self._selected_id is None:
            QMessageBox.information(self, "Info", "Pilih barang yang ingin diedit terlebih dahulu.")
            return
        from database.db_manager import ambil_barang_by_id
        data = ambil_barang_by_id(self._selected_id)
        if not data:
            QMessageBox.warning(self, "Error", "Data barang tidak ditemukan.")
            return
        dialog = DialogBarang(self, data_barang=data)
        if dialog.exec():
            self._load_data(self.search_box.text())

    def _on_hapus(self):
        if self._selected_id is None:
            QMessageBox.information(self, "Info", "Pilih barang yang ingin dihapus terlebih dahulu.")
            return

        # Dialog konfirmasi (QMessageBox)
        row = self.table.currentRow()
        nama = self.table.item(row, 2).text() if self.table.item(row, 2) else "barang ini"
        konfirmasi = QMessageBox.question(
            self, "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus:\n\n🗑️  {nama}\n\nTindakan ini tidak dapat dibatalkan.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if konfirmasi == QMessageBox.Yes:
            berhasil, pesan = proses_hapus_barang(self._selected_id)
            if berhasil:
                QMessageBox.information(self, "Berhasil", pesan)
                self._load_data(self.search_box.text())
            else:
                QMessageBox.warning(self, "Gagal", pesan)

    def _on_tentang(self):
        dialog = DialogTentang(self)
        dialog.exec()

    def closeEvent(self, event):
        konfirmasi = QMessageBox.question(
            self, "Keluar Aplikasi",
            "Apakah Anda yakin ingin keluar dari aplikasi?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if konfirmasi == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
