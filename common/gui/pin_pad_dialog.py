import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QVBoxLayout

from common.utils.utils import load_stylesheet

logger = logging.getLogger("global_logger")

class PinPadDialog(QDialog):
    """
    A dialog window for entering a PIN code.

    Attributes:
        pin (str): The current PIN entered by the user.
        pin_length (int): The maximum length of the PIN.

    Methods:
        init_ui():
            Initializes the user interface of the dialog.
        add_number(number):
            Adds a number to the current PIN.
        clear_pin():
            Clears the current PIN.
        backspace():
            Removes the last digit from the current PIN.
        get_pin():
            Returns the current PIN.

    """

    def __init__(self):
        """
        Initializes a new instance of the PinPad dialog.

        This constructor sets up the initial state of the PinPad dialog, including
        initializing the pin to an empty string and setting the pin length to 4.
        It also logs the creation of the PinPad instance and calls the method to
        initialize the user interface.

        Attributes:
            pin (str): The current pin entered by the user, initially an empty string.
            pin_length (int): The required length of the pin, set to 4.

        """
        super().__init__()
        self.pin = ""
        self.pin_length = 4
        logger.info("Instance of PinPad created")
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface for the PIN pad dialog.
        This method sets up the window title, geometry, and layout for the PIN pad dialog.
        It includes a display for the PIN, a grid layout for the number buttons (1-9),
        and additional buttons for submitting, clearing, and backspacing the PIN input.
        The stylesheet for the dialog is loaded from "common/gui/css/pin_pad.css".
        Widgets:
            - QLabel: Displays the current PIN.
            - QPushButton: Number buttons (1-9) to input the PIN.
            - QPushButton: Submit button to accept the entered PIN.
            - QPushButton: Clear button to clear the entered PIN.
            - QPushButton: Backspace button to remove the last digit of the entered PIN.
        """
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
        """
        Adds a number to the PIN if the current length of the PIN is less than the maximum allowed length.

        Args:
            number (int): The number to be added to the PIN.

        Side Effects:
            Updates the PIN display with the new PIN.
            Logs the number that was clicked.

        """
        if len(self.pin) < self.pin_length:
            self.pin += str(number)
            self.pin_display.setText(f"PIN: {self.pin}")
            logger.info("Clicked number %s", number)

    def clear_pin(self):
        """
        Clears the current PIN.

        This method resets the stored PIN to an empty string and updates the
        display to show "PIN: ". It also logs an informational message indicating
        that the PIN has been cleared.
        """
        self.pin = ""
        self.pin_display.setText("PIN: ")
        logger.info("Cleared pin")

    def backspace(self):
        """
        Removes the last character from the current PIN and updates the display.

        If the PIN is not empty, this method removes the last character from the
        `self.pin` attribute and updates the `self.pin_display` to reflect the
        change. It also logs the current state of the PIN after the backspace
        operation.

        Returns:
            None

        """
        if self.pin:
            self.pin = self.pin[:-1]
            self.pin_display.setText(f"PIN: {self.pin}")
            logger.info("Backspace pressed, current PIN: %s", self.pin)

    def get_pin(self):
        """
        Retrieve the PIN.

        Returns:
            str: The PIN code.

        """
        return self.pin
