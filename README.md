# Secure Internet Communication Using Cryptography

## Project Overview

Secure Internet Communication Using Cryptography is a secure client-server communication system developed using cryptographic techniques. The system allows registered users to log in, send messages to other users, and receive messages securely.

Messages are encrypted before being stored in the MySQL database, while HTTPS/TLS protects communication between the browser and server.

## Objectives

- Develop a secure client-server communication system.
- Protect messages from unauthorized access.
- Encrypt messages before database storage.
- Securely protect the AES encryption key using RSA.
- Provide message integrity and tamper detection.
- Secure browser-to-server communication using HTTPS/TLS.
- Prevent replay attacks using unique request IDs.
- Verify the implemented security mechanisms using automated tests.

## Technologies Used

| Component | Technology |
|---|---|
| Programming Language | Python |
| Web Framework | Flask |
| Database | MySQL |
| Symmetric Encryption | AES-256-GCM |
| Asymmetric Encryption | RSA-2048 |
| Key Protection | RSA-OAEP with SHA-256 |
| Integrity Verification | HMAC-SHA256 |
| Transport Security | HTTPS / TLS 1.3 |
| Authentication | Flask Sessions + Password Hashing |
| Certificate Generation | OpenSSL |
| Frontend | HTML / CSS |
| IDE | Visual Studio Code |

## System Architecture

```text
                    CLIENT / BROWSER
                          |
                          | HTTPS / TLS 1.3
                          v
                 +-------------------+
                 |   Flask Server    |
                 +-------------------+
                          |
              +-----------+-----------+
              |                       |
              v                       v
       Authentication          Cryptographic Layer
              |                       |
       Password Hashing        AES-256-GCM
                                      |
                              RSA-2048 OAEP
                                      |
                              HMAC-SHA256
                                      |
                                      v
                              +---------------+
                              |     MySQL     |
                              |   Database    |
                              +---------------+
```

## Security Workflow

### Sending a Message

1. The user logs into the system.
2. The sender selects a registered receiver.
3. A unique request ID is generated for the message request.
4. A new AES-256 key is generated.
5. The message is encrypted using AES-256-GCM.
6. A unique nonce is generated for AES-GCM.
7. The AES key is encrypted using the server's RSA-2048 public key with OAEP and SHA-256.
8. HMAC-SHA256 is generated for the encrypted message as an additional integrity layer.
9. The encrypted data and cryptographic metadata are stored in MySQL.
10. The security result is displayed to the sender.

### Receiving a Message

1. The authenticated receiver opens the inbox.
2. The server retrieves the encrypted message and cryptographic metadata.
3. The RSA private key is used to recover the AES key.
4. HMAC-SHA256 integrity is verified.
5. AES-256-GCM decrypts the message if integrity verification succeeds.
6. The decrypted message is displayed to the authorized receiver.

## Cryptographic Techniques

### AES-256-GCM

AES-256-GCM is used for message encryption.

- 256-bit symmetric key
- 12-byte nonce
- Provides confidentiality
- Provides authenticated encryption and detects modified ciphertext

A fresh nonce is generated for each encryption.

### RSA-2048

RSA-2048 is used to protect the AES key.

The system uses:

- RSA key size: 2048 bits
- OAEP padding
- SHA-256
- Public key for encryption
- Private key for decryption

The RSA private key is stored on the server.

### HMAC-SHA256

HMAC-SHA256 is used as an additional explicit integrity verification mechanism.

It allows the system to detect whether the encrypted message has been modified.

> Note: AES-GCM already provides authenticated integrity through its GCM authentication tag. HMAC is retained in this project as an additional academic integrity layer and explicit demonstration of HMAC-based tamper detection.

## Authentication and Session Security

User passwords are not stored as plaintext. The application uses password hashing through Werkzeug.

The Flask session is configured with:

- `SESSION_COOKIE_SECURE = True`
- `SESSION_COOKIE_HTTPONLY = True`
- `SESSION_COOKIE_SAMESITE = "Lax"`

The application also uses security headers to improve browser-side protection.

## HTTPS / TLS Security

The application runs using HTTPS instead of plain HTTP.

A local self-signed certificate was generated using OpenSSL:

```text
app/certs/cert.pem
app/certs/key.pem
```

The Flask application loads these certificate files when starting the server.

The application is accessed locally using:

```text
https://localhost:5000
```

The certificate has been trusted locally on the development machine.

### Security Headers

The application sends:

- Strict-Transport-Security
- X-Content-Type-Options
- X-Frame-Options
- Content-Security-Policy

## Replay Attack Protection

Each message request contains a unique UUID-based request ID.

Before processing a message, the server checks whether the request ID has already been used.

If the same request ID is submitted again, the server rejects it with:

```text
Security Error: Replay attack detected.
```

The request ID is stored in the database with a unique constraint.

## Database

The project uses MySQL with the database:

```text
secure_communication
```

### Users Table

Stores:

- User ID
- Username
- Password hash
- Account creation time

### Messages Table

Stores:

- Message ID
- Sender
- Receiver
- Request ID
- Encrypted message
- AES-GCM nonce
- RSA-encrypted AES key
- HMAC
- Creation timestamp

Plaintext message content is not stored in the messages table.

## Project Structure

