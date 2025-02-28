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

    def refresh(self) -> list[str]:
        """
        Returns a list of USB drives
        """
        self.drive_list = [disk.device for disk in psutil.disk_partitions() if "removable" in disk.opts]
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

