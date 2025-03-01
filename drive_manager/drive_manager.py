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

    def read_files(self, path: str) -> list[str]:
        """
        Reads all files from the specified disk path.

        Args:
            path (str): The path to the disk or directory.

        Returns:
            list[str]: A list of filenames in the specified directory.

        """
        # Error handling should be skipped in the future and moved into the decorator in gui,
        # in order to catch errors and display messages for users
        try:
            files = [file.name for file in Path(path).iterdir() if file.is_file()]
        except FileNotFoundError:
            logger.exception("Path not found: %s", path)
            return []
        except PermissionError:
            logger.exception("Permission denied for path: %s", path)
            return []
        except Exception:
            logger.exception("Unexpected error reading files from %s", path)
            return []
        else:
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

        success = False
        try:
            with destination_path.open("wb") as dest:
                dest.write(data)

            logger.info("File successfully saved to: %s", destination_path)
            success = True

        except PermissionError:
            logger.exception("Permission denied when writing to: %s", destination_path)
        except OSError:
            logger.exception("I/O error occurred while writing to: %s", destination_path)
        except Exception:
            logger.exception("Unexpected error occurred while saving to: %s", destination_path)

        return success


