from cryptography.fernet import Fernet
import json

# Should this be an env variable?
STATIC_KEY = "4xu3i8YiTDl5Zm7HOAZTPlHh3gpqBbe7Gfn6vanqPyI=".encode()

f = Fernet(STATIC_KEY)


def decrypt_token(token) -> tuple:
    decrypted = f.decrypt(token).decode()
    return json.loads(decrypted)


def encrypt_token(google_id, last_login) -> str:
    byte_string = json.dumps({"google_id": google_id, "last_login": str(last_login)}).encode()
    return f.encrypt(byte_string).decode()
