import unittest
from unittest.mock import patch
import sys

from buper import Buper
from buper.windows import WindowsBuper


class TestWindowsBuper(unittest.TestCase):

    @patch.object(sys, 'platform', 'win32')
    def setUp(self) -> None:
        self.buper = Buper()

    def test_buper_is_linux(self):
        self.assertIsInstance(self.buper, WindowsBuper)

    def test__generate_command(self):
        self.assertIsInstance(self.buper._generate_command(), str)

    def test__files(self):
        self.assertIsInstance(self.buper._files(), str)

    def tearDown(self) -> None:
        del self.buper