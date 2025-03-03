import logging

from gui.enums import SignState
from PyQt6.QtCore import QThread, pyqtSignal
from utils.utils import decrypt_rsa_key, sign_pdf

logger = logging.getLogger("global_logger")


class SignThread(QThread):
    progress_update = pyqtSignal(str, int)
    status = pyqtSignal(SignState, str)

    def __init__(self, pin, drive_manager, pdf_path):
        super().__init__()
        self.pin = pin
        self.drive_manager = drive_manager
        self.pdf_path = pdf_path

    def run(self):
        try:
            self.progress_update.emit("Initializing RSA key decryption...", 10)
            self.rsa_key = decrypt_rsa_key(self.pin, self.drive_manager, self.progress_update)
            self.progress_update.emit("Initializing PDF File signing...", 10)
            sign_pdf(self.pdf_path, self.rsa_key, self.progress_update)
            self.progress_update.emit("Finalizing process...", 95)
            self.progress_update.emit("Done!", 100)
            self.status.emit(SignState.FINISHED, "PDF File signed successfully.")
        except Exception as e:
            logger.exception("Error during signing PDF File")
            self.status.emit(SignState.ERRORED, str(e))
