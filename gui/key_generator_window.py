import logging

from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget

from gui.pin_pad_dialog import PinPadDialog

logger = logging.getLogger("global_logger")

class KeyGeneratorWindow(QWidget):
    def __init__(self):
        super().__init__()
        logger.info("Instance of Key Generator created")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PAdES Key Generator")
        self.setGeometry(100, 100, 200, 200)

        layout = QVBoxLayout()

        self.keygen_btn = QPushButton("Generate RSA Keys")
        self.keygen_btn.clicked.connect(self.open_pin_pad)
        layout.addWidget(self.keygen_btn)

        self.quit_btn = QPushButton("Quit")
        self.quit_btn.clicked.connect(self.close_application)
        layout.addWidget(self.quit_btn)

        self.setLayout(layout)

    def open_pin_pad(self):
        pin_dialog = PinPadDialog()
        logger.info("Opened PinPad")
        if pin_dialog.exec():
            pin = pin_dialog.get_pin()
            logger.info("PIN: %s", pin)
            #-> generate rsa keys using pin password

    def close_application(self):
        logger.info("Application closed by user")
        self.close()
