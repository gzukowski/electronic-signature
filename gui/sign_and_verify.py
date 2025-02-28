import logging

from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget

from gui.pin_pad_dialog import PinPadDialog
from utils.utils import load_stylesheet

logger = logging.getLogger("global_logger")

class SignVerifyWindow(QWidget):
    def __init__(self):
        super().__init__()
        logger.info("Instance of Sign and Verify created")
        self.init_ui()

    def init_ui(self):
        load_stylesheet(self, "gui/sign_and_verify.css")
        self.setWindowTitle("PDF Signer & Verifier")
        self.setGeometry(300, 300, 500, 300)

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

        self.setLayout(layout)

    def close_application(self):
        logger.info("Application closed by user")
        self.close()

    def open_pin_pad(self):
        pin_dialog = PinPadDialog()
        logger.info("Opened PinPad")
        if pin_dialog.exec():
            pin = pin_dialog.get_pin()
            logger.info("PIN: %s", pin)
            # decrypt key here
