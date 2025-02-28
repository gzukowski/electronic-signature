import sys

from PyQt6.QtWidgets import QApplication

from drive_manager.drive_manager import DriveManager
from gui.key_generator_window import KeyGeneratorWindow
from logger.logger import initialize

logger = initialize()

if __name__ == "__main__":
    dev_manager = DriveManager()


    app = QApplication(sys.argv)
    window = KeyGeneratorWindow()
    window.show()
    sys.exit(app.exec())

