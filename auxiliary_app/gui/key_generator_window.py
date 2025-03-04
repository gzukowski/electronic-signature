import logging

from gui.enums import RsaGenState
from gui.key_generation_thread import KeyGenerationThread
from PyQt6.QtWidgets import QMessageBox, QProgressDialog, QPushButton, QVBoxLayout, QWidget

from common.gui.drive_selection import DriveSelectionWidget
from common.gui.pin_pad_dialog import PinPadDialog
from common.utils.utils import load_stylesheet

logger = logging.getLogger("global_logger")

class KeyGeneratorWindow(QWidget):
    def __init__(self):
        super().__init__()
        logger.info("Instance of Key Generator created")
        self.init_ui()

    def init_ui(self):
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
        self.progress_dialog.setLabelText(message)
        self.progress_dialog.setValue(value)

    def handle_status(self, status_code, message):
        if status_code == RsaGenState.ERRORED:
            self.progress_dialog.close()
            QMessageBox.critical(self, "Error", f"Key generation failed!\n\n{message}")
        elif status_code == RsaGenState.FINISHED:
            self.progress_dialog.close()
            QMessageBox.information(self, "Success", message)

    def close_application(self):
        logger.info("Application closed by user")
        self.close()
