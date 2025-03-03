import logging
import time
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from PyPDF2 import PdfReader, PdfWriter

logger = logging.getLogger("global_logger")

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
            progress_signal.emit("RSA key successfully decrypted!", 99)

        logger.info("RSA key successfully decrypted.")

    except (ValueError, KeyError):
        logger.exception("Decryption failed: Invalid PIN or corrupted key. Error: %s")
    except FileNotFoundError:
        logger.exception("File not found: %s", private_key_path)
    except Exception:
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

    except Exception:
        logger.exception("Error while signing PDF File: %s")


