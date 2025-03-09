"""
auxiliary_app.utils

This module provides utility functions for the auxiliary application. It includes functions for generating RSA keys, encrypting the private key with a PIN, and saving the keys to a USB drive.

Modules:

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
