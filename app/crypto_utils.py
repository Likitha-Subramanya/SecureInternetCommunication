from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, hmac
import os


# AES-256 key generation
def generate_aes_key():
    return AESGCM.generate_key(bit_length=256)


# AES-256-GCM encryption
def encrypt_message(message, key):
    aes = AESGCM(key)

    nonce = os.urandom(12)

    encrypted_message = aes.encrypt(
        nonce,
        message.encode(),
        None
    )

    return nonce, encrypted_message


# AES-256-GCM decryption
def decrypt_message(nonce, encrypted_message, key):
    aes = AESGCM(key)

    decrypted_message = aes.decrypt(
        nonce,
        encrypted_message,
        None
    )

    return decrypted_message.decode()


# RSA-2048 key pair generation
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    return private_key, public_key


# Encrypt AES key using RSA public key
def encrypt_aes_key(aes_key, public_key):
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_key


# Decrypt AES key using RSA private key
def decrypt_aes_key(encrypted_key, private_key):
    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return aes_key


# Generate HMAC-SHA256
def generate_hmac(message, key):
    h = hmac.HMAC(
        key,
        hashes.SHA256()
    )

    h.update(message)

    return h.finalize()


# Verify HMAC-SHA256
def verify_hmac(message, received_hmac, key):
    h = hmac.HMAC(
        key,
        hashes.SHA256()
    )

    h.update(message)

    try:
        h.verify(received_hmac)
        return True
    except Exception:
        return False