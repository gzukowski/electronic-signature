import logging
import time

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from PyQt6.QtCore import QFile, QTextStream

logger = logging.getLogger("global_logger")

def load_stylesheet(widget, filename):
    file = QFile(filename)
    if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(file)
        stylesheet = stream.readAll()
        widget.setStyleSheet(stylesheet)
        file.close()

def generate_rsa_keys(pin, drive_manager, progress_signal=None):
    try:
        if progress_signal:
            progress_signal.emit("Initializing RSA key generation...", 10)
        logger.info("Generating RSA Keys")
        time.sleep(1)

        if progress_signal:
            progress_signal.emit("Generating 4096-bit RSA key...", 30)
        key = RSA.generate(4096)
        time.sleep(0.5)

        if progress_signal:
            progress_signal.emit("Hashing PIN...", 50)
        pin_hash = SHA256.new(pin.encode()).digest()
        time.sleep(0.5)

        if progress_signal:
            progress_signal.emit("Encrypting private key...", 65)
        cipher = AES.new(pin_hash, AES.MODE_EAX)
        encrypted_key, _ = cipher.encrypt_and_digest(key.export_key())
        time.sleep(0.5)

        if progress_signal:
            progress_signal.emit("Saving RSA keys to USB...", 80)
        logger.info("Saving RSA Keys to USB")
        drive_manager.save_to_drive(encrypted_key, "private_key.enc")
        drive_manager.save_to_drive(key.publickey().export_key(), "public_key.key")
        time.sleep(0.5)

        if progress_signal:
            progress_signal.emit("Finalizing process...", 95)
        logger.info("RSA keys saved to USB")
        time.sleep(0.5)

    except Exception:
        logger.exception("Error during key generation")
        raise

def decrypt_rsa_key(pin, drive_manager, progress_signal=None):
    pass

