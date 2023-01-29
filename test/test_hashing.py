import unittest
from src import hashing
from unittest import TestCase


class Test(TestCase):
    def test_make_hash(self):
        verwacht = 'c5d1859a5cfbf15bdc3d976a2a67537a84250ed801f74deb24d5de00bec41390'
        resultaat = hashing.make_hash(plaintext='test dit')
        print(resultaat)
        unittest.TestCase.assertEqual(self, verwacht, resultaat, 'hashes matchen niet!')
