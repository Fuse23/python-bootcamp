import unittest
from key import Key


class TestKey(unittest.TestCase):
    def setUp(self):
        self.key = Key()


    def test_init(self):
        self.assertEqual(
            first=self.key.passphrase,
            second="zax2rulez",
            msg="key.passphrase == 'zax2rulez'"
        )
        self.assertNotEqual(
            first=self.key.passphrase,
            second="zax2",
            msg="key.passphrase == 'zax2'"
        )


    def test_str(self):
        self.assertEqual(
            first=str(self.key),
            second="GeneralTsoKeycard",
            msg="str(key) == 'GeneralTsoKeycard'"
        )
        self.assertNotEqual(
            first=str(self.key),
            second="General",
            msg="str(key) == 'General'"
        )


    def test_len(self):
        self.assertEqual(
            first=len(self.key),
            second=1337,
            msg="len(key) == 1337"
        )
        self.assertNotEqual(
            first=len(self.key),
            second=133,
            msg="len(key) == 133"
        )


    def test_gt(self):
        self.assertTrue(
            expr=self.key > 9000,
            msg="key > 9000"
        )
        self.assertFalse(
            expr=self.key == 9000,
            msg="key == 9000"
        )


    def test_getitem(self):
        self.assertEqual(
            first=self.key[404],
            second=3,
            msg="key[404] == 3"
        )
        self.assertNotEqual(
            first=self.key[4],
            second=3,
            msg="key[4] == 3"
        )


if __name__ == "__main__":
    unittest.main()
