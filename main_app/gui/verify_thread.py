import logging

from gui.enums import VerifyState
from PyQt6.QtCore import QThread, pyqtSignal
from utils.crypto_utils import read_public_key
from utils.pdf_utils import verify_pdf

logger = logging.getLogger("global_logger")

class VerifyThread(QThread):
    """
    A QThread subclass to handle the verification of a PDF file in a separate thread.
    Signals:
        progress_update (str, int): Emitted to update the progress of the verification process.
        status (VerifyState, str): Emitted to update the status of the verification process.

    Args:
        pub_key_path (str): The file path to the public key used for verification.
        pdf_path (str): The file path to the PDF file to be verified.

    Methods:
        run(): Executes the verification process, emitting progress updates and status changes.

    """

    progress_update = pyqtSignal(str, int)
    status = pyqtSignal(VerifyState, str)

    def __init__(self, pub_key_path, pdf_path):
        """
        Initializes the VerifyThread instance with the provided public key path and PDF path.

        Args:
            pub_key_path (str): The file path to the public key.
            pdf_path (str): The file path to the PDF document to be verified.

        """
        super().__init__()
        self.pub_key_path = pub_key_path
        self.pdf_path = pdf_path

    def run(self):
        """
        Executes the verification process for a PDF file.

        This method performs the following steps:
        1. Emits a progress update indicating the start of reading the public key.
        2. Reads the public key from the specified path.
        3. Emits a progress update indicating the start of PDF file verification.
        4. Verifies the PDF file using the provided public key.
        5. Emits progress updates throughout the verification process.
        6. Emits a final progress update upon completion.
        7. Emits a status signal indicating the success or failure of the verification process.

        Emits:
            progress_update (str, int): Signal to update the progress with a message and percentage.
            status (VerifyState, str): Signal to update the status of the verification process.

        Raises:
            Exception: If an error occurs during the verification process, it is caught and logged, and the status is updated to indicate an error.

        """
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
