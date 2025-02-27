import datetime
import logging
import sys
import zipfile
from pathlib import Path

LOG_FILE = Path("application.log")
ZIP_FILE = Path("logs.zip")

def compress_old_log():
    """Compresses the existing log file into a single ZIP archive before starting a new session"""
    if LOG_FILE.exists():
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # noqa: DTZ005
        log_name = f"application_{timestamp}.log"

        with zipfile.ZipFile(ZIP_FILE, "a", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(LOG_FILE, arcname=log_name)

        LOG_FILE.unlink()


def initialize():
    """Initializes the new global logger instance"""
    compress_old_log()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(module)-20s - %(funcName)-40s: %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )


    return logging.getLogger("global_logger")
