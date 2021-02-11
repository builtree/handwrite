import os
import shutil
import tempfile
import unittest
import subprocess

from handwrite.sheettopng import ALL_CHARS


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.file_dir = os.path.dirname(os.path.abspath(__file__))
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_single_input(self):
        # Check working with excellent input and no optional parameters
        subprocess.call(
            [
                "handwrite",
                os.path.join(self.file_dir, "test_data", "sheettopng", "excellent.jpg"),
                self.temp_dir,
            ]
        )
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "MyFont.ttf")))

    def test_single_input_with_optional_parameters(self):
        # Check working with optional parameters
        subprocess.call(
            [
                "handwrite",
                os.path.join(self.file_dir, "test_data", "sheettopng", "excellent.jpg"),
                self.temp_dir,
                "--directory",
                self.temp_dir,
                "--config",
                os.path.join(self.file_dir, "test_data", "default.json"),
            ]
        )
        for i in ALL_CHARS:
            for suffix in [".bmp", ".png", ".svg"]:
                self.assertTrue(
                    os.path.exists(os.path.join(self.temp_dir, f"{i}", f"{i}{suffix}"))
                )
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "MyFont.ttf")))

    def test_multiple_inputs(self):
        # Check working with multiple inputs
        sheets_dir = os.path.join(self.file_dir, "test_data", "sheettopng")
        subprocess.call(
            [
                "handwrite",
                "--directory",
                self.temp_dir,
                sheets_dir,
                self.temp_dir,
            ]
        )
        for sheet_name in sorted(os.listdir(sheets_dir)):
            for i in ALL_CHARS:
                for suffix in [".bmp", ".png", ".svg"]:
                    self.assertTrue(
                        os.path.exists(
                            os.path.join(
                                self.temp_dir,
                                os.path.splitext(sheet_name)[0],
                                f"{i}",
                                f"{i}{suffix}",
                            )
                        )
                    )
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "MyFont.ttf")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "MyFont-excellent2.ttf")))
