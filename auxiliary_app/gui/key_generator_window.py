import logging

from gui.enums import RsaGenState
from gui.key_generation_thread import KeyGenerationThread
from PyQt6.QtWidgets import QMessageBox, QProgressDialog, QPushButton, QVBoxLayout, QWidget

from common.gui.drive_selection import DriveSelectionWidget
from common.gui.pin_pad_dialog import PinPadDialog
from common.utils.utils import load_stylesheet

logger = logging.getLogger("global_logger")

class KeyGeneratorWindow(QWidget):
    """
    A window for generating RSA keys with a graphical user interface.

    Methods
    -------
    __init__():
        Initializes the KeyGeneratorWindow instance and sets up the UI.

    init_ui():
        Sets up the user interface components, including buttons and layout.

    open_pin_pad():
        Opens a PIN pad dialog for the user to enter a PIN before generating keys.

    start_key_generation(pin):
        Starts the key generation process in a separate thread and shows a progress dialog.

    update_progress(message, value):
        Updates the progress dialog with the current progress of the key generation.

    handle_status(status_code, message):
        Handles the status updates from the key generation thread, showing appropriate messages.

    close_application():
        Closes the application when the quit button is clicked.

    """

    def __init__(self):
        super().__init__()
        logger.info("Instance of Key Generator created")
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface for the key generator window.
        This method sets up the window title, geometry, and layout. It creates and configures
        the buttons for generating RSA keys and quitting the application, as well as a drive
        selection widget. The buttons are connected to their respective event handlers.
        Widgets:
            - QPushButton: "Generate RSA Keys" button to initiate RSA key generation.
            - QPushButton: "Quit" button to close the application.
            - DriveSelectionWidget: Custom widget for drive selection.
        Layout:
            - QVBoxLayout: Vertical layout to arrange the buttons and drive selection widget.
        """
        load_stylesheet(self, "auxiliary_app/gui/css/key_gen.css")
        self.setWindowTitle("PAdES Key Generator")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.keygen_btn = QPushButton("Generate RSA Keys")
        self.keygen_btn.setObjectName("keygenBtn")
        self.keygen_btn.clicked.connect(self.open_pin_pad)

        self.quit_btn = QPushButton("Quit")
        self.quit_btn.setObjectName("quitBtn")
        self.quit_btn.clicked.connect(self.close_application)

        self.drive_selection_widget = DriveSelectionWidget()

        layout.addWidget(self.keygen_btn)
        layout.addWidget(self.quit_btn)
        layout.addWidget(self.drive_selection_widget)
        self.setLayout(layout)

        layout.addWidget(self.keygen_btn)
        layout.addWidget(self.quit_btn)
        layout.addWidget(self.drive_selection_widget)
        self.setLayout(layout)

    def open_pin_pad(self):
        """
        Opens a PIN pad dialog for the user to enter a PIN and starts the key generation process.
        This method first checks if a drive is selected. If no drive is selected, it logs an
        informational message and shows a warning message box to the user, then returns without
        proceeding further. If a drive is selected, it opens a PIN pad dialog for the user to
        enter their PIN. If the user successfully enters a PIN, it logs that the PIN was entered
        and starts the key generation process using the entered PIN.

        Returns:
            None

        """
        selected_drive = self.drive_selection_widget.drive_manager.selected_drive
        if not selected_drive:
            logger.info("No drive selected. Key generation aborted.")
            QMessageBox.warning(self, "Drive missing", "Please select a drive before generating RSA keys.")
            return

        pin_dialog = PinPadDialog()
        logger.info("Opened PinPad")
        if pin_dialog.exec():
            pin = pin_dialog.get_pin()
            logger.info("PIN entered.")
            self.start_key_generation(pin)

    def start_key_generation(self, pin):
        """
        Initiates the RSA key generation process and displays a progress dialog.

        Args:
            pin (str): The PIN code required for key generation.
        This method sets up a QProgressDialog to inform the user about the progress
        of the key generation process. It then starts a KeyGenerationThread to
        perform the actual key generation in the background. The progress of the
        key generation is updated via the `progress_update` signal, and the status
        is handled via the `status` signal.

        """
        self.progress_dialog = QProgressDialog("Preparing key generation...", "Cancel", 0, 100, self)
        self.progress_dialog.setWindowTitle("Generating RSA Keys")
        self.progress_dialog.setMinimumWidth(300)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setAutoReset(True)
        self.progress_dialog.show()

        self.keygen_thread = KeyGenerationThread(pin, self.drive_selection_widget.drive_manager)
        self.keygen_thread.progress_update.connect(self.update_progress)
        self.keygen_thread.status.connect(self.handle_status)
        self.keygen_thread.start()

    def update_progress(self, message, value):
        """
        Updates the progress dialog with a new message and progress value.

        Args:
            message (str): The message to display on the progress dialog.
            value (int): The progress value to set on the progress dialog.

        """
        self.progress_dialog.setLabelText(message)
        self.progress_dialog.setValue(value)

    def handle_status(self, status_code, message):
        """
        Handles the status of the RSA key generation process.

        Args:
        status_code (RsaGenState): The current state of the RSA key generation process.
        message (str): A message providing additional information about the status.

        Actions:
        - If the status_code is RsaGenState.ERRORED, closes the progress dialog and shows a critical error message.
        - If the status_code is RsaGenState.FINISHED, closes the progress dialog and shows an informational success message.

        """
        if status_code == RsaGenState.ERRORED:
            self.progress_dialog.close()
            QMessageBox.critical(self, "Error", f"Key generation failed!\n\n{message}")
        elif status_code == RsaGenState.FINISHED:
            self.progress_dialog.close()
            QMessageBox.information(self, "Success", message)

    def close_application(self):
        """
        Closes the application window.

        This method logs an informational message indicating that the application
        was closed by the user and then proceeds to close the application window.
        """
        logger.info("Application closed by user")
        self.close()
