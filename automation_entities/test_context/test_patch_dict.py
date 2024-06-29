import unittest

from ..context import patch_dict


class TestPatchDict(unittest.TestCase):
    original: dict
    patch: dict

    def setUp(self) -> None:
        self.original = {}
        self.patch = {}

    def test_empty(self) -> None:
        patch_dict(self.original, self.patch)
        self.assertEqual({}, self.original)

    def test_set_key(self) -> None:
        self.patch["key"] = "val"
        patch_dict(self.original, self.patch)
        self.assertEqual({"key": "val"}, self.original)

    def test_override_key(self) -> None:
        self.original["key"] = "val1"
        self.patch["key"] = "val2"
        patch_dict(self.original, self.patch)
        self.assertEqual({"key": "val2"}, self.original)

    def test_set_different_key(self) -> None:
        self.original["key1"] = "val1"
        self.patch["key2"] = "val2"
        patch_dict(self.original, self.patch)
        self.assertEqual(
            {
                "key1": "val1",
                "key2": "val2",
            },
            self.original,
        )

    def test_recurse_empty(self) -> None:
        self.patch["key"] = {}
        patch_dict(self.original, self.patch)
        self.assertEqual(
            {
                "key": {},
            },
            self.original,
        )

    def test_recurse_set(self) -> None:
        self.original["key1"] = "val1"
        self.original["key2"] = "val2-1"
        self.original["recurse"] = {}
        self.patch["key2"] = "val2-2"
        self.patch["recurse"] = {"recurse-key1": "recurse-val1"}
        patch_dict(self.original, self.patch)
        self.assertEqual(
            {
                "key1": "val1",
                "key2": "val2-2",
                "recurse": {"recurse-key1": "recurse-val1"},
            },
            self.original,
        )
