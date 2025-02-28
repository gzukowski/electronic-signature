import logging

from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QVBoxLayout

logger = logging.getLogger("global_logger")

class PinPadDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.pin = ""
        self.pin_length = 4
        logger.info("Instance of PinPad created")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Enter PIN")
        self.setGeometry(200, 200, 300, 300)

        layout = QVBoxLayout()

        self.pin_display = QLabel("PIN: ")
        layout.addWidget(self.pin_display)

        #PinPad Grid Creation
        grid_layout = QGridLayout()
        for i in range(9):
            button = QPushButton(str(i + 1))
            button.clicked.connect(lambda _, num=i + 1: self.add_number(num))
            grid_layout.addWidget(button, i // 3, i % 3)

        layout.addLayout(grid_layout)

        #Submit and Clear buttons
        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.accept)
        layout.addWidget(submit_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_pin)
        layout.addWidget(clear_btn)

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

    def get_pin(self):
        return self.pin