```text
SecureInternetCommunication/
│
├── venv/
│
├── app/
│   ├── app.py
│   ├── crypto_utils.py
│   ├── database.py
│   ├── init_db.py
│   ├── key_manager.py
│   ├── verify_network_security.py
│   ├── secure_communication_test.py
│   ├── test_security.py
│   ├── final_security_test.py
│   │
│   ├── certs/
│   │   ├── cert.pem
│   │   └── key.pem
│   │
│   ├── keys/
│   │   ├── server_private_key.pem
│   │   └── server_public_key.pem
│   │
│   └── templates/
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── send.html
│       ├── receive.html
│       ├── messages.html
│       ├── message_result.html
│       └── security.html
│
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.x
- MySQL Server
- MySQL Workbench
- Visual Studio Code
- OpenSSL

### Create Virtual Environment

From the project directory:

```cmd
python -m venv venv
```

Activate it:

```cmd
venv\Scripts\activate
```

### Install Required Packages

```cmd
pip install flask cryptography mysql-connector-python werkzeug
```

## Database Setup

Create the database in MySQL:

```sql
CREATE DATABASE secure_communication;
```

Select it:

```sql
USE secure_communication;
```

Initialize the users table:

```cmd
cd app
python init_db.py
```

The messages table contains:

```text
id
sender
receiver
request_id
encrypted_message
nonce
encrypted_aes_key
hmac
created_at
```

## Running the Application

Activate the virtual environment:

```cmd
venv\Scripts\activate
```

Go to the app folder:

```cmd
cd app
```

Start the Flask server:

```cmd
python app.py
```

Open the application in Chrome:

```text
https://localhost:5000
```

## Security Verification

The project includes an automated network security verification script:

```cmd
python verify_network_security.py
```

The script verifies:

1. TLS handshake
2. Plaintext HTTP rejection
3. AES-256-GCM encryption/decryption
4. AES-GCM tamper detection
5. HMAC-SHA256 integrity verification
6. AES-GCM nonce uniqueness

### Verification Result

All network security verification tests passed:

```text
=======================================================
 SECURE INTERNET COMMUNICATION
 NETWORK SECURITY VERIFICATION
=======================================================

[PASS] TLS handshake (TLSv1.3)
[PASS] Plaintext HTTP rejected
[PASS] AES-256-GCM encryption/decryption
[PASS] AES-GCM tamper detection
[PASS] HMAC-SHA256 integrity verification
[PASS] AES-GCM nonce uniqueness

=======================================================
 ALL NETWORK SECURITY TESTS PASSED
=======================================================
```

## Security Test Results

Additional testing was performed for:

- AES-256 encryption and decryption
- RSA-2048 key generation
- RSA-based AES key protection
- RSA key recovery
- HMAC-SHA256 generation
- HMAC integrity verification
- AES-GCM tamper detection
- Persistent RSA key management
- Receiver-side message decryption
- Replay attack detection
- HTTPS/TLS communication

Final cryptographic security testing:

```text
=== SECURE INTERNET COMMUNICATION TEST ===
AES-256 key generation: PASSED
RSA-2048 key generation: PASSED
AES-256-GCM encryption: PASSED
RSA-2048 key protection: PASSED
RSA key recovery: PASSED
HMAC-SHA256 generation: PASSED
Integrity verification: PASSED
AES-256-GCM decryption: PASSED
=== ALL SECURITY TESTS COMPLETED ===
```

## Attack and Protection Demonstrations

### Message Tampering

If the encrypted message stored in the database is modified, integrity verification fails and the receiver does not accept the message as valid.

```text
Security Error: Message integrity verification failed.
```

### Replay Attack

If a previously processed request ID is submitted again, the server rejects the request:

```text
Security Error: Replay attack detected.
```

### Plaintext Storage Protection

Messages are stored as ciphertext rather than plaintext in MySQL.

### Network Protection

Browser-to-server communication uses HTTPS/TLS 1.3.

## Security Architecture Note

This project is a **secure client-server communication system**, not a true end-to-end encrypted messaging system.

The server owns the RSA private key and can recover the AES key. Therefore, the server is part of the trusted security boundary.

In a true E2EE architecture, private keys would be controlled by the communicating clients/recipients and the server would not have the ability to decrypt message content.

## Limitations

1. The project uses a locally trusted self-signed TLS certificate for development.
2. The server holds the RSA private key and is therefore trusted with message decryption.
3. HMAC-SHA256 is an additional integrity layer; AES-GCM already provides authenticated integrity.
4. The system is intended as an academic secure communication demonstration rather than a production messaging platform.
5. Production deployment would require proper certificate authority management, hardened key storage, secure secret management, and additional operational security controls.

## Future Enhancements

- True end-to-end encryption
- Per-user RSA key pairs
- Hardware-backed/private key storage
- Multi-factor authentication
- Certificate Authority-based TLS certificates for deployment
- Mutual TLS (mTLS)
- Secure key rotation
- Message expiration
- File encryption and secure file transfer
- Rate limiting and account lockout
- Production-grade secret management

## Conclusion

The project demonstrates how multiple cryptographic and network security mechanisms can be combined to build a secure client-server communication system.

HTTPS/TLS 1.3 protects communication in transit, AES-256-GCM provides message confidentiality, RSA-2048 protects the symmetric AES key, HMAC-SHA256 provides an explicit integrity verification layer, password hashing protects user credentials, and replay protection prevents reuse of previously processed requests.

The implemented security verification tests successfully passed, demonstrating the functioning of the major security components of the system.
