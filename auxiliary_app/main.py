import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

sys.path.append(str(Path(__file__).resolve().parent.parent))

from gui.key_generator_window import KeyGeneratorWindow

from common.drive_manager.drive_manager import DriveManager
from common.logger.logger import AUXILIARY_LOG_FILE, initialize

logger = initialize(AUXILIARY_LOG_FILE)

if __name__ == "__main__":
    dev_manager = DriveManager()


    app = QApplication(sys.argv)
    window = KeyGeneratorWindow()
    window.show()
    sys.exit(app.exec())
