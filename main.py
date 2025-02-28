from drive_manager.drive_manager import DriveManager
from gui.main_window import MainWindow
from logger.logger import initialize

logger = initialize()

if __name__ == "__main__":
    dev_manager = DriveManager()
    app = MainWindow()

