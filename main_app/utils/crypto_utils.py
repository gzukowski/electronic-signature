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
            public_key = RSA.import_key(f.read())

        return public_key
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
        raise
    except FileNotFoundError:
        logger.exception("File not found: %s", private_key_path)
        raise
    except Exception:
        logger.exception("Unexpected error during RSA key decryption: %s")
        raise

    return rsa_key

def sign_pdf(pdf_path: str, rsa_key: RSA.RsaKey, progress_signal=None):
    try:
        if not Path(pdf_path).exists():
            logger.error("Didn't find pdf file: %s", pdf_path)
            raise

        if progress_signal:
            progress_signal.emit("Initializing PDF File signing...", 20)
        logger.info("Signing PDF File: %s", pdf_path)
        time.sleep(1)

        with Path.open(pdf_path, "rb") as f:
            pdf_content = f.read()

        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        metadata = reader.metadata
        if "/Signature" in metadata:
            logger.info("Existing signature found. Removing old signature...")
            del metadata["/Signature"]

        if progress_signal:
            progress_signal.emit("Hashing PDF File...", 40)
        time.sleep(0.5)
        pdf_hash = SHA256.new(pdf_content)

        if progress_signal:
            progress_signal.emit("Creating signature...", 60)
        time.sleep(0.5)
        signature = pkcs1_15.new(rsa_key).sign(pdf_hash)

        for page in reader.pages:
            writer.add_page(page)

        if progress_signal:
            progress_signal.emit("Adding signature to PDF File...", 80)
        time.sleep(0.5)
        writer.add_metadata({"/Signature": signature.hex()})

        signed_pdf_path = pdf_path.replace(".pdf", "_signed.pdf")

        with Path.open(signed_pdf_path, "wb") as f:
            writer.write(f)

        if progress_signal:
            progress_signal.emit("Finalizing process...", 95)
        time.sleep(0.5)
        logger.info("PDF File successfully signed: %s", signed_pdf_path)

    except Exception:
        logger.exception("Error while signing PDF File: %s")
        raise

def verify_pdf(pdf_path: str, public_key: RSA.RsaKey, progress_signal=None) -> bool:
    try:
        if not Path(pdf_path).exists():
            logger.error("Didn't find pdf file: %s", pdf_path)
            raise

        reader = PdfReader(pdf_path)
        signature_hex = reader.metadata.get("/Signature")
        if not signature_hex:
            logger.error("No signature found in PDF metadata: %s", pdf_path)
            raise
        signature = bytes.fromhex(signature_hex)

        metadata = reader.metadata.copy()
        del metadata["/Signature"]
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata(metadata)

        temp_pdf_path = pdf_path.replace(".pdf", "_temp.pdf")
        with Path.open(temp_pdf_path, "wb") as f:
            writer.write(f)

        with Path.open(temp_pdf_path, "rb") as f:
            pdf_content = f.read()

        Path(temp_pdf_path).unlink(missing_ok=True)

        pdf_hash = SHA256.new(pdf_content)

        logger.info("Verification %s", pdf_content)

        try:
            pkcs1_15.new(public_key).verify(pdf_hash, signature)
            logger.info("Signature verification successful for PDF: %s", pdf_path)
            #raise Exception("Gites")
        except (ValueError, TypeError):
            logger.exception("Signature verification failed for PDF: %s", pdf_path)
            raise Exception("Nie gites")

    except Exception:
        logger.exception("Error while verifying PDF File: %s", pdf_path)
        raise

