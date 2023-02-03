import hashlib

# maak een hash voor een username of emailadres
#TODO: meegeven van de seedvalue, zodat deze eenmalig uitgelezen wordt.
def make_hash(plaintext):

    seedfile = open('var/commitextractor.seed', 'r')
    seededtext = seedfile.read() + plaintext
    seedfile.close()

    hash_object = hashlib.sha256(seededtext.encode())
    hash_value = hash_object.hexdigest()
    return hash_value
