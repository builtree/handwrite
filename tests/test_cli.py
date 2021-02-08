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

    def test_handwrite(self):
        # Check working with excellent input and no optional parameters
        subprocess.call(
            [
                "handwrite",
                os.path.join(self.file_dir, "test_data", "sheettopng", "excellent.jpg"),
                self.temp_dir,
            ]
        )
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "MyFont.ttf")))

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
                    os.path.exists(os.path.join(self.temp_dir, f"{i}", f"0{suffix}"))
                )
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "MyFont.ttf")))

        # Check working with multiple inputs
        subprocess.call(
            [
                "handwrite",
                "--directory",
                self.temp_dir,
                os.path.join(self.file_dir, "test_data", "sheettopng"),
                self.temp_dir,
            ]
        )
        for c in ALL_CHARS:
            for suffix in [".bmp", ".png", ".svg"]:
                for index in range(2):
                    self.assertTrue(
                        os.path.exists(
                            os.path.join(self.temp_dir, f"{c}", f"{index}{suffix}")
                        )
                    )
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "FirstFont.ttf")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "SecondFont.ttf")))
