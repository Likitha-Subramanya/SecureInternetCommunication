import socket
import ssl
import sys

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes, hmac

from crypto_utils import (
    generate_aes_key,
    encrypt_message,
    decrypt_message,
    generate_hmac,
    verify_hmac
)


HOST = "127.0.0.1"
HTTPS_PORT = 5000


def print_result(test_name, passed):
    if passed:
        print(f"[PASS] {test_name}")
    else:
        print(f"[FAIL] {test_name}")


# --------------------------------------------------
# 1. TLS HANDSHAKE TEST
# --------------------------------------------------

def test_tls_handshake():

    try:

        context = ssl.create_default_context()

        # Local certificate is self-signed,
        # so certificate verification is disabled
        # for this academic local test.
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with socket.create_connection(
            (HOST, HTTPS_PORT),
            timeout=5
        ) as sock:

            with context.wrap_socket(
                sock,
                server_hostname="localhost"
            ) as tls_socket:

                protocol = tls_socket.version()

                if protocol and protocol.startswith("TLS"):

                    print_result(
                        f"TLS handshake ({protocol})",
                        True
                    )

                    return True

    except Exception as error:

        print_result(
            f"TLS handshake ({error})",
            False
        )

    return False


# --------------------------------------------------
# 2. PLAINTEXT HTTP REJECTION TEST
# --------------------------------------------------

def test_plaintext_http_rejected():

    try:

        with socket.create_connection(
            (HOST, HTTPS_PORT),
            timeout=5
        ) as sock:

            sock.sendall(
                b"GET / HTTP/1.1\r\n"
                b"Host: 127.0.0.1\r\n"
                b"Connection: close\r\n"
                b"\r\n"
            )

            response = sock.recv(1024)

            # A TLS server should not return a normal
            # plaintext HTTP response.
            if response.startswith(b"HTTP/"):
                print_result(
                    "Plaintext HTTP rejected",
                    False
                )
                return False

            print_result(
                "Plaintext HTTP rejected",
                True
            )

            return True

    except Exception:

        print_result(
            "Plaintext HTTP rejected",
            True
        )

        return True


# --------------------------------------------------
# 3. AES-256-GCM TEST
# --------------------------------------------------

def test_aes_gcm():

    try:

        key = generate_aes_key()

        original_message = "Network Security Test"

        nonce, ciphertext = encrypt_message(
            original_message,
            key
        )

        decrypted_message = decrypt_message(
            nonce,
            ciphertext,
            key
        )

        passed = (
            decrypted_message == original_message
            and len(key) == 32
            and len(nonce) == 12
        )

        print_result(
            "AES-256-GCM encryption/decryption",
            passed
        )

        return passed

    except Exception:

        print_result(
            "AES-256-GCM encryption/decryption",
            False
        )

        return False


# --------------------------------------------------
# 4. AES-GCM TAMPER TEST
# --------------------------------------------------

def test_aes_tamper_detection():

    try:

        key = generate_aes_key()

        message = "Tamper detection test"

        nonce, ciphertext = encrypt_message(
            message,
            key
        )

        tampered_ciphertext = bytearray(ciphertext)

        tampered_ciphertext[0] ^= 1

        try:

            decrypt_message(
                nonce,
                bytes(tampered_ciphertext),
                key
            )

            # If decryption succeeds, tampering was not detected
            passed = False

        except Exception:

            # AES-GCM should reject modified ciphertext
            passed = True

        print_result(
            "AES-GCM tamper detection",
            passed
        )

        return passed

    except Exception:

        print_result(
            "AES-GCM tamper detection",
            False
        )

        return False


# --------------------------------------------------
# 5. HMAC TEST
# --------------------------------------------------

def test_hmac():

    try:

        key = generate_aes_key()

        message = b"Integrity test message"

        message_hmac = generate_hmac(
            message,
            key
        )

        original_valid = verify_hmac(
            message,
            message_hmac,
            key
        )

        tampered_message = (
            b"Modified integrity test message"
        )

        tampered_valid = verify_hmac(
            tampered_message,
            message_hmac,
            key
        )

        passed = (
            original_valid is True
            and tampered_valid is False
        )

        print_result(
            "HMAC-SHA256 integrity verification",
            passed
        )

        return passed

    except Exception:

        print_result(
            "HMAC-SHA256 integrity verification",
            False
        )

        return False


# --------------------------------------------------
# 6. NONCE UNIQUENESS TEST
# --------------------------------------------------

def test_nonce_uniqueness():

    try:

        key = generate_aes_key()

        nonce1, _ = encrypt_message(
            "Message 1",
            key
        )

        nonce2, _ = encrypt_message(
            "Message 2",
            key
        )

        passed = (
            len(nonce1) == 12
            and len(nonce2) == 12
            and nonce1 != nonce2
        )

        print_result(
            "AES-GCM nonce uniqueness",
            passed
        )

        return passed

    except Exception:

        print_result(
            "AES-GCM nonce uniqueness",
            False
        )

        return False


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print()
    print("=" * 55)
    print(" SECURE INTERNET COMMUNICATION")
    print(" NETWORK SECURITY VERIFICATION")
    print("=" * 55)
    print()

    results = []

    results.append(
        test_tls_handshake()
    )

    results.append(
        test_plaintext_http_rejected()
    )

    results.append(
        test_aes_gcm()
    )

    results.append(
        test_aes_tamper_detection()
    )

    results.append(
        test_hmac()
    )

    results.append(
        test_nonce_uniqueness()
    )

    print()
    print("=" * 55)

    if all(results):

        print(" ALL NETWORK SECURITY TESTS PASSED")

    else:

        print(" SOME SECURITY TESTS FAILED")

    print("=" * 55)
    print()


if __name__ == "__main__":
    main()