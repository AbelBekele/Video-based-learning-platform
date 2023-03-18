from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

def generate_has(pw_raw ):
    ph = PasswordHasher()
    return ph.hash(pw_raw)

def verify_hash(pw_hash, pw_raw):
    ph = PasswordHasher()
    verified = False
    msg = ""
    try:
        verified = ph.verify(pw_hash, pw_raw)
    except VerifyMismatchError:
        verified = False
        msg = "Incorrect password"
    except Exception as e:
        verified = False
        msg = f"Can't very hash: \n{e}"
    return verified
