import unittest
from ..utils import try_timeout, TryAgain, TimedOut
from unittest.mock import patch, MagicMock, call


class TestTryTimeout(unittest.TestCase):
    def test_returns_value(self) -> None:
        def fcn():
            return 5

        cmp_ret = try_timeout(fcn)
        self.assertEqual(5, cmp_ret)

    def test_raises_unknown_exception(self) -> None:
        def fcn():
            raise Exception("unknown exception")

        with self.assertRaisesRegex(Exception, "unknown exception"):
            try_timeout(fcn)

    @patch("time.time")
    def test_timeout(self, mock_time: MagicMock) -> None:
        mock_time.side_effect = [0, 6]

        def fcn():
            raise TryAgain

        with self.assertRaisesRegex(TimedOut, "timeout reached"):
            try_timeout(fcn, timeout=5)

    @patch("time.time")
    def test_timeout_before_start(self, mock_time: MagicMock) -> None:
        mock_time.side_effect = [5, 1]

        def fcn():
            raise TryAgain

        with self.assertRaisesRegex(TimedOut, "timeout reached"):
            try_timeout(fcn, timeout=5)

    @patch("time.time")
    @patch("time.sleep")
    def test_retry(self, mock_sleep: MagicMock, mock_time: MagicMock) -> None:
        mock_time.side_effect = [0, 3]
        fcn = MagicMock(side_effect=[TryAgain, 5])
        cmp_ret = try_timeout(fcn, timeout=5)
        self.assertEqual(5, cmp_ret)

        mock_sleep.assert_called_once_with(1.0)

    @patch("time.time")
    @patch("time.sleep")
    def test_retry_with_action(
        self, mock_sleep: MagicMock, mock_time: MagicMock
    ) -> None:
        mock_time.side_effect = [0, 3]
        fcn = MagicMock(side_effect=[TryAgain, 5])
        retry_action = MagicMock()

        cmp_ret = try_timeout(fcn, timeout=5, retry_action=retry_action)

        retry_action.assert_called_once_with()

    @patch("time.time")
    @patch("time.sleep")
    def test_retry_step(self, mock_sleep: MagicMock, mock_time: MagicMock) -> None:
        mock_time.side_effect = [0, 3]
        fcn = MagicMock(side_effect=[TryAgain, 5])
        cmp_ret = try_timeout(fcn, timeout=10, step=3)
        self.assertEqual(5, cmp_ret)

        mock_sleep.assert_called_once_with(3)

    @patch("time.time")
    @patch("time.sleep")
    def test_retry_remainder(self, mock_sleep: MagicMock, mock_time: MagicMock) -> None:
        mock_time.side_effect = [0, 3]
        fcn = MagicMock(side_effect=[TryAgain, 5])
        cmp_ret = try_timeout(fcn, timeout=5, step=5)
        self.assertEqual(5, cmp_ret)

        mock_sleep.assert_called_once_with(2)

    @patch("time.time")
    @patch("time.sleep")
    def test_retry_exponential_backoff(
        self, mock_sleep: MagicMock, mock_time: MagicMock
    ) -> None:
        mock_time.side_effect = [0, 1, 3, 7]
        fcn = MagicMock(side_effect=[TryAgain, TryAgain, TryAgain, 5])
        cmp_ret = try_timeout(fcn)
        self.assertEqual(5, cmp_ret)

        mock_sleep.assert_has_calls(
            [
                call(1.0),
                call(2.0),
                call(4.0),
            ]
        )

    @patch("time.time")
    @patch("time.sleep")
    def test_retry_linear_backoff(
        self, mock_sleep: MagicMock, mock_time: MagicMock
    ) -> None:
        mock_time.side_effect = [0, 1, 2, 3]
        fcn = MagicMock(side_effect=[TryAgain, TryAgain, TryAgain, 5])
        cmp_ret = try_timeout(fcn, step_exp=1.0)
        self.assertEqual(5, cmp_ret)

        mock_sleep.assert_has_calls(
            [
                call(1.0),
                call(1.0),
                call(1.0),
            ]
        )
