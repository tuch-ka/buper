import unittest
from unittest.mock import patch
import sys

from buper import Buper
from buper.linux import LinuxBuper


class TestLinuxBuper(unittest.TestCase):

    @patch.object(sys, 'platform', 'linux')
    def setUp(self) -> None:
        self.buper = Buper()

    def test_buper_is_linux(self):
        self.assertIsInstance(self.buper, LinuxBuper)

    def test__generate_command(self):
        self.assertIsInstance(self.buper._generate_command(), list)

    def test__files(self):
        self.assertIsInstance(self.buper._files(), list)

    def tearDown(self) -> None:
        del self.buper