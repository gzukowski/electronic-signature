import logging

from gui.enums import RsaGenState
from PyQt6.QtCore import QThread, pyqtSignal
from utils.utils import generate_rsa_keys

logger = logging.getLogger("global_logger")


class KeyGenerationThread(QThread):
    progress_update = pyqtSignal(str, int)
    status = pyqtSignal(RsaGenState, str)

    def __init__(self, pin, drive_manager):
        super().__init__()
        self.pin = pin
        self.drive_manager = drive_manager

    def run(self):
        try:
            self.progress_update.emit("Initializing RSA key generation...", 10)
            generate_rsa_keys(self.pin, self.drive_manager, self.progress_update)
            self.progress_update.emit("Finalizing process...", 95)
            self.progress_update.emit("Done!", 100)
            self.status.emit(RsaGenState.FINISHED, "RSA keys generated successfully.")
        except Exception as e:
            logger.exception("Error during key generation")
            self.status.emit(RsaGenState.ERRORED, str(e))
