from argon2 import PasswordHasher

# ? consider using my own configuration for PasswordHasher instead of the default
ph = PasswordHasher()

def hash_password(password) -> str:
    return ph.hash(password)


def verify_hash(password_hash, password) -> bool:
    try:
        return ph.verify(password_hash, password)
    except Exception:
        return False