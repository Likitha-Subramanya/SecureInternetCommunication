from crypto_utils import (
    generate_aes_key,
    encrypt_message,
    decrypt_message,
    generate_rsa_keys,
    encrypt_aes_key,
    decrypt_aes_key
)


# Generate RSA key pair
private_key, public_key = generate_rsa_keys()

# Generate AES key
aes_key = generate_aes_key()

# Original message
original_message = "Hello Secure World"

# Encrypt message using AES
nonce, encrypted_message = encrypt_message(
    original_message,
    aes_key
)

# Encrypt AES key using RSA public key
encrypted_aes_key = encrypt_aes_key(
    aes_key,
    public_key
)

# Receiver decrypts AES key using RSA private key
decrypted_aes_key = decrypt_aes_key(
    encrypted_aes_key,
    private_key
)

# Receiver decrypts message using recovered AES key
decrypted_message = decrypt_message(
    nonce,
    encrypted_message,
    decrypted_aes_key
)

print("Original Message:", original_message)
print("Encrypted Message:", encrypted_message.hex())
print("Decrypted Message:", decrypted_message)

if original_message == decrypted_message:
    print("Secure communication successful")
else:
    print("Secure communication failed")