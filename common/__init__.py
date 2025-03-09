"""
common

This module provides common functionalities for the electronic signature project. It includes submodules for managing USB drives, graphical user interface components, logging, and utility functions.

Modules:

- drive_manager
    - drive_manager.py
        - DriveManager: A class responsible for managing USB drives.
            - Methods:
                - __init__(): Initializes the DriveManager instance.
                - refresh() -> list[str]: Refreshes and returns a list of USB drives.
                - list_drives_with_keys() -> list[str]: Returns a list of USB drives that contain specific key files.
                - read_files(path: str) -> list[str]: Reads and returns a list of filenames from the specified disk path.
                - save_to_drive(data: bytes, destination_name: str) -> bool: Saves binary data to a file on the selected drive.

- gui
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

- logger
    - logger.py
        - compress_old_log(log_file): Compresses the existing log file into a single ZIP archive before starting a new session.
            - Args:
                - log_file (Path): The path to the log file to be compressed.
        - initialize(log_file): Initializes the new global logger instance.
            - Args:
                - log_file (Path): The path to the log file to be initialized.

- utils
    - utils.py
        - load_stylesheet(widget, relative_path): Loads a stylesheet from a given relative path and applies it to the specified widget.
            - Args:
                - widget (QWidget): The widget to which the stylesheet will be applied.
                - relative_path (str): The relative path to the stylesheet file.
            - Raises:
                - FileNotFoundError: If the stylesheet file does not exist.
                - IOError: If there is an error reading the stylesheet file.
"""
