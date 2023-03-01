import hashlib

# locatie van de file die de seed bevat
SEED_FILE = '../var/commitextractor.seed'

global seed_value


def make_hash(plaintext):
    # maak een hash voor een username of emailadres
    if 'seed_value' not in globals():
        _store_seedfile()
    seededtext = seed_value + plaintext
    hash_object = hashlib.sha256(seededtext.encode())
    hash_value = hash_object.hexdigest()
    return hash_value


def _store_seedfile():
    # Bewaar de seed value, zodat we maar 1 keer de file hoeven uit te lezen.
    seedfile = open(SEED_FILE, 'r')
    global seed_value
    seed_value = seedfile.read()
    seedfile.close()
