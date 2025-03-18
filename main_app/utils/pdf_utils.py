import logging
import time
from pathlib import Path

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from PyPDF2 import PdfReader, PdfWriter

logger = logging.getLogger("global_logger")

def sign_pdf(pdf_path: str, rsa_key: RSA.RsaKey, progress_signal=None):
    """
    Signs a PDF file using the provided RSA key.

    Args:
        pdf_path (str): The path to the PDF file to be signed.
        rsa_key (RSA.RsaKey): The RSA key to use for signing the PDF.
        progress_signal (optional): A signal to report progress, if applicable.

    Raises:
        Exception: If an error occurs during the signing process.

    This function performs the following steps:
        1. Checks if the PDF file exists.
        2. Initializes the signing process.
        3. Reads the content of the PDF file.
        4. Initializes the PDF writer and reader.
        5. Hashes the PDF content.
        6. Creates a signature using the RSA key and the PDF hash.
        7. Adds the signature to the PDF.
        8. Saves the signed PDF file.

    """
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
    """
    Verifies the digital signature of a PDF file.

    Args:
        pdf_path (str): The file path to the PDF document to be verified.
        public_key (RSA.RsaKey): The public RSA key used to verify the signature.
        progress_signal (optional): A signal to report progress, if applicable.

    Returns:
        bool: True if the PDF signature is valid, False otherwise.

    Raises:
        Exception: If an error occurs during the verification process.

    """
    check_pdf_exists(pdf_path, progress_signal)
    try:
        reader, signature = read_pdf_metadata(pdf_path, progress_signal)
        pdf_hash = prepare_unsigned_pdf(reader, pdf_path, progress_signal)
        verify_signature(public_key, pdf_hash, signature, pdf_path, progress_signal)
    except Exception:
        logger.exception("Error verifying signature: %s", pdf_path)
        raise

def check_pdf_exists(pdf_path: str, progress_signal=None):
    """
    Checks if a PDF file exists at the given path.

    Args:
        pdf_path (str): The path to the PDF file.
        progress_signal (optional): A signal to emit progress updates.
                                    If provided, emits an error message with 100% progress if the file is not found.

    Raises:
        FileNotFoundError: If the PDF file does not exist at the specified path.

    """
    if not Path(pdf_path).exists():
        logger.error("Didn't find pdf file: %s", pdf_path)
        if progress_signal:
            progress_signal.emit("Error: PDF file not found.", 100)
        msg = f"PDF file not found: {pdf_path}"
        raise FileNotFoundError(msg)

def initialize_signing_process(pdf_path: str, progress_signal=None):
    """
    Initializes the process of signing a PDF file.

    Args:
        pdf_path (str): The path to the PDF file that needs to be signed.
        progress_signal (optional): A signal object to emit progress updates.
                                    If provided, it should have an `emit` method
                                    that accepts a message and a progress percentage.

    Returns:
        None

    """
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
    """
    Reads the content of a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        bytes: The content of the PDF file as bytes.

    """
    with Path.open(pdf_path, "rb") as f:
        return f.read()

def clear_signature_metadata(pdf_path: str):
    """
    Removes signature metadata from the PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The path to the cleaned PDF file.

    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    with Path.open(pdf_path, "wb") as f:
        writer.write(f)

    logger.info("Signature metadata cleared. New file saved: %s", pdf_path)
    return pdf_path

def hash_pdf(pdf_content: bytes, progress_signal=None):
    """
    Hashes the content of a PDF file using SHA-256.

    Args:
        pdf_content (bytes): The content of the PDF file to be hashed.
        progress_signal (optional): A signal to emit progress updates.
                                    If provided, it will emit a message indicating the progress of the hashing process.

    Returns:
        SHA256: The SHA-256 hash object of the PDF content.

    """
    if progress_signal:
        progress_signal.emit("Hashing PDF File...", 40)
    time.sleep(0.5)
    pdf_hash = SHA256.new(pdf_content)
    logger.info("Generated PDF hash: %s", pdf_hash.hexdigest())
    return pdf_hash

def create_signature(rsa_key: RSA.RsaKey, pdf_hash, progress_signal=None):
    """
    Creates a digital signature for a given PDF hash using the provided RSA key.

    Args:
        rsa_key (RSA.RsaKey): The RSA key to sign the PDF hash.
        pdf_hash: The hash of the PDF to be signed.
        progress_signal (optional): A signal to emit progress updates. Defaults to None.

    Returns:
        bytes: The digital signature of the PDF hash.

    """
    if progress_signal:
        progress_signal.emit("Creating signature...", 60)
    time.sleep(0.5)
    signature = pkcs1_15.new(rsa_key).sign(pdf_hash)
    logger.info("Generated signature: %s", signature.hex())
    return signature

def add_signature_to_pdf(pdf_path, signature: bytes, progress_signal=None):
    """
    Adds a digital signature to the metadata of the PDF file.

    Args:
        pdf_path (str): The path to the PDF file.
        signature (bytes): The digital signature to be added.
        progress_signal (optional): A signal to emit progress updates.

    Returns:
        str: The path to the signed PDF file.

    """
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
    """
    Saves the signed PDF file.

    Args:
        pdf_path (str): The path to save the signed PDF file.
        writer (PdfWriter): The PdfWriter object containing the signed content.
        progress_signal (optional): A signal to emit progress updates.

    """
    with Path.open(pdf_path, "wb") as f:
        writer.write(f)

    if progress_signal:
        progress_signal.emit("Finalizing process...", 95)
    time.sleep(0.5)
    logger.info("PDF File successfully signed: %s", pdf_path)

def read_pdf_metadata(pdf_path: str, progress_signal=None):
    """
    Reads the metadata of a PDF file to extract the signature.

    Args:
        pdf_path (str): The path to the PDF file.
        progress_signal (optional): A signal to emit progress updates. Defaults to None.

    Returns:
        tuple: A tuple containing the PdfReader object and the signature in bytes.

    Raises:
        ValueError: If no signature is found in the PDF metadata.
        Exception: If there is an error reading the PDF metadata.

    """
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
    """
    Creates a temporary unsigned version of the PDF for signature verification.

    Args:
        reader (PdfReader): The PdfReader object of the original PDF.
        pdf_path (str): The path to the original PDF file.
        progress_signal (optional): A signal to emit progress updates.

    Returns:
        SHA256.SHA256Hash: The hash of the unsigned PDF content.

    """
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
        
        Path(temp_pdf_path).unlink()

        return SHA256.new(pdf_content)
    except Exception:
        logger.exception("Error processing PDF file: %s", pdf_path)
        if progress_signal:
            progress_signal.emit("Error: Failed to process PDF file.", 100)
        raise

def verify_signature(public_key: RSA.RsaKey, pdf_hash, signature: bytes, pdf_path: str, progress_signal=None):
    """
    Verifies the digital signature of a PDF document.

    Args:
        public_key (RSA.RsaKey): The RSA public key used to verify the signature.
        pdf_hash: The hash of the PDF document.
        signature (bytes): The digital signature to be verified.
        pdf_path (str): The file path of the PDF document.
        progress_signal (optional): A signal to emit progress updates.

    Raises:
        ValueError: If the signature verification fails.
    Emits:
        progress_signal: Emits progress updates if provided.

    """
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
