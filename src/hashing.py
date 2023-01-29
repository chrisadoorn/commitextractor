import hashlib


def make_hash(plaintext):
    hash_object = hashlib.sha256(plaintext.encode())
    hash_value = hash_object.hexdigest()
    return hash_value
