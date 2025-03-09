import logging

from gui.enums import SignState
from PyQt6.QtCore import QThread, pyqtSignal
from utils.crypto_utils import decrypt_rsa_key
from utils.pdf_utils import sign_pdf

logger = logging.getLogger("global_logger")


class SignThread(QThread):
    """
    A QThread subclass to handle the process of signing a PDF file in a separate thread.
    Signals:
        progress_update (str, int): Emitted to update the progress of the signing process.
        status (SignState, str): Emitted to update the status of the signing process.

    Attributes:
        pin (str): The PIN code used for RSA key decryption.
        drive_manager (DriveManager): The drive manager instance to manage the drive operations.
        pdf_path (str): The file path of the PDF to be signed.

    Methods:
        run(): Executes the signing process, emitting progress updates and status changes.

    """

    progress_update = pyqtSignal(str, int)
    status = pyqtSignal(SignState, str)

    def __init__(self, pin, drive_manager, pdf_path):
        """
        Initializes the SignThread class with the provided PIN, drive manager, and PDF path.

        Args:
            pin (str): The personal identification number used for authentication.
            drive_manager (DriveManager): An instance of the DriveManager class to manage drive operations.
            pdf_path (str): The file path to the PDF document to be signed.

        """
        super().__init__()
        self.pin = pin
        self.drive_manager = drive_manager
        self.pdf_path = pdf_path

    def run(self):
        """
        Executes the signing process in a separate thread.

        This method performs the following steps:
        1. Emits a progress update indicating the start of RSA key decryption.
        2. Decrypts the RSA key using the provided PIN and drive manager.
        3. Emits a progress update indicating the start of PDF file signing.
        4. Signs the PDF file using the decrypted RSA key.
        5. Emits a progress update indicating the finalization of the process.
        6. Emits a final progress update indicating completion.
        7. Emits a status signal indicating the successful completion of the signing process.

        If an exception occurs during any of these steps, it logs the exception and emits a status signal indicating an error.

        Raises:
            Exception: If an error occurs during the signing process, it is caught and logged, and the status is updated to indicate an error.

        """
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
