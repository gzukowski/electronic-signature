"""
auxiliary_app.gui

This module provides the graphical user interface (GUI) components for the auxiliary application. It includes classes and functions for generating RSA keys, handling user input through a PIN pad, and managing the key generation process.

Modules:

- key_generator_window.py
    - KeyGeneratorWindow: A window for generating RSA keys with a graphical user interface.
        - Methods:
            - __init__(): Initializes the KeyGeneratorWindow instance and sets up the UI.
            - init_ui(): Sets up the user interface components, including buttons and layout.
            - open_pin_pad(): Opens a PIN pad dialog for the user to enter a PIN before generating keys.
            - start_key_generation(pin): Starts the key generation process in a separate thread and shows a progress dialog.
            - update_progress(message, value): Updates the progress dialog with the current progress of the key generation.
            - handle_status(status_code, message): Handles the status updates from the key generation thread, showing appropriate messages.
            - close_application(): Closes the application when the quit button is clicked.

- key_generation_thread.py
    - KeyGenerationThread: A QThread subclass responsible for generating RSA keys in a separate thread.
        - Signals:
            - progress_update (str, int): Emitted to update the progress of the RSA key generation process.
            - status (RsaGenState, str): Emitted to indicate the status of the RSA key generation process.
        - Attributes:
            - pin (str): The PIN code used for RSA key generation.
            - drive_manager (DriveManager): The drive manager instance used for managing drives during RSA key generation.
        - Methods:
            - __init__(pin, drive_manager): Initializes the KeyGenerationThread instance with the provided PIN and drive manager.
            - run(): Executes the RSA key generation process and emits progress and status updates.

- enums.py
    - RsaGenState: Enum representing the state of RSA key generation.
        - Attributes:
            - FINISHED (int): Indicates that the RSA key generation has finished successfully.
            - ERRORED (int): Indicates that an error occurred during RSA key generation.
"""
