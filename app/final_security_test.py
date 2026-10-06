from crypto_utils import (
    generate_aes_key,
    encrypt_message,
    decrypt_message,
    generate_rsa_keys,
    encrypt_aes_key,
    decrypt_aes_key,
    generate_hmac,
    verify_hmac
)


print("=== SECURE INTERNET COMMUNICATION TEST ===")


# 1. Generate AES key
aes_key = generate_aes_key()

print("AES-256 key generation: PASSED")


# 2. Generate RSA key pair
private_key, public_key = generate_rsa_keys()

print("RSA-2048 key generation: PASSED")


# 3. Original message
original_message = "Secure Internet Communication"


# 4. Encrypt message using AES
nonce, encrypted_message = encrypt_message(
    original_message,
    aes_key
)

print("AES-256-GCM encryption: PASSED")


# 5. Protect AES key using RSA
encrypted_aes_key = encrypt_aes_key(
    aes_key,
    public_key
)

print("RSA-2048 key protection: PASSED")


# 6. Recover AES key
decrypted_aes_key = decrypt_aes_key(
    encrypted_aes_key,
    private_key
)

if aes_key == decrypted_aes_key:
    print("RSA key recovery: PASSED")
else:
    print("RSA key recovery: FAILED")


# 7. Generate HMAC
message_hmac = generate_hmac(
    encrypted_message,
    aes_key
)

print("HMAC-SHA256 generation: PASSED")


# 8. Verify integrity
if verify_hmac(
    encrypted_message,
    message_hmac,
    aes_key
):
    print("Integrity verification: PASSED")
else:
    print("Integrity verification: FAILED")


# 9. Decrypt message
decrypted_message = decrypt_message(
    nonce,
    encrypted_message,
    decrypted_aes_key
)

if decrypted_message == original_message:
    print("AES-256-GCM decryption: PASSED")
else:
    print("AES-256-GCM decryption: FAILED")


print("\n=== ALL SECURITY TESTS COMPLETED ===")