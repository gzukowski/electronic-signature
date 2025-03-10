"""
common.drive_manager

This module provides functionality for managing USB drives. It includes classes and methods for listing available drives, detecting drives with specific key files, reading files from a drive, and saving data to a selected drive.

Modules:

- drive_manager.py
    - DriveManager: A class responsible for managing USB drives.
        - Methods:
            - __init__(): Initializes the DriveManager instance.
            - refresh() -> list[str]: Refreshes and returns a list of USB drives.
            - list_drives_with_keys() -> list[str]: Returns a list of USB drives that contain specific key files.
            - read_files(path: str) -> list[str]: Reads and returns a list of filenames from the specified disk path.
            - save_to_drive(data: bytes, destination_name: str) -> bool: Saves binary data to a file on the selected drive.
"""
