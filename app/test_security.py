from crypto_utils import (
    generate_aes_key,
    encrypt_message,
    generate_hmac,
    verify_hmac
)


# Generate AES key
aes_key = generate_aes_key()

# Original message
message = "This is a secure message"

# Encrypt message
nonce, encrypted_message = encrypt_message(
    message,
    aes_key
)

# Generate HMAC
message_hmac = generate_hmac(
    encrypted_message,
    aes_key
)

# Verify original encrypted message
original_result = verify_hmac(
    encrypted_message,
    message_hmac,
    aes_key
)

# Simulate tampering
tampered_message = bytearray(encrypted_message)
tampered_message[0] ^= 1
tampered_message = bytes(tampered_message)

# Verify tampered message
tampered_result = verify_hmac(
    tampered_message,
    message_hmac,
    aes_key
)

print("Original message integrity:", original_result)
print("Tampered message integrity:", tampered_result)

if original_result and not tampered_result:
    print("Tamper detection successful")
else:
    print("Tamper detection failed")