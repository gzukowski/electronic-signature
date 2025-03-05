import logging

from gui.enums import VerifyState
from PyQt6.QtCore import QThread, pyqtSignal
from utils.crypto_utils import read_public_key
from utils.pdf_utils import verify_pdf

logger = logging.getLogger("global_logger")

class VerifyThread(QThread):
    progress_update = pyqtSignal(str, int)
    status = pyqtSignal(VerifyState, str)

    def __init__(self, pub_key_path, pdf_path):
        super().__init__()
        self.pub_key_path = pub_key_path
        self.pdf_path = pdf_path

    def run(self):
        try:
            self.progress_update.emit("Reading public key...", 10)
            self.public_key = read_public_key(self.pub_key_path)
            logger.exception("Error during verifying PDF File")
            self.progress_update.emit("Initializing PDF File verification...", 10)
            verify_pdf(self.pdf_path, self.public_key, self.progress_update)
            self.progress_update.emit("Finalizing process...", 95)
            self.progress_update.emit("Done!", 100)
            self.status.emit(VerifyState.FINISHED, "PDF File verified successfully.")
        except Exception as e:
            logger.exception("Error during verifying PDF File")
            self.status.emit(VerifyState.ERRORED, str(e))
