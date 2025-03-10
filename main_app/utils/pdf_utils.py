import logging
import time
from pathlib import Path

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from PyPDF2 import PdfReader, PdfWriter

logger = logging.getLogger("global_logger")

def sign_pdf(pdf_path: str, rsa_key: RSA.RsaKey, progress_signal=None):
    check_pdf_exists(pdf_path, progress_signal)
    try:
        pdf_path = initialize_signing_process(pdf_path, progress_signal)
        pdf_content = read_pdf_file(pdf_path)
        pdf_hash = hash_pdf(pdf_content, progress_signal)

        temp_pdf_path = clear_signature_metadata(pdf_path)
        pdf_content = read_pdf_file(temp_pdf_path)
        pdf_hash = hash_pdf(pdf_content, progress_signal)

        signature = create_signature(rsa_key, pdf_hash, progress_signal)
        result_path = add_signature_to_pdf(temp_pdf_path, signature, progress_signal)
        pdf_content = read_pdf_file(result_path)
        pdf_hash = hash_pdf(pdf_content, progress_signal)
    except Exception:
        logger.exception("Error while signing PDF File: %s")
        raise

def verify_pdf(pdf_path: str, public_key: RSA.RsaKey, progress_signal=None) -> bool:
    check_pdf_exists(pdf_path, progress_signal)
    try:
        reader, signature = read_pdf_metadata(pdf_path, progress_signal)
        pdf_hash = prepare_unsigned_pdf(reader, pdf_path, progress_signal)
        verify_signature(public_key, pdf_hash, signature, pdf_path, progress_signal)
    except Exception:
        logger.exception("Error verifying signature: %s", pdf_path)
        raise

def check_pdf_exists(pdf_path: str, progress_signal=None):
    if not Path(pdf_path).exists():
        logger.error("Didn't find pdf file: %s", pdf_path)
        if progress_signal:
            progress_signal.emit("Error: PDF file not found.", 100)
        msg = f"PDF file not found: {pdf_path}"
        raise FileNotFoundError(msg)

def initialize_signing_process(pdf_path: str, progress_signal=None):
    if progress_signal:
        progress_signal.emit("Initializing PDF File signing...", 20)
    logger.info("Signing PDF File: %s", pdf_path)
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    metadata = reader.metadata
    writer.add_metadata(metadata)

    with Path.open(pdf_path, "wb") as f:
        writer.write(f)
    return pdf_path

def read_pdf_file(pdf_path: str):
    with Path.open(pdf_path, "rb") as f:
        return f.read()

def clear_signature_metadata(pdf_path: str):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    with Path.open(pdf_path, "wb") as f:
        writer.write(f)

    logger.info("Signature metadata cleared. New file saved: %s", pdf_path)
    return pdf_path

def hash_pdf(pdf_content: bytes, progress_signal=None):
    if progress_signal:
        progress_signal.emit("Hashing PDF File...", 40)
    time.sleep(0.5)
    pdf_hash = SHA256.new(pdf_content)
    logger.info("Generated PDF hash: %s", pdf_hash.hexdigest())
    return pdf_hash

def create_signature(rsa_key: RSA.RsaKey, pdf_hash, progress_signal=None):
    if progress_signal:
        progress_signal.emit("Creating signature...", 60)
    time.sleep(0.5)
    signature = pkcs1_15.new(rsa_key).sign(pdf_hash)
    logger.info("Generated signature: %s", signature.hex())
    return signature

def add_signature_to_pdf(pdf_path, signature: bytes, progress_signal=None):
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

    return pdf_path

def save_signed_pdf(pdf_path: str, writer, progress_signal=None):
    with Path.open(pdf_path, "wb") as f:
        writer.write(f)

    if progress_signal:
        progress_signal.emit("Finalizing process...", 95)
    time.sleep(0.5)
    logger.info("PDF File successfully signed: %s", pdf_path)

def read_pdf_metadata(pdf_path: str, progress_signal=None):
    try:
        reader = PdfReader(pdf_path)
        signature_hex = reader.metadata.get("/Signature")
        if not signature_hex:
            msg = "No signature found in PDF metadata."
            raise ValueError(msg)  # noqa: TRY301

        logger.info("Retrieved signature from metadata: %s", signature_hex)
        return reader, bytes.fromhex(signature_hex)
    except Exception:
        logger.exception("Error reading PDF metadata: %s", pdf_path)
        if progress_signal:
            progress_signal.emit("Error: Failed to read PDF metadata.", 100)
        raise

def prepare_unsigned_pdf(reader, pdf_path: str, progress_signal=None):
    writer = PdfWriter()

    if progress_signal:
        progress_signal.emit("Extracting signature...", 50)
    time.sleep(1)

    try:
        for page in reader.pages:
            writer.add_page(page)

        temp_pdf_path = pdf_path.replace(".pdf", "_temp.pdf")
        with Path.open(temp_pdf_path, "wb") as f:
            writer.write(f)

        with Path.open(temp_pdf_path, "rb") as f:
            pdf_content = f.read()

        return SHA256.new(pdf_content)
    except Exception:
        logger.exception("Error processing PDF file: %s", pdf_path)
        if progress_signal:
            progress_signal.emit("Error: Failed to process PDF file.", 100)
        raise

def verify_signature(public_key: RSA.RsaKey, pdf_hash, signature: bytes, pdf_path: str, progress_signal=None):
    if progress_signal:
        progress_signal.emit("Verifying signature...", 80)
    time.sleep(1)

    try:
        logger.info("Verifying signature with hash: %s", pdf_hash.hexdigest())
        logger.info("Signature to verify: %s", signature.hex())
        pkcs1_15.new(public_key).verify(pdf_hash, signature)
        logger.info("Signature verification successful for PDF: %s", pdf_path)
        if progress_signal:
            progress_signal.emit("Signature verification successful.", 100)
    except (ValueError, TypeError):
        logger.exception("Signature verification failed for PDF: %s", pdf_path)
        if progress_signal:
            progress_signal.emit("Error: Signature verification failed.", 100)
        msg = "Signature verification failed."
        raise ValueError(msg)
