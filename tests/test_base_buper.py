import unittest
from unittest.mock import patch

import shutil
import os

from buper import Buper
from config.backup import conf_backup


def shutil_disk_usage(*args, **kwargs):
    return 0, 0, 5486820720.64


def os_path_get_size(*args, **kwargs):
    return 2147483648


class TestBaseBuper(unittest.TestCase):
    def setUp(self) -> None:
        self.buper = Buper()
        self.buper.folder = os.getcwd()
        self.buper.archive = __file__

    def test_date(self):
        """Дата представлена строкой"""
        self.assertIsInstance(self.buper.date, str)

    @patch.object(shutil, 'disk_usage', shutil_disk_usage)
    def test_free_space(self):
        self.assertEqual(self.buper.free_space, 5.11)

    @patch.object(os.path, 'getsize', os_path_get_size)
    def test_arch_size(self):
        self.assertEqual(self.buper.arch_size, 2.0)

    @patch.object(shutil, 'disk_usage', shutil_disk_usage)
    @patch.object(os.path, 'getsize', os_path_get_size)
    def test_calculate_disk_capacity(self):
        self.assertEqual(self.buper.calculate_disk_capacity(), 2.555)

    @patch.object(shutil, 'disk_usage', shutil_disk_usage)
    @patch.object(os.path, 'getsize', os_path_get_size)
    def test_check_disk_capacity_true(self):
        conf_backup.min_capacity = 1
        self.assertEqual(self.buper.check_disk_capacity(), True)

    @patch.object(shutil, 'disk_usage', shutil_disk_usage)
    @patch.object(os.path, 'getsize', os_path_get_size)
    def test_check_disk_capacity_false(self):
        conf_backup.min_capacity = 3
        self.assertEqual(self.buper.check_disk_capacity(), False)

    def tearDown(self) -> None:
        try:
            os.remove('log.txt')
        except:
            pass
        finally:
            del self.buper
