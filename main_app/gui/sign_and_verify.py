import logging

from gui.enums import SignState, VerifyState
from gui.sign_thread import SignThread
from gui.verify_thread import VerifyThread
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QProgressDialog, QPushButton, QVBoxLayout, QWidget

from common.gui.drive_selection import DriveSelectionWidget
from common.gui.enums import DriveSelectorMode
from common.gui.pin_pad_dialog import PinPadDialog
from common.utils.utils import load_stylesheet

logger = logging.getLogger("global_logger")

class SignVerifyWindow(QWidget):
    """
    A window for signing and verifying PDF files.

    Methods
    -------
    __init__():
        Initializes the SignVerifyWindow instance and sets up the UI.
    init_ui():
        Sets up the user interface for the window, including buttons for signing, verifying, and quitting,
        as well as a drive selection widget.
    start_signing_file(pin, pdf_path):
        Starts the process of signing a PDF file, showing a progress dialog and running the signing in a separate thread.
    start_verifying_file(pub_key_path, pdf_path):
        Starts the process of verifying a PDF file, showing a progress dialog and running the verification in a separate thread.
    update_progress(message, value):
        Updates the progress dialog with the current progress message and value.
    handle_status(status_code, message):
        Handles the status updates from the signing or verifying process, showing appropriate messages to the user.
    verify_sign():
        Initiates the process of verifying a PDF file by selecting the PDF and public key files and starting the verification.
    sign_pdf():
        Initiates the process of signing a PDF file by opening a PIN dialog, selecting the PDF file, and starting the signing.
    select_pdf_file():
        Opens a file dialog to select a PDF file for signing or verifying.
    select_pub_key_file():
        Opens a file dialog to select a public key file for verifying a PDF.
    close_application():
        Closes the application and logs the closure.

    """

    def __init__(self):
        """
        Initializes an instance of the Sign and Verify class.

        This constructor calls the parent class's constructor, logs the creation
        of the instance, and initializes the user interface.

        Methods:
            init_ui: Initializes the user interface components.

        """
        super().__init__()
        logger.info("Instance of Sign and Verify created")
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface for the PDF Signer & Verifier application.
        This method sets up the main window's title, geometry, and layout. It includes
        buttons for signing PDFs, verifying PDF signatures, and quitting the application.
        Additionally, it adds a drive selection widget for selecting drives with keys.
        UI Elements:
        - Sign PDF Button: A button to sign a PDF document.
        - Verify PDF Signature Button: A button to verify the signature of a PDF document.
        - Quit Button: A button to close the application.
        - Drive Selection Widget: A widget to select drives with keys.
        The method also connects the buttons to their respective event handlers.
        """
        load_stylesheet(self, "main_app/gui/css/sign_and_verify.css")
        self.setWindowTitle("PDF Signer & Verifier")
        self.setGeometry(100, 100, 400, 500)

        layout = QVBoxLayout()

        self.sign_button = QPushButton("Sign PDF")
        self.sign_button.setObjectName("signBtn")
        self.sign_button.clicked.connect(self.sign_pdf)
        layout.addWidget(self.sign_button)

        self.verify_button = QPushButton("Verify PDF Signature")
        self.verify_button.setObjectName("verifyBtn")
        self.verify_button.clicked.connect(self.verify_sign)
        layout.addWidget(self.verify_button)

        self.quit_button = QPushButton("Quit")
        self.quit_button.setObjectName("quitBtn")
        self.quit_button.clicked.connect(self.close)
        layout.addWidget(self.quit_button)

        self.drive_selection_widget = DriveSelectionWidget(DriveSelectorMode.WITH_KEYS)
        layout.addWidget(self.drive_selection_widget)

        self.setLayout(layout)

    def start_signing_file(self, pin, pdf_path):
        """
        Initiates the process of signing a PDF file.
        This method sets up a progress dialog to inform the user about the signing process and starts a separate thread to handle the signing operation.

        Args:
            pin (str): The PIN code required for signing the PDF.
            pdf_path (str): The file path of the PDF to be signed.

        Attributes:
            progress_dialog (QProgressDialog): A dialog to show the progress of the signing process.
            keygen_thread (SignThread): A thread that handles the signing process.

        """
        self.progress_dialog = QProgressDialog("Preparing PDF file signing...", "Cancel", 0, 100, self)
        self.progress_dialog.setWindowTitle("Signing of PDF file")
        self.progress_dialog.setMinimumWidth(300)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setAutoReset(True)
        self.progress_dialog.show()

        self.keygen_thread = SignThread(pin, self.drive_selection_widget.drive_manager, pdf_path)
        self.keygen_thread.progress_update.connect(self.update_progress)
        self.keygen_thread.status.connect(self.handle_status)
        self.keygen_thread.start()

    def start_verifying_file(self, pub_key_path, pdf_path):
        """
        Starts the process of verifying a PDF file using a public key.
        This method initializes a progress dialog to inform the user about the
        verification process and starts a separate thread to handle the verification.

        Args:
            pub_key_path (str): The file path to the public key used for verification.
            pdf_path (str): The file path to the PDF file to be verified.

        """
        self.progress_dialog = QProgressDialog("Preparing PDF file verification...", "Cancel", 0, 100, self)
        self.progress_dialog.setWindowTitle("PDF verification")
        self.progress_dialog.setMinimumWidth(300)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setAutoReset(True)
        self.progress_dialog.show()

        self.keygen_thread = VerifyThread(pub_key_path, pdf_path)
        self.keygen_thread.progress_update.connect(self.update_progress)
        self.keygen_thread.status.connect(self.handle_status)
        self.keygen_thread.start()


    def update_progress(self, message, value):
        """
        Updates the progress dialog with the given message and value.

        Args:
            message (str): The message to display in the progress dialog.
            value (int): The progress value to set in the progress dialog.

        """
        self.progress_dialog.setLabelText(message)
        self.progress_dialog.setValue(value)

    def handle_status(self, status_code, message):
        """
        Handles the status of signing or verifying a PDF file and displays appropriate message dialogs.

        Args:
        status_code (Enum): The status code indicating the result of the signing or verifying process.
                            Possible values are SignState.ERRORED, SignState.FINISHED, VerifyState.ERRORED, VerifyState.FINISHED.
        message (str): The message to be displayed in the dialog.

        Behavior:
        - If the status code is SignState.ERRORED, closes the progress dialog and shows a critical error message box.
        - If the status code is SignState.FINISHED, closes the progress dialog and shows an information message box.
        - If the status code is VerifyState.ERRORED, closes the progress dialog and shows a critical error message box.
        - If the status code is VerifyState.FINISHED, closes the progress dialog and shows an information message box.

        """
        if status_code == SignState.ERRORED:
            self.progress_dialog.close()
            QMessageBox.critical(self, "Error", f"Signing PDF File failed!\n\n{message}")
        elif status_code == SignState.FINISHED:
            self.progress_dialog.close()
            QMessageBox.information(self, "Success", message)
        elif status_code == VerifyState.ERRORED:
            self.progress_dialog.close()
            QMessageBox.critical(self, "Error", f"Verifying PDF File failed!\n\n{message}")
        elif status_code == VerifyState.FINISHED:
            self.progress_dialog.close()
            QMessageBox.information(self, "Success", message)

    def verify_sign(self):
        """
        Verifies the digital signature of a selected PDF file using a selected public key file.
        This method prompts the user to select a PDF file and a public key file. If both files are selected,
        it initiates the verification process.

        Returns:
            None

        """
        pdf_path = self.select_pdf_file()
        if not pdf_path:
            return

        pub_key_path = self.select_pub_key_file()
        if pdf_path:
            self.start_verifying_file(pub_key_path, pdf_path)

    def sign_pdf(self):
        """
        Opens a dialog to enter a PIN, selects a PDF file, and starts the signing process.

        This method performs the following steps:
        1. Opens a PinPadDialog for the user to enter their PIN.
        2. Logs the opening of the PinPadDialog.
        3. If the user confirms the dialog, retrieves the entered PIN.
        4. Logs the entered PIN.
        5. Opens a file selection dialog for the user to select a PDF file.
        6. If a PDF file is selected, starts the signing process with the entered PIN and selected PDF file.

        Returns:
            None

        """
        pin_dialog = PinPadDialog()
        logger.info("Opened PinPad")
        if pin_dialog.exec():
            pin = pin_dialog.get_pin()
            logger.info("PIN: %s", pin)
            pdf_path = self.select_pdf_file()
            if pdf_path:
                self.start_signing_file(pin, pdf_path)

    def select_pdf_file(self):
        """
        Opens a file dialog for the user to select a PDF file.

        Returns:
            str: The path to the selected PDF file, or None if no file was selected.

        """
        input_pdf_path, _ = QFileDialog.getOpenFileName(self, "Choose PDF file", "", "PDF Files (*.pdf)")

        if not input_pdf_path:
            QMessageBox.warning(self, "Cancelled", "PDF file not selected for signature.")
            return None

        return input_pdf_path

    def select_pub_key_file(self):
        """
        Opens a file dialog for the user to select a public key file.
        This method displays a file dialog that allows the user to choose a public key file.
        If the user cancels the dialog or does not select a file, a warning message is shown
        and the method returns None.

        Returns:
            str or None: The path to the selected public key file, or None if no file was selected.

        """
        input_path, _ = QFileDialog.getOpenFileName(self, "Choose your public key", "", "")

        if not input_path:
            QMessageBox.warning(self, "Cancelled", "Public key not selected.")
            return None

        return input_path

    def close_application(self):
        """
        Closes the application.

        This method logs an informational message indicating that the application
        was closed by the user and then proceeds to close the application window.
        """
        logger.info("Application closed by user")
        self.close()

