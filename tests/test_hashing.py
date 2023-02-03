import unittest
from src import hashing
from unittest import TestCase


class Test(TestCase):
    # tests of de juiste combinatie van hash methode en seed gebruikt wordt
    def test_make_hash(self):
        hashing.set_seed()
        verwacht = '50fc4dda8b91cda4664edc536b472f225c7731b35f4af7a47b11d7fa2e7ec208'
        resultaat = hashing.make_hash(plaintext='test dit')
        unittest.TestCase.assertEqual(self, verwacht, resultaat, 'hashes matchen niet!')
