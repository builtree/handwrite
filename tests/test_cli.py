import os
import shutil
import tempfile
import unittest
import subprocess
import filecmp

from handwrite.sheettopng import ALL_CHARS


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.file_dir = os.path.dirname(os.path.abspath(__file__))
        self.temp_dir = tempfile.mkdtemp()
        self.sheets_dir = os.path.join(self.file_dir, "test_data", "sheettopng")

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
                os.path.join(self.file_dir, "test_data", "config_data", "default.json"),
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
        subprocess.call(
            [
                "handwrite",
                self.sheets_dir,
                self.temp_dir,
            ]
        )
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "MyFont.ttf")))
        self.assertTrue(
            os.path.exists(os.path.join(self.temp_dir, "MyFont-excellent2.ttf"))
        )

    def test_multiple_inputs_with_optional_parameters(self):
        # Check working with multiple inputs and optional parameters
        configs_dir = os.path.join(self.file_dir, "test_data", "config_data", "configs")
        subprocess.call(
            [
                "handwrite",
                self.sheets_dir,
                self.temp_dir,
                "--directory",
                self.temp_dir,
                "--config",
                configs_dir,
            ]
        )
        for sheet_name in sorted(os.listdir(self.sheets_dir)):
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
        self.assertTrue(
            os.path.exists(os.path.join(self.temp_dir, "ExcellentFont.ttf"))
        )
        self.assertTrue(
            os.path.exists(os.path.join(self.temp_dir, "ExcellentFont2.ttf"))
        )

    def test_multiple_inputs_without_configs_dir(self):
        subprocess.call(
            [
                "handwrite",
                self.sheets_dir,
                self.temp_dir,
                "--directory",
                self.temp_dir,
            ]
        )
        # Check if config directory is created inside given character directory
        configs_dir = os.path.join(self.temp_dir, "configs")
        self.assertTrue(os.path.exists(configs_dir))

        # Check if the config file created inside config directory is the same
        # as default config
        for config in os.listdir(configs_dir):
            self.assertTrue(
                filecmp.cmp(
                    os.path.join(configs_dir, config),
                    os.path.join(
                        self.file_dir, "test_data", "config_data", "default.json"
                    ),
                )
            )
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "MyFont.ttf")))
        self.assertTrue(
            os.path.exists(os.path.join(self.temp_dir, "MyFont-excellent2.ttf"))
        )

    def test_multiple_inputs_with_incomplete_configs_dir(self):
        configs_dir = os.path.join(self.file_dir, "test_data", "config_data", "config")
        subprocess.call(
            [
                "handwrite",
                self.sheets_dir,
                self.temp_dir,
                "--directory",
                self.temp_dir,
                "--config",
                configs_dir,
            ]
        )
        # Check if the missing config file created inside config directory is the
        # same as default config
        self.assertTrue(
            filecmp.cmp(
                os.path.join(configs_dir, "excellent.json"),
                os.path.join(self.file_dir, "test_data", "config_data", "default.json"),
            )
        )
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "MyFont.ttf")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "MyFont3.ttf")))

    def test_multiple_inputs_with_single_config(self):
        config_file = os.path.join(
            self.file_dir,
            "test_data",
            "config_data",
            "config",
            "excellent2.json",
        )
        subprocess.call(
            [
                "handwrite",
                self.sheets_dir,
                self.temp_dir,
                "--directory",
                self.temp_dir,
                "--config",
                config_file,
            ]
        )
        # Check if config directory is created inside given character directory
        configs_dir = os.path.join(self.temp_dir, "configs")
        self.assertTrue(os.path.exists(configs_dir))
        # Check if the missing config file created inside config directory is the
        # same as the given config file
        for config in os.listdir(configs_dir):
            self.assertTrue(
                filecmp.cmp(
                    os.path.join(configs_dir, config),
                    config_file,
                )
            )
        # Font for the first image in sorted list of files inside sheet directory
        # gets created first
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "MyFont3.ttf")))
        self.assertTrue(
            os.path.exists(os.path.join(self.temp_dir, "MyFont3-excellent2.ttf"))
        )

    def test_multiple_inputs_without_directory(self):
        configs_dir = os.path.join(self.file_dir, "test_data", "config_data", "configs")
        # Check working with sheet and config directory but no character directory
        subprocess.call(
            [
                "handwrite",
                self.sheets_dir,
                self.temp_dir,
                "--config",
                configs_dir,
            ]
        )
        self.assertTrue(
            os.path.exists(os.path.join(self.temp_dir, "ExcellentFont.ttf"))
        )
        self.assertTrue(
            os.path.exists(os.path.join(self.temp_dir, "ExcellentFont2.ttf"))
        )
