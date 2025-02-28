import logging

from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget

from gui.drive_selection import DriveSelectionWidget
from gui.pin_pad_dialog import PinPadDialog
from utils.utils import generate_rsa_keys, load_stylesheet

logger = logging.getLogger("global_logger")

class KeyGeneratorWindow(QWidget):
    def __init__(self):
        super().__init__()
        logger.info("Instance of Key Generator created")
        self.init_ui()

    def init_ui(self):
        load_stylesheet(self, "gui/css/key_gen.css")
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

    def open_pin_pad(self):
        pin_dialog = PinPadDialog()
        logger.info("Opened PinPad")
        if pin_dialog.exec():
            pin = pin_dialog.get_pin()
            logger.info("PIN: %s", pin)
            generate_rsa_keys(pin, self.drive_selection_widget.drive_manager)

    def close_application(self):
        logger.info("Application closed by user")
        self.close()
