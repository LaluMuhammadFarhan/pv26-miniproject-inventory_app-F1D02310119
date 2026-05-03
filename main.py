"""
main.py - Entry point Aplikasi Manajemen Inventaris
"""

import sys
import os

# Pastikan direktori project ada di sys.path agar impor antar modul berjalan lancar
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from database.db_manager import initialize_db
from ui.main_window import MainWindow


def load_stylesheet(app: QApplication) -> None:
    """Memuat file QSS eksternal dan menerapkannya ke seluruh aplikasi."""
    qss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles", "style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Sistem Manajemen Inventaris")
    app.setOrganizationName("Universitas Tadulako")

    # Inisialisasi database
    initialize_db()

    # Terapkan stylesheet dari file eksternal
    load_stylesheet(app)

    # Tampilkan jendela utama
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
