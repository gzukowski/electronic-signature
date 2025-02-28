import logging

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

def generate_rsa_keys(pin, drive_manager):
    logger.info("Generating RSA Keys")
    key = RSA.generate(4096)

    pin_hash = SHA256.new(pin.encode()).digest()

    cipher = AES.new(pin_hash, AES.MODE_EAX)
    encrypted_key, _ = cipher.encrypt_and_digest(key.export_key())

    logger.info("Saving RSA Keys to USB")
    drive_manager.save_to_drive(encrypted_key, "private_key.enc")
    drive_manager.save_to_drive(key.publickey().export_key(), "public_key.key")
    logger.info("RSA keys saved to USB")
