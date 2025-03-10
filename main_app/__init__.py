"""
main_app

This module provides the main application for the electronic signature project. It includes functionality for signing and verifying PDF files, as well as managing the signing and verification processes in separate threads. The main application also provides a graphical user interface (GUI) for user interaction.

Modules:

- gui
    - sign_and_verify.py
        - SignVerifyWindow: A window for signing and verifying PDF files.
            - Methods:
                - __init__(): Initializes the SignVerifyWindow instance and sets up the UI.
                - init_ui(): Sets up the user interface for the window, including buttons for signing, verifying, and quitting, as well as a drive selection widget.
                - start_signing_file(pin, pdf_path): Starts the process of signing a PDF file, showing a progress dialog and running the signing in a separate thread.
                - start_verifying_file(pub_key_path, pdf_path): Starts the process of verifying a PDF file, showing a progress dialog and running the verification in a separate thread.
                - update_progress(message, value): Updates the progress dialog with the current progress message and value.
                - handle_status(status_code, message): Handles the status updates from the signing or verifying process, showing appropriate messages to the user.
                - verify_sign(): Initiates the process of verifying a PDF file by selecting the PDF and public key files and starting the verification.
                - sign_pdf(): Initiates the process of signing a PDF file by opening a PIN dialog, selecting the PDF file, and starting the signing.
                - select_pdf_file(): Opens a file dialog to select a PDF file for signing or verifying.
                - select_pub_key_file(): Opens a file dialog to select a public key file for verifying a PDF.
                - close_application(): Closes the application and logs the closure.

    - sign_thread.py
        - SignThread: A QThread subclass to handle the process of signing a PDF file in a separate thread.
            - Signals:
                - progress_update (str, int): Emitted to update the progress of the signing process.
                - status (SignState, str): Emitted to update the status of the signing process.
            - Attributes:
                - pin (str): The PIN code used for RSA key decryption.
                - drive_manager (DriveManager): The drive manager instance to manage the drive operations.
                - pdf_path (str): The file path of the PDF to be signed.
            - Methods:
                - __init__(pin, drive_manager, pdf_path): Initializes the SignThread class with the provided PIN, drive manager, and PDF path.
                - run(): Executes the signing process, emitting progress updates and status changes.

    - verify_thread.py
        - VerifyThread: A QThread subclass to handle the verification of a PDF file in a separate thread.
            - Signals:
                - progress_update (str, int): Emitted to update the progress of the verification process.
                - status (VerifyState, str): Emitted to update the status of the verification process.
            - Attributes:
                - pub_key_path (str): The file path to the public key used for verification.
                - pdf_path (str): The file path to the PDF file to be verified.
            - Methods:
                - __init__(pub_key_path, pdf_path): Initializes the VerifyThread instance with the provided public key path and PDF path.
                - run(): Executes the verification process, emitting progress updates and status changes.

    - enums.py
        - SignState: Enumeration representing the state of a signing process.
            - Attributes:
                - FINISHED (int): Indicates that the signing process has completed successfully.
                - ERRORED (int): Indicates that an error occurred during the signing process.
        - VerifyState: Enumeration representing the state of a verification process.
            - Attributes:
                - FINISHED (int): Indicates that the verification process has finished successfully.
                - ERRORED (int): Indicates that an error occurred during the verification process.

- utils
    - pdf_utils.py
        - sign_pdf(pdf_path, rsa_key, progress_signal=None): Signs a PDF file using the provided RSA key.
            - Args:
                - pdf_path (str): The path to the PDF file to be signed.
                - rsa_key (RSA.RsaKey): The RSA key to use for signing the PDF.
                - progress_signal (optional): A signal to report progress, if applicable.
            - Raises:
                - Exception: If an error occurs during the signing process.
        - verify_pdf(pdf_path, public_key, progress_signal=None) -> bool: Verifies the digital signature of a PDF file.
            - Args:
                - pdf_path (str): The file path to the PDF document to be verified.
                - public_key (RSA.RsaKey): The public RSA key used to verify the signature.
                - progress_signal (optional): A signal to report progress, if applicable.
            - Returns:
                - bool: True if the PDF signature is valid, False otherwise.
            - Raises:
                - Exception: If an error occurs during the verification process.

    - crypto_utils.py
        - read_public_key(public_key_path) -> RSA.RsaKey: Reads an RSA public key from the specified file path.
            - Args:
                - public_key_path (str or Path): The path to the public key file.
            - Returns:
                - RSA.RsaKey: The RSA public key.
            - Raises:
                - ValueError: If the key is invalid or corrupted.
                - KeyError: If the key is invalid or corrupted.
                - FileNotFoundError: If the specified file does not exist.
                - Exception: For any other unexpected errors during key decryption.
        - decrypt_rsa_key(pin, drive_manager, progress_signal=None) -> RSA.RsaKey: Decrypts an RSA private key using a provided PIN and drive manager.
            - Args:
                - pin (str): The PIN used to decrypt the RSA key.
                - drive_manager: An object that manages the drive where the encrypted key is stored.
                - progress_signal (optional): A signal object to emit progress updates. Defaults to None.
            - Returns:
                - RSA.RsaKey: The decrypted RSA private key.
            - Raises:
                - Exception: If the decryption fails due to an invalid PIN, corrupted key, file not found, or any other unexpected error.
"""
