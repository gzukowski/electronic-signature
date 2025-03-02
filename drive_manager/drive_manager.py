import logging
from pathlib import Path

import psutil

logger = logging.getLogger("global_logger")

class DriveManager:
    def __init__(self):
        """
        Initializes the DriveManager instance.
        """
        logger.info("Drive manager's instance created")
        self.drive_list = []
        self.selected_drive = None

    def refresh(self) -> list[str]:
        """
        Returns a list of USB drives
        """
        self.drive_list = [disk.device for disk in psutil.disk_partitions() if "removable" in disk.opts]
        self.drive_list = [disk.device for disk in psutil.disk_partitions()]
        logger.info("Detected devices: %s", self.drive_list)

    def list_drives_with_keys(self) -> list[str]:
        """
        Returns a list of USB drivers with key files
        """
        self.drive_list = [disk.device for disk in psutil.disk_partitions() if "removable" in disk.opts]
        self.drive_list = [disk.device for disk in psutil.disk_partitions()]

        return [
            drive for drive in self.drive_list
                if all(key in self.read_files(drive) for key in ["private_key.enc", "public_key.key"])
        ]

    def read_files(self, path: str) -> list[str]:
        """
        Reads all files from the specified disk path.

        Args:
            path (str): The path to the disk or directory.

        Returns:
            list[str]: A list of filenames in the specified directory.

        """
        files = [file.name for file in Path(path).iterdir() if file.is_file()]
        logger.info("Files in %s: %s", path, files)
        return files

    def save_to_drive(self, data: bytes, destination_name: str) -> bool:
        """
        Saves binary data to a file on the selected drive.

        Args:
            data (bytes): Binary data to be saved on the USB drive.
            destination_name (str): Name of the file on the selected drive.

        Returns:
            bool: True if the data is successfully saved, False otherwise.

        """
        if not self.selected_drive:
            logger.error("No drive selected. Set 'self.selected_drive' before saving.")
            return False

        if not Path(self.selected_drive).exists():
            logger.error("Selected drive does not exist: %s", self.selected_drive)
            return False

        destination_path = Path(self.selected_drive) / destination_name

        with destination_path.open("wb") as dest:
            dest.write(data)

        logger.info("File successfully saved to: %s", destination_path)

        return True


