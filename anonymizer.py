# anonymizer.py
import hashlib

SECRET_SALT = "replace_with_random_string"

def anon_name(user_id, post_id):
    raw = f"{user_id}:{post_id}:{SECRET_SALT}".encode()
    return "User_" + hashlib.sha256(raw).hexdigest()[:8]
