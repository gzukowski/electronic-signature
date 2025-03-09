import logging

from gui.enums import RsaGenState
from PyQt6.QtCore import QThread, pyqtSignal
from utils.utils import generate_rsa_keys

logger = logging.getLogger("global_logger")


class KeyGenerationThread(QThread):
    """
    A QThread subclass responsible for generating RSA keys in a separate thread.
    Signals:
        progress_update (str, int): Emitted to update the progress of the RSA key generation process.
        status (RsaGenState, str): Emitted to indicate the status of the RSA key generation process.

    Attributes:
        pin (str): The PIN code used for RSA key generation.
        drive_manager (DriveManager): The drive manager instance used for managing drives during RSA key generation.

    Methods:
        run(): Executes the RSA key generation process and emits progress and status updates.

    """

    progress_update = pyqtSignal(str, int)
    status = pyqtSignal(RsaGenState, str)

    def __init__(self, pin, drive_manager):
        super().__init__()
        self.pin = pin
        self.drive_manager = drive_manager

    def run(self):
        """
        Executes the RSA key generation process in a separate thread.

        This method updates the progress at various stages of the key generation
        process and emits the final status upon completion or error.

        Emits:
            progress_update (str, int): Updates the progress message and percentage.
            status (RsaGenState, str): Emits the final status of the key generation process.

        Raises:
            Exception: If an error occurs during the key generation process.

        """
        try:
            self.progress_update.emit("Initializing RSA key generation...", 10)
            generate_rsa_keys(self.pin, self.drive_manager, self.progress_update)
            self.progress_update.emit("Finalizing process...", 95)
            self.progress_update.emit("Done!", 100)
            self.status.emit(RsaGenState.FINISHED, "RSA keys generated successfully.")
        except Exception as e:
            logger.exception("Error during key generation")
            self.status.emit(RsaGenState.ERRORED, str(e))
