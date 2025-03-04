# Tool for Emulating the PAdES Qualified Electronic Signature

## Project Overview

This project aims to develop a software tool that emulates a **qualified electronic signature** according to the **PAdES (PDF Advanced Electronic Signature)** standard. The primary objective is to provide a secure method for digitally signing PDF documents using RSA encryption, with the private key stored on a USB drive encrypted by the AES algorithm.

---

## 📌 Project Goals
1. **Develop an application** for generating and verifying PAdES-compliant electronic signatures.
2. Implement a **hardware-based** approach using a USB drive to securely store the private RSA key.
3. Ensure the application can both **sign** and **verify** PDF documents.
4. Provide a **user-friendly GUI** for easy interaction.

---

## 🛠️ Features and Requirements

### Main Features:
- **RSA Key Generation**: Create a 4096-bit RSA key pair using a pseudorandom generator.
- **Private Key Encryption**: Encrypt the private key with AES-256 using a PIN-derived hash.
- **USB Integration**: Automatically detect a USB drive containing the encrypted private key.
- **PAdES Signature**: Embed the digital signature inside the PDF document.
- **Signature Verification**: Verify the document's integrity using the public RSA key.
- **User Authentication**: Require PIN input to decrypt the private key before signing.
- **Status/Message Icons**: Display application states (e.g., hardware detection, signing status).

### Technical Requirements:
- **Encryption Algorithms**: RSA (4096-bit) and AES (256-bit in CBC mode).
- **GUI**: Enable PDF selection, signing, and verification.
- **Language**: Any programming language can be used.
- **Doxygen Documentation**: Provide full code documentation.
- **GitHub Repository**: Host the source code and share the link in the final report.

---

## 📚 Usage Workflow

1. **RSA Key Generation**:
   - Use the auxiliary app to generate RSA keys.
   - Store the encrypted private key on a USB drive (secured with AES and PIN).
2. **PDF Signing**:
   - Select a PDF document through the main application.
   - Insert the USB drive and enter the correct PIN to sign the document.
3. **Signature Verification**:
   - Use the public key to verify the document’s authenticity and integrity through the main application.

---