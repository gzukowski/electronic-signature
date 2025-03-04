import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QVBoxLayout

from common.utils.utils import load_stylesheet

logger = logging.getLogger("global_logger")

class PinPadDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.pin = ""
        self.pin_length = 4
        logger.info("Instance of PinPad created")
        self.init_ui()

    def init_ui(self):
        load_stylesheet(self, "common/gui/css/pin_pad.css")

        self.setWindowTitle("Enter PIN")
        self.setGeometry(200, 200, 350, 400)

        layout = QVBoxLayout()

        self.pin_display = QLabel("PIN: ")
        layout.addWidget(self.pin_display)

        grid_layout = QGridLayout()
        for i in range(9):
            button = QPushButton(str(i + 1))
            button.setObjectName(f"button{i + 1}")
            button.clicked.connect(lambda _, num=i + 1: self.add_number(num))
            grid_layout.addWidget(button, i // 3, i % 3)

        layout.addLayout(grid_layout)

        submit_btn = QPushButton("Submit")
        submit_btn.setObjectName("submitBtn")
        submit_btn.clicked.connect(self.accept)

        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("clearBtn")
        clear_btn.clicked.connect(self.clear_pin)

        backspace_btn = QPushButton("Backspace")
        backspace_btn.setObjectName("backspaceBtn")
        backspace_btn.clicked.connect(self.backspace)

        layout.addWidget(submit_btn)
        layout.addWidget(clear_btn)
        layout.addWidget(backspace_btn)

        self.setLayout(layout)

    def add_number(self, number):
        if len(self.pin) < self.pin_length:
            self.pin += str(number)
            self.pin_display.setText(f"PIN: {self.pin}")
            logger.info("Clicked number %s", number)

    def clear_pin(self):
        self.pin = ""
        self.pin_display.setText("PIN: ")
        logger.info("Cleared pin")

    def backspace(self):
        if self.pin:
            self.pin = self.pin[:-1]
            self.pin_display.setText(f"PIN: {self.pin}")
            logger.info("Backspace pressed, current PIN: %s", self.pin)

    def get_pin(self):
        return self.pin
