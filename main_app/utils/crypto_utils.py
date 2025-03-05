import logging
import time
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

logger = logging.getLogger("global_logger")

def read_public_key(public_key_path) -> RSA.RsaKey:
    try:
        with Path.open(public_key_path, "rb") as f:
            return RSA.import_key(f.read())

    except (ValueError, KeyError):
        logger.exception("Decryption failed: Invalid PIN or corrupted key. Error: %s")
        raise
    except FileNotFoundError:
        logger.exception("File not found: %s", public_key_path)
        raise
    except Exception:
        logger.exception("Unexpected error during RSA key decryption: %s")
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
            progress_signal.emit("RSA key successfully decrypted!", 99)

        logger.info("RSA key successfully decrypted.")

    except (ValueError, KeyError):
        logger.exception("Decryption failed: Invalid PIN or corrupted key. Error: %s")
        msg = "Decryption failed: Invalid PIN or corrupted key."
        raise Exception(msg)
    except FileNotFoundError:
        logger.exception("File not found: %s", private_key_path)
        msg = f"File not found {private_key_path}"
        raise Exception(msg)
    except Exception:
        logger.exception("Unexpected error during RSA key decryption")
        msg = "Unexpected error during RSA key decryption, check log"
        raise Exception(msg)

    return rsa_key
