import os
import shutil
import tempfile
import unittest
import subprocess

from handwrite.sheettopng import ALL_CHARS


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.file_dir = os.path.dirname(os.path.abspath(__file__))

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_handwrite(self):
        # Check working with excellent input and no optional parameters
        subprocess.call(
            [
                "handwrite",
                os.path.join(self.file_dir, "test_data", "sheettopng", "excellent.jpg"),
                os.path.join(self.temp_dir, "test"),
            ]
        )
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "test.ttf")))

        # Check working with optional parameters
        subprocess.call(
            [
                "handwrite",
                os.path.join(self.file_dir, "test_data", "sheettopng", "excellent.jpg"),
                os.path.join(self.temp_dir, "test2"),
                "--directory",
                self.temp_dir,
                "--config",
                os.path.join(self.file_dir, "test_data", "default.json"),
            ]
        )
        for i in ALL_CHARS:
            for suffix in [".bmp", ".png", ".svg"]:
                self.assertTrue(
                    os.path.exists(
                        os.path.join(self.temp_dir, f"{i}" + os.sep + f"{i}{suffix}")
                    )
                )
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "test2.ttf")))