import os
import shutil
import tempfile
import unittest

from handwrite.sheettopng import SheetToPNG, ALL_CHARS


class TestSheetToPNG(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.mkdtemp()
        self.sheets_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "test_data" + os.sep + "sheettopng",
        )
        self.converter = SheetToPNG()

    def tearDown(self):
        shutil.rmtree(self.directory)

    def test_convert(self):
        # Single sheet input
        excellent_scan = os.path.join(self.sheets_path, "excellent.jpg")
        config = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "test_data",
            "config_data",
            "default.json",
        )
        self.converter.convert(excellent_scan, self.directory, config)
        for i in ALL_CHARS:
            self.assertTrue(
                os.path.exists(os.path.join(self.directory, f"{i}", f"{i}.png"))
            )

    # TODO Once all the errors are done for detect_characters
    # Write tests to check each kind of scan and whether it raises
    # helpful errors, Boilerplate below:
    # def test_detect_characters(self):
    #     scans = ["excellent", "good", "average"]
    #     for scan in scans:
    #         detected_chars = self.converter.detect_characters(
    #             os.path.join(self.sheets_path, f"{scan}.jpg")
    #         )
