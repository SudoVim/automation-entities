import unittest

from ..utils import SecretString


class TestSecretString(unittest.TestCase):
    def test_obfuscates_string(self) -> None:
        s = SecretString("secret val")
        self.assertEqual("'**********'", repr(s))
