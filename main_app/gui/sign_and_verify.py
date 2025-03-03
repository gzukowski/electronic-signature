import logging

from gui.enums import SignState
from gui.sign_thread import SignThread
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QProgressDialog, QPushButton, QVBoxLayout, QWidget

from common.gui.drive_selection import DriveSelectionWidget
from common.gui.enums import DriveSelectorMode
from common.gui.pin_pad_dialog import PinPadDialog
from common.utils.utils import load_stylesheet

logger = logging.getLogger("global_logger")

class SignVerifyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_pdf = None
        logger.info("Instance of Sign and Verify created")
        self.init_ui()

    def init_ui(self):
        load_stylesheet(self, "main_app/gui/css/sign_and_verify.css")
        self.setWindowTitle("PDF Signer & Verifier")
        self.setGeometry(100, 100, 400, 500)

        layout = QVBoxLayout()

        self.sign_button = QPushButton("✍️ Sign PDF")
        self.sign_button.setObjectName("signBtn")
        self.sign_button.clicked.connect(self.open_pin_pad)
        layout.addWidget(self.sign_button)

        self.verify_button = QPushButton("✅ Verify PDF Signature")
        self.verify_button.setObjectName("verifyBtn")
        layout.addWidget(self.verify_button)

        self.quit_button = QPushButton("❌ Quit")
        self.quit_button.setObjectName("quitBtn")
        self.quit_button.clicked.connect(self.close)
        layout.addWidget(self.quit_button)

        self.drive_selection_widget = DriveSelectionWidget(DriveSelectorMode.WITH_KEYS)
        layout.addWidget(self.drive_selection_widget)

        self.setLayout(layout)

    def start_signing_file(self, pin):
        self.progress_dialog = QProgressDialog("Preparing PDF file signing...", "Cancel", 0, 100, self)
        self.progress_dialog.setWindowTitle("Signing of PDF file")
        self.progress_dialog.setMinimumWidth(300)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setAutoReset(True)
        self.progress_dialog.show()

        self.keygen_thread = SignThread(pin, self.drive_selection_widget.drive_manager, self.selected_pdf)
        self.keygen_thread.progress_update.connect(self.update_progress)
        self.keygen_thread.status.connect(self.handle_status)
        self.keygen_thread.start()

    def update_progress(self, message, value):
        self.progress_dialog.setLabelText(message)
        self.progress_dialog.setValue(value)

    def handle_status(self, status_code, message):
        if status_code == SignState.ERRORED:
            self.progress_dialog.close()
            QMessageBox.critical(self, "Error", f"Signing PDF File failed!\n\n{message}")
        elif status_code == SignState.FINISHED:
            self.progress_dialog.close()
            QMessageBox.information(self, "Success", message)

    def close_application(self):
        logger.info("Application closed by user")
        self.close()

    def open_pin_pad(self):
        pin_dialog = PinPadDialog()
        logger.info("Opened PinPad")
        if pin_dialog.exec():
            pin = pin_dialog.get_pin()
            logger.info("PIN: %s", pin)
            self.select_pdf_file()
            if self.selected_pdf:
                self.start_signing_file(pin)

    def select_pdf_file(self):
        input_pdf_path, _ = QFileDialog.getOpenFileName(self, "Choose PDF file", "", "PDF Files (*.pdf)")

        if not input_pdf_path:
            QMessageBox.warning(self, "Cancelled", "PDF file not selected for signature.")

        self.selected_pdf = input_pdf_path

