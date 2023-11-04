import unittest
from unittest.mock import patch, MagicMock, call
from ..context import Config


class TestInitialize(unittest.TestCase):
    def test_no_defaults(self) -> None:
        config = Config()
        self.assertIsNone(config.filepath)
        self.assertIsNone(config.defaults)
        self.assertEqual({}, config._data)

    def test_with_defaults(self) -> None:
        defaults = {"key": "val"}
        config = Config(defaults=defaults)
        self.assertIsNone(config.filepath)
        self.assertEqual(defaults, config.defaults)
        self.assertEqual(defaults, config._data)


class ConfigTestCase(unittest.TestCase):
    DEFAULTS: dict = {"key": "val"}
    config: Config

    def setUp(self) -> None:
        self.config = Config(defaults=self.DEFAULTS)


class TestPatch(ConfigTestCase):
    def test_patch(self) -> None:
        self.config.patch({"key2": "val2"})
        self.assertEqual({"key": "val", "key2": "val2"}, self.config._data)


class TestSetFilepath(ConfigTestCase):
    @patch("builtins.open")
    @patch("os.path")
    def test_set_filepath(self, mock_path: MagicMock, mock_open: MagicMock) -> None:
        mock_path.is_file.return_value = True

        mock_fobj = MagicMock()
        mock_open.return_value = mock_fobj
        mock_fobj.__enter__.return_value = mock_fobj
        mock_fobj.read.return_value = '{"new-key":"new-val"}'

        self.config.set_filepath("config/filepath.json")
        self.assertEqual({"key": "val", "new-key": "new-val"}, self.config._data)


class TestPersist(ConfigTestCase):
    def test_no_filepath(self) -> None:
        with self.assertRaisesRegex(
            AssertionError, "filepath must be set before calling persist"
        ):
            self.config.persist()

    @patch("builtins.open")
    @patch("json.dump")
    def test_persist(self, mock_json_dump: MagicMock, mock_open: MagicMock) -> None:
        mock_fobj = MagicMock()
        mock_open.return_value = mock_fobj
        mock_fobj.__enter__.return_value = mock_fobj

        self.config.filepath = "config/filepath.json"
        self.config.persist()

        mock_open.assert_called_once_with("config/filepath.json", "w")
        mock_json_dump.assert_called_once_with(
            self.DEFAULTS, mock_fobj, sort_keys=True, indent=4
        )


class TestLoad(ConfigTestCase):
    def test_no_filepath(self) -> None:
        with self.assertRaisesRegex(
            AssertionError, "filepath must be set before calling load"
        ):
            self.config.load()

    @patch("builtins.open")
    @patch("os.path")
    @patch("json.dump")
    def test_no_file(
        self, mock_json_dump: MagicMock, mock_path: MagicMock, mock_open: MagicMock
    ) -> None:
        mock_path.isfile.return_value = False

        mock_fobj = MagicMock()
        mock_open.return_value = mock_fobj
        mock_fobj.__enter__.return_value = mock_fobj

        self.config.filepath = "config/filepath.json"
        self.config.load()

        mock_open.assert_called_once_with("config/filepath.json", "w")
        mock_json_dump.assert_called_once_with(
            self.DEFAULTS, mock_fobj, sort_keys=True, indent=4
        )

    @patch("builtins.open")
    @patch("os.path")
    @patch("json.dump")
    @patch("json.load")
    def test_file_exists(
        self,
        mock_json_load: MagicMock,
        mock_json_dump: MagicMock,
        mock_path: MagicMock,
        mock_open: MagicMock,
    ) -> None:
        mock_path.isfile.return_value = True

        mock_fobj = MagicMock()
        mock_open.return_value = mock_fobj
        mock_fobj.__enter__.return_value = mock_fobj

        mock_json_load.return_value = {"new-key": "new-val"}

        self.config.filepath = "config/filepath.json"
        self.config.load()

        mock_open.assert_any_call("config/filepath.json")
        mock_open.assert_any_call("config/filepath.json", "w")
        mock_json_dump.assert_called_once_with(
            dict(
                self.DEFAULTS,
                **{
                    "new-key": "new-val",
                }
            ),
            mock_fobj,
            sort_keys=True,
            indent=4,
        )


class TestMutableMapping(ConfigTestCase):
    def test_get(self) -> None:
        self.assertEqual("val", self.config["key"])

    def test_set(self) -> None:
        self.config["new-key"] = "new-val"
        self.assertEqual(
            dict(self.DEFAULTS, **{"new-key": "new-val"}), self.config._data
        )

    def test_del(self) -> None:
        del self.config["key"]
        self.assertEqual({}, self.config._data)

    def test_iter(self) -> None:
        for k, v in self.config.items():
            self.assertEqual("key", k)
            self.assertEqual("val", v)

    def test_len(self) -> None:
        self.assertEqual(1, len(self.config))
