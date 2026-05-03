"""
dialogs.py - Dialog form tambah/edit barang untuk Aplikasi Manajemen Inventaris
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QSpinBox, QDoubleSpinBox,
    QComboBox, QTextEdit, QDateEdit, QPushButton,
    QMessageBox, QWidget, QGroupBox
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

from logic.inventory_logic import (
    KATEGORI_LIST, SATUAN_LIST,
    proses_tambah_barang, proses_edit_barang
)


class DialogBarang(QDialog):
    """
    Dialog untuk menambah atau mengedit data barang inventaris.
    Berisi form dengan minimal 5 field menggunakan berbagai komponen PySide6.
    """

    def __init__(self, parent=None, data_barang: dict = None):
        super().__init__(parent)
        self._data_barang = data_barang  # None = mode tambah, dict = mode edit
        self._id_barang = data_barang["id"] if data_barang else None
        self._is_edit = data_barang is not None

        self.setWindowTitle("Edit Barang" if self._is_edit else "Tambah Barang Baru")
        self.setMinimumWidth(520)
        self.setModal(True)

        self._build_ui()
        if self._is_edit:
            self._isi_form(data_barang)

    # ─── Build UI ─────────────────────────────────────────────────
    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 16)
        main_layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setObjectName("dialogHeader")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 14, 20, 14)
        judul = "✏️  Edit Data Barang" if self._is_edit else "➕  Tambah Barang Baru"
        lbl_judul = QLabel(judul)
        lbl_judul.setObjectName("dialogTitle")
        header_layout.addWidget(lbl_judul)
        main_layout.addWidget(header)

        # ── Grup: Identitas Barang ──
        grp_identitas = QGroupBox("Identitas Barang")
        form_identitas = QFormLayout(grp_identitas)
        form_identitas.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form_identitas.setVerticalSpacing(10)
        form_identitas.setHorizontalSpacing(14)
        form_identitas.setContentsMargins(14, 16, 14, 12)

        # Field 1 – Kode Barang
        self.input_kode = QLineEdit()
        self.input_kode.setPlaceholderText("Contoh: EL-001")
        self.input_kode.setMaxLength(20)
        form_identitas.addRow(self._label("Kode Barang *"), self.input_kode)

        # Field 2 – Nama Barang
        self.input_nama = QLineEdit()
        self.input_nama.setPlaceholderText("Nama lengkap barang")
        self.input_nama.setMaxLength(100)
        form_identitas.addRow(self._label("Nama Barang *"), self.input_nama)

        # Field 3 – Kategori (QComboBox)
        self.combo_kategori = QComboBox()
        self.combo_kategori.addItems(KATEGORI_LIST)
        form_identitas.addRow(self._label("Kategori *"), self.combo_kategori)

        # Field 4 – Lokasi
        self.input_lokasi = QLineEdit()
        self.input_lokasi.setPlaceholderText("Contoh: Gudang A - Rak 3")
        form_identitas.addRow(self._label("Lokasi Penyimpanan"), self.input_lokasi)

        main_layout.addSpacing(12)
        main_layout.addWidget(grp_identitas)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ── Grup: Stok & Harga ──
        grp_stok = QGroupBox("Stok & Harga")
        form_stok = QFormLayout(grp_stok)
        form_stok.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form_stok.setVerticalSpacing(10)
        form_stok.setHorizontalSpacing(14)
        form_stok.setContentsMargins(14, 16, 14, 12)

        # Field 5 – Jumlah (QSpinBox)
        self.spin_jumlah = QSpinBox()
        self.spin_jumlah.setRange(0, 999999)
        self.spin_jumlah.setSuffix("  unit")
        form_stok.addRow(self._label("Jumlah Stok *"), self.spin_jumlah)

        # Field 6 – Satuan (QComboBox)
        self.combo_satuan = QComboBox()
        self.combo_satuan.addItems(SATUAN_LIST)
        form_stok.addRow(self._label("Satuan *"), self.combo_satuan)

        # Field 7 – Harga Satuan (QDoubleSpinBox)
        self.spin_harga = QDoubleSpinBox()
        self.spin_harga.setRange(0, 999_999_999)
        self.spin_harga.setDecimals(0)
        self.spin_harga.setSingleStep(1000)
        self.spin_harga.setPrefix("Rp ")
        form_stok.addRow(self._label("Harga Satuan *"), self.spin_harga)

        # Field 8 – Tanggal Masuk (QDateEdit)
        self.date_masuk = QDateEdit()
        self.date_masuk.setCalendarPopup(True)
        self.date_masuk.setDate(QDate.currentDate())
        self.date_masuk.setDisplayFormat("dd MMMM yyyy")
        form_stok.addRow(self._label("Tanggal Masuk *"), self.date_masuk)

        # ── Grup: Keterangan ──
        grp_ket = QGroupBox("Keterangan Tambahan")
        layout_ket = QVBoxLayout(grp_ket)
        layout_ket.setContentsMargins(14, 12, 14, 12)

        # Field 9 – Keterangan (QTextEdit)
        self.input_keterangan = QTextEdit()
        self.input_keterangan.setPlaceholderText("Catatan tambahan tentang barang ini (opsional)...")
        self.input_keterangan.setMaximumHeight(80)
        layout_ket.addWidget(self.input_keterangan)

        # Susun grup ke layout
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(16, 12, 16, 0)
        content_layout.setSpacing(10)
        content_layout.addWidget(grp_identitas)
        content_layout.addWidget(grp_stok)
        content_layout.addWidget(grp_ket)

        main_layout.addLayout(content_layout)

        # ── Tombol Aksi ──
        main_layout.addSpacing(16)
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(16, 0, 16, 0)
        btn_layout.addStretch()

        self.btn_batal = QPushButton("Batal")
        self.btn_batal.setObjectName("btnBatal")
        self.btn_batal.setCursor(Qt.PointingHandCursor)

        self.btn_simpan = QPushButton("💾  Simpan")
        self.btn_simpan.setObjectName("btnSimpan")
        self.btn_simpan.setCursor(Qt.PointingHandCursor)
        self.btn_simpan.setDefault(True)

        btn_layout.addWidget(self.btn_batal)
        btn_layout.addWidget(self.btn_simpan)
        main_layout.addLayout(btn_layout)

        # ── Signals & Slots ──
        self.btn_simpan.clicked.connect(self._on_simpan)
        self.btn_batal.clicked.connect(self.reject)

    def _label(self, teks: str) -> QLabel:
        lbl = QLabel(teks)
        lbl.setObjectName("formLabel")
        return lbl

    # ─── Isi Form (mode edit) ──────────────────────────────────────
    def _isi_form(self, data: dict):
        self.input_kode.setText(data.get("kode_barang", ""))
        self.input_nama.setText(data.get("nama_barang", ""))
        idx_kat = self.combo_kategori.findText(data.get("kategori", ""))
        if idx_kat >= 0:
            self.combo_kategori.setCurrentIndex(idx_kat)
        self.input_lokasi.setText(data.get("lokasi", "") or "")
        self.spin_jumlah.setValue(int(data.get("jumlah", 0)))
        idx_sat = self.combo_satuan.findText(data.get("satuan", ""))
        if idx_sat >= 0:
            self.combo_satuan.setCurrentIndex(idx_sat)
        self.spin_harga.setValue(float(data.get("harga_satuan", 0)))
        tanggal = data.get("tanggal_masuk", "")
        if tanggal:
            qdate = QDate.fromString(tanggal, "yyyy-MM-dd")
            if qdate.isValid():
                self.date_masuk.setDate(qdate)
        self.input_keterangan.setPlainText(data.get("keterangan", "") or "")

    # ─── Slot Simpan ──────────────────────────────────────────────
    def _on_simpan(self):
        data = {
            "kode_barang": self.input_kode.text().strip(),
            "nama_barang": self.input_nama.text().strip(),
            "kategori": self.combo_kategori.currentText(),
            "jumlah": self.spin_jumlah.value(),
            "satuan": self.combo_satuan.currentText(),
            "harga_satuan": self.spin_harga.value(),
            "lokasi": self.input_lokasi.text().strip(),
            "keterangan": self.input_keterangan.toPlainText().strip(),
            "tanggal_masuk": self.date_masuk.date().toString("yyyy-MM-dd"),
        }

        if self._is_edit:
            berhasil, pesan = proses_edit_barang(self._id_barang, data)
        else:
            berhasil, pesan = proses_tambah_barang(data)

        if berhasil:
            QMessageBox.information(self, "Berhasil", pesan)
            self.accept()
        else:
            QMessageBox.warning(self, "Gagal", pesan)


class DialogTentang(QDialog):
    """Dialog 'Tentang Aplikasi' yang menampilkan info aplikasi dan identitas mahasiswa."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tentang Aplikasi")
        self.setFixedSize(420, 340)
        self.setModal(True)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)
        layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setObjectName("dialogHeader")
        h_layout = QVBoxLayout(header)
        h_layout.setContentsMargins(20, 16, 20, 16)
        lbl_judul = QLabel("ℹ️  Tentang Aplikasi")
        lbl_judul.setObjectName("dialogTitle")
        h_layout.addWidget(lbl_judul)
        layout.addWidget(header)

        # Konten
        konten = QWidget()
        k_layout = QVBoxLayout(konten)
        k_layout.setContentsMargins(28, 20, 28, 10)
        k_layout.setSpacing(12)

        def baris(label, nilai, bold_nilai=False):
            row = QHBoxLayout()
            lbl_l = QLabel(label)
            lbl_l.setObjectName("formLabel")
            lbl_l.setFixedWidth(140)
            lbl_v = QLabel(nilai)
            if bold_nilai:
                font = lbl_v.font()
                font.setBold(True)
                lbl_v.setFont(font)
            lbl_v.setWordWrap(True)
            row.addWidget(lbl_l)
            row.addWidget(lbl_v, 1)
            return row

        k_layout.addLayout(baris("Nama Aplikasi", "Sistem Manajemen Inventaris", bold_nilai=True))
        k_layout.addLayout(baris("Versi", "1.0.0"))
        k_layout.addLayout(baris("Deskripsi",
            "Aplikasi desktop untuk mengelola data inventaris barang, "
            "termasuk pencatatan stok, harga, dan lokasi penyimpanan."))
        k_layout.addLayout(baris("Framework", "PySide6 (Qt for Python)"))
        k_layout.addLayout(baris("Database", "SQLite 3"))
        k_layout.addLayout(baris("Nama Mahasiswa", "Muhammad Rizky Ramadhan", bold_nilai=True))
        k_layout.addLayout(baris("NIM", "F55123048", bold_nilai=True))

        layout.addWidget(konten)

        # Tombol tutup
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(28, 0, 28, 0)
        btn_layout.addStretch()
        btn_tutup = QPushButton("Tutup")
        btn_tutup.setObjectName("btnBatal")
        btn_tutup.setCursor(Qt.PointingHandCursor)
        btn_tutup.clicked.connect(self.accept)
        btn_layout.addWidget(btn_tutup)
        layout.addLayout(btn_layout)
