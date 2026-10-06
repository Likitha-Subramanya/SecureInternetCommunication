from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os


KEY_FOLDER = "app/keys"

PRIVATE_KEY_FILE = os.path.join(
    KEY_FOLDER,
    "server_private_key.pem"
)

PUBLIC_KEY_FILE = os.path.join(
    KEY_FOLDER,
    "server_public_key.pem"
)


def load_or_generate_keys():

    os.makedirs(KEY_FOLDER, exist_ok=True)

    # Generate keys if they do not already exist
    if not os.path.exists(PRIVATE_KEY_FILE):

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        public_key = private_key.public_key()

        # Save private key
        with open(PRIVATE_KEY_FILE, "wb") as file:
            file.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

        # Save public key
        with open(PUBLIC_KEY_FILE, "wb") as file:
            file.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )

    # Load private key
    with open(PRIVATE_KEY_FILE, "rb") as file:
        private_key = serialization.load_pem_private_key(
            file.read(),
            password=None
        )

    # Load public key
    with open(PUBLIC_KEY_FILE, "rb") as file:
        public_key = serialization.load_pem_public_key(
            file.read()
        )

    return private_key, public_key