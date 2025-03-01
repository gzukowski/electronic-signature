import logging
import time
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from PyPDF2 import PdfReader, PdfWriter
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
        encrypted_key, tag = cipher.encrypt_and_digest(key.export_key())
        time.sleep(0.5)

        encrypted_data = cipher.nonce + tag + encrypted_key

        if progress_signal:
            progress_signal.emit("Saving RSA keys to USB...", 80)
        logger.info("Saving RSA Keys to USB")
        drive_manager.save_to_drive(encrypted_data, "private_key.enc")
        drive_manager.save_to_drive(key.publickey().export_key(), "public_key.key")
        time.sleep(0.5)

        if progress_signal:
            progress_signal.emit("Finalizing process...", 95)
        logger.info("RSA keys saved to USB")
        time.sleep(0.5)

    except Exception:
        logger.exception("Error during key generation")
        raise


def decrypt_rsa_key(pin: str, drive_manager, progress_signal=None) -> RSA.RsaKey:
    try:
        private_key_path = f"{drive_manager.selected_drive}/private_key.enc"

        if progress_signal:
            progress_signal.emit("Initializing RSA key decryption...", 10)
        logger.info("Decrypting RSA key")
        time.sleep(1)

        with Path.open(private_key_path, "rb") as f:
            encrypted_key = f.read()

        logger.info("Encrypted RSA key loaded from: %s", private_key_path)

        if progress_signal:
            progress_signal.emit("Checking if PIN is correct...", 30)
        time.sleep(0.5)

        pin_hash = SHA256.new(pin.encode()).digest()

        nonce = encrypted_key[:16]
        tag = encrypted_key[16:32]
        ciphertext = encrypted_key[32:]

        if progress_signal:
            progress_signal.emit("Decrypting the key...", 55)
        time.sleep(0.5)

        cipher = AES.new(pin_hash, AES.MODE_EAX, nonce=nonce)
        decrypted_key = cipher.decrypt(ciphertext)
        cipher.verify(tag)

        if progress_signal:
            progress_signal.emit("Finalizing process...", 75)

        rsa_key = RSA.import_key(decrypted_key)

        if progress_signal:
            progress_signal.emit("RSA key successfully decrypted!", 100)

        logger.info("RSA key successfully decrypted.")

    except (ValueError, KeyError) as e:
        logger.exception("Decryption failed: Invalid PIN or corrupted key. Error: %s")
    except FileNotFoundError:
        logger.exception("File not found: %s", private_key_path)
    except Exception as e:
        logger.exception("Unexpected error during RSA key decryption: %s")

    if progress_signal:
        progress_signal.emit("Decryption failed!", 0)

    return rsa_key


def sign_pdf(pdf_path: str, rsa_key: RSA.RsaKey, progress_signal=None) -> bool:
    try:
        if not Path(pdf_path).exists():
            logger.error("Didn't find pdf file: %s", pdf_path)
            return False

        if progress_signal:
            progress_signal.emit("Initializing PDF File signing...", 20)
        logger.info("Signing PDF File: %s", pdf_path)
        time.sleep(1)

        with Path.open(pdf_path, "rb") as f:
            pdf_content = f.read()

        if progress_signal:
            progress_signal.emit("Hashing PDF File...", 40)
        time.sleep(0.5)
        pdf_hash = SHA256.new(pdf_content)

        if progress_signal:
            progress_signal.emit("Creating signature...", 60)
        time.sleep(0.5)
        signature = pkcs1_15.new(rsa_key).sign(pdf_hash)

        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        if progress_signal:
            progress_signal.emit("Adding signature to PDF File...", 80)
        time.sleep(0.5)
        writer.add_metadata({"/Signature": signature.hex()})

        with Path.open(pdf_path, "wb") as f:
            writer.write(f)

        if progress_signal:
            progress_signal.emit("Finalizing process...", 95)
        time.sleep(0.5)
        logger.info("PDF File successfully signed: %s", pdf_path)

    except Exception as e:
        logger.exception("Error while signing PDF File: %s")


