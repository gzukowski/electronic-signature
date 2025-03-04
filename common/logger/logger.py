import datetime
import logging
import sys
import zipfile
from pathlib import Path

AUXILIARY_LOG_FILE = Path("auxiliary.log")
MAIN_LOG_FILE = Path("main.log")
ZIP_FILE = Path("logs.zip")

def compress_old_log(log_file):
    """Compresses the existing log file into a single ZIP archive before starting a new session"""
    if log_file.exists():
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # noqa: DTZ005
        log_name = f"application_{timestamp}.log"

        with zipfile.ZipFile(ZIP_FILE, "a", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(log_file, arcname=log_name)

        log_file.unlink()


def initialize(log_file):
    """Initializes the new global logger instance"""
    compress_old_log(log_file)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(module)-20s - %(funcName)-40s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )


    return logging.getLogger("global_logger")
