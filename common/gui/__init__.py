"""
common.gui

This module provides graphical user interface (GUI) components for the common functionalities of the electronic signature project. It includes classes and methods for drive selection, PIN pad input, and enumerations for GUI modes.

Modules:

- drive_selection.py
    - DriveSelectionWidget: A widget for selecting a drive from a list of connected drives.
        - Methods:
            - __init__(mode=DriveSelectorMode.STANDARD): Initializes the DriveSelectionWidget.
            - init_ui(): Initializes the user interface.
            - refresh_drives(): Refreshes the list of connected drives.
            - get_connected_drives(): Retrieves the list of connected drives based on the mode.
            - select_drive(): Selects the currently highlighted drive in the list.

- pin_pad_dialog.py
    - PinPadDialog: A dialog window for entering a PIN code.
        - Methods:
            - __init__(): Initializes a new instance of the PinPad dialog.
            - init_ui(): Initializes the user interface for the PIN pad dialog.
            - add_number(number): Adds a number to the current PIN.
            - clear_pin(): Clears the current PIN.
            - backspace(): Removes the last digit from the current PIN.
            - get_pin(): Returns the current PIN.

- enums.py
    - DriveSelectorMode: Enumeration for drive selector modes.
        - Attributes:
            - STANDARD (int): Standard drive selection mode.
            - WITH_KEYS (int): Drive selection mode with keys.
"""
