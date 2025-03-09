"""
auxiliary_app

This module provides the auxiliary application for the electronic signature project. It includes functionality for generating RSA keys, encrypting the private key with a PIN, and saving the keys to a USB drive. The auxiliary application also provides a graphical user interface (GUI) for user interaction.

Modules:

- gui
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

- utils
    - utils.py
        - generate_rsa_keys(pin, drive_manager, progress_signal=None): Generates RSA keys, encrypts the private key with a hashed PIN, and saves both keys to a USB drive.
            - Args:
                - pin (str): The PIN used to hash and encrypt the private key.
                - drive_manager (DriveManager): An object responsible for managing the USB drive operations.
                - progress_signal (object, optional): An optional signal object to emit progress updates.
            - Raises:
                - Exception: If any error occurs during the key generation process.
            - Emits:
                - progress_signal (str, int): Emits progress updates with a message and a percentage.
"""
